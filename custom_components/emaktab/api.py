import aiohttp
import datetime
import asyncio
from .const import LOGIN_URL, SCHEDULE_URL

class EMaktabAPI:
    def __init__(self, username, password, person_id, school_id, group_id, session):
        self.username = username
        self.password = password
        self.person_id = person_id
        self.school_id = school_id
        self.group_id = group_id
        self.session = session

    async def login(self):
        """Асинхронная авторизация"""
        async with self.session.post(LOGIN_URL, data={"username": self.username, "password": self.password, "captcha.id": "639dcede-f3e1-4e2f-8ef2-17f5f53aaca6", "exceededAttempts": "false"}) as response:
            return response.status == 200  

    async def get_schedule(self):
        """Асинхронное получение расписания"""
        timestamp = int(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timestamp())
        url = SCHEDULE_URL.format(self.person_id, self.school_id, self.group_id, timestamp)
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None
