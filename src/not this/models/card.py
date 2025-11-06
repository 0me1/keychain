import flet as app


class Card(app.Container):
    def __init__(self, service_name, login, pwd):
        super().__init__()

        self.expand = True
        self.height = 75
        self.border_radius = 30
        self.bgcolor = app.Colors.SECONDARY_CONTAINER
        self.service_name = service_name
        self.login = login
        self.pwd = pwd

        self.content = app.Row(controls=[app.Icon(name=app.Icons.EURO_SYMBOL, size=70), 
                         app.Column(
                             controls=[app.Text(self.service_name), app.Text(self.login), app.Text(self.pwd)],
                             expand=True
                         ), 
                         app.Icon(name=app.Icons.ARROW_FORWARD_IOS)])