import os

if __name__ == "__main__" :

    # Data struct
    
    list_major = []

    data_struc_ch_devices = {
        "major" : None,
        "devices_name" : None,
    }


    list_minor = []

    # Get major devices
    with open("/proc/devices","r") as files :
        content = files.readlines()
        for major in content :
            if major != "Character devices:\n" and major != "Blocks devices:\n" :
                data = major.split(" ")
                data = [el for el in data if el!=""]
                if len(data) > 1  : 
                    data_struc_ch_devices["major"] = data[0]
                    data_struc_ch_devices["devices_name"] = data [1]
                    list_major.append(data_struc_ch_devices.copy())