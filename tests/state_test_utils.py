from __future__ import annotations

from typing import Any


def build_state(state_cls: type, **attrs: Any) -> Any:
    """Create a Reflex State instance for unit tests without booting the app runtime."""
    state = object.__new__(state_cls)
    object.__setattr__(state, "dirty_vars", set())
    object.__setattr__(state, "dirty_substates", set())
    object.__setattr__(state, "router_data", {})
    object.__setattr__(state, "substates", {})
    object.__setattr__(state, "parent_state", None)
    object.__setattr__(state, "_was_touched", False)
    for key, value in attrs.items():
        object.__setattr__(state, key, value)
    return state
