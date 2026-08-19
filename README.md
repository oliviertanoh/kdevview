# kdevview

> A unified, readable view of the device state of a Linux system — character devices, kernel modules, buses (I2C/SPI/GPIO) and device classes, in one place.

`kdevview` gathers information that is normally scattered across `/proc/devices`,
`/sys/class/`, `lsmod`, `i2cdetect` and `dmesg`, and presents it as a clean,
colorized view in your terminal. It works on both x86 desktops and ARM embedded
boards (tested on Raspberry Pi CM4), adapting what it shows to the platform it
runs on.

## Why
Inspecting the device state of a Linux system usually means running several
different commands, each with its own format, and mentally cross-referencing
their output. `kdevview` does that cross-referencing for you: for example, it
maps each `/dev` node to the driver that handles it, and each I2C device to the
bus and driver it belongs to.

It is **read-only**: it never modifies any device or writes anywhere. It only
reads and displays.

## Features

- **Character & block devices** :  major/minor numbers and the driver behind each `/dev` node
- **Kernel modules** : loaded modules, size, usage count and dependencies
- **I2C bus** : buses and the devices detected on them, with their driver
- **SPI bus** : SPI devices and their driver
- **GPIO** : GPIO controllers and their line count
- **Device classes** : a map of `/sys/class/` (network, tty, iio, ...)
- **Recent kernel messages** : errors and warnings from the kernel ring buffer

## Modes

`kdevview` can be used three ways:

- **Snapshot (default)** : prints the current state once and exits.
- **Live (`--watch`)** : stays open and refreshes in place, like `htop`. Exit with `Ctrl+C`.
- **JSON (`--json`)** : a machine-readable snapshot, for scripting.

### Options

<!-- Keep this table in sync with the actual argparse definition. -->

| Option | Effect |
|--------|--------|
| *(none)* | Full snapshot, rich output |
| `--watch` | Live mode, refreshes in place |
| `--only <section>` | Restrict to one section: `chardev`, `modules`, `i2c`, `spi`, `gpio`, `classes`, `kmsg` |
| `--interval <N>` | Refresh interval in seconds for `--watch` |
| `--json` | Machine-readable snapshot (cannot be combined with `--watch`) |
| `--no-color` | Disable colors |
| `--version` | Print version |

In live mode, the global view shows a **summary** of each section (counts and
aggregate state); use `--only <section>` to watch one section in full detail.

## Platform support

`kdevview` detects whether it runs on a device-tree system (embedded ARM) or a
regular x86 machine, and adapts accordingly. Bus sections (I2C/SPI/GPIO) are most
relevant on embedded boards and are often empty on a desktop, that is expected.

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file for details.