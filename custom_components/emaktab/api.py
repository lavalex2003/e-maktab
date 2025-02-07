import aiohttp
import logging
import datetime
from yarl import URL
from .const import LOGIN_URL, SCHEDULE_URL

_LOGGER = logging.getLogger(__name__)

class EMaktabAPI:
    """Клиент API для E-Maktab."""

    def __init__(self, username, password, person_id, school_id, group_id, session):
        """Инициализация."""
        self.username = username
        self.password = password
        self.person_id = person_id
        self.school_id = school_id
        self.group_id = group_id
        self.session = session
        self.logged_in = False

    async def login(self):
        """Авторизация и сохранение cookie."""
        try:
            # data = {
            #     "username": self.username,
            #     "password": self.password,
            #     "exceededAttempts": "false",
            #     "ReturnUrl": "",
            #     "FingerprintId": "",
            #     "Captcha.Input": "",
            #     "Captcha.Id": "639dcede-f3e1-4e2f-8ef2-17f5f53aaca6"
                
            }
            payload = f"exceededAttempts=False&ReturnUrl=&FingerprintId=&login={self.username}&password={self.password}&Captcha.Input=&Captcha.Id=639dcede-f3e1-4e2f-8ef2-17f5f53aaca6"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            async with self.session.post(LOGIN_URL, data=payload, headers=headers) as response:
                _LOGGER.info("Попытка авторизации в E-Maktab")
                _LOGGER.info(f"payload {payload}")
                _LOGGER.info(f"headers {headers}")
                if response.status == 200:
                    _LOGGER.info("✅ Успешная авторизация в E-Maktab")
                    self.logged_in = True
                    _LOGGER.warning(f"Заголовок авторизации: {response.headers}")
                    return True
                else:
                    _LOGGER.error(f"❌ Ошибка авторизации: {response.status}")
                    self.logged_in = False
                    return False
        except Exception as e:
            _LOGGER.error(f"❌ Ошибка при авторизации: {e}")
            self.logged_in = False
            return False

    async def get_schedule(self):
        _LOGGER.info("Попытка получения расписания")
        if not self.logged_in == True:
            _LOGGER.warning("⚠️ Сессия истекла, повторная авторизация...")
            await self.login()
        timestamp = int(datetime.datetime.combine(datetime.date.today(), datetime.time.min).timestamp()) + 18000 #Добавляем 5 часов
        url = URL(SCHEDULE_URL).with_path(
            f"/api/userfeed/persons/{self.person_id}/schools/{self.school_id}/groups/{self.group_id}/schedule"
        ).with_query(date=timestamp, takeDays=1)

        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    else:
                        _LOGGER.error(f"❌ Ошибка: Неправильный Content-Type ({content_type}) URL: {url}")
                        return None
                else:
                    _LOGGER.error(f"❌ Ошибка запроса расписания: {response.status}")
                    return None
        except Exception as e:
            _LOGGER.error(f"❌ Ошибка при получении расписания: {e}")
            return None
