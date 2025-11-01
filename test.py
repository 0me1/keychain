import flet as ft

def main(page: ft.Page):
    page.title = "Карточки с поиском"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window.width = 400
    page.window.height = 700
    page.scroll = ft.ScrollMode.AUTO

    # Список карточек (данные)
    cards_data = [
        {"title": "Python", "subtitle": "Язык программирования", "icon": ft.Icons.CODE},
        {"title": "Flet", "subtitle": "UI фреймворк", "icon": ft.Icons.FLUTTER_DASH},
        {"title": "Django", "subtitle": "Веб-фреймворк", "icon": ft.Icons.WEB},
        {"title": "FastAPI", "subtitle": "API фреймворк", "icon": ft.Icons.API},
        {"title": "Docker", "subtitle": "Контейнеризация", "icon": ft.Icons.STORAGE},
        {"title": "Git", "subtitle": "Система контроля версий", "icon": ft.Icons.HISTORY},
    ]

    # Контейнер для карточек
    cards_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    # Функция создания карточки
    def create_card(item):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(item["icon"]),
                            title=ft.Text(item["title"], weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(item["subtitle"]),
                        ),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=15,
            ),
            elevation=2,
        )

    # Изначально добавляем все карточки
    for item in cards_data:
        cards_container.controls.append(create_card(item))

    # Поле поиска
    search_field = ft.TextField(
        hint_text="Поиск по названию...",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filter_cards(e.control.value.lower()),
        border_radius=30,
        filled=True,
    )

    # Функция фильтрации
    def filter_cards(query):
        cards_container.controls.clear()
        for item in cards_data:
            if query in item["title"].lower() or query in item["subtitle"].lower():
                cards_container.controls.append(create_card(item))
        page.update()

    # Нижнее меню
    def open_add_dialog(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Добавить карточку"),
            content=ft.Column(
                [
                    ft.TextField(label="Название", autofocus=True),
                    ft.TextField(label="Подзаголовок"),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: close_dialog(dialog)),
                ft.TextButton("Добавить", on_click=lambda e: add_card(dialog)),
            ],
        )
        # page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def add_card(dialog):
        title_field = dialog.content.controls[0]
        subtitle_field = dialog.content.controls[1]
        if title_field.value:
            new_item = {
                "title": title_field.value,
                "subtitle": subtitle_field.value or "Без описания",
                "icon": ft.Icons.STAR
            }
            cards_data.append(new_item)
            cards_container.controls.append(create_card(new_item))
            close_dialog(dialog)
            page.update()

    # Кнопка +
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=open_add_dialog,
        bgcolor=ft.Colors.BLUE,
    )

    # Нижняя панель навигации
    bottom_nav = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(ft.Icons.HOME, selected=True),
                ft.IconButton(ft.Icons.SEARCH),
                ft.Container(width=60),  # Пространство под FAB
                ft.IconButton(ft.Icons.FAVORITE),
                ft.IconButton(ft.Icons.PERSON),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=ft.Colors.SURFACE,
        padding=10,
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
    )

    # Основной layout
    page.add(
        ft.Column(
            [
                ft.Text("Мои карточки", size=24, weight=ft.FontWeight.BOLD),
                search_field,
                ft.Container(height=20),
                ft.Container(
                    content=cards_container,
                    expand=True,
                ),
            ],
            expand=True,
        ),
        ft.Stack(
            [
                bottom_nav,
                ft.Container(
                    content=fab,
                    alignment=ft.alignment.center,
                    top=page.height - 90,  # Поднимаем FAB над нижней панелью
                    left=page.width // 2 - 28,
                ),
            ],
            expand=False,
        ),
    )

    # Инициализация
    page.update()


# Запуск приложения
ft.app(target=main)