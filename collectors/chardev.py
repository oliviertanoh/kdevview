from .common.devices_type_dict import CHAR_DEVICE_TYPE, DEVICES, DEVICES_COLLECTORS
from .common.utils import read_sysfs, chunk_list
from .collector import Collector

from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.columns import Columns
from rich import box


class CharacterDevice (Collector):
    """Collects and displays character and block devices from /proc/devices."""

    def __init__(self):
        pass

    def parse_device_line(self, line) -> list:
        """Parse a device line into tokens."""
        parse_line = line.split(" ")
        parse_line = [el for el in parse_line if el != ""]
        return parse_line

    def get_device_type(self, line) -> tuple[bool, str | None]:
        """Identify device type (character or block devices)."""
        data = self.parse_device_line(line)
        if (len(data) > 1):
            type_ = data[0] + " " + data[1]
            if type_ in CHAR_DEVICE_TYPE:
                return True, type_

        return False, None

    def get_device_major_name(self, device) -> tuple[str, str] | None:
        """Extract major number and device name."""
        line = self.parse_device_line(device)
        if (len(line) > 1):
            return (line[0], line[1])
        return None

    def collect(self) -> dict:
        """Collect character and block devices from /proc/devices."""

        character_devices = []
        block_devices = []

        is_device_char = False
        current_device_type = None
        device_content = read_sysfs("/proc/devices")

        for device in device_content:

            is_device_char, device_type = self.get_device_type(device)

            if is_device_char:
                current_device_type = device_type

            else:

                if current_device_type == "Character devices:":
                    result = self.get_device_major_name(device)
                    if result is not None:
                        character_devices.append(result)

                if current_device_type == "Block devices:":
                    result = self.get_device_major_name(device)
                    if result is not None:
                        block_devices.append(result)

        return {"CHARACTER DEVICES": character_devices,
                "BLOCK DEVICES": block_devices}

    def render_full(self, data, colone):
        """Create a table displaying devices in n columns."""
        if colone == 0:
            table = Table(box=box.SIMPLE_HEAD, show_header=True)
            table.add_column("Major", justify="right", style="cyan")
            table.add_column("Name")
            for major, name in data:
                table.add_row(major, name)
            return table

        chunks = chunk_list(data, n_chunks=colone)
        table = Table(box=box.SIMPLE_HEAD, show_header=True)

        for i in range(colone):
            table.add_column("Major", justify="right", style="cyan")
            table.add_column("Name")
            if i < colone - 1:
                table.add_column("", style="on blue")

        max_len = max(len(chunk) for chunk in chunks) if chunks else 0
        for row_idx in range(max_len):
            row_data = []
            for i, chunk in enumerate(chunks):
                if row_idx < len(chunk):
                    major, name = chunk[row_idx]
                    row_data.extend([major, name])
                else:
                    row_data.extend(["", ""])
                if i < colone - 1:
                    row_data.append("")
            table.add_row(*row_data)

        return table
