class QueueForPublication:
    """Данный класс реализует очередь на публикацию"""
    def __init__(self):
        self.ads_list = list()

    async def add_ads_in_queue(self, ads_container):
        """Здесь происходит добавление объявления в очередь на публикацию"""
        self.ads_list.append(ads_container)
