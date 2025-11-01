import flet as app

from card_manager import filter_card, get_in_card


def current(page: app.Page):


    def search(s):
        s = s_bar.value.lower().strip()

        if len(s) > 3:
            filter_card(s)
            fcards = get_in_card()[1]
            col = app.Column(spacing=10, expand=True, controls=fcards, scroll=app.ScrollMode.ALWAYS, on_scroll_interval=0)
            page.update()
        


    s_bar = app.SearchBar(
        bar_hint_text="search",
        on_change=search
    )



    return s_bar