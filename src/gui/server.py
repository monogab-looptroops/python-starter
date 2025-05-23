from nicegui import ui
from gui.example import ui


def init_gui(api):
    # example how to add nicegui pages beside the api
    ui.run_with(api, mount_path='/monitor', storage_secret='pick your private secret here')
