from .common.utils import read_sysfs
from .chardev import CharacterDevice

from rich.table import Table
from rich.columns import Columns
from rich import box


class Modules:

    def parse_device_line(self, line) -> list:
        parse_line = line.split(" ")
        parse_line = [el for el in parse_line if el !=
                      "" and el != "-" and el != "Live" and el != "0x0000000000000000"]
        return tuple(parse_line)

    def __init__(self):
        pass

    def collect(self) -> dict:
        modules = []

        modules_loaded = read_sysfs("/proc/modules")

        for module in modules_loaded:
            modules.append(self.parse_device_line(module))

        return {"MODULES": modules}

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
        table = Table(box=box.SIMPLE_HEAVY,
                      show_lines=False, show_header=True)
        table.add_column(style="cyan bold", justify="right")
        table.add_column(style="white")
        table.add_column(style="white")
        table.add_column(style="white")

        for module in rows:
            if (len(module) == 3):
                table.add_row(module[0], module[1], module[2], "0")
            else:
                table.add_row(module[0], module[1], module[2], module[3])

        return table

    @staticmethod
    def display_in_columns(devices, console, n_columns=3):
        chunks = Modules.chunk_list(devices, n_columns)
        tables = [Modules.make_table(chunk) for chunk in chunks]
        console.print(Columns(tables))

    def render_full(self, devices, console):
        for device_type, device in devices.items():
            console.print(f"[bold]{device_type}[/bold]")
            Modules.display_in_columns(device, console, n_columns=7)


# test = Modules()
# module = test.collect()
# print(module)
