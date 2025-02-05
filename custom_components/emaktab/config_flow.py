import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_PERSON_ID, CONF_SCHOOL_ID, CONF_GROUP_ID

class EMaktabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Настройка интеграции через UI"""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="E-Maktab", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_PERSON_ID): str,
                vol.Required(CONF_SCHOOL_ID): str,
                vol.Required(CONF_GROUP_ID): str
                
            }),
            errors=errors
        )
