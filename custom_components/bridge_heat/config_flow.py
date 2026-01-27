from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(
                        "Permission to send Temperature Data",
                        default=False
                    ): bool,
                }),
                description_placeholders={
                    "info": (
                        "Temperature data will be sent to an external database "
                        "outside of Home Assistant."
                    )
                },
            )

        return self.async_create_entry(
            title="Temperature",
            data=user_input,
        )
