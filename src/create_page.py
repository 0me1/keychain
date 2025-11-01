from typing import Any, Sequence
import flet as app

from models.card import Card
from card_manager import get_in_card
from search import current


cards_container = app.Column(spacing=10, expand=True, scroll=app.ScrollMode.AUTO)


def appbar(page: app.Page, search_bar):
    page.appbar = app.AppBar(
        bgcolor=app.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[search_bar]
    )
    page.update()


def bottom_appbar(page: app.Page):
    page.bottom_appbar = app.BottomAppBar(
        content=app.Row(
            controls=[
                app.IconButton(icon=app.Icons.SORT, icon_color=app.Colors.WHITE),
                app.Container(expand=True),
                app.IconButton(icon=app.Icons.ADD, icon_color=app.Colors.WHITE)
            ]
        ),
    )
    page.update()


