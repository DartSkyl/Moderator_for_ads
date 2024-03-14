class ContainerForAds:
    """Через данный класс реализуется контейнер для объявлений"""
    def __init__(self, container_id: str, text: str, user_id: int, public_time: str, validity: int, file_id):
        self._container_id = container_id
        self._text = text
        self._file_id = file_id
        self._user_id = user_id
        self._public_time = public_time
        self._validity = validity

    def __str__(self):
        itself_str = (f'\nID: {self._container_id}\n'
                      f'User ID: {self._user_id}\n'
                      f'File ID: {self._file_id}\n'
                      f'Text: {self._text}\n'
                      f'Public time: {self._public_time}\n'
                      f'Validity: {self._validity}\n')
        return itself_str

    def get_id(self):
        return self._container_id


    def get_file_id(self):
        return self._file_id

    def get_text(self):
        return self._text
