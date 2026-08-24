from .common.utils import read_sysfs, chunk_list
from .collector import Collector

from rich.table import Table
from rich.panel import Panel
from rich import box

import os


class I2CDevice (Collector):
    """Collects and displays I2C devices from /sys/bus/i2c/devices."""

    def __init__(self):
        pass

    def collect(self) -> dict:
        """Collect I2C devices and their properties."""
        i2c_devices = []
        list_device_path = "/sys/bus/i2c/devices/"

        try:
            list_driver = [f for f in os.listdir(list_device_path)
                           if os.path.isdir(os.path.join(list_device_path, f))]
            list_driver = [d for d in list_driver if "i2c" in d]

            for device in list_driver:
                device_name_path = list_device_path + device + "/name"
                device_state_path = list_device_path + device + "/device/enable"
                device_class_path = list_device_path + device + "/device/class"

                name = read_sysfs(device_name_path)
                state = read_sysfs(device_state_path)
                device_class = read_sysfs(device_class_path)

                name_str = name[0] if name else "N/A"
                state_str = state[0] if state else "N/A"
                class_str = device_class[0] if device_class else "N/A"

                i2c_devices.append((device, name_str, state_str, class_str))

        except (OSError, FileNotFoundError):
            pass

        return {"I2C DEVICES": i2c_devices}

    def render_full(self, data, colone):
        """Create a table displaying I2C devices in n columns."""
        if colone == 0:
            table = Table(box=box.SIMPLE_HEAD, show_header=True)
            table.add_column("Device", style="cyan bold", justify="right", overflow="fold")
            table.add_column("Name", style="white", overflow="fold")
            table.add_column("State", style="white", overflow="fold")
            table.add_column("Class", style="white", overflow="fold")
            for device, name, state, device_class in data:
                table.add_row(device, name, state, device_class)
            return table

        chunks = chunk_list(data, n_chunks=colone)
        table = Table(box=box.SIMPLE_HEAD, show_header=True)

        for i in range(colone):
            table.add_column("Device", style="cyan bold",
                             justify="right", overflow="fold")
            table.add_column("Name", style="white", overflow="fold")
            table.add_column("State", style="white", overflow="fold")
            table.add_column("Class", style="white", overflow="fold")
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
