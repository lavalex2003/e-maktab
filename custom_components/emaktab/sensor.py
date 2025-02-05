from datetime import timedelta
import logging
import requests
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Настройка сенсоров"""
    username = entry.data["username"]
    password = entry.data["password"]

    api = EMaktabAPI(username, password)
    if not api.login():
        _LOGGER.error("Не удалось войти в E-Maktab")
        return

    async def async_update_data():
        """Получение данных"""
        data = api.get_schedule("1000009940640", "1000000000108", "2248292570190413489")
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

    sensors = []
    for i in range(8):
        sensors.append(EMaktabSensor(coordinator, i))
    
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
