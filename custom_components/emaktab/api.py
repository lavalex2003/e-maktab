import aiohttp
import datetime
import asyncio
from .const import LOGIN_URL, SCHEDULE_URL
from yarl import URL  # Импортируем YARL

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
        """Получение расписания."""
        if not self.logged_in:
            _LOGGER.warning("Сессия истекла, повторная авторизация...")
            await self.login()
    
        # Формируем URL корректно
        url = URL(SCHEDULE_URL).with_path(
            f"/api/userfeed/persons/{self.person_id}/schools/{self.school_id}/groups/{self.group_id}/schedule"
        ).with_query(date=int(time.time()), takeDays=1)
    
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    else:
                        _LOGGER.error(f"Ошибка: Неправильный Content-Type ({content_type})")
                        return None
                else:
                    _LOGGER.error(f"Ошибка запроса расписания: {response.status}")
                    return None
        except Exception as e:
            _LOGGER.error(f"Ошибка при получении расписания: {e}")
            return None
