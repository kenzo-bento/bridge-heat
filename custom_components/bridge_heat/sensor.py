from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([TemperatureSensor()])


class TemperatureSensor(Entity):
    _attr_name = "Temperature"
    _attr_unique_id = "bridge_heat_temperature"
    _attr_unit_of_measurement = "°C"

    @property
    def state(self):
        state = self.hass.states.get("weather.forecast_home")
        if state is None:
            return None

        return state.attributes.get("temperature")  # replace with real temperature
