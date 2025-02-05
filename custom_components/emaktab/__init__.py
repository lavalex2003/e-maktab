"""Инициализация интеграции E-Maktab."""
import asyncio
import aiohttp
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from .const import DOMAIN
from .api import EMaktabAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Настройка через configuration.yaml (не используется, но должен быть)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Настройка интеграции через UI."""
    hass.data.setdefault(DOMAIN, {})

    session = aiohttp.ClientSession()
    username = entry.data["username"]
    password = entry.data["password"]
    person_id = entry.data["person_id"]
    school_id = entry.data["school_id"]
    group_id = entry.data["group_id"]

    api = EMaktabAPI(username, password, person_id, school_id, group_id, session)

    # Проверяем подключение перед вызовом async_forward_entry_setup
    try:
        success = await api.login()
        if not success:
            raise ConfigEntryNotReady("Ошибка авторизации в E-Maktab")
    except Exception as e:
        _LOGGER.error(f"Ошибка при подключении к E-Maktab: {e}")
        raise ConfigEntryNotReady from e

    # Сохраняем API-объект в hass.data
    hass.data[DOMAIN][entry.entry_id] = api

    # Теперь сенсоры можно загружать, так как API работает
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Удаление интеграции."""
    if entry.entry_id in hass.data[DOMAIN]:
        del hass.data[DOMAIN][entry.entry_id]

    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
