import logging
from pathlib import Path



def read_sysfs (filename: str) -> list[str] :
    
    """
        Open files proprely with error handling
    """
    try : 
        with open(filename, "r") as files :
            content = files.readlines()
            content = [line.rstrip() for line in content]
            return content  
    except OSError as err :
        logging.warning("could not read %s: %s", filename, err)
        return []
    
    
          