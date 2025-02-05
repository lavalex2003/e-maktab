import requests
import datetime

class EMaktabAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.school_id = school_id
        self.person_id = person_id
        self.group_id = group_id
        self.session = requests.Session()

    def login(self):
        """Авторизация и получение cookies"""
        response = self.session.post(LOGIN_URL, data={"username": self.username, "password": self.password})
        return response.status_code == 200  # Предполагаем, что авторизация успешна

    def get_schedule(self, person_id, school_id, group_id):
        """Получение расписания на текущий день"""
        timestamp = int(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timestamp())
        url = SCHEDULE_URL.format(person_id, school_id, group_id, timestamp)
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        return None
