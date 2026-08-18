from common.devices_type_dict import CHAR_DEVICE_TYPE
from common.utils import read_sysfs



class CharacterDevice :
    
    def __init__(self):
        pass
        
    
    def parse_device_line(self, line) -> list :
        parse_line = line.split(" ")
        parse_line = [el for el in parse_line if el != ""]
        return parse_line
    
    
    def get_device_type(self, line)-> tuple[bool, str | None] :
            data = self.parse_device_line(line) 
            if (len(data) > 1 ) :
                type_ = data[0] +" "+ data[1] 
                if type_ in CHAR_DEVICE_TYPE :
                    return True, type_
                    
            return False, None
        
    def get_device_major_name(self, device)-> tuple[str, str] | None  :
            line = self.parse_device_line(device) 
            if (len(line) > 1 ) :
                return (line[0], line[1])
            return None
            
            
    def collect(self) -> dict :
        
        character_devices = []
        block_devices = []
        
        is_device_char = False
        current_device_type = None
        device_content = read_sysfs("/proc/devices")
        
        for device in device_content :
            
            is_device_char, device_type = self.get_device_type(device)
            
            if is_device_char :
                current_device_type = device_type
                
            else : 
                
                if current_device_type == "Character devices:" :
                    result = self.get_device_major_name(device)
                    if result is not None:
                        character_devices.append(result)
                        
                if current_device_type == "Block devices:" :
                    result = self.get_device_major_name(device)
                    if result is not None:
                        block_devices.append(result)
                        
        return {"character_devices": character_devices, 
                "block_devices" : block_devices}
        
if __name__ == "__main__" :
    
    chardev = CharacterDevice()
    data = chardev.collect()
    print(data)        
        
