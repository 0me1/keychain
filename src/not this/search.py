import flet as app

from card_manager import filter_card, get_in_card

cards_container = app.Column(spacing=10, expand=True, scroll=app.ScrollMode.AUTO, controls=get_in_card()[0])

def start(page: app.Page):
    page.add(cards_container)
    page.update()

def current(page: app.Page):


    def search(s):
        s = s_bar.value.lower().strip()

    
        filter_card(s)
        fcards = get_in_card()[1]
        cards_container.controls = fcards
        page.update()
    


    s_bar = app.SearchBar(
        bar_hint_text="search",
        on_change=search
    )



    return s_bar