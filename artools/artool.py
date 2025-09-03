
from textual.app import App
from textual.widgets import Header, Footer, Static, Button, Select
from textual.containers import Vertical

class ArtToolApp(App):
    def compose(self):
        yield Header()
        with Vertical():
            yield Select(options=[("Network", "network"), ("Disk", "disk")], prompt="請選擇功能", id="main_menu")
            yield Button("離開程式", id="exit_button")
        yield Footer()

    async def on_mount(self):
        self.title = "ArtTool"

    async def on_button_pressed(self, event):
        if event.button.id == "exit_button":
            await self.action_quit()

    async def on_select_changed(self, event):
        if event.select.id == "main_menu":
            if event.value == "network":
                await self.push_screen(Static("Network 功能尚未實作"))
            elif event.value == "disk":
                await self.push_screen(Static("Disk 功能尚未實作"))

if __name__ == "__main__":
    ArtToolApp().run()