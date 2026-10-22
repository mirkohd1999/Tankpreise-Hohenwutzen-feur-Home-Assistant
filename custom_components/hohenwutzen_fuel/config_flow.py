"""Configure German/EUR or Polish/PLN display."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, NAME
from .display import CONF_PROFILE, DEFAULT_PROFILE, PROFILE_LABELS, selected_profile


def profile_schema(default):
    return vol.Schema({vol.Required(CONF_PROFILE, default=default): vol.In(PROFILE_LABELS)})


class HohenwutzenConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title=NAME, data=user_input)
        return self.async_show_form(step_id="user", data_schema=profile_schema(DEFAULT_PROFILE))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HohenwutzenOptionsFlow()


class HohenwutzenOptionsFlow(config_entries.OptionsFlowWithReload):
    """Update the profile and automatically reload the entry."""

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        default = selected_profile(self.config_entry.data, self.config_entry.options)
        return self.async_show_form(step_id="init", data_schema=profile_schema(default))
