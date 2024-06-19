from lxml import etree
import json
import enum
import logging
import traceback
from pygelf import GelfTcpHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(GelfTcpHandler(host='127.0.0.1', port=12201, include_extra_fields=True))

class Mode(enum.Enum):
    ROOT_ELEMENT = 1
    ONE_ELEMENT = 2
    LIST_OF_ELEMENTS = 3

async def __find_elements(element, root, mode, return_value=None):
    try:
        if mode == Mode.ROOT_ELEMENT:
            return root.find(element)
        elif mode == Mode.ONE_ELEMENT:
            return root.findtext(element)
        elif mode == Mode.LIST_OF_ELEMENTS:
            return root.findall(element)
    except:
        logger.warning(f'Не нашли "{element}"')
        return return_value

async def __search_new_ram_information(root, serial_number):
    try:
        new_rams = await __find_elements('.//NEW_MEMORIES', root, Mode.LIST_OF_ELEMENTS)
        
        for new_ram in new_rams:
            if await __find_elements('SERIALNUMBER', new_ram, Mode.ONE_ELEMENT) == serial_number:
                new_type_v1 = await __find_elements('TYPE_V1', new_ram, Mode.ONE_ELEMENT, 'UNKNOWN')
                new_type_v2 = await __find_elements('TYPE_V2', new_ram, Mode.ONE_ELEMENT, 'UNKNOWN')
                new_vendor = await __find_elements('MANUFACTURER', new_ram, Mode.ONE_ELEMENT)

                if new_type_v1.upper() != 'UNKNOWN':
                    return new_type_v1, new_vendor
                else:
                    return new_type_v2, new_vendor

        return 'UNKNOWN RAM TYPE', 'UNKNOWN RAM VENDOR'
    except:
        return 'UNKNOWN RAM TYPE', 'UNKNOWN RAM VENDOR'
    
async def __search_new_monitor_information(root, serial_number):
    try:
        new_monitors = await __find_elements('.//NEW_MONITORS', root, Mode.LIST_OF_ELEMENTS)
        
        for new_monitor in new_monitors:
            if await __find_elements('SERIALNUMBER', new_monitor, Mode.ONE_ELEMENT) == serial_number:
                new_resolution = await __find_elements('RESOLUTION', new_monitor, Mode.ONE_ELEMENT)
                return new_resolution
            
        return 'UNKNOWN MONITOR RESOLUTION'
    except:
        return 'UNKNOWN MONITOR RESOLUTION'
    
async def __search_storage_type(root, serial_number):
    try:
        new_storages = await __find_elements('.//NEW_STORAGES', root, Mode.LIST_OF_ELEMENTS)
        
        for new_storage in new_storages:
            if await __find_elements('SERIALNUMBER', new_storage, Mode.ONE_ELEMENT) == serial_number:
                storage_type = await __find_elements('MEDIA_TYPE', new_storage, Mode.ONE_ELEMENT)

                return storage_type
            
        return 'UNKNOWN STORAGE TYPE'
    except:
        return 'UNKNOWN STORAGE TYPE'

