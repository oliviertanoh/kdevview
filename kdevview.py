import argparse
import json

from rich.console import Console
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

    def run_watch(self):
        pass

    def run_snapshot(self):
        get_devices_state = collect_devices(self.args.only)
        display_devices(get_devices_state, console, self.args.colone)


test = KdevviewCommands()
