from datetime import timedelta
import logging
import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, UPDATE_INTERVAL, CONF_USERNAME, CONF_PASSWORD, CONF_PERSON_ID, CONF_SCHOOL_ID, CONF_GROUP_ID
from .api import EMaktabAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Настройка сенсоров"""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    person_id = entry.data[CONF_PERSON_ID]
    school_id = entry.data[CONF_SCHOOL_ID]
    group_id = entry.data[CONF_GROUP_ID]

    session = aiohttp.ClientSession()
    api = EMaktabAPI(username, password, person_id, school_id, group_id, session)
    
    if not await api.login():
        _LOGGER.error("Не удалось войти в E-Maktab")
        return

    async def async_update_data():
        """Получение данных"""
        data = await api.get_schedule()
        if not data:
            raise UpdateFailed("Ошибка обновления данных")
        return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="emaktab_schedule",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [EMaktabSensor(coordinator, i) for i in range(8)]
    
    async_add_entities(sensors, True)

class EMaktabSensor(SensorEntity):
    """Сенсоры E-Maktab"""

    def __init__(self, coordinator, index):
        self.coordinator = coordinator
        self.index = index
        self._attr_name = f"E-Maktab Lesson {index+1}"
        self._attr_unique_id = f"emaktab_lesson_{index+1}"

    @property
    def state(self):
        """Возвращает название урока"""
        try:
            return self.coordinator.data["schedule"][self.index]["lesson_name"]
        except (IndexError, KeyError):
            return "Нет данных"

    async def async_update(self):
        await self.coordinator.async_request_refresh()
