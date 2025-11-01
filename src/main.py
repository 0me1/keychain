import flet as app

from create_page import *
from search import *


def main(page: app.Page):
    page.title = "Test Keychain"
    page.horizontal_alignment = app.CrossAxisAlignment.CENTER
    
    appbar(page, current(page))
    bottom_appbar(page)
    current(page)


app.app(main)