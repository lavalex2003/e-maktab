"""Сенсоры для E-Maktab."""
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Настройка сенсоров."""
    api = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        EMaktabSensor(api, "subject"),
        EMaktabSensor(api, "teacher"),
        EMaktabSensor(api, "room"),
        EMaktabSensor(api, "start_time"),
        EMaktabSensor(api, "end_time"),
        EMaktabSensor(api, "lesson_number"),
        EMaktabSensor(api, "day"),
        EMaktabSensor(api, "date"),
    ]
    
    async_add_entities(sensors, True)

class EMaktabSensor(Entity):
    """Сенсор E-Maktab."""
    def __init__(self, api, field):
        self.api = api
        self.field = field
        self._state = None

    @property
    def name(self):
        return f"E-Maktab {self.field}"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Обновление данных с API."""
        data = await self.api.get_schedule()
        if data:
            self._state = data.get(self.field)
