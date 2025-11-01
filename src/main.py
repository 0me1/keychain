import flet as app

from create_page import *
from search import *


def main(page: app.Page):
    general_options(page)
    appbar(page, current(page))
    bottom_appbar(page)
    current(page)


app.app(main)