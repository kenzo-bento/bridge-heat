from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([BridgeHeat()])


class BridgeHeat(Entity):
    _attr_name = "Bridge Heat"
    _attr_unique_id = "bridge_heat"

    @property
    def state(self):
        state = self.hass.states.get("weather.forecast_home")
        if state is None:
            return "No Data"

        return "Collecting Data"  # replace with real temperature
    
    @property
    def extra_state_attributes(self):
        state = self.hass.states.get("weather.forecast_home")
        if state is None:
            return None

        return {
            "temperature": state.attributes.get("temperature"),
            "humidity": state.attributes.get("humidity"),
            "wind_speed": state.attributes.get("wind_speed")
        }
