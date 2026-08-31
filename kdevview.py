import argparse
import json
import time

from rich.console import Console, Group
from rich.live import Live
from rich.rule import Rule
from collectors.chardev import CharacterDevice
from collectors.modules import Modules
from collectors.i2c import I2CDevice
from collectors.usb import UsbDevices
from collectors.common.devices_type_dict import DEVICES, CURRENT_VERSION

console = Console()

DEVICES_COLLECTOR = {
    "chardev": CharacterDevice(),
    "modules": Modules(),
    "i2c": I2CDevice(),
    "usb": UsbDevices()
}


def collect_devices(device: str | None = None) -> dict:

    result = {}

    if device is not None:
        collector = DEVICES_COLLECTOR[device]
        result[device] = collector.collect()
    else:
        for device in DEVICES:
            collector = DEVICES_COLLECTOR[device]
            result[device] = collector.collect()

    return result


def display_devices(devices_states, console, colone):
    for section, data in devices_states.items():
        collector = DEVICES_COLLECTOR[section]
        collector.display_dashboard(collector, data, console, colone)


class KdevviewCommands:

    def __init__(self):

        self.start_time = time.time()

        parser = argparse.ArgumentParser(prog="kdevview")

        parser.add_argument("-o", "--only", choices=DEVICES,
                            help="Display only one device")
        parser.add_argument("-i", "--interval", type=int,
                            default=2, help="Set refresh interval in seconds")
        parser.add_argument("--no-color", action="store_true",
                            help="Desactivate color")
        parser.add_argument("-v", "--version", action="version",
                            version=CURRENT_VERSION, help="Show version")

        parser.add_argument("-c", "--colone", type=int, default=0,
                            help="Number of columns to display (0=vertical, 1-4 = multi-column)")

        exclusive_group = parser.add_mutually_exclusive_group()
        exclusive_group.add_argument(
            "-w", "--watch", action="store_true", help="Active live monitoring")
        exclusive_group.add_argument(
            "-j", "--json", action="store_true", help="Display data in json")

        self.args = parser.parse_args()

        if self.args.watch:
            self.run_watch()
        elif self.args.json:
            self.run_json()
        else:
            self.run_snapshot()

    def run_json(self):
        get_devices_state = collect_devices(self.args.only)
        print(json.dumps(get_devices_state, indent=2))

    def get_renderable(self, last_device_state, new_device_timestamps, removed_device_timestamps):
        if not self.args.only:
            renderables = []
            for section in DEVICES:
                collector = DEVICES_COLLECTOR[section]
                if section in last_device_state:
                    data = last_device_state[section]
                    for title, device_data in data.items():
                        renderables.append(Rule(title, style="cyan"))
                        renderable = collector.render_full(
                            device_data, self.args.colone, new_device_timestamps, removed_device_timestamps)
                        renderables.append(renderable)
            return Group(*renderables) if renderables else console.print("")
        else:
            collector = DEVICES_COLLECTOR[self.args.only]
            data = last_device_state[self.args.only]
            title = list(data.keys())[0]
            device_data = data[title]
            renderable = collector.render_full(
                device_data, self.args.colone, new_device_timestamps, removed_device_timestamps)
            return Group(Rule(title, style="cyan"), renderable)

    def _clean_timestamps(self, timestamps: dict, current_time: float, timeout: float = 5) -> None:
        to_remove = [d for d, t in timestamps.items() if current_time - t > timeout]
        for device in to_remove:
            del timestamps[device]

    def run_watch(self):
        console.print("[yellow]Press 'Ctrl + c' to quit[/yellow]\n")

        new_device_timestamps = {}
        removed_device_timestamps = {}

        last_device_state_dict = collect_devices(self.args.only)
        last_device_state_list = set(last_device_state_dict["usb"]["USB DEVICES"])

        if not self.args.only:
            for device in DEVICES:
                DEVICES_COLLECTOR[device].convert_dict_to_set(last_device_state_dict)

        try:
            with Live(console=console) as live:
                while True:
                    new_device_state_dict = collect_devices(self.args.only)
                    new_devices_state_list = set(new_device_state_dict["usb"]["USB DEVICES"])

                    new_device = new_devices_state_list - last_device_state_list
                    removed_device = last_device_state_list - new_devices_state_list
                    current_time = time.time()

                    for device in new_device:
                        new_device_timestamps[device] = current_time
                    for device in removed_device:
                        removed_device_timestamps[device] = current_time

                    self._clean_timestamps(new_device_timestamps, current_time)
                    self._clean_timestamps(removed_device_timestamps, current_time)

                    if not self.args.only:
                        for device in DEVICES:
                            DEVICES_COLLECTOR[device].convert_dict_to_set(new_device_state_dict)

                    last_device_state_dict = new_device_state_dict
                    last_device_state_list = new_devices_state_list

                    live.update(self.get_renderable(
                        last_device_state_dict, new_device_timestamps, removed_device_timestamps))

                    time.sleep(self.args.interval)

        except KeyboardInterrupt:
            elapsed = time.time() - self.start_time
            minutes, seconds = divmod(elapsed, 60)
            console.print(
                f"\n[yellow]Stopped after {int(minutes)}m {int(seconds)}s ({elapsed:.3f}s)[/yellow]\n")

    def run_snapshot(self):
        get_devices_state = collect_devices(self.args.only)
        display_devices(get_devices_state, console, self.args.colone)


test = KdevviewCommands()
