import logging
from pathlib import Path


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


def read_sysfs(filename: str) -> list[str]:
    """
        Open files proprely with error handling
    """
    try:
        with open(filename, "r") as files:
            content = files.readlines()
            content = [line.rstrip() for line in content]
            return content
    except OSError as err:
        # logging.warning("could not read %s: %s", filename, err)
        return ['']
