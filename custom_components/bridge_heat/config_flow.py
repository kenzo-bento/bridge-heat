from homeassistant.helpers import selector
from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, TEMP, HUMIDITY, PRESSURE, PERMS_TITLE


PERMS_SCHEMA = vol.Schema({
    vol.Optional(TEMP, default=False): bool,
    vol.Optional(HUMIDITY, default=False): bool,
    vol.Optional(PRESSURE, default=False): bool,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=PERMS_SCHEMA,
            )

        return self.async_create_entry(
            title=PERMS_TITLE,
            data = {},
            options=user_input,
        )
    @staticmethod
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler()

class OptionsFlowHandler(config_entries.OptionsFlow):

    async def async_step_init(self, user_input=None):
        return await self.async_step_options()

    async def async_step_options(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="options",
                data_schema=vol.Schema({
                    vol.Optional(
                        TEMP,
                        default=self.config_entry.options.get(TEMP, False),
                    ): bool,
                    vol.Optional(
                        HUMIDITY,
                        default=self.config_entry.options.get(HUMIDITY, False),
                    ): bool,
                    vol.Optional(
                        PRESSURE,
                        default=self.config_entry.options.get(PRESSURE, False),
                    ): bool,
                }),
            )

        return self.async_create_entry(
            title="",
            data=user_input,
        )


