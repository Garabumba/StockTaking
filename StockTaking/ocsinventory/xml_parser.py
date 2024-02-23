from lxml import etree
import json

def get_computer_info(xml_str):
    root = etree.fromstring(xml_str)

    bios_element = root.find('.//BIOS')

    motherboard_vendor = bios_element.findtext('SMANUFACTURER')
    motherboard_model = bios_element.findtext('SMODEL')

    cpu_element = root.find('.//CPUS')

    cpu_vendor = cpu_element.findtext('MANUFACTURER')
    cpu_model = cpu_element.findtext('TYPE')
    cpu_frequency = cpu_element.findtext('SPEED')

    memories_elements = root.findall('.//MEMORIES')

    memories = []
    for memory_element in memories_elements:
        ram_slot = memory_element.findtext('NUMSLOTS')
        ram_type = memory_element.findtext('TYPE')
        ram_name = memory_element.findtext('CAPTION')
        ram_memory = memory_element.findtext('CAPACITY')
        ram_frequency = memory_element.findtext('SPEED')
        memories.append({'ram_slot': ram_slot, 'ram_type': ram_type, 'ram_name': ram_name, 'ram_memory': ram_memory, 'ram_frequency': ram_frequency})

    storages_elements = root.findall('.//STORAGES')
    storages = []
    for storage_element in storages_elements:
        storage_name = storage_element.findtext('NAME')
        storage_disksize = storage_element.findtext('DISKSIZE')
        storage_serialnumber = storage_element.findtext('SERIALNUMBER')
        storages.append({'storage_name': storage_name, 'storage_disksize': storage_disksize, 'storage_serialnumber': storage_serialnumber})

    drives_elements = root.findall('.//DRIVES')
    drives = []
    for drive_element in drives_elements:
        drive_name = drive_element.findtext('LETTER')
        drive_total_memory = drive_element.findtext('TOTAL')
        drive_free_memory = drive_element.findtext('FREE')
        drives.append({'drive_name': drive_name, 'drive_total_memory': drive_total_memory, 'drive_free_memory': drive_free_memory})

    videocards_elements = root.findall('.//VIDEOS')
    videocards = []
    for videocard_element in videocards_elements:
        videocard_name = videocard_element.findtext('NAME')
        videocard_memory = videocard_element.findtext('MEMORY')
        videocard_resolution = videocard_element.findtext('RESOLUTION')
        videocards.append({'videocard_name': videocard_name, 'videocard_memory': videocard_memory, 'videocard_resolution': videocard_resolution})

    monitors_elements = root.findall('.//MONITORS')
    monitors = []
    for monitor_element in monitors_elements:
        monitor_vendor = monitor_element.findtext('MANUFACTURER')
        monitor_model = monitor_element.findtext('CAPTION')
        monitor_serialnumber = monitor_element.findtext('SERIAL')
        monitors.append({'monitor_vendor': monitor_vendor, 'monitor_model': monitor_model, 'monitor_serialnumber': monitor_serialnumber, 'monitor_name': f'{monitor_vendor} {monitor_model}'})

    os_name_element = root.find('.//HARDWARE')
    os_name = os_name_element.findtext('OSNAME')
    ip_addr = os_name_element.findtext('IPADDR')
    windows_key = os_name_element.findtext('WINPRODKEY')
    win_arch = os_name_element.findtext('ARCH')
    total_ram_memory = os_name_element.findtext('MEMORY')
    inventory_number = os_name_element.findtext('NAME')
    computer_name = os_name_element.findtext('NAME')

    inventory_info = root.find('.//ACCOUNTINFO')
    if inventory_info is not None:
        inventory_number = inventory_info.findtext('KEYVALUE')

    # Заменяем значения None на null
    computer_info = {
        'motherboard': {'vendor': motherboard_vendor, 'model': motherboard_model, 'name': f'{motherboard_vendor} {motherboard_model}'},
        'cpu': {'vendor': cpu_vendor, 'model': cpu_model, 'frequency': cpu_frequency, 'name': f'{cpu_vendor} {cpu_model}'},
        'memories': memories,
        'storages': storages,
        'drives': drives,
        'videocards': videocards,
        'monitors': monitors,
        'os': {'os_name': os_name, 'ip': ip_addr, 'winkey': windows_key, 'win_arch': win_arch, 'inventory_number': inventory_number, 'computer_name': computer_name, 'total_ram_memory' : total_ram_memory}
    }

    # Преобразуем в JSON
    json_data = json.dumps(computer_info, indent=4)
    
    return json_data


# def get_computer_info(xml_str):
#     root = etree.fromstring(xml_str)

#     bios_element = root.find('.//BIOS')

#     motherboard_vendor = bios_element.findtext('SMANUFACTURER')
#     motherboard_model = bios_element.findtext('SMODEL')

#     cpu_element = root.find('.//CPUS')

