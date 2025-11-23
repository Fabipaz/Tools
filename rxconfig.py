import reflex as rx

config = rx.Config(
    app_name="Tools",
    overlay_component=None,
    favicon="favicon.png",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)