from .common.utils import read_sysfs, chunk_list
from .collector import Collector

from rich.table import Table
from rich.panel import Panel
from rich import box

import os


class UsbDevices(Collector):

    def __init__(self):

        self.usb_device_data = []

    def collect(self):
        """ Collect usb devices and their property. """

        usb_devices = []

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

                usb_devices.append((
                    device_num[0], device_id[0], device_product_name[0], device_vendor[0], device_manufacturer[0]))

        except (OSError, FileNotFoundError):
            pass

        return {"USB DEVICES": usb_devices}

    def convert_dict_to_set(self, devices_tuples: list) -> list:

        list_devices_hash = []
        for bus, id, name, vendor, manufacturer in devices_tuples["usb"]["USB DEVICES"]:
            list_devices_hash.append("usb-"+bus+":"+id)

        return list_devices_hash

    def render_full(self, data, colone):
        """Create a table displaying USB devices in n columns."""
        if colone == 0:
            table = Table(box=box.SIMPLE_HEAD, show_header=True)
            table.add_column("Bus", style="cyan bold",
                             justify="right", overflow="fold")
            table.add_column("Id", style="white", overflow="fold")
            table.add_column("Name", style="white", overflow="fold")
            table.add_column("Vendor", style="white", overflow="fold")
            table.add_column("Manufacturer", style="white", overflow="fold")
            for bus, id, name, vendor, manufacturer in data:
                table.add_row(bus, id, name, vendor, manufacturer)
            return table

        chunks = chunk_list(data, n_chunks=colone)
        table = Table(box=box.SIMPLE_HEAD, show_header=True)

        for i in range(colone):
            table.add_column("Bus", style="cyan bold",
                             justify="right", overflow="fold")
            table.add_column("Id", style="white", overflow="fold")
            table.add_column("Name", style="white", overflow="fold")
            table.add_column("Vendor", style="white", overflow="fold")
            table.add_column(
                "Manufacturer", style="white", overflow="fold")
            if i < colone - 1:
                table.add_column("", style="on blue")

        max_len = max(len(chunk) for chunk in chunks) if chunks else 0
        for row_idx in range(max_len):
            row_data = []
            for i, chunk in enumerate(chunks):
                if row_idx < len(chunk):
                    device, name, state, device_class = chunk[row_idx]
                    row_data.extend([device, name, state, device_class])
                else:
                    row_data.extend(["", "", "", ""])
                if i < colone - 1:
                    row_data.append("")
            table.add_row(*row_data)

        return table
