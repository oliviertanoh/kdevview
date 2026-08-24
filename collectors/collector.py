from rich.panel import Panel
from abc import ABC, abstractmethod


class Collector:

    def __init__(self):
        pass

    @abstractmethod
    def collect(self) -> dict:
        ...

    @abstractmethod
    def render_full(self):
        ...

    def display_dashboard(self, collector, devices_states, console):
        for section, data in devices_states.items():
            renderable = collector.render_full(section, data)
            panel = Panel(renderable, title=section, border_style="cyan")
            console.print(panel)
