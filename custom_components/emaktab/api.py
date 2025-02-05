import requests
import datetime
from .const import LOGIN_URL, SCHEDULE_URL

class EMaktabAPI:
    def __init__(self, username, password, person_id, school_id, group_id):
        self.username = username
        self.password = password
        self.person_id = person_id
        self.school_id = school_id
        self.group_id = group_id
        self.session = requests.Session()

    def login(self):
        """Авторизация и получение cookies"""
        response = self.session.post(LOGIN_URL, data={"username": self.username, "password": self.password, "captcha.id": "639dcede-f3e1-4e2f-8ef2-17f5f53aaca6", "exceededAttempts": "false"})
        return response.status_code == 200  

    def get_schedule(self):
        """Получение расписания на текущий день"""
        timestamp = int(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timestamp())
        url = SCHEDULE_URL.format(self.person_id, self.school_id, self.group_id, timestamp)
        response = self.session.get(url)
        if response.status_code == 200:
            return response.json()
        return None
