from .common.utils import read_sysfs, chunk_list
from .collector import Collector

from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich import box

import os
import time


class UsbDevices(Collector):

    def __init__(self):

        self.usb_device_data = []
        self.table = Table(box=box.SIMPLE_HEAD, show_header=True)

    def collect(self):
        """ Collect usb devices and their property. """

        self.usb_device_data = []

        list_devices_path = "/sys/bus/usb/devices/"

        list_driver = [f for f in os.listdir(list_devices_path)
                       if os.path.isdir(os.path.join(list_devices_path, f))]

        list_driver = [d for d in list_driver if ":" not in d]

        try:

            for device in list_driver:

                device_id_path = list_devices_path + device + "/idProduct"
                device_vendor_path = list_devices_path + device + "/idVendor"
                device_num_path = list_devices_path + device + "/devnum"
                device_product_name_path = list_devices_path + device + "/product"
                device_manufacturer_path = list_devices_path + device + "/manufacturer"

                device_id = read_sysfs(device_id_path)
                device_vendor = read_sysfs(device_vendor_path)
                device_num = read_sysfs(device_num_path)
                device_product_name = read_sysfs(device_product_name_path)
                device_manufacturer = read_sysfs(device_manufacturer_path)

                self.usb_device_data.append((
                    device_num[0], device_id[0], device_product_name[0], device_vendor[0], device_manufacturer[0]))

        except (OSError, FileNotFoundError):
            pass

        return {"USB DEVICES": self.usb_device_data}

    def convert_dict_to_set(self, devices_tuples: list) -> list:

        list_devices_hash = []
        for bus, id, name, vendor, manufacturer in devices_tuples["usb"]["USB DEVICES"]:
            list_devices_hash.append("usb:"+bus+":"+id)

        return list_devices_hash

    def update_table(self, hash_new_device):

        id_new_device = hash_new_device[0].split(":")[2]

        with Live(self.table, refresh_per_second=0.1):

            for bus, id, name, vendor, manufacture in self.usb_device_data:

                if id == id_new_device:
                    self.table.add_row(bus, id, name, vendor,
                                       manufacture, style="green bold")

    def render_full(self, data, colone, new_device_timestamps=None, removed_device_timestamps=None):
        """Create a table displaying USB devices in n columns."""
        if new_device_timestamps is None:
            new_device_timestamps = {}
        if removed_device_timestamps is None:
            removed_device_timestamps = {}

        self.table = Table(box=box.SIMPLE_HEAD, show_header=True)
        if colone == 0:
            self.table.add_column("Bus", style="cyan bold",
                                  justify="right", overflow="fold")
            self.table.add_column("Id", style="white", overflow="fold")
            self.table.add_column("Name", style="white", overflow="fold")
            self.table.add_column("Vendor", style="white", overflow="fold")
            self.table.add_column(
                "Manufacturer", style="white", overflow="fold")
            for bus, id, name, vendor, manufacturer in data:
                device_tuple = (bus, id, name, vendor, manufacturer)
                style = "green bold" if device_tuple in new_device_timestamps else ""
                self.table.add_row(bus, id, name, vendor, manufacturer, style=style)

            for device_tuple in removed_device_timestamps:
                bus, id, name, vendor, manufacturer = device_tuple
                self.table.add_row(bus, id, name, vendor, manufacturer, style="red bold")

            return self.table

        chunks = chunk_list(data, n_chunks=colone)

        for i in range(colone):
            self.table.add_column("Bus", style="cyan bold",
                                  justify="right", overflow="fold")
            self.table.add_column("Id", style="white", overflow="fold")
            self.table.add_column("Name", style="white", overflow="fold")
            self.table.add_column("Vendor", style="white", overflow="fold")
            self.table.add_column(
                "Manufacturer", style="white", overflow="fold")
            if i < colone - 1:
                self.table.add_column("", style="on blue")

        max_len = max(len(chunk) for chunk in chunks) if chunks else 0
        for row_idx in range(max_len):
            row_data = []
            for i, chunk in enumerate(chunks):
                if row_idx < len(chunk):
                    bus, id, name, vendor, manufacturer = chunk[row_idx]
                    device_tuple = (bus, id, name, vendor, manufacturer)
                    style = "green bold" if device_tuple in new_device_timestamps else ""
                    row_data.extend([bus, id, name, vendor, manufacturer])
                else:
                    row_data.extend(["", "", "", "", ""])
                if i < colone - 1:
                    row_data.append("")
            self.table.add_row(*row_data)

        return self.table
