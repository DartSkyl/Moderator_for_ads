import time
from config_data.config import PG_URI, MAIN_GROUP_ID
from loader import db, bot, admins_id
from .container_for_ads import ContainerForAds

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class QueueForPublication:
    """Данный класс реализует очередь на публикацию"""
    def __init__(self):
        self.ads_list = list()

    async def add_ads_in_queue(self, container_id, text, user_id, mediafile, public_time, validity):
        """Здесь происходит добавление объявления в очередь на публикацию"""
        container = ContainerForAds(
            container_id=container_id,
            text=text,
            user_id=user_id,
            file_id=mediafile,
            public_time=public_time,
            validity=validity
        )
        self.ads_list.append(container)

    async def get_ads_list(self):
        """Метод выдает всю очередь для просмотра если она не пуста"""
        return self.ads_list if len(self.ads_list) > 0 else 'Очередь на публикацию пуста!'


queue_for_publication = QueueForPublication()


class Publisher:
    """Данный класс реализует публикатора объявлений в канал"""

    def __init__(self):
        self._scheduler = AsyncIOScheduler(gconfig={'apscheduler.timezone': 'Europe/Moscow'})
        self._scheduler.add_jobstore(jobstore='sqlalchemy', alias='publisher', url=PG_URI, tablename='aps_publisher')
        self._scheduler.start()


