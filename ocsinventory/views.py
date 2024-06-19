from pygelf import GelfTcpHandler
import logging
import traceback
import zlib
import re
import helper
import asyncio
import json
from asgiref.sync import sync_to_async
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from lxml import etree
from lxml.etree import XMLSyntaxError
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification
from . import xml_parser
import math
from home.models import OS, RAM, CPUHistory, Computer, MonitorHistory, MotherboardHistory, OS_Computer, OSVersion, RAMHistory, RAMModel, RAMType, Resolution, ResolutionFormat, SoftwareType, StorageHistory, Drive, Monitor, MonitorModel, MotherboardModel, Motherboard, CPUModel, CPU, Software, Software_Computer, Storage, StorageModel, StorageType, TechniqueStatus, TechniqueType, Vendor, VendorType, Videocard, VideocardHistory, VideocardModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(GelfTcpHandler(host='127.0.0.1', port=12201, include_extra_fields=True))

class MyTimeoutError(Exception):
    pass

async def generate_prolog():
    content = """<?xml version='1.0' encoding='UTF-8'?>
<REPLY>
  <OPTION>
    <NAME>DOWNLOAD</NAME>
    <PARAM CYCLE_LATENCY="60" PERIOD_LENGTH="10" ON="0" TYPE="CONF" FRAG_LATENCY="10" PERIOD_LATENCY="1" TIMEOUT="30" EXECUTION_TIMEOUT="120" />
  </OPTION>
  <RESPONSE>SEND</RESPONSE>
  <INVENTORY_ON_STARTUP>1</INVENTORY_ON_STARTUP>
  <PROLOG_FREQ>1</PROLOG_FREQ>
</REPLY>
"""
    chunk = zlib.compress(content.encode())
    return chunk

async def not_change_data():
    content = """<?xml version='1.0' encoding='UTF-8'?>
<REPLY>
  <RESPONSE>NO_ACCOUNT_UPDATE</RESPONSE>
</REPLY>
"""
    chunk = zlib.compress(content.encode())
    return chunk

async def timeout_func(func, args=None, kwargs=None, timeout=30):
    """
    Asynchronous version of the timeout function.
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    try:
        return await asyncio.wait_for(func(*args, **kwargs), timeout)
    except asyncio.TimeoutError:
        raise MyTimeoutError(f"{func.__name__} timeout (taking more than {timeout} sec)")

@csrf_exempt
@never_cache
@require_http_methods(['POST'])
async def ocsinventory(request):
    log = logging.getLogger('comp')

    async def _get_body():
        return request.body

    try:
        content = await timeout_func(_get_body, timeout=0.5)
    except Exception as ex:
        content = await generate_prolog()
        response = HttpResponse(content)
        response['Content-Length'] = len(content)
        response['Content-Type'] = 'application/x-compressed'
        log.error(ex)
        return response

    if content:
        try:
            zobj = zlib.decompressobj()
            raw_xml_str = zobj.decompress(content)
            raw_xml_str = raw_xml_str.decode('utf-8')
        except zlib.error:
            response = HttpResponse('Error decompressing data.')
            return response

        try:
            raw_xml_str = raw_xml_str.encode('utf-8')
            root_xml = etree.fromstring(raw_xml_str)
        except XMLSyntaxError:
            log.error(f'Error parsing XML. Data=\n{raw_xml_str}')
            response = HttpResponse('Error parsing XML.')
            return response

        query_type = root_xml.findtext('QUERY', default='')

        if query_type == 'PROLOG':
            content = await generate_prolog()
            response = HttpResponse(content)
            response['Content-Length'] = len(content)
            response['Content-Type'] = 'application/x-compressed'
            return response

        if query_type == 'INVENTORY':
            computer_info = json.loads(await xml_parser.get_computer_info(raw_xml_str))
            
            log.info(f'{str(await xml_parser.get_computer_info(raw_xml_str))}')
            
            with open(r"D:\\otus3.txt", "w") as file:
                file.write(f'{str(await xml_parser.get_computer_info(raw_xml_str))}')
            with open(r"D:\\otus.txt", "w") as file:
                file.write(f'{str(raw_xml_str)}')
            
            try:
                total_info = '----------КОМПЬЮТЕР----------\n'
                total_errors = ''

                try:
                    computer, info, is_new_computer = await search_create_computer(computer_info)
                    total_info += info
                except:
                    computer = None
                    is_new_computer = True
                    logger.error(f'Ошибка поиска/добавления компьютера\n{traceback.format_exc()}')
                
                total_info += '----------ОС----------\n'

                try:
                    os, info = await search_create_os(computer_info, computer)
                    total_info += info
                except:
                    logger.error(f'Ошибка поиска/добавления ОС\n{traceback.format_exc()}')

                total_info += '----------МАТ. ПЛАТА----------\n'

                try:
                    motherboard, info = await search_create_motherboard(computer_info, computer, is_new_computer)
                    total_info += info
                except:
                    logger.error(f'Ошибка поиска/добавления материнской платы\n{traceback.format_exc()}')
                
                total_info += '----------ПРОЦЕССОР----------\n'

                try:
                    cpu, info = await search_create_cpu(computer_info, computer, is_new_computer)
                    total_info += info
                except:
                    logger.error(f'Ошибка поиска/добавления материнской платы\n{traceback.format_exc()}')

                total_info += '----------НАКОПИТЕЛИ----------\n'

                try:
                    storages, info = await search_create_storage(computer_info, computer, is_new_computer)
                    total_info += info
                except:
                    logger.error(f'Ошибка поиска/добавления накопителей памяти\n{traceback.format_exc()}')
                
                total_info += '----------ВИДЕОКАРТЫ----------\n'

                try:              
                    videocards, info = await search_create_videocard(computer_info, computer, is_new_computer)
                    total_info += info
                except:
                    logger.error(f'Ошибка поиска/добавления видеокарт\n{traceback.format_exc()}')

                total_info += '----------ОПЕРАТИВНАЯ ПАМЯТЬ----------\n'

                try:              
                    rams, info = await search_create_ram(computer_info, computer, is_new_computer)
                    total_info += info
                except:
                    logger.error(f'Ошибка поиска/добавления видеокарт\n{traceback.format_exc()}')

                total_info += '----------МОНИТОРЫ----------\n'

                try: 
                    monitors, info = await search_create_monitor(computer_info, computer, is_new_computer)
                except:
                    logger.error(f'Ошибка поиска/добавления мониторов\n{traceback.format_exc()}')
                

                total_info += '----------ПО----------\n'

                try: 
                    softwares, info, errors = await search_create_software(computer_info, computer)
                except:
                    logger.error(f'Ошибка поиска/добавления программного обеспечения\n{traceback.format_exc()}')

                try:
                    drives, info, errors = await search_create_drive(computer_info, computer)
                except:
                    logger.error(f'Ошибка поиска/добавления разделов памяти\n{traceback.format_exc()}')

                logger.info(total_info)

            except Exception as err:
                logger.info(err)
                logger.error(err)
                logger.error(traceback.format_exc())

            content = await not_change_data()
            response = HttpResponse(content)
            response['Content-Length'] = len(content)
            response['Content-Type'] = 'application/x-compressed'
            return response
        
        content = await generate_prolog()
        response = HttpResponse(content)
        response['Content-Length'] = len(content)
        response['Content-Type'] = 'application/x-compressed'
        return response
    else:
        content = await generate_prolog()
        response = HttpResponse(content)
        response['Content-Length'] = len(content)
        response['Content-Type'] = 'application/x-compressed'
        return response

async def search_create_computer(computer_info):
    info = ''
    is_new_computer = False

    computer_name = computer_info['os']['computer_name']
    computer_ip = computer_info['os']['ip']
    computer_arch = computer_info['os']['win_arch']
    computer_inventory_number = computer_info['os']['inventory_number']
    
    try:
        computer = await Computer.objects.aget(inventory_number=computer_inventory_number)
        info += f'Нашли компьютер "{computer_inventory_number}"\n'
        try:
            computer, update_info = await sync_to_async(helper.update_computer)(computer, computer_name, computer_ip, computer_arch)
            info += update_info
        except:
            logger.error(f'Ошибка обновления компьютера\n{traceback.format_exc()}')
    except ObjectDoesNotExist:
        computer = await Computer.objects.acreate(inventory_number=computer_inventory_number, ip=computer_ip, name=computer_name, arch=computer_arch, technique_type_id=TechniqueType.Type.COMPUTER, status_id=TechniqueStatus.Status.OK)
        info += f'Создали компьютер "{computer_inventory_number}"'
        is_new_computer = True
    except:
        logger.error(f'Ошибка получения компьютера\n{traceback.format_exc()}')

    return computer, info, is_new_computer

async def search_create_motherboard(computer_info, computer, is_new_computer):
    info = ''
    motherboard = None

    motherboard_vendor_name = computer_info['motherboard']['vendor']
    motherboard_model_name = computer_info['motherboard']['model']
    motherboard_name = computer_info['motherboard']['name']
    
    try:
        motherboard_vendor, vendor_info = await __search_add_vendor(motherboard_vendor_name, VendorType.Type.MOTHERBOARD)
        info += vendor_info
    except ObjectDoesNotExist:
        info += f'Не нашли производителя материнской платы: "{motherboard_vendor_name}"'
        return None, info
        
    motherboard_model, motherboard_model_created = await MotherboardModel.objects.aget_or_create(name=motherboard_model_name, vendor=motherboard_vendor)
    if motherboard_model_created:
        info += f'Создали модель материнской платы: "{motherboard_model_name}"\n'
    else:
        info += f'Нашли модель материнской платы: "{motherboard_model_name}"\n'

    if is_new_computer:
        try:
            motherboard, motherboard_info = await __get_unused_motherboard_or_create_new(motherboard_name, motherboard_model, computer)
            info += motherboard_info
        except:
            logger.error(f'Ошибка привязки/создания материнской платы\n{traceback.format_exc()}')
    else:
        old_motherboard = await computer.motherboard_set.afirst()

        try:
            motherboard = await Motherboard.objects.aget(name=motherboard_name, model=motherboard_model, computer=computer)
            info += f'Нашли материнскую плату: "{motherboard_name}"\n'
        except ObjectDoesNotExist:
            try:
                motherboard, motherboard_info = await __get_unused_motherboard_or_create_new(motherboard_name, motherboard_model, computer)
                info += motherboard_info
            except:
                logger.error(f'Ошибка привязки/создания материнской платы\n{traceback.format_exc()}')
        except:
            logger.error(f'Ошибка получения материнской платы\n{traceback.format_exc()}')
        
        if old_motherboard:
            if old_motherboard != motherboard:
                try:
                    update_info = await sync_to_async(helper.update_motherboard)(computer, old_motherboard, motherboard)
                    info += update_info
                except:
                    logger.error(f'Ошибка замены материнской платы\n{traceback.format_exc()}')

    return motherboard, info

async def search_create_cpu(computer_info, computer, is_new_computer):
    info = ''

    cpu_vendor_name = computer_info['cpu']['vendor']
    cpu_model_name = computer_info['cpu']['model']
    cpu_name = computer_info['cpu']['name']
    cpu_frequency = float(computer_info['cpu']['frequency'])
    cpu_cores = int(computer_info['cpu']['cores'])
    cpu_threads = int(computer_info['cpu']['threads'])

    try:
        cpu_vendor, vendor_info = await __search_add_vendor(cpu_vendor_name, VendorType.Type.CPU)
        info += vendor_info
    except ObjectDoesNotExist:
        info += f'Не нашли производителя процессора: "{cpu_vendor_name}"'
        return None, info

    cpu_model, cpu_model_created = await CPUModel.objects.aget_or_create(name=cpu_model_name, cores=cpu_cores, threads=cpu_threads, vendor=cpu_vendor)
    if cpu_model_created:
        info += f'Создали модель процессора: "{cpu_model_name}"\n'
    else:
        info += f'Нашли модель процессора: "{cpu_model_name}"\n'

    if is_new_computer:
        try:
            cpu, cpu_info = await __get_unused_cpu_or_create_new(cpu_name, cpu_model, cpu_frequency, computer)
            info += cpu_info
        except:
            logger.error(f'Ошибка привязки/создания материнской платы\n{traceback.format_exc()}')
    else:
        old_cpu = await computer.cpu_set.afirst()

        try:
            cpu = await CPU.objects.aget(name=cpu_name, model=cpu_model, computer=computer)
            info += f'Нашли процессор: "{cpu_name}"\n'
            if cpu.is_updating and cpu.frequency != cpu_frequency:
                info += f'Обновляем частоту процессора ({cpu.frequency} -> {cpu_frequency})'
                cpu.frequency = cpu_frequency
                await cpu.asave()
        except ObjectDoesNotExist:
            try:
                cpu, cpu_info = await __get_unused_cpu_or_create_new(cpu_name, cpu_model, cpu_frequency, computer)
                info += cpu_info
            except:
                logger.error(f'Ошибка привязки/создания процессора\n{traceback.format_exc()}')
        except:
            logger.error(f'Ошибка получения процессора\n{traceback.format_exc()}')
                    
        if old_cpu:
            if old_cpu != cpu:
                try:
                    update_info = await sync_to_async(helper.update_cpu)(computer, old_cpu, cpu)
                    info += update_info
                except:
                    logger.error(f'Ошибка замены процессора\n{traceback.format_exc()}')

    return cpu, info

async def search_create_storage(computer_info, computer, is_new_computer):
    info = ''
    
    storages = computer_info['storages']
    storage_model_name = None
    storage_name = ''

    old_storages = await sync_to_async(list)(computer.storage_set.all())
    new_storages = []

    for storage_element in storages:
        storage_vendor = None
        storage_model = None            
        storage_serial = storage_element['storage_serialnumber']
        storage_name = storage_element['storage_name']
        storage_memory = storage_element['storage_disksize']
        storage_type = storage_element['storage_type']
        
        try:
            storage_vendor, vendor_info = await __get_storage_vendor_from_name(storage_name)
            info += vendor_info
        except ObjectDoesNotExist:
            info += f'Не нашли производителя накопителя памяти: "{storage_name}"\n'
            return None, info
        
        regex = re.compile(re.escape(str(storage_vendor)), re.IGNORECASE)
        storage_model_name = regex.sub('', storage_name).strip()
        
        storage_type, storage_type_created = await StorageType.objects.aget_or_create(name=storage_type)
        if storage_type_created:
            info += f'Не нашли тип накопителя памяти: "{storage_type}" - создаём\n'
        else:
            info += f'Нашли тип накопителя памяти: "{storage_type}"\n'

        storage_model, storage_model_created = await StorageModel.objects.aget_or_create(name=storage_model_name, vendor=storage_vendor, memory=storage_memory, type=storage_type)
        if storage_model_created:
            info += f'Не нашли модель накопителя памяти: "{storage_model_name}" - создаём\n'
        else:
            info += f'Нашли модель накопителя памяти: "{storage_model_name}"\n'

        if is_new_computer:
            try:
                storage, storage_info = await __get_unused_storage_or_create_new(storage_serial, storage_name, storage_model, computer)
                info += storage_info
            except:
                logger.error(f'Ошибка привязки/создания накопителя памяти\n{traceback.format_exc()}')
        else:
            try:
                storage = await Storage.objects.aget(name=storage_name, serial_number=storage_serial, computer=computer)
                info += f'Нашли накопитель памяти: "{storage_name}"\n'
                new_storages.append(storage)
            except ObjectDoesNotExist:
                try:
                    storage, storage_info = await __get_unused_storage_or_create_new(storage_serial, storage_name, storage_model, computer)
                    info += storage_info
                    new_storages.append(storage)
                except:
                    logger.error(f'Ошибка привязки/создания накопителя памяти\n{traceback.format_exc()}')
            except:
                logger.error(f'Ошибка поиска накопителя памяти {storage_name}\n{traceback.format_exc()}')

    if len(old_storages) > 0:
        if set(old_storages) != set(new_storages):
            try:
                update_info = await sync_to_async(helper.update_storages)(computer, old_storages, new_storages)
                info += update_info
            except:
                logger.error(f'Ошибка замены накопителей памяти\n{traceback.format_exc()}')

    return None, info

async def search_create_videocard(computer_info, computer, is_new_computer):
    info = ''

    videocard_elements = computer_info.get('videocards', [])
    
    old_videocards = await sync_to_async(list)(computer.videocard_set.all())
    new_videocards = []
    videocard_vendor = None
    videocard_model_name = None
    
    videocard_name = ''
    
    for videocard_element in videocard_elements:
        videocard_model = None
        videocard_name = videocard_element.get('videocard_name', '')
        videocard_memory = videocard_element.get('videocard_memory', '')
        
        try:
            videocard_vendor, vendor_info = await __get_videocard_vendor_from_name(videocard_name)
            info += vendor_info
        except ObjectDoesNotExist:
            info += f'Не нашли производителя видеокарты: "{videocard_name}"\n'
            return None, info

        regex = re.compile(re.escape(str(videocard_vendor)), re.IGNORECASE)
        videocard_model_name = regex.sub('', videocard_name).strip()

        videocard_model, videocard_model_created = await VideocardModel.objects.aget_or_create(name=videocard_model_name, memory=videocard_memory, vendor=videocard_vendor)
        if videocard_model_created:
            info += f'Не нашли модель видеокарты: "{videocard_model_name}" - создаём\n'
        else:
            info += f'Нашли модель видеокарты: "{videocard_model_name}"\n'

        if is_new_computer:
            try:
                videocard, videocard_info = await __get_unused_videocard_or_create_new(videocard_name, videocard_model, computer)
                info += videocard_info
            except:
                logger.error(f'Ошибка привязки/создания накопителя памяти\n{traceback.format_exc()}')
        else:
            try:
                videocard = await Videocard.objects.aget(name=videocard_name, model=videocard_model, computer=computer)
                info += f'Нашли видеокарту: "{videocard_name}"\n'
                new_videocards.append(videocard)
            except ObjectDoesNotExist:
                try:
                    videocard, videocard_info = await __get_unused_videocard_or_create_new(videocard_name, videocard_model, computer)
                    info += videocard_info
                    new_videocards.append(videocard)
                except:
                    logger.error(f'Ошибка привязки/создания накопителя памяти\n{traceback.format_exc()}')
            except:
                logger.error(f'Ошибка поиска видеокарты {videocard_name}\n{traceback.format_exc()}')

    if len(old_videocards) > 0:
        if set(old_videocards) != set(new_videocards):
            try:
                update_info = await sync_to_async(helper.update_videocards)(computer, old_videocards, new_videocards)
                info += update_info
            except:
                logger.error(f'Ошибка замены видеокарт\n{traceback.format_exc()}')

    return None, info

async def search_create_ram(computer_info, computer, is_new_computer):
    info = ''
    rams = computer_info['memories']
    
    old_rams = await sync_to_async(list)(computer.ram_set.all())
    new_rams = []

    for ram_element in rams:
        ram_name = f"{computer_info['os']['computer_name']} {ram_element['ram_slot']}"
        ram_model_element = ram_element['ram_model']
        ram_vendor_element = ram_element['ram_vendor']
        ram_memory = float(ram_element['ram_memory'])
        ram_frequency = ram_element['ram_frequency']
        ram_slot = ram_element['ram_slot']
        ram_type_name = ram_element['ram_type'] if ram_element['ram_type'].upper() != "UNKNOWN" else None
        ram_model = None
        ram_type = None
                
        try:
            ram_vendor, vendor_info = await __search_add_vendor(ram_vendor_element, VendorType.Type.RAM)
            info += vendor_info
        except ObjectDoesNotExist:
            info += f'Не нашли производителя оперативной памяти: "{ram_name}"\n'
            return None, info
        
        if ram_type_name:
            ram_type, ram_type_created = await RAMType.objects.aget_or_create(name=ram_type_name)
            if ram_type_created:
                info += f'Не нашли тип оперативной памяти: "{ram_type_name}" - создаём\n'
            else:
                info += f'Нашли тип оперативной памяти: "{ram_type_name}"\n'

        ram_model, ram_model_created = await RAMModel.objects.aget_or_create(name=ram_model_element, vendor=ram_vendor, memory=ram_memory, type=ram_type)
        if ram_model_created:
            info += f'Не нашли модель оперативной памяти: "{ram_model_element}" - создаём\n'
        else:
            info += f'Нашли модель оперативной памяти: "{ram_model_element}"\n'

        if is_new_computer:
            try:
                ram, ram_info = await __get_unused_ram_or_create(ram_name, ram_model, ram_slot, ram_frequency, computer)
                info += ram_info
            except:
                logger.error(f'Ошибка привязки/создания оперативной памяти\n{traceback.format_exc()}')
        else:
            try:
                ram = await RAM.objects.aget(name=ram_name, model=ram_model, computer=computer)
                info += f'Нашли оперативную память: "{ram_name}"\n'
                if ram.is_updating and ram.frequency != ram_frequency:
                    info += f'Обновляем частоту оперативной памяти ({ram.frequency} -> {ram_frequency})'
                    ram.frequency = ram_frequency
                    await ram.asave()
                new_rams.append(ram)
            except ObjectDoesNotExist:
                try:
                    ram, ram_info = await __get_unused_ram_or_create(ram_name, ram_model, ram_slot, ram_frequency, computer)
                    info += ram_info
                    new_rams.append(ram)
                except:
                    logger.error(f'Ошибка привязки/создания оперативной памяти\n{traceback.format_exc()}')
            except:
                logger.error(f'Ошибка поиска оперативной памяти {ram_name}\n{traceback.format_exc()}')
            
    if len(old_rams) > 0:
        if set(old_rams) != set(new_rams):
            try:
                update_info = await sync_to_async(helper.update_rams)(computer, old_rams, new_rams)
                info += update_info
            except:
                logger.error(f'Ошибка замены оперативной памяти\n{traceback.format_exc()}')

    return None, info

async def search_create_monitor(computer_info, computer, is_new_computer):
    info = ''
    monitor_elements = computer_info.get('monitors', [])

    old_monitors = await sync_to_async(list)(computer.monitor_set.all())
    new_monitors = []
    monitor_vendor_name = None
    monitor_model_name = None
    monitor_name = ''
    monitor_serial = ''

    for monitor_element in monitor_elements:
        monitor_vendor_name = monitor_element['monitor_vendor']
        monitor_model_name = monitor_element['monitor_model']
        monitor_name = monitor_element['monitor_name']
        monitor_serial = monitor_element['monitor_serialnumber']
        monitor_resolution = monitor_element['monitor_resolution']
        monitor = None
        resolution = None
        resolution_format = None

        if not monitor_resolution:
            try:
                monitor_resolution = computer_info['videocards'][0]['videocard_resolution']
            except:
                monitor_resolution = "UNKNOWN RESOLUTION"
                
        try:
            monitor_vendor, vendor_info = await __search_add_vendor(monitor_vendor_name, VendorType.Type.MONITOR)
            info += vendor_info
        except ObjectDoesNotExist:
            info += f'Не нашли производителя монитора: "{monitor_name}"\n'
            return None, info
        
        monitor_model, monitor_model_created = await MonitorModel.objects.aget_or_create(name=monitor_model_name, vendor=monitor_vendor)
        if monitor_model_created:
            info += f'Не нашли модель монитора: "{monitor_model_name}" - создаём\n'
        else:
            info += f'Нашли модель монитора: "{monitor_model_name}"\n'

        if monitor_resolution:
            try:
                resolution = await Resolution.objects.aget(name=monitor_resolution)
                info += f'Нашли разрешение: "{monitor_resolution}"\n'
            except ObjectDoesNotExist:
                resolution_format, resolution_format_created = await ResolutionFormat.objects.aget_or_create(name=await __calculate_resolution_format(monitor_resolution))
                if resolution_format_created:
                    info += f'Не нашли соотношение сторон для разрешения: "{monitor_resolution}" - создаём\n'
                else:
                    info += f'Нашли соотношение сторон: "{resolution_format.name}"\n'
                info += f'Не нашли разрешение: "{monitor_resolution}" - создаём\n'
                resolution = await Resolution.objects.acreate(name=monitor_resolution, resolution_format=resolution_format)
            except:
                logger.error(f'Ошибка поиска разрешения {monitor_resolution}\n{traceback.format_exc()}')

        if is_new_computer:
            try:
                monitor, monitor_info = await __get_unused_monitor_or_create(monitor_serial, monitor_name, monitor_model, resolution, computer)
                info += monitor_info
            except:
                logger.error(f'Ошибка привязки/создания монитора\n{traceback.format_exc()}')
        else:
            try:
                monitor = await Monitor.objects.aget(serial_number=monitor_serial, name=monitor_name, model=monitor_model, computer=computer)
                new_monitors.append(monitor)
            except ObjectDoesNotExist:
                try:
                    monitor, monitor_info = await __get_unused_monitor_or_create(monitor_serial, monitor_name, monitor_model, resolution, computer)
                    info += monitor_info
                except:
                    logger.error(f'Ошибка привязки/создания монитора\n{traceback.format_exc()}')
            except:
                logger.error(f'Ошибка поиска монитора {monitor_serial}\n{traceback.format_exc()}')

    if len(old_monitors) > 0:
        if set(old_monitors) != set(new_monitors):
            try:
                update_info = await sync_to_async(helper.update_monitors)(computer, old_monitors, new_monitors)
                info += update_info
            except:
                logger.error(f'Ошибка замены мониторов\n{traceback.format_exc()}')
    return None, info

async def search_create_software(computer_info, computer):
    info, errors = '', ''
    softwares = computer_info['softwares']

    if len(softwares) > 0:
        for software_element in softwares:
            software_vendor_name = software_element['software_publisher']
            software_name = software_element['software_name']
            software_version = software_element['software_version']
            software_install_date = software_element['software_install_date']
            software_folder = software_element['software_folder']

            software_type, software_type_created = await SoftwareType.objects.aget_or_create(name="UNKNOWN SOFTWARE TYPE")

            try:
                software_vendor, vendor_info = await __search_add_vendor(software_vendor_name, VendorType.Type.SOFTWARE)
            except ObjectDoesNotExist:
                return None, info, errors
            
            software = await Software.objects.filter(name=software_name, vendor=software_vendor).afirst()
            if software is None:
                software = await Software.objects.acreate(name=software_name, vendor=software_vendor, type=software_type)
            
            soft_version = await Software_Computer.objects.filter(software=software, version=software_version, computer=computer).afirst()
            if soft_version is None:
                info = info + f'Не нашли ПО: "{software_name}" версии: "{software_version}" и издателя: "{software_vendor}", поэтому создаём\n'
                try:
                    software = await Software_Computer.objects.acreate(software=software, computer=computer, version=software_version, install_date=software_install_date, folder=software_folder)
                except:
                    software = await Software_Computer.objects.acreate(software=software, computer=computer, version=software_version, install_date=None, folder=software_folder)
            else:
                info = info + f'Нашли ПО: "{software_name}" версии: "{software_version}" и издателя: "{software_vendor}"'
            
    else:
        errors = errors + 'Не найдена информация о ПО\n'

    return None, info, errors

async def search_create_drive(computer_info, computer):
    info, errors = '', ''
    drives = computer_info['drives']

    if len(drives) > 0:
        for drive in drives:
            drive_letter = drive['drive_letter']
            drive_total_memory = drive['drive_total_memory']
            drive_free_memory = drive['drive_free_memory']

            drive = await Drive.objects.filter(letter=drive_letter, computer=computer).afirst()

            if drive is None:
                await Drive.objects.acreate(letter=drive_letter, total_memory=drive_total_memory, free_memory=drive_free_memory, computer=computer)
            else:
                if float(drive_total_memory) != float(drive.total_memory) or float(drive_free_memory) != float(drive.free_memory):
                    drive.total_memory = drive_total_memory
                    drive.free_memory = drive_free_memory
                    await drive.asave()

    return None, info, errors

# async def search_create_os(computer_info, computer):
#     name = computer_info['os']['os_name']
#     version = computer_info['os']['os_version']
#     license_key = computer_info['os']['winkey']
#     os = None
#     os_version = None
#     info = ''

#     os, os_created = await OS.objects.aget_or_create(name=name)
        
#     if not os_created and await os.version.afirst():
#         os_version = await os.version.afirst()
#         if os_version.name != version:
#             os_version.name = version
#             await os_version.asave()
#     else:
#         os_version, os_version_created = await OSVersion.objects.aget_or_create(name=version)
#         await os.version.aadd(os_version)

#     os_computer, os_computer_created = await OS_Computer.objects.aupdate_or_create(os=os, computer=computer, defaults={'license_key': license_key})

#     return os_computer, info

async def search_create_os(computer_info, computer):
    name = computer_info['os']['os_name']
    version = computer_info['os']['os_version']
    license_key = computer_info['os']['winkey']
    os = None
    os_computer = None
    info = ''

    os, os_created = await OS.objects.aget_or_create(name=name)

    os_version, os_version_created = await OSVersion.objects.aget_or_create(name=version)

    os_computer, os_computer_created = await OS_Computer.objects.aupdate_or_create(
        os=os, 
        computer=computer, 
        defaults={'license_key': license_key, 'version': os_version}
    )

    return os_computer, info

async def notificate(text, type):
    if type == 'info':
        if text == '':
            
            text = f'INFO: всё нашлось'
            await Notification.objects.acreate(message=text, created_at=datetime.datetime.now())
        else:
            await Notification.objects.acreate(message=text, created_at=datetime.datetime.now())
            
    else:
        if text == '':
            print(f'ERRORS: всё гуд, ошибок нет')
        else:
            print(f'ERRORS: {text}')

def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as err:
            
            print(err)
            return None
        return result
    return wrapper

async def update_CPU_model(cpu_model, **kwargs):
    changes = {}
    for key, value in kwargs.items():
        if getattr(cpu_model, key) != value:
            changes[key] = {
                'old_value': getattr(cpu_model, key),
                'new_value': value
            }
            setattr(cpu_model, key, value)
    await cpu_model.asave()

    return cpu_model

async def send_error_in_telegram(message):
    print(message)

async def __get_storage_vendor_from_name(name):
    for word in name.split():
        try:
            return await __search_add_vendor(word, VendorType.Type.STORAGE, True)
        except ObjectDoesNotExist:
            continue
    
    vendor = await Vendor.objects.acreate(name=f'Unknown storage vendor')
    info = f'Не нашли производителя накопителя памяти "{name}" в справочнике - создаём\n'
    await vendor.vendor_type.aadd(VendorType.Type.STORAGE)
    return vendor, info

async def __get_videocard_vendor_from_name(name):
    info = ''
    for word in name.split():
        try:
            return await __search_add_vendor(word, VendorType.Type.VIDEOCARD, True)
        except ObjectDoesNotExist:
            continue

    vendor = await Vendor.objects.acreate(name=f'Unknown videocard vendor')
    await vendor.vendor_type.aadd(VendorType.Type.VIDEOCARD)
    return vendor, info

async def __get_unused_motherboard_or_create_new(name, model, computer):
    info = ''

    motherboard = await Motherboard.objects.filter(name=name, model=model, computer=None, can_installing=True).afirst()
    if motherboard:
        info += f'Нашли не привязанную материнскую плату: "{name}"\n'
        motherboard.computer = computer
        motherboard.can_installing = False
        await motherboard.asave()
    else:
        info += f'Не нашли не привязанную материнскую плату: "{name}" - создаём\n'
        motherboard = await Motherboard.objects.acreate(name=name, model=model, computer=computer, can_installing=False, is_updating=True)
    
    await MotherboardHistory.objects.acreate(computer=computer, motherboard=motherboard)
    return motherboard, info

async def __get_unused_cpu_or_create_new(name, model, frequency, computer):
    info = ''
    
    cpu = await CPU.objects.filter(name=name, model=model, computer=None, can_installing=True, is_updating=True).afirst()
    if cpu:
        info += f'Нашли не привязанный процессор: "{name}"\n'
        cpu.computer = computer
        cpu.can_installing = False
        if cpu.frequency != frequency:
            info += f'Обновляем частоту процессора: ("{cpu.frequency}" -> "{frequency}")\n'
            cpu.frequency = frequency
            await cpu.asave()
        await cpu.asave()
    else:
        info += f'Не нашли не привязанный процессор: "{name}" - создаём\n'
        cpu = await CPU.objects.acreate(name=name, model=model, frequency=frequency, computer=computer, can_installing=False, is_updating=True)
    
    await CPUHistory.objects.acreate(computer=computer, cpu=cpu)
    return cpu, info

async def __get_unused_storage_or_create_new(serial, name, model, computer):
    info = ''
    
    storage = await Storage.objects.filter(serial_number=serial, computer=None).afirst()
    if storage:
        info += f'Нашли не привязанный накопитель памяти: "{name}"\n'
        storage.computer = computer
        storage.can_installing = False
        await storage.asave()
    else:
        info += f'Не нашли не привязанный накопитель памяти: "{name}" - создаём\n'
        storage = await Storage.objects.acreate(serial_number=serial, name=name, model=model, computer=computer, can_installing=False, is_updating=True)
    
    await StorageHistory.objects.acreate(storage=storage, computer=computer)

    return storage, info

async def __get_unused_videocard_or_create_new(name, model, computer):
    info = ''

    videocard = await Videocard.objects.filter(name=name, model=model, computer=None, can_installing=True).afirst()
    if videocard:
        info += f'Нашли не привязанную видеокарту: "{name}"\n'
        videocard.computer = computer
        videocard.can_installing = False
        await videocard.asave()
    else:
        info += f'Не нашли не привязанную видеокарту: "{name}" - создаём\n'
        videocard = await Videocard.objects.acreate(name=name, model=model, computer=computer, can_installing=False, is_updating=True)
    
    await VideocardHistory.objects.acreate(videocard=videocard, computer=computer)

    return videocard, info

async def __get_unused_ram_or_create(name, model, slot, frequency, computer):
    info = ''

    ram = await RAM.objects.filter(name=name, model=model, computer=None, can_installing=True, is_updating=True).afirst()
    if ram:
        info += f'Нашли не привязанную оперативную память: "{name}"\n'
        if ram.frequency != frequency:
            info += f'Обновляем частоту ({ram.frequency} -> {frequency})\n'
            ram.frequency = frequency
        ram.computer = computer
        ram.slot = slot
        ram.can_installing = False
        await ram.asave()
    else:
        info += f'Не нашли не привязанную оперативную память: "{name}"\n'
        ram = await RAM.objects.acreate(name=name, slot=slot, frequency=frequency, model=model, computer=computer, can_installing=False, is_updating=False)
    
    await RAMHistory.objects.acreate(ram=ram, computer=computer)

    return ram, info

async def __get_unused_monitor_or_create(serial_number, name, model, resolution, computer):
    info = ''

    monitor = await Monitor.objects.filter(serial_number=serial_number, computer=None).select_related('computer', 'resolution').afirst()
    if monitor:
        info += f'Нашли не привязанный монитор: "{name}"\n'
        monitor.computer = computer
        monitor.can_installing = False
        if resolution:
            if monitor.resolution != resolution:
                info += f'Обновляем разрешение ({monitor.resolution} -> {resolution})\n'
                monitor.resolution = resolution
        await monitor.asave()
    else:
        info += f'Не нашли не привязанный монитор: "{name}"\n'
        monitor = await Monitor.objects.acreate(name=name, model=model, serial_number=serial_number, resolution=resolution, inventory_number=serial_number, computer=computer, technique_type_id=TechniqueType.Type.MONITOR, can_installing=False, is_updating=True)
    
    await MonitorHistory.objects.acreate(monitor=monitor, computer=computer)

    return monitor, info

async def __search_add_vendor(vendor_name, vendor_type, is_unknown_name=False):
    vendor = None
    info = ''

    if is_unknown_name:
        vendor = await Vendor.objects.aget(name__icontains=vendor_name, vendor_type=vendor_type)
        info += f'Нашли производителя: "{vendor_name}"\n'
    else:
        vendor, vendor_created = await Vendor.objects.aget_or_create(name=vendor_name)
        if vendor_created:
            info += f'Создали производителя: "{vendor_name}"\n'
        else:
            info += f'Нашли производителя: "{vendor_name}"\n'
    
    if vendor_type not in await sync_to_async(list)(vendor.vendor_type.values_list('id', flat=True)):
        await vendor.vendor_type.aadd(vendor_type)
        info += f'Добавляем тип производителя: "{vendor_type}" к производителю: "{vendor_name}"\n'
        await vendor.asave()

    return vendor, info

async def __calculate_resolution_format(resolution):
    if resolution == "UNKNOWN RESOLUTION":
        return "UNKNOWN ASPECT RATIO"

    try:
        width = int(resolution.split(' x ')[0])
        height = int(resolution.split(' x ')[1])
        gcd = math.gcd(width, height)
        
        simplified_width = width // gcd
        simplified_height = height // gcd
    except:
        logger.error(f'Ошибка вычисления соотношения сторон у разрешения: "{resolution}"\n{traceback.format_exc()}')
        return "UNKNOWN ASPECT RATIO"

    return f'{simplified_width}:{simplified_height}'