class TemasManager:
    def __init__(self, master):
        self.master = master
        self.selected_theme_name = None

        self.THEMES = {
            "Tema Claro": {
                "background": "white",
                "foreground": "black",
                "button_bg": "#f0f0f0",
                "button_fg": "black",
            },
            "Tema Oscuro": {
                "background": "#1e1e1e",
                "foreground": "white",
                "button_bg": "#2e2e2e",
                "button_fg": "white",
            },
            "Tema Azul": {
                "background": "#cfe2f3",
                "foreground": "black",
                "button_bg": "#4d94ff",
                "button_fg": "white",
            }
        }

    def change_theme(self, theme_name):
        selected_theme = self.THEMES[theme_name]
        self.master.config(bg=selected_theme["background"])
        for widget in self.root.winfo_children():
            widget.config(bg=selected_theme["button_bg"], fg=selected_theme["button_fg"])

        self.selected_theme_name = theme_name

    def get_current_theme(self):
        return self.selected_theme_name