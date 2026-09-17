"""
Desktop application tests using Pywinauto and Pytest
Application: Calculator (Windows)
Author: Jose Camacho
"""
from support import utils, paths
from pywinauto import mouse as m, keyboard as k, Application


class CalculatorPage:
    def __init__(self, app_name: str):
        app_path = paths.desktop_app_paths[app_name]
        Application(backend="uia").start(app_path)
        app = Application(backend="uia").connect(title_re=f'.*{app_name}.*', timeout=10)
        app_window = app.top_window()
        self.app = app
        self.window = app_window

    def wait_for_ready(self):
        self.window.exists(timeout=5)
        return self

    def click_button_by_name(self, button_name: str):
        self.window.child_window(title=button_name, control_type="Button").click()

    def get_calculator_result(self) -> str:
        result_text = self.window.child_window(auto_id="CalculatorResults", control_type="Text")
        raw_text = result_text.window_text()
        return raw_text.replace("Display is", "").strip()

    def close(self):
        self.app.kill()
