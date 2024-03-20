class ContainerForAds:
    """Через данный класс реализуется контейнер для объявлений"""
    def __init__(self, container_id: str, text: str, user_id: int, public_time: str, file_id):
        self.container_id = container_id
        self.text = text
        self.file_id = file_id
        self.user_id = user_id
        self.public_time = public_time

    def __str__(self):
        itself_str = (f'\nID: {self.container_id}\n'
                      f'User ID: {self.user_id}\n'
                      f'File ID: {self.file_id}\n'
                      f'Text: {self.text}\n'
                      f'Public time: {self.public_time}\n')
        return itself_str