#     cpu_vendor = cpu_element.findtext('MANUFACTURER')
#     cpu_model = cpu_element.findtext('TYPE')
#     cpu_frequency = cpu_element.findtext('SPEED')

#     memories_elements = root.findall('.//MEMORIES')

#     memories = []
#     for memory_element in memories_elements:
#         #if memory_element.findtext('TYPE').upper() != 'EMPTY SLOT':
#         ram_slot = memory_element.findtext('NUMSLOTS')
#         ram_type = memory_element.findtext('TYPE')
#         ram_name = memory_element.findtext('CAPTION')
#         ram_amount = memory_element.findtext('CAPACITY')
#         #memories.append({'ram_slot': })
#         memories.append({'ram_slot': ram_slot, 'ram_type': ram_type, 'ram_name': ram_name, 'ram_amount': ram_amount})

#     storages_elements = root.findall('.//STORAGES')
#     storages = []
#     for storage_element in storages_elements:
#         storage_name = storage_element.findtext('NAME') #мб отсюда модель тянуть
#         storage_disksize = storage_element.findtext('DISKSIZE')
#         storage_serialnumber = storage_element.findtext('SERIALNUMBER')
#         storages.append({'storage_name': storage_name, 'storage_disksize': storage_disksize, 'storage_serialnumber': storage_serialnumber})

#     drives_elements = root.findall('.//DRIVES')
#     drives = []
#     for drive_element in drives_elements:
#         drive_name = drive_element.findtext('LETTER')
#         drive_total_memory = drive_element.findtext('TOTAL')
#         drive_free_memory = drive_element.findtext('FREE')
#         drives.append({'drive_name': drive_name, 'drive_total_memory': drive_total_memory, 'drive_free_memory': drive_free_memory})

#     videocards_elements = root.findall('.//VIDEOS')
#     videocards = []
#     for videocard_element in videocards_elements:
#         videocard_name = videocard_element.findtext('NAME')
#         videocard_memory = videocard_element.findtext('MEMORY')
#         videocard_resolution = videocard_element.findtext('RESOLUTION')
#         videocards.append({'videocard_name': videocard_name, 'videocard_memory': videocard_memory, 'videocard_resolution': videocard_resolution})

#     monitors_elements = root.findall('.//MONITORS')
#     monitors = []
#     for monitor_element in monitors_elements:
#         monitor_vendor = monitor_element.findtext('MANUFACTURER')
#         monitor_model = monitor_element.findtext('CAPTION')
#         monitor_serialnumber = monitor_element.findtext('SERIAL')
#         monitors.append({'monitor_vendor': monitor_vendor, 'monitor_model': monitor_model, 'monitor_serialnumber': monitor_serialnumber, 'monitor_name': f'{monitor_vendor} {monitor_model}'})

#     os_name_element = root.find('.//HARDWARE')
#     os_name = os_name_element.findtext('OSNAME')
#     ip_addr = os_name_element.findtext('IPADDR')
#     windows_key = os_name_element.findtext('WINPRODKEY')
#     win_arch = os_name_element.findtext('ARCH')
#     inventory_number = os_name_element.findtext('NAME')
#     computer_name = os_name_element.findtext('NAME')

#     inventory_info = root.find('.//ACCOUNTINFO')
#     if inventory_info is not None:
#         inventory_number = inventory_info.findtext('KEYVALUE')

#     # Выводим результаты
#     #print("SMANUFACTURER:", motherboard_vendor)
#     #print("SMODEL:", motherboard_model)

#     return {'motherboard': {'vendor': motherboard_vendor, 'model': motherboard_model, 'name': f'{motherboard_vendor} {motherboard_model}'}, 'cpu': {'vendor': cpu_vendor, 'model': cpu_model, 'frequency': cpu_frequency, 'name': f'{cpu_vendor} {cpu_model}'}, 'memories': [{'ram_slot': ram['ram_slot'], 'ram_type': ram['ram_type'], 'ram_name': ram['ram_name'], 'ram_amount': ram['ram_amount']} for ram in memories], 'storages': [{'storage_name': storage['storage_name'], 'storage_diskzie': storage['storage_disksize'], 'storage_serialnumber': storage['storage_serialnumber']} for storage in storages], 'drives': [{'drive_name': drive['drive_name'], 'drive_total_memory': drive['drive_total_memory'], 'drive_free_memory': drive['drive_free_memory']} for drive in drives], 'videocards': [{'videocard_name': videocard['videocard_name'], 'videocard_memory': videocard['videocard_memory'], 'videocard_resolution': videocard['videocard_resolution']} for videocard in videocards], 'monitors': [{'monitor_vendor': monitor['monitor_vendor'], 'monitor_model': monitor['monitor_model'], 'monitor_serialnumber': monitor['monitor_serialnumber'], 'monitor_name': monitor['monitor_name']} for monitor in monitors], 'os': {'os_name': os_name, 'ip': ip_addr, 'winkey': windows_key, 'win_arch': win_arch, 'inventory_number': inventory_number, 'computer_name': computer_name}}