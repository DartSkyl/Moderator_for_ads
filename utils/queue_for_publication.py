from .container_for_ads import ContainerForAds


class QueueForPublication:
    """Данный класс реализует очередь на публикацию"""
    def __init__(self):
        self.ads_list = list()

    async def add_ads_in_queue(self, container_id, text, user_id, mediafile, public_time, validity):
        """Здесь происходит добавление объявления в очередь на публикацию"""
        # file_id_list = mediafile if len(mediafile) > 0 else None
        container = ContainerForAds(
            container_id=container_id,
            text=text,
            user_id=user_id,
            file_id=mediafile,
            public_time=public_time,
            validity=validity
        )
        self.ads_list.append(container)


queue_for_publication = QueueForPublication()
