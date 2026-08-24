from .common.utils import read_sysfs, chunk_list
from .chardev import CharacterDevice
from .collector import Collector

from rich.table import Table
from rich.columns import Columns
from rich import box


class Modules (Collector):
    """Collects and displays kernel modules from /proc/modules."""

    def __init__(self):
        pass

    def parse_device_line(self, line) -> list:
        """Parse a module line into components."""
        parse_line = line.split(" ")
        parse_line = [el for el in parse_line if el !=
                      "" and el != "-" and el != "Live" and el != "0x0000000000000000"]
        return tuple(parse_line)

    def collect(self) -> dict:
        """Collect kernel modules from /proc/modules."""
        modules = []

        modules_loaded = read_sysfs("/proc/modules")

        for module in modules_loaded:
            modules.append(self.parse_device_line(module))

        return {"MODULES": modules}

    def render_full(self, data, colone):
        """Create a table displaying modules in n columns."""
        if colone == 0:
            table = Table(box=box.SIMPLE_HEAD, show_header=True)
            table.add_column("Module", style="cyan bold", justify="right", overflow="fold")
            table.add_column("Size", style="white", overflow="fold")
            table.add_column("Used", style="white")
            table.add_column("By", style="white", overflow="fold")
            for module in data:
                if len(module) == 3:
                    table.add_row(module[0], module[1], module[2], "")
                else:
                    table.add_row(module[0], module[1], module[2], module[3])
            return table

        chunks = chunk_list(data, n_chunks=colone)
        table = Table(box=box.SIMPLE_HEAD, show_header=True)

        for i in range(colone):
            table.add_column("Module", style="cyan bold",
                             justify="right", overflow="fold")
            table.add_column("Size", style="white", overflow="fold")
            table.add_column("Used", style="white")
            table.add_column("By", style="white", overflow="fold")
            if i < colone - 1:
                table.add_column("", style="on blue")

        max_len = max(len(chunk) for chunk in chunks) if chunks else 0
        for row_idx in range(max_len):
            row_data = []
            for i, chunk in enumerate(chunks):
                if row_idx < len(chunk):
                    module = chunk[row_idx]
                    if len(module) == 3:
                        row_data.extend([module[0], module[1], module[2], ""])
                    else:
                        row_data.extend(
                            [module[0], module[1], module[2], module[3]])
                else:
                    row_data.extend(["", "", "", ""])
                if i < colone - 1:
                    row_data.append("")
            table.add_row(*row_data)

        return table
