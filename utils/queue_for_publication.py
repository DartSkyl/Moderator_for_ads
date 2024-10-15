import datetime
from config import PG_URI, MAIN_GROUP_ID
from loader import db, bot
from .container_for_ads import ContainerForAds

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import html


publisher = None


async def create_publisher():
    global publisher
    publisher = Publisher()


class QueueForPublication:
    """Данный класс реализует очередь на публикацию"""

    def __init__(self):
        self.ads_list = list()

    async def add_ads_in_queue(self, container_id, text, user_id, mediafile, public_time, time_index):
        """Здесь происходит добавление объявления в очередь на публикацию"""
        container = ContainerForAds(
            container_id=container_id,
            text=text,
            user_id=user_id,
            file_id=mediafile,
            public_time=public_time,
            time_index=time_index
        )

        # Ниже описанная конструкция нужна для сортировки объявлений при добавлении в очередь на публикацию
        if time_index:
            if len(self.ads_list) > 0:
                for i_elem in range(len(self.ads_list)):
                    if self.ads_list[i_elem].time_index >= container.time_index:
                        self.ads_list.insert(i_elem, container)
                        break
                else:
                    self.ads_list.append(container)
            else:
                self.ads_list.append(container)

        await publisher.add_ads_in_publisher(container)  # noqa

    @staticmethod
    async def add_container_in_db(container: ContainerForAds):
        file_id_from_for_db = ''
        if container.file_id:
            for elem in container.file_id:
                file_id_from_for_db += '!$!$'.join(elem)
                file_id_from_for_db += '$!$!'  # разделитель между записями
        else:
            file_id_from_for_db = 'None'

        await db.input_ads_pub(
            container_id=container.container_id,
            text=container.text,
            user_id=container.user_id,
            file_id=file_id_from_for_db,
            public_time=container.public_time,
            time_index=container.time_index
        )

    async def load_queue_from_base(self):
        """Выгружаем очередь из базы"""

        mod_queue = await db.output_queue_pub()
        for ads in mod_queue:
            if ads['file_id'] != 'None':
                file_id_list = ads['file_id'].split('$!$!')
                file_id_list = [elem.split('!$!$') for elem in file_id_list]
                file_id_list.pop()  # В конце образуется пустой элемент

            else:
                file_id_list = None
            container = ContainerForAds(
                container_id=ads['container_id'],
                text=ads['text'],
                user_id=ads['user_id'],
                file_id=file_id_list,
                public_time=ads['public_time'],
                time_index=ads['time_index']
            )

            if len(self.ads_list) > 0:
                for i_elem in range(len(self.ads_list)):
                    if self.ads_list[i_elem].time_index >= container.time_index:
                        self.ads_list.insert(i_elem, container)
                        break
                else:
                    self.ads_list.append(container)
            else:
                self.ads_list.append(container)

    @staticmethod
    async def edit_time_for_publication(ads: ContainerForAds):
        """Здесь изменяем время для публикации в планировщике"""
        # По сути, просто объявляем задачу заново
        await publisher.add_ads_in_publisher(ads)  # noqa

    async def get_ads_list(self):
        """Метод выдает всю очередь для просмотра если она не пуста"""
        return self.ads_list if len(self.ads_list) > 0 else 'Очередь на публикацию пуста!'

    async def remove_ads_container(self, container: ContainerForAds):
        """Удаляет контейнер из списка"""
        try:
            self.ads_list.remove(container)
        except ValueError:
            pass


queue_for_publication = QueueForPublication()


async def publisher_function(ads: ContainerForAds, shed=False):
    """Данная функция публикует объявление в канал"""
    # validity_str = (datetime.datetime.now() + datetime.timedelta(days=ads.validity)).strftime('%H:%M %Y.%m.%d')
    # msg_with_validity = f'\n\n<b>Опубликовано до: {validity_str}</b>\n'
    if ads.file_id:  # Если данный список пуст, значит объявление без медиафайлов
        media_group = MediaGroupBuilder(caption=html.quote(ads.text))
        for mediafile in ads.file_id:
            media_group.add(type=mediafile[1], media=mediafile[0])
        await bot.send_media_group(chat_id=MAIN_GROUP_ID, media=media_group.build())

    else:
        await bot.send_message(chat_id=MAIN_GROUP_ID, text=html.quote(ads.text))
    await db.remove_ads_pub(ads.container_id)
    if not shed:
        await queue_for_publication.remove_ads_container(ads)
    else:
        for elem in queue_for_publication.ads_list:
            if elem.container_id == ads.container_id:
                await queue_for_publication.remove_ads_container(elem)


class Publisher:
    def __init__(self):
        self._scheduler = AsyncIOScheduler(gconfig={'apscheduler.timezone': 'Europe/Moscow'})
        self._scheduler.add_jobstore(jobstore='sqlalchemy', alias='publisher', url=PG_URI, tablename='aps_publisher')
        self._scheduler.start()

    async def add_ads_in_publisher(self, ads: ContainerForAds):
        """Здесь добавляем задача на публикацию объявления"""
        if ads.public_time != 'None':
            trigger_setting = ads.public_time
            trigger_setting = trigger_setting.split()
            trigger_setting = (trigger_setting[1].split('.'))[::-1] + trigger_setting[0].split(':')
            trigger_setting = [int(num) for num in trigger_setting]

            publication_time = datetime.datetime(
                year=trigger_setting[0],
                month=trigger_setting[1],
                day=trigger_setting[2],
                hour=trigger_setting[3],
                minute=trigger_setting[4]
            )

            # Если, к этому моменту время для публикации уже прошло, то просто опубликуем
            if datetime.datetime.now() > publication_time:
                await publisher_function(ads=ads)
            else:
                self._scheduler.add_job(func=publisher_function, kwargs={'ads': ads, 'shed': True}, id=ads.container_id,
                                        trigger='date', run_date=publication_time, jobstore='publisher', max_instances=1,
                                        replace_existing=True)
                await queue_for_publication.add_container_in_db(container=ads)
        else:
            await publisher_function(ads=ads)
