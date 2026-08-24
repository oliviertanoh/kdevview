from .common.utils import read_sysfs, chunk_list
from .chardev import CharacterDevice
from .collector import Collector

from rich.table import Table
from rich.columns import Columns
from rich import box


class Modules (Collector):

    def __init__(self):
        pass

    def parse_device_line(self, line) -> list:
        parse_line = line.split(" ")
        parse_line = [el for el in parse_line if el !=
                      "" and el != "-" and el != "Live" and el != "0x0000000000000000"]
        return tuple(parse_line)

    def collect(self) -> dict:
        modules = []

        modules_loaded = read_sysfs("/proc/modules")

        for module in modules_loaded:
            modules.append(self.parse_device_line(module))

        return {"MODULES": modules}

    def render_full(self, section, data):
        chunks = chunk_list(data, n_chunks=3)
        table = Table(box=box.SIMPLE_HEAVY, show_header=True)

        for _ in range(3):
            table.add_column("Module", style="cyan bold", justify="right")
            table.add_column("Size", style="white")
            table.add_column("Used", style="white")
            table.add_column("By", style="white")

        max_len = max(len(chunk) for chunk in chunks) if chunks else 0
        for row_idx in range(max_len):
            row_data = []
            for chunk in chunks:
                if row_idx < len(chunk):
                    module = chunk[row_idx]
                    if len(module) == 3:
                        row_data.extend([module[0], module[1], module[2], ""])
                    else:
                        row_data.extend(
                            [module[0], module[1], module[2], module[3]])
                else:
                    row_data.extend(["", "", "", ""])
            table.add_row(*row_data)

        return table
