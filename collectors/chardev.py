from .common.devices_type_dict import CHAR_DEVICE_TYPE
from .common.utils import read_sysfs

from rich.table import Table
from rich.columns import Columns
from rich import box


class CharacterDevice:

    def __init__(self):
        pass

    def parse_device_line(self, line) -> list:
        parse_line = line.split(" ")
        parse_line = [el for el in parse_line if el != ""]
        return parse_line

    def get_device_type(self, line) -> tuple[bool, str | None]:
        data = self.parse_device_line(line)
        if (len(data) > 1):
            type_ = data[0] + " " + data[1]
            if type_ in CHAR_DEVICE_TYPE:
                return True, type_

        return False, None

    def get_device_major_name(self, device) -> tuple[str, str] | None:
        line = self.parse_device_line(device)
        if (len(line) > 1):
            return (line[0], line[1])
        return None

    def collect(self) -> dict:

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

        return {"character_devices": character_devices,
                "block_devices": block_devices}

    @staticmethod
    def chunk_list(items, n_chunks):
        k, r = divmod(len(items), n_chunks)
        chunks = []
        start = 0
        for i in range(n_chunks):
            # les r premières tranches ont un élément de plus
            size = k + (1 if i < r else 0)
            chunks.append(items[start:start + size])
            start += size
        return chunks

    @staticmethod
    def make_table(rows):
        table = Table(box=box.SIMPLE_HEAVY, show_lines=False, show_header=True)
        table.add_column(style="cyan bold", justify="right")
        table.add_column(style="white")
        for major, name in rows:
            table.add_row(major, name)
        return table

    @staticmethod
    def display_in_columns(devices, console, n_columns=3):
        chunks = CharacterDevice.chunk_list(devices, n_columns)
        tables = [CharacterDevice.make_table(chunk) for chunk in chunks]
        console.print(Columns(tables))

    def render_full(self, devices, console):
        for device_type, device in devices.items():
            console.print(f"[bold]{device_type}[/bold]")
            CharacterDevice.display_in_columns(device, console, n_columns=5)