async def get_computer_info(xml_str):
    root = etree.fromstring(xml_str)

    errors_text = ''

    os_name_element = await __find_elements('.//HARDWARE', root, Mode.ROOT_ELEMENT)
    if os_name_element:
        os_name = await __find_elements('OSNAME', os_name_element, Mode.ONE_ELEMENT, 'UNKNONWN OS NAME')
        ip_addr = await __find_elements('IPADDR', os_name_element, Mode.ONE_ELEMENT, 'UNKNONWN IP ADDRESS')
        windows_key = await __find_elements('WINPRODKEY', os_name_element, Mode.ONE_ELEMENT, 'UNKNONWN LICENSE KEY')
        win_arch = await __find_elements('ARCH', os_name_element, Mode.ONE_ELEMENT, 'UNKNONWN ARCHNITECTURE')
        total_ram_memory = await __find_elements('MEMORY', os_name_element, Mode.ONE_ELEMENT, 0)
        computer_name = await __find_elements('NAME', os_name_element, Mode.ONE_ELEMENT, 'UNKNONWN COMPUTER NAME')
        os_version = await __find_elements('OSVERSION', os_name_element, Mode.ONE_ELEMENT, 'UNKNONWN OS VERSION')
    else:
        os_name = 'UNKNONWN OS NAME'
        ip_addr = 'UNKNONWN IP ADDRESS'
        windows_key = 'UNKNONWN LICENSE KEY'
        win_arch = 'UNKNONWN ARCHNITECTURE'
        total_ram_memory = 0
        computer_name = 'UNKNONWN COMPUTER NAME'
        os_version = 'UNKNONWN OS VERSION'

    bios_element = await __find_elements('.//BIOS', root, Mode.ROOT_ELEMENT)
    if bios_element:
        motherboard_vendor = await __find_elements('SMANUFACTURER', bios_element, Mode.ONE_ELEMENT, 'UNKNOWN MOTHERBOARD VENDOR')
        motherboard_model = await __find_elements('SMODEL', bios_element, Mode.ONE_ELEMENT, 'UNKNOWN MOTHERBOARD MODEL')
    else:
        motherboard_vendor = 'UNKNOWN MOTHERBOARD VENDOR'
        motherboard_model = 'UNKNOWN MOTHERBOARD MODEL'

    cpu_element = await __find_elements('.//CPUS', root, Mode.ROOT_ELEMENT)
    if cpu_element:
        cpu_vendor = await __find_elements('MANUFACTURER', cpu_element, Mode.ONE_ELEMENT, 'UNKNOWN CPU VENDOR')
        cpu_model = await __find_elements('TYPE', cpu_element, Mode.ONE_ELEMENT, 'UNKNOWN CPU MODEL')
        cpu_frequency = await __find_elements('SPEED', cpu_element, Mode.ONE_ELEMENT, 0)
        cpu_cores = await __find_elements('CORES', cpu_element, Mode.ONE_ELEMENT, 0)
        cpu_threads = await __find_elements('LOGICAL_CPUS', cpu_element, Mode.ONE_ELEMENT, 0)
    else:
        cpu_vendor = 'UNKNOWN CPU VENDOR'
        cpu_model = 'UNKNOWN CPU MODEL'
        cpu_frequency = 0
        cpu_cores = 0
        cpu_threads = 0

    memories_elements = await __find_elements('.//MEMORIES', root, Mode.LIST_OF_ELEMENTS)
    software_elements = await __find_elements('.//SOFTWARES', root, Mode.LIST_OF_ELEMENTS)
    drive_elements = await __find_elements('.//DRIVES', root, Mode.LIST_OF_ELEMENTS)

    slot_num = 1
    memories = []
    if memories_elements:
        for memory_element in memories_elements:
            if await __find_elements('TYPE', memory_element, Mode.ONE_ELEMENT) and await __find_elements('TYPE', memory_element, Mode.ONE_ELEMENT) != 'Empty slot':
                ram_serial = await __find_elements('SERIALNUMBER', memory_element, Mode.ONE_ELEMENT, 'UNKNOWN RAM SERIAL')
                _, ram_vendor = await __search_new_ram_information(root, ram_serial)
                ram_slot = await __find_elements('NUMSLOTS', memory_element, Mode.ONE_ELEMENT, slot_num)
                ram_type = await __find_elements('TYPE', memory_element, Mode.ONE_ELEMENT)
                if ram_type.upper() == 'UNKNOWN':
                    ram_type, ram_vendor = await __search_new_ram_information(root, ram_serial)
                ram_name = await __find_elements('CAPTION', memory_element, Mode.ONE_ELEMENT, 'UNKNOWN RAM NAME')
                ram_memory = await __find_elements('CAPACITY', memory_element, Mode.ONE_ELEMENT, 0)
                ram_frequency = await __find_elements('SPEED', memory_element, Mode.ONE_ELEMENT, 0)
                memories.append({
                    'ram_slot': ram_slot, 
                    'ram_type': ram_type, 
                    'ram_name': ram_name, 
                    'ram_memory': ram_memory, 
                    'ram_frequency': ram_frequency, 
                    'ram_model': 'UNKNOWN RAM MODEL', 
                    'ram_vendor': ram_vendor
                    })
                slot_num += 1                

    softwares = []
    if software_elements:
        for software_element in software_elements:
            software_publisher = await __find_elements('PUBLISHER', software_element, Mode.ONE_ELEMENT, 'UNKNOWN SOFTWARE VENDOR')
            software_name = await __find_elements('NAME', software_element, Mode.ONE_ELEMENT, 'UNKNOWN SOFTWARE NAME')
            software_version = await __find_elements('VERSION', software_element, Mode.ONE_ELEMENT, 'UNKNOWN SOFTWARE VERSION')
            software_install_date = await __find_elements('INSTALLDATE', software_element, Mode.ONE_ELEMENT, '0000//0/0/00')
            software_folder = await __find_elements('FOLDER', software_element, Mode.ONE_ELEMENT, 'UNKNOWN SOFTWARE FOLDER')
            if software_install_date == '0000//0/0/00':
                software_install_date = None
            if software_install_date:
                software_install_date = software_install_date.replace('/', '-')
            softwares.append({
                'software_publisher': software_publisher, 
                'software_name': software_name, 
                'software_version': software_version, 
                'software_install_date': software_install_date, 
                'software_folder': software_folder
                })

    storages_elements = await __find_elements('.//STORAGES', root, Mode.LIST_OF_ELEMENTS)
    storages = []
    if storages_elements:
        for storage_element in storages_elements:
            storage_name = await __find_elements('NAME', storage_element, Mode.ONE_ELEMENT, 'UNKNOWN STORAGE NAME')
            storage_disksize = await __find_elements('DISKSIZE', storage_element, Mode.ONE_ELEMENT, 0)
            storage_serialnumber = await __find_elements('SERIALNUMBER', storage_element, Mode.ONE_ELEMENT, 'UNKNOWN STORAGE SERIAL')
            storage_type = await __search_storage_type(root, storage_serialnumber)
            storages.append({
                'storage_name': storage_name, 
                'storage_disksize': storage_disksize, 
                'storage_serialnumber': storage_serialnumber,
                'storage_type': storage_type
                })

    drives_elements = await __find_elements('.//DRIVES', root, Mode.LIST_OF_ELEMENTS)
    drives = []
    if drive_elements:
        for drive_element in drives_elements:
            drive_letter = await __find_elements('LETTER', drive_element, Mode.ONE_ELEMENT, 'UNKNOWN DRIVE LETTER')
            drive_total_memory = await __find_elements('TOTAL', drive_element, Mode.ONE_ELEMENT, 0)
            drive_free_memory = await __find_elements('FREE', drive_element, Mode.ONE_ELEMENT, 0)
            drives.append({
                'drive_letter': drive_letter, 
                'drive_total_memory': drive_total_memory, 
                'drive_free_memory': drive_free_memory
                })

    videocards_elements = await __find_elements('.//VIDEOS', root, Mode.LIST_OF_ELEMENTS)
    videocards = []
    if videocards_elements:
        if len(videocards_elements) > 0:
            for videocard_element in videocards_elements:
                videocard_name = await __find_elements('NAME', videocard_element, Mode.ONE_ELEMENT, 'UNKNNOWN VIDEOCARD NAME')
                videocard_memory = await __find_elements('MEMORY', videocard_element, Mode.ONE_ELEMENT, 0)
                videocard_resolution = await __find_elements('RESOLUTION', videocard_element, Mode.ONE_ELEMENT)
                
                videocards.append({
                    'videocard_name': videocard_name, 
                    'videocard_memory': videocard_memory, 
                    'videocard_resolution': videocard_resolution
                    })

    monitors_elements = await __find_elements('.//MONITORS', root, Mode.LIST_OF_ELEMENTS)
    monitors = []
    if monitors_elements:
        for monitor_element in monitors_elements:
            monitor_vendor = await __find_elements('MANUFACTURER', monitor_element, Mode.ONE_ELEMENT, 'UNKNOWN MONITOR VENDOR')
            monitor_model = await __find_elements('CAPTION', monitor_element, Mode.ONE_ELEMENT, 'UNKNOWN MONITOR MODEL')
            monitor_serialnumber = await __find_elements('SERIAL', monitor_element, Mode.ONE_ELEMENT, 'UNKNOWN MONITOR SERIALNUMBER')
            monitor_resolution = await __search_new_monitor_information(root, monitor_serialnumber)
            monitors.append({
                'monitor_vendor': monitor_vendor, 
                'monitor_model': monitor_model, 
                'monitor_serialnumber': monitor_serialnumber, 
                'monitor_name': f'{monitor_vendor} {monitor_model}',
                'monitor_resolution': monitor_resolution
                })

    inventory_number = 'UNKNOWN INVENTORY NUMBER'
    inventory_info = await __find_elements('.//ACCOUNTINFO', root, Mode.ROOT_ELEMENT)
    if inventory_info:
        inventory_number = await __find_elements('KEYVALUE', inventory_info, Mode.ONE_ELEMENT, 'UNKNOWN INVENTORY NUMBER')

    computer_info = {
        'motherboard': {
            'vendor': motherboard_vendor, 
            'model': motherboard_model, 
            'name': f'{motherboard_vendor} {motherboard_model}'
            },
        'cpu': {
            'vendor': cpu_vendor, 
            'model': cpu_model, 
            'frequency': cpu_frequency, 
            'name': f'{cpu_vendor} {cpu_model}', 
            'cores': cpu_cores, 
            'threads': cpu_threads
            },
        'memories': memories,
        'storages': storages,
        'drives': drives,
        'videocards': videocards,
        'monitors': monitors,
        'os': {
            'os_name': os_name, 
            'os_version': os_version, 
            'ip': ip_addr, 
            'winkey': windows_key, 
            'win_arch': win_arch, 
            'inventory_number': computer_name if inventory_number == 'UNKNOWN INVENTORY NUMBER' else inventory_number, 
            'computer_name': computer_name, 
            'total_ram_memory' : total_ram_memory
            },
        'softwares': softwares
    }

    json_data = json.dumps(computer_info, indent=4)
    
    return json_data
