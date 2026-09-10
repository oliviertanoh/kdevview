CURRENT_VERSION = "kdevview 0.1.0"

CHAR_DEVICE_TYPE = ["Character devices:", "Block devices:"]

DEVICES = ["chardev", "modules", "i2c", "usb"]

DEVICES_DICT_MATCH = {"chardev": "CHARACTER DEVICES",
                      "blockdev": "BLOCK DEVICES",
                      "modules": "MODULES",
                      "i2c": "I2C DEVICES",
                      "usb": "USB DEVICES"}

sys_paths = {
    "usb": "/sys/bus/usb/devices/",
    "i2c": "/sys/bus/i2c/devices/",
    "modules": "/proc/modules",
    "chardev": "/proc/devices",
}

ARCHITECETURE = {
    "x86_64": sys_paths,
    "x86_32": sys_paths,
}
