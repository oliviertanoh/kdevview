import argparse

from collectors.chardev import CharacterDevice
from collectors.common.devices_type_dict import DEVICES, CURRENT_VERSION

from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich import box

console = Console()


def get_chardev_data() -> dict :
    chardev = CharacterDevice()
    return chardev.collect()

def chunk_list(items, n_chunks):
    """Découpe une liste en n_chunks tranches à peu près égales."""
    k, r = divmod(len(items), n_chunks)
    chunks = []
    start = 0
    for i in range(n_chunks):
        # les r premières tranches ont un élément de plus
        size = k + (1 if i < r else 0)
        chunks.append(items[start:start + size])
        start += size
    return chunks


def make_table(rows):
    """Construit une petite table Major/Name à partir d'une tranche."""
    table = Table(box=box.SIMPLE_HEAVY, show_lines=False, show_header=True)
    table.add_column(style="cyan bold", justify="right")
    table.add_column(style="white")
    for major, name in rows:
        table.add_row(major, name)
    return table


def display_in_columns(devices, n_columns=3):
    chunks = chunk_list(devices, n_columns)
    tables = [make_table(chunk) for chunk in chunks]
    console.print(Columns(tables))
    
    
def display_chardev_device () :
    device_data = get_chardev_data()
    for type, device in device_data.items() :
        console.print(f"[bold]{type}[/bold]")
        display_in_columns(device, n_columns=5)

def test(args) :
    print(args)



class KdevviewCommands:
    
    def __init__(self):
        
        parser = argparse.ArgumentParser(prog="kdevview")
        
        parser.add_argument("-o", "--only", choices= DEVICES,help="Display only one device")
        parser.add_argument("-i", "--interval", type=int, default= 2, help="Set refresh interval in seconds")
        parser.add_argument("--no-color",action="store_true" ,help="Desactivate color")
        parser.add_argument("-v", "--version",action="version" , version = CURRENT_VERSION,help="Show version")
        
        exclusive_group = parser.add_mutually_exclusive_group()
        exclusive_group.add_argument("-w", "--watch",action="store_true" ,help="Active live monitoring")
        exclusive_group.add_argument("-j", "--json",action="store_true" ,help="Display data in json")
        
        
        self.args = parser.parse_args()
        
    

    def run_command(self) :
        
        pass
    
    
    def get_command(self) :
        pass
    
        
        
test = KdevviewCommands()