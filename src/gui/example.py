from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from gui.styles import style_row
from gui.models import ResourceGui
import psutil
from os import getenv
import threading
from gui.styles import style_card
#
# This is an example for nicegui
# This can be used like a boilerplate for creating new nicegui interface
# go to localhost:8000/nicegui
process = psutil.Process()
resource = ResourceGui()


def update_resource():
    while True:
        resource.cpu_usage = process.cpu_percent(interval=1)
        memory_info = process.memory_info()
        resource.memory_usage = memory_info.rss / (1024 * 1024)


threading.Thread(target=update_resource, daemon=True).start()


@ui.page('/other_page')
def other_page():
    with ui.card().style(style_card):
        ui.icon('thumb_up')
        ui.markdown('This is **Markdown**.')
        ui.html('This is <strong>HTML</strong>.')
        with ui.row().style(style_row):
            ui.label('CSS').style('color: #888; font-weight: bold')
            ui.label('Tailwind').classes('font-serif')
            ui.label('Quasar').classes('q-ml-xl')
        ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')


@ui.page('/dark_page', dark=True)
def dark_page():
    def show(event: ValueChangeEventArguments):
        name = type(event.sender).__name__
        ui.notify(f'{name}: {event.value}')
    with ui.card().style(style_card):
        ui.button('Button', on_click=lambda: ui.notify('Click'))
        with ui.row():
            ui.checkbox('Checkbox', on_change=show)
            ui.switch('Switch', on_change=show)
        ui.radio(['A', 'B', 'C'], value='A', on_change=show).props('inline')
        with ui.row():
            ui.input('Text input', on_change=show)
            ui.select(['One', 'Two'], value='One', on_change=show)
        ui.link('And many more...', '/documentation').classes('mt-8')


def draw_resource_panel():

    with ui.card().style(style_card):
        with ui.row().style(style_row):
            ui.label(f"Monitoring (version={getenv("IMAGE_TAG")})")

            with ui.row():
                ui.label().bind_text_from(resource, "cpu_usage", lambda n: f"CPU: {n:.2f}%")
                ui.label().bind_text_from(resource, "memory_usage", lambda n: f"Memory: {n:.2f}MB")


def draw_page():
    draw_resource_panel()
    with ui.card().style(style_card):
        ui.link('Example of markdown, html, icon, css', other_page)
        ui.link('Example of form component and dark theme ', dark_page)


draw_page()
