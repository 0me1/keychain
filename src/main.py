import flet as app
from pydantic import BaseModel
import uuid

import json
import os
from pydantic import BaseModel



# from create_page import *
# from card_manager import *
# from search import *

class CardItem(BaseModel):
    service: str
    login: str
    password: str

# storage

DATA_PATH = "./local_storage/"
os.makedirs(DATA_PATH, exist_ok=True)

class Pull():
    @staticmethod
    def get() -> list[CardItem]:
        path = os.path.join(DATA_PATH, "data.json") #type: ignore

        with open(path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            result = [CardItem(**p) for p in data]
        
        return result

             
    @staticmethod
    def set(data: list[CardItem]):
        path = os.path.join(DATA_PATH, "data.json") #type: ignore
        with open(path, 'w', encoding="utf-8") as file:
            json.dump([p.model_dump() for p in data], file, indent=4)

    # @staticmethod
    # def set(page: app.Page, data: list[CardItem]):
    #     page.client_storage.set(key="1", value=data)

    # @staticmethod
    # def get(page: app.Page):
    #     data = page.client_storage.get("1")
    #     result = [CardItem(**p) for p in data] #type: ignore

    #     return result


active_card = CardItem(service="1", login="1", password="1")

# main
def main(page: app.Page):
    page.title = "Test Keychain"
    page.theme_mode = app.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    try:
        cards_data = Pull.get()
    except Exception:
        cards_data = [CardItem(service="Placeholder", login="Placeholder", password="Placeholder",)]
    

    def search():
        query = search_bar.value.lower() #type: ignore
        result = [c for c in cards_data if query in c.service.lower() or query in c.login.lower()]
        build_cards(result)

    search_bar = app.SearchBar(
        bar_hint_text="search...",
        on_change=lambda e: search(),
        expand=True
    )

    cards_container = app.Column(scroll=app.ScrollMode.AUTO, expand=True)


    def build_cards(card_list: list[CardItem]):
        cards_container.controls.clear()
        for card in card_list:
            cards_container.controls.append(
                app.Container(
                    padding=10,
                    height=75,
                    border_radius=30,
                    bgcolor=app.Colors.SECONDARY_CONTAINER,
                    on_click=lambda e, c=card: open_detail(c),
                    content=app.Row(
                        # alignment=app.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            app.Container(app.Column([app.Text(f"{card.service[0]}", size=40, scale=1.5, color=app.Colors.SURFACE_TINT)]), width=60, alignment=app.alignment.top_center),
                            app.Column(controls=[
                                app.Text(card.service, size=20),
                                app.Text(card.login),
                            ], expand=True, spacing=0),
                            app.Icon(name=app.Icons.ARROW_FORWARD_IOS)
                        ], spacing=5
                    )
                )
            )
        page.update()


    def show_add_dialog(e):
        title_field = app.TextField(label="Сервис", autofocus=True)
        desc_field = app.TextField(label="Логин")
        password_field = app.TextField(label="Пароль")

        dlg = app.AlertDialog(
            title=app.Text("Новая карточка"),
            content=app.Column([title_field, desc_field, password_field], height=350, expand=True),
            actions=[
                app.TextButton("Отмена", on_click=lambda e: page.close(dlg)),
                app.FilledButton("Создать", on_click=lambda e: (
                    cards_data.append(CardItem(
                        service=title_field.value.strip() or "Без названия", #type: ignore
                        login=desc_field.value.strip() or "Нет описания", #type: ignore
                        password=password_field.value.strip() or "Нет пароля" #type: ignore
                    )),
                    search(),
                    Pull.set(cards_data),
                    page.close(dlg)
                )),
            ],
        )
        page.open(dlg)


    detail_title = app.Text(size=32, weight=app.FontWeight.BOLD, selectable=True)
    detail_password = app.Text(size=21, weight=app.FontWeight.BOLD, selectable=True)
    detail_login = app.Text(size=21, weight=app.FontWeight.BOLD, selectable=True)

    back_btn = app.IconButton(app.Icons.ARROW_BACK_IOS_NEW, on_click=lambda e: show_main())
    change_btn = app.IconButton(app.Icons.CREATE, on_click=lambda e, c=active_card:  open_change_details())
    

    detail_view = app.Container(
        visible=False,
        expand=True,
        content= app.Column(controls=[
            app.Row(controls=[back_btn, change_btn]),
            app.Container(
                margin=15,
                border_radius=10,
                padding=10,
                bgcolor=app.Colors.SECONDARY_CONTAINER,
                content=app.Column(
                    controls=[
                        
                        app.Row([detail_title]),
                        app.Divider(color=app.Colors.SURFACE),
                        app.Row([detail_login]),
                        app.Divider(color=app.Colors.SURFACE),
                        app.Row([detail_password]),
                        app.Divider(color=app.Colors.SURFACE),
                    ]
                )
            )
            ]))
            

    main_view = app.Container(
        visible=True,
        expand=True,
        content=app.Column([
            app.Container(
                content=app.Row([
                    search_bar,
                ], alignment=app.MainAxisAlignment.CENTER),
                padding=15,
                bgcolor=app.Colors.SURFACE,
            ),
            app.Divider(),
            app.Container(cards_container, padding=15, expand=True),
        ], expand=True)
    )

    cancel_btn = app.IconButton(app.Icons.ARROW_BACK_IOS_NEW, on_click=lambda e: open_detail(active_card))
    delete_btn = app.FilledButton("Delete", on_click=lambda e: delete_card())
    submit_btn = app.FilledButton("Submit", on_click=lambda e: change_card())
    service_field = app.TextField()
    login_field = app.TextField()
    password_field = app.TextField()

    change_detail = app.Container(
        visible=False,
        expand=True,
        content= app.Column(controls=[
            app.Row(controls=[cancel_btn]),
            app.Container(
                margin=15,
                border_radius=10,
                padding=10,
                bgcolor=app.Colors.SECONDARY_CONTAINER,
                content=app.Column(
                    controls=[
                        
                        app.Row([service_field]),
                        app.Divider(color=app.Colors.SURFACE),
                        app.Row([login_field]),
                        app.Divider(color=app.Colors.SURFACE),
                        app.Row([password_field]),
                        app.Divider(color=app.Colors.SURFACE),

                    ]
                )
            ),
            submit_btn,
            delete_btn
            ]))

    def open_detail(card: CardItem):
        global active_card
        active_card = card
        detail_title.value = card.service
        detail_login.value = card.login
        detail_password.value = card.password

        main_view.visible = False
        detail_view.visible = True
        change_detail.visible = False
        page.update()
    
    def open_change_details():
        global active_card
        service_field.value = active_card.service
        login_field.value = active_card.login
        password_field.value = active_card.password

        main_view.visible = False
        detail_view.visible = False
        change_detail.visible = True
        page.update()

    def show_main():
        change_detail.visible = False
        detail_view.visible = False
        main_view.visible = True
        search()

    def change_card():
        index = cards_data.index(active_card)
        cards_data[index] = CardItem(service=service_field.value, login=login_field.value, password=password_field.value) #type: ignore
        Pull.set(cards_data)
        open_detail(cards_data[index])

    def delete_card():
        index = cards_data.index(active_card)
        cards_data.pop(index)
        Pull.set(cards_data)
        show_main()


    bottom_appbar = app.BottomAppBar(
        content=app.Row(
            controls=[
                app.IconButton(icon=app.Icons.SORT, icon_color=app.Colors.WHITE),
                app.Container(expand=True),
                app.IconButton(icon=app.Icons.ADD, icon_color=app.Colors.WHITE, on_click=show_add_dialog)
            ]
        ),
    )

    stack = app.Stack([main_view, detail_view, change_detail], expand=True)
    page.add(app.SafeArea(app.Column([stack, bottom_appbar], expand=True, spacing=0), expand=True))
    build_cards(cards_data)

    
app.app(main)

# bottom shit
# z stack in details
# 1 var for all values