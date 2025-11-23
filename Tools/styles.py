import reflex as rx

STYLES = {
    "font_family": "Inter, sans-serif",
    "background_color": "#0A0E27",
    "color": "#EAECFB",
    "--accent-color": "#9D4EDD",
    "--accent-color-light": "#C77DFF",
    "--secondary-accent": "#00F5FF",
    "min-height": "100vh",
    "display": "flex",
    "flex_direction": "column",
    "_dark": {"background_color": "#0A0E27"},
}


def icon_button_style(is_active: rx.Var[bool]) -> dict:
    return {
        "display": "flex",
        "flex_direction": "column",
        "align_items": "center",
        "justify_content": "center",
        "padding": "0.5rem",
        "border_radius": "0.75rem",
        "color": rx.cond(is_active, "var(--accent-color-light)", "#A0AEC0"),
        "background": rx.cond(is_active, "rgba(157, 78, 221, 0.1)", "transparent"),
        "transition": "all 0.3s ease",
        "_hover": {
            "background": "rgba(157, 78, 221, 0.15)",
            "color": "var(--accent-color-light)",
        },
    }