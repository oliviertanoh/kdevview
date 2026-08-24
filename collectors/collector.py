from rich.panel import Panel
from abc import ABC, abstractmethod


class Collector:
    """Base class for device collectors."""

    def __init__(self):
        pass

    @abstractmethod
    def collect(self) -> dict:
        """Collect device data and return as dictionary."""
        ...

    @abstractmethod
    def render_full(self):
        """Render collected data as a table."""
        ...

    def display_dashboard(self, collector, devices_states, console):
        """Display dashboard with collected device data."""

        for section, data in devices_states.items():
            renderable = collector.render_full(section, data)
            panel = Panel(renderable, title=section, border_style="cyan")
            console.print(panel)
