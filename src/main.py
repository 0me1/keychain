import flet as app
import uuid

# from create_page import *
# from card_manager import *
# from search import *


class CardItem():
    def __init__(self, service, login, password):
        self.id = str(uuid.uuid4())
        self.service = service
        self.login = login
        self.password = password

active_card = CardItem("...", "...", "...")

def main(page: app.Page):
    page.title = "Test Keychain"
    page.theme_mode = app.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    cards_data = [
        CardItem("Mail", "login", "password"),
        CardItem("GMail", "login", "password"),
        CardItem("YandexMail", "login", "password")
    ]

    

    def search():
        query = search_bar.value.lower()
        result = [c for c in cards_data if query in c.service.lower() or query in c.login.lower()]
        build_cards(result)

    search_bar = app.SearchBar(
        bar_hint_text="search...",
        on_change=lambda e: search(), # зачем лямбда
        expand=True
    )

    cards_container = app.Column(scroll=app.ScrollMode.AUTO, expand=True)


    def build_cards(card_list: list[CardItem]):
        cards_container.controls.clear()
        for card in card_list:
            cards_container.controls.append(
                app.Container(
                    height=75,
                    border_radius=30,
                    bgcolor=app.Colors.SECONDARY_CONTAINER,
                    on_click=lambda e, c=card: open_detail(c), # зачем лямбда
                    content=app.Row(
                        alignment=app.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            app.Icon(name=app.Icons.EURO_SYMBOL, size=70),
                            app.Column(controls=[
                                app.Text(card.service, selectable=True),
                                app.Text(card.login, selectable=True),
                            ]),
                            app.Icon(name=app.Icons.ARROW_FORWARD_IOS)
                        ]
                    )
                )
            )
        page.update()

    def delete_card(card):
        cards_data.remove(card)
        search()

    def show_add_dialog(e):
        title_field = app.TextField(label="Сервис", autofocus=True)
        desc_field = app.TextField(label="Логин")
        password_field = app.TextField(label="Пароль")

        dlg = app.AlertDialog(
            modal=True,
            title=app.Text("Новая карточка"),
            content=app.Column([title_field, desc_field, password_field], expand=True),
            actions=[
                app.TextButton("Отмена", on_click=lambda e: page.close(dlg)),
                app.FilledButton("Создать", on_click=lambda e: (
                    cards_data.append(CardItem(
                        title_field.value.strip() or "Без названия",
                        desc_field.value.strip() or "Нет описания",
                        password_field.value.strip() or "Нет пароля"
                    )),
                    search(),
                    page.close(dlg)
                )),
            ],
        )
        page.open(dlg)


    detail_title = app.Text(size=32, weight=app.FontWeight.BOLD, selectable=True)
    detail_password = app.Text(size=21, weight=app.FontWeight.BOLD, selectable=True)
    detail_login = app.Text(size=21, weight=app.FontWeight.BOLD, selectable=True)

    back_btn = app.IconButton(app.Icons.ARROW_BACK_IOS_NEW, on_click=lambda e: show_main())
    change_btn = app.IconButton(app.Icons.ARROW_FORWARD_IOS, on_click=lambda e, c=active_card:  open_change_details())
    

    detail_view = app.SafeArea(
        visible=False,
        expand=True,
        content= app.Column(controls=[
            app.Row(controls=[back_btn, change_btn]),
            app.Container(
                margin=40,
                border_radius=20,
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
            

    main_view = app.SafeArea(
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

    cancel_btn = app.IconButton(app.Icons.CANCEL, on_click=lambda e: open_detail(active_card))
    submit_btn = app.FilledButton("Submit", on_click=...)
    service_field = app.TextField(label="...")
    login_field = app.TextField(label="...")
    password_field = app.TextField(label="...")

    change_detail = app.SafeArea(
        visible=False,
        expand=True,
        content= app.Column(controls=[
            app.Row(controls=[cancel_btn]),
            app.Container(
                margin=40,
                border_radius=20,
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
            )
            ]))

    def open_detail(card: CardItem | None):
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
        service_field.label = active_card.service
        login_field.label = active_card.login
        password_field.label = active_card.password

        main_view.visible = False
        detail_view.visible = False
        change_detail.visible = True
        page.update()

    def show_main():
        change_detail.visible = False
        detail_view.visible = False
        main_view.visible = True
        search_bar.value = ""
        search()


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
    page.add(app.Column([stack, bottom_appbar], expand=True, spacing=0))
    build_cards(cards_data)

app.app(main)