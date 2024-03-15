from random import choices
import string
from .container_for_ads import ContainerForAds


class QueueForModeration:
    """Через данный класс реализуется очередь на модерацию"""

    def __init__(self):
        self.ads_list = list()

    async def add_ads_in_queue(self, mediafile, text, user_id, public_time, validity):
        """Метод добавляет объявление в очередь на модерацию"""
        generate_id = ''.join(choices(string.digits + string.ascii_letters, k=8))
        file_id_list = mediafile if len(mediafile) > 0 else None
        container = ContainerForAds(
            container_id=generate_id,
            text=text,
            user_id=user_id,
            file_id=file_id_list,
            public_time=public_time,
            validity=validity
        )
        self.ads_list.append(container)

    async def remove_ads_from_queue(self, container_id):
        """Метод удаляет объявление из очереди на модерацию.
        Не важно, отправляется оно в очередь на публикацию или не прошло модерацию
        удаляется всегда первое объявление из списка"""
        # На всякий случай проверим, что бы их ID совпадали
        if self.ads_list[0].container_id == container_id:
            self.ads_list.pop(0)

    async def get_ads_from_queue(self):
        """Метод получения объявления из очереди на модерацию. Всегда выдается первое в списке!"""
        return self.ads_list[0] if len(self.ads_list) > 0 else 'Очередь объявлений на модерацию пуста!'

    async def get_quantity(self):
        """Возвращает строку с кол-вом объявлений ожидающих модерации"""
        return str(len(self.ads_list))


queue_for_moderation = QueueForModeration()
