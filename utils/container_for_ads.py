class ContainerForAds:
    """Через данный класс реализуется контейнер для объявлений"""
    def __init__(self,
                 container_id: str,
                 text: str,
                 user_id: int,
                 public_time: str,
                 file_id,
                 public_channel: int,
                 time_index=None):

        self.container_id = container_id
        self.text = text
        self.file_id = file_id
        self.user_id = user_id
        self.public_time = public_time
        self.time_index = time_index
        self.public_channel = public_channel

    def __str__(self):
        itself_str = (f'\nID: {self.container_id}\n'
                      f'User ID: {self.user_id}\n'
                      f'File ID: {self.file_id}\n'
                      f'Text: {self.text}\n'
                      f'Public time: {self.public_time}\n'
                      f'Time index: {self.time_index}\n'
                      f'Public channel: {self.public_channel}')
        return itself_str
