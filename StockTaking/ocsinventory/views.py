from django.shortcuts import render

# Create your views here.
import zlib
import logging
import re

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from lxml import etree
from lxml.etree import XMLSyntaxError

#from accounts.models import User
#from agent.update_data import update_computer_data

from multiprocessing import TimeoutError as MpTimeoutError
from queue import Empty as Queue_Empty
from queue import Queue
from _thread import start_new_thread
from ctypes import c_long
from ctypes import py_object
from ctypes import pythonapi

from notifications.models import Notification

from . import xml_parser
from home.models import RAM, Computer, Monitor, MonitorModel, MonitorVendor, MotherboardVendor, MotherboardModel, Motherboard, CPUVendor, CPUModel, CPU, Storage, StorageModel, StorageVendor, Videocard, VideocardModel, VideocardVendor

from django.db.models import Sum

class MyTimeoutError(Exception):
    pass


def async_raise(tid, exctype=Exception):
    """
    Raise an Exception in the Thread with id `tid`. Perform cleanup if
    needed.
    Based on Killable Threads By Tomer Filiba
    from http://tomerfiliba.com/recipes/Thread2/
    license: public domain.
    """
    assert isinstance(tid, int), 'Invalid  thread id: must an integer'

    tid = c_long(tid)
    exception = py_object(Exception)
    res = pythonapi.PyThreadState_SetAsyncExc(tid, exception)
    if res == 0:
        raise ValueError('Invalid thread id.')
    elif res != 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError('PyThreadState_SetAsyncExc failed.')


def timeout_func(func, args=None, kwargs=None, timeout=30, q=None):
    """
    Threads-based interruptible runner, but is not reliable and works
    only if everything is pickable.
    """
    # We run `func` in a thread and block on a queue until timeout
    if not q:
        q = Queue()

    def runner():
        try:
            _res = func(*(args or ()), **(kwargs or {}))
            q.put((None, _res))
        except MyTimeoutError:
            # rasied by async_rasie to kill the orphan threads
            pass
        except Exception as ex:
            q.put((ex, None))

    tid = start_new_thread(runner, ())

    try:
        err, res = q.get(timeout=timeout)
        if err:
            raise err
        return res
    except (Queue_Empty, MpTimeoutError):
        raise MyTimeoutError(
                "{0} timeout (taking more than {1} sec)".format(func.__name__, timeout)
            )
    finally:
        try:
            async_raise(tid, MyTimeoutError)
        except (SystemExit, ValueError):
            pass


def generate_prolog():
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


def not_change_data():
    content = """<?xml version='1.0' encoding='UTF-8'?>
<REPLY>
  <RESPONSE>NO_ACCOUNT_UPDATE</RESPONSE>
</REPLY>
"""
    chunk = zlib.compress(content.encode())
    return chunk


@csrf_exempt
@never_cache
@require_http_methods(['POST'])
def ocsinventory(request):
    """
    """
    log = logging.getLogger('comp')

    def _get_body():
        return request.body

    try:
        content = timeout_func(_get_body, timeout=0.5)
    except Exception:
        content = generate_prolog()
        response = HttpResponse(content)
        response['Content-Length'] = len(content)
        response['Content-Type'] = 'application/x-compressed'
        return response

    if bool(content):
        try:
            zobj = zlib.decompressobj()
            raw_xml_str = zobj.decompress(content)
            raw_xml_str = raw_xml_str.decode('utf-8')
        except zlib.error:
            response = HttpResponse('Error decompress data.')
            return response

        try:
            raw_xml_str = raw_xml_str.encode('utf-8')
            root_xml = etree.fromstring(raw_xml_str)
        except XMLSyntaxError:
            log.error('Error parsing xml. Data=\n%s' % (raw_xml_str,))
            response = HttpResponse('Error paring xml.')
            return response

        #print(raw_xml_str)
        query_type = '' if root_xml.find('QUERY') is None else root_xml.find('QUERY').text

        if query_type == 'PROLOG':
            content = generate_prolog()
            response = HttpResponse(content)
            response['Content-Length'] = len(content)
            response['Content-Type'] = 'application/x-compressed'
            return response

        if query_type == 'INVENTORY':
            import json
            computer_info = json.loads(xml_parser.get_computer_info(raw_xml_str))

            with open(r"D:\\otus.txt", "w") as file:
                file.write(str(xml_parser.get_computer_info(raw_xml_str)))
            
            try:
                total_info = ''
                total_errors = ''

                computer, info, errors = search_create_computer(computer_info)
                
                total_info = total_info + info
                total_errors = total_errors + errors
                

                motherboard, info, errors = search_create_motherboard(computer_info, computer)
                
                total_info = total_info + info
                total_errors = total_errors + errors

                cpu, info, errors = search_create_cpu(computer_info, computer)
                
                total_info = total_info + info
                total_errors = total_errors + errors

                storages, info, errors = search_create_storage(computer_info, computer)
                
                total_info = total_info + info
                total_errors = total_errors + errors
                
                # comp_name = computer_info['os']['computer_name']
                # comp_ip = computer_info['os']['ip']
                # comp_winkey = computer_info['os']['winkey']
                # comp_arch = computer_info['os']['win_arch']
                # comp_inventory_number = computer_info['os']['inventory_number']
                    
                # c_vendor = computer_info['cpu']['vendor']
                # c_model = computer_info['cpu']['model']
                # c_frequency = computer_info['cpu']['frequency']
                # c_name = computer_info['cpu']['name']

                # storages = computer_info['storages']
                # s_vendor = None
                # s_model = None
                # storage_model = None
                
                videocards, info, errors = search_create_videocard(computer_info, computer)
                
                total_info = total_info + info
                total_errors = total_errors + errors

                rams, info, errors = search_create_ram(computer_info, computer)
                
                total_info = total_info + info
                total_errors = total_errors + errors

                monitors, info, errors = search_create_monitor(computer_info, computer)
                
                total_info = total_info + info
                total_errors = total_errors + errors
                
                notificate(total_info, 'info')
                notificate(total_errors, 'errors')

                # videocards = computer_info['videocards']
                # v_vendor = None
                # v_model = None
                # videocard_model = None

                #rams = computer_info['memories']

                #monitors = computer_info['monitors']
                    
                #print(f'storage_vendor: {storage_vendor}\nstorage_model: {storage_model}\nstorage_name: {storage_name}')

                #print(f'############\nm_vendor: {m_vendor}\nm_model: {m_model}\nm_name: {m_name}\n############\nc_vendor: {cpu_vendor}\nc_model: {cpu_model}\ncpu_frequency: {cpu_frequency}\nc_name: {cpu_name}')

                # motherboard_vendor = MotherboardVendor.objects.filter(motherboardVendor_name=m_vendor).first()
                # if motherboard_vendor is None:
                #     motherboard_vendor = create_motherboardVendor(m_vendor)
                
                # motherboard_model = MotherboardModel.objects.filter(motherboardModel_name=m_model).first()
                # if motherboard_model is None:
                #     motherboard_model = create_motherboardModel(m_model, motherboard_vendor.id)

                # motherboard_name = Motherboard.objects.filter(motherboard_name=m_name).first()
                # if motherboard_name is None:
                #     motherboard_name = create_motherboard(m_name, motherboard_model.id)
                    
                #############################################################################################

                # cpu_vendor = CPUVendor.objects.filter(CPU_vendor_name=c_vendor).first()
                # if cpu_vendor is None:
                #     cpu_vendor = create_CPU_vendor(c_vendor)

                # cpu_model = CPUModel.objects.filter(CPU_model_name=c_model).first()
                # if cpu_model is None:
                #     cpu_model = create_CPU_model(c_model, cpu_vendor.id)

                # cpu = CPU.objects.filter(CPU_name=c_name).first()
                # if cpu is None:
                #     cpu = create_CPU(c_name, c_frequency, cpu_model.id)

                #############################################################################################
                
                # computer = Computer.objects.filter(computer_name=comp_name, computer_inventory_number=comp_inventory_number).first()
                # if computer is None:
                #     if motherboard:
                #         if cpu:
                #             computer = create_computer(comp_name, comp_inventory_number, comp_arch, motherboard, cpu)
                #         else:
                #             print('Не нашли проц у компа')
                #     else:
                #         print('Не нашли мать у компа')
                #storage_type = StorageType.objects.filter(storage_type_name=)

                ############################################################################################# 

                # if len(storages) > 0:
                #     for storage in storages:
                #         s_name = storage['storage_name']
                #         for word in s_name.split():
                #             s_vendor = StorageVendor.objects.filter(storage_vendor_name__icontains=word).first()
                #             if (s_vendor):
                #                 break
                            
                #         if s_vendor is not None:
                #             regex = re.compile(re.escape(str(s_vendor)), re.IGNORECASE)
                #             s_model = regex.sub('', s_name).strip()
                #             storage_model = StorageModel.objects.filter(storage_model_name=s_model).first()
                #             if storage_model is None:
                #                 storage_model = create_storage_model(s_model, storage['storage_disksize'], s_vendor.id)

                #         storage_name = Storage.objects.filter(storage_name=s_name, storage_serial=storage['storage_serialnumber'], computer=computer).first()
                #         if storage_name is None and storage_model is not None:
                #             storage_name = create_storage(name=s_name, serial=storage['storage_serialnumber'], s_model_id=storage_model.id, computer=computer)
                #         elif storage_name is None and storage_model is None:
                #             storage_name = create_storage(name=s_name, serial=storage['storage_serialnumber'], computer=computer)
                #                 #storage_model = storage_name.toupper().replace(str(storage_vendor).toupper(), '').lstrip().rstrip()

                #############################################################################################

                # if len(videocards) > 0:
                #     for videocard in videocards:
                #         v_name = videocard['videocard_name']
                #         for word in v_name.split():
                #             v_vendor = VideocardVendor.objects.filter(videocard_vendor_name=word).first()
                #             if (v_vendor):
                #                 break

                #         if v_vendor is not None:
                #             regex = re.compile(re.escape(str(v_vendor)), re.IGNORECASE)
                #             v_model = regex.sub('', v_name).strip()
                #             videocard_model = VideocardModel.objects.filter(videocard_model_name=v_model, videocardVendors=v_vendor).first()
                #             if videocard_model is None:
                #                 videocard_model = create_videocard_model(v_model, videocard['videocard_memory'], v_vendor)
                        
                #         videocard_name = Videocard.objects.filter(videocard_name=v_name, videocardModel=videocard_model).first()
                #         if videocard_name is None and videocard_model is not None:
                #             videocard_name = create_videocard(name=v_name, v_model_id=videocard_model.id, computer=computer)
                #         elif videocard_name is None and videocard_model is None:
                #             videocard_name = create_videocard(name=v_name, computer=computer)

                #############################################################################################

                # from django.db.models import Sum
                # if len(rams) > 0:
                #     for ram in rams:
                #         ram_name = RAM.objects.filter(ram_memory=ram['ram_memory'], ram_frequency=ram['ram_frequency'], computer=computer).first()
                #         total_ram_memory = RAM.objects.filter(computer=computer).aggregate(Sum('ram_memory'))
                #         if ram_name is None or total_ram_memory['ram_memory__sum'] != float(computer_info['os']['total_ram_memory']):
                #             ram_name = create_ram(name='', memory=ram['ram_memory'], frequency=ram['ram_frequency'], computer=computer)

                #############################################################################################

                # if len(monitors) > 0:
                #     for monitor in monitors:
                #         mon_vendor = monitor['monitor_vendor']
                #         mon_model = monitor['monitor_model']
                #         mon_name = monitor['monitor_name']
                #         mon_serial = monitor['monitor_serialnumber']
                #         mon_resolution = computer_info['videocards'][0]['videocard_resolution']
                        
                #         monitor_vendor = MonitorVendor.objects.filter(monitor_vendor_name=mon_vendor).first()
                #         if monitor_vendor is None:
                #             monitor_vendor = create_monitor_vendor(mon_vendor)
                        
                #         monitor_model = MonitorModel.objects.filter(monitor_model_name=mon_model, monitorVendor_id=monitor_vendor.id).first()
                #         if monitor_model is None:
                #             monitor_model = create_monitor_model(mon_model, monitor_vendor)

                #         monitor_name = Monitor.objects.filter(monitor_name=mon_name, monitorModel=monitor_model).first()
                #         if monitor_name is None:
                #             monitor_name = create_monitor(mon_name, monitor_model, mon_serial, mon_resolution, computer)

                #############################################################################################
            except Exception as err:
                print(f'tyt {err}')
                with open(r"D:\\otus2.txt", "w") as file:
                    file.write(f'error {err}')

            content = not_change_data()
            response = HttpResponse(content)
            response['Content-Length'] = len(content)
            response['Content-Type'] = 'application/x-compressed'
            return response

        # Answer default
        content = generate_prolog()
        response = HttpResponse(content)
        response['Content-Length'] = len(content)
        response['Content-Type'] = 'application/x-compressed'
        return response
    else:
        content = generate_prolog()
        response = HttpResponse(content)
        response['Content-Length'] = len(content)
        response['Content-Type'] = 'application/x-compressed'
        return response

def search_create_computer(computer_info):
    info = ''
    errors = ''
    
    computer_name = computer_info['os']['computer_name']
    computer_ip = computer_info['os']['ip']
    computer_winkey = computer_info['os']['winkey']
    computer_arch = computer_info['os']['win_arch']
    computer_inventory_number = computer_info['os']['inventory_number']

    computer = Computer.objects.filter(computer_inventory_number=computer_inventory_number).first()

    if computer is None:
        info = info + f'Не смогли найти компьютер по инвентарному номеру: {computer_inventory_number}. Пробуем найти по названию\n'
        computer = Computer.objects.filter(computer_name=computer_name).first()
        if computer is None:
            errors = errors + f'Не смогли найти компьюте по инвентарному номеру: {computer_inventory_number} и названию: {computer_name}, поэтому создаём\n'
            computer = create_computer(computer_name, computer_inventory_number, computer_arch)

    return computer, info, errors

def search_create_motherboard(computer_info, computer):
    info = ''
    errors = ''

    motherboard_vendor_name = computer_info['motherboard']['vendor']
    motherboard_model_name = computer_info['motherboard']['model']
    motherboard_name = computer_info['motherboard']['name']

    motherboard_vendor = MotherboardVendor.objects.filter(motherboardVendor_name=motherboard_vendor_name).first()
    if motherboard_vendor is None:
        info = info + f'Не нашли производителя материнской платы: "{motherboard_vendor_name}", поэтому создаём\n'
        motherboard_vendor = create_motherboardVendor(motherboard_vendor_name)

    if motherboard_vendor is None:
        errors = errors + f'Не нашли производителя материнской платы: {motherboard_vendor_name}\n'
        
    motherboard_model = MotherboardModel.objects.filter(motherboardModel_name=motherboard_model_name, motherboardVendor=motherboard_vendor).first()
    if motherboard_model is None:
        info = info + f'Не нашли модель материнской платы: "{motherboard_model_name}" с производителем: "{motherboard_vendor_name}", поэтому создаём\n'
        motherboard_model = create_motherboardModel(motherboard_model_name, motherboard_vendor)

    if motherboard_model is None:
        errors = errors + f'Не нашли модель материнской платы: {motherboard_model_name}\n'

    motherboard = Motherboard.objects.filter(motherboard_name=motherboard_name, motherboardModel=motherboard_model).first()
    if motherboard is None:
        info = info + f'Не нашли материнскую плату: "{motherboard_name} с моделью "{motherboard_model_name}" и производителем "{motherboard_vendor_name}", поэтому создаём\n'
        motherboard = create_motherboard(motherboard_name, motherboard_model, computer)

    return motherboard, info, errors

def search_create_cpu(computer_info, computer):
    info = ''
    errors = ''

    cpu_vendor_name = computer_info['cpu']['vendor']
    cpu_model_name = computer_info['cpu']['model']
    cpu_name = computer_info['cpu']['name']
    cpu_frequency = computer_info['cpu']['frequency']

    cpu_vendor = CPUVendor.objects.filter(CPU_vendor_name=cpu_vendor_name).first()
    if cpu_vendor is None:
        info = info + f'Не нашли производителя процессора: "{cpu_vendor_name}", поэтому создаём\n'
        cpu_vendor = create_CPU_vendor(cpu_vendor_name)

    if cpu_vendor is None:
        errors = errors + f'Не нашли производителя процессора: {cpu_vendor_name}\n'
        
    cpu_model = CPUModel.objects.filter(CPU_model_name=cpu_model_name, CPUVendor=cpu_vendor).first()
    if cpu_model is None:
        info = info + f'Не нашли модель материнской платы: "{cpu_model_name}" с производителем: "{cpu_vendor}", поэтому создаём\n'
        cpu_model = create_CPU_model(cpu_model_name, cpu_vendor)

    if cpu_model is None:
        errors = errors + f'Не нашли модель процессора: {cpu_model_name}\n'

    cpu = CPU.objects.filter(CPU_name=cpu_name, CPU_frequency=cpu_frequency, CPUModel=cpu_model).first()
    if cpu is None:
        info = info + f'Не нашли процессор: "{cpu_name} с моделью "{cpu_model_name}", производителем "{cpu_vendor_name}" и частотой: "{cpu_frequency}", поэтому создаём\n'
        cpu = create_CPU(cpu_name, cpu_frequency, cpu_model, computer)

    return cpu, info, errors

def search_create_storage(computer_info, computer):
    info, errors = '', ''
    
    storages = computer_info['storages']
    storage_vendor = None
    storage_model_name = None
    storage_model = None
    storage_name = ''

    if len(storages) > 0:
        for storage_element in storages:
            storage_serial = storage_element['storage_serialnumber']
            storage_name = storage_element['storage_name']
            for word in storage_name.split():
                storage_vendor = StorageVendor.objects.filter(storage_vendor_name__icontains=word).first()
                if (storage_vendor):
                    break
                            
            if storage_vendor is not None:
                regex = re.compile(re.escape(str(storage_vendor)), re.IGNORECASE)
                storage_model_name = regex.sub('', storage_name).strip()
                storage_model = StorageModel.objects.filter(storage_model_name=storage_model_name).first()
                if storage_model is None:
                    info = info + f'Не нашли модель накоителя памяти у: {storage_name}, поэтому создаём модель: {storage_model_name}\n'
                    storage_model = create_storage_model(storage_model_name, storage_element['storage_disksize'], storage_vendor.id)
            else:
                errors = errors + f'Не нашли производителя накопителя памяти у: "{storage_name}"\n'

            storage = Storage.objects.filter(storage_name=storage_name, storage_serial=storage_element['storage_serialnumber'], computer=computer).first()
            if storage is None:
                info = info + f'Не нашли накопитель памяти по наименованию: "{storage_name}", серийному номеру: "{storage_serial}", поэтому создаём его\n'
                storage = create_storage(name=storage_name, serial=storage_serial, model=storage_model, computer=computer)
    else:
        errors = errors + 'Не нашли ни одного накопителя памяти у компьютера'

    return None, info, errors

def search_create_videocard(computer_info, computer):
    info, errors = '', ''
    
    videocards = computer_info['videocards']
    videocard_vendor = None
    videocard_model_name = None
    videocard_model = None
    videocard_name = ''

    for videocard_element in videocards:
        videocard_memory = videocard_element['videocard_memory']
        videocard_name = videocard_element['videocard_name']
        for word in videocard_name.split():
            videocard_vendor = VideocardVendor.objects.filter(videocard_vendor_name=word).first()
            if (videocard_vendor):
                break

        if videocard_vendor is not None:
            regex = re.compile(re.escape(str(videocard_vendor)), re.IGNORECASE)
            videocard_model_name = regex.sub('', videocard_name).strip()
            videocard_model = VideocardModel.objects.filter(videocard_model_name=videocard_model_name, videocardVendors=videocard_vendor).first()
            if videocard_model is None:
                info = info + f'Не нашли модель видеокарты: "{videocard_model_name}" у производителя: "{videocard_vendor}", поэтому создаём\n'
                videocard_model = create_videocard_model(videocard_model_name, videocard_memory, videocard_vendor)
        else:
            errors = errors + f'Не нашли производителя видеокарты у: "{videocard_name}"\n'
                        
        videocard = Videocard.objects.filter(videocard_name=videocard_name, videocardModel=videocard_model).first()
        if videocard is None:
            info = info + f'Не нашли видеокарту: "{videocard_model_name}" с моделью: "{videocard_model}", поэтому создаём\n'
            videocard = create_videocard(videocard_name, videocard_model, computer)

    return None, info, errors

def search_create_ram(computer_info, computer):
    info, errors = '', ''
    rams = computer_info['memories']
    computer_ram_memory = total_ram_memory = RAM.objects.filter(computer=computer).aggregate(Sum('ram_memory'))['ram_memory__sum']
    computer_total_ram_memory = float(computer_info['os']['total_ram_memory'])

    if len(rams) > 0:
        for ram_element in rams:
            ram_memory = float(ram_element['ram_memory'])
            ram_frequency = ram_element['ram_frequency']

            ram = RAM.objects.filter(ram_memory=ram_memory, ram_frequency=ram_frequency, computer=computer).first()
            
            if ram is None or computer_ram_memory != computer_total_ram_memory:
                info = info + f'Добавляем оперативную память с объёмом: "{ram_memory / 1024.0} ГБ" и частотой: "{ram_frequency} МГц"\n'
                '''По идее, раз не приходит имя, и чтоб хоть как-то в оперативке понимать, можно давать названия оперативке по имени компа + слот оперативки'''
                ram = create_ram(f"{computer_info['os']['computer_name']} {ram_element['ram_slot']}", ram_memory, ram_frequency, computer)
    else:
        errors = errors + 'Не найдена информация об оперативной памяти\n'

    return None, info, errors

def search_create_monitor(computer_info, computer):
    info, errors = '', ''
    monitors = computer_info['monitors']

    if len(monitors) > 0:
        for monitor_element in monitors:
            monitor_vendor_name = monitor_element['monitor_vendor']
            monitor_model_name = monitor_element['monitor_model']
            monitor_name = monitor_element['monitor_name']
            monitor_serial = monitor_element['monitor_serialnumber']
            monitor_resolution = computer_info['videocards'][0]['videocard_resolution']
                        
            monitor_vendor = MonitorVendor.objects.filter(monitor_vendor_name=monitor_vendor_name).first()
            if monitor_vendor is None:
                info = info + f'Не нашли производителя монитора: "{monitor_vendor_name}", поэтому создаём\n'
                monitor_vendor = create_monitor_vendor(monitor_vendor_name)

            monitor_model = MonitorModel.objects.filter(monitor_model_name=monitor_model_name, monitorVendor_id=monitor_vendor.id).first()
            if monitor_model is None:
                info = info + f'Не нашли модель монитора: "{monitor_model_name}" у производителя: "{monitor_vendor}", поэтому создаём\n'
                monitor_model = create_monitor_model(monitor_model_name, monitor_vendor)

            monitor = Monitor.objects.filter(monitor_name=monitor_name, monitorModel=monitor_model).first()
            if monitor is None:
                info = info + f'Не нашли монитор с названием: "{monitor_name}" и моделью: "{monitor_model}", поэтому создаём\n'
                monitor = create_monitor(monitor_name, monitor_model, monitor_serial, monitor_resolution, computer)
    else:
        errors = errors + 'Не нашли информацию о мониторах\n'

    return None, info, errors

        










import datetime
def notificate(text, type):
    if type == 'info':
        if text == '':
            #print(f'INFO: всё нашлось, ёпта')
            text = f'INFO: всё нашлось, ёпта'
            Notification.objects.create(message=text, created_at=datetime.datetime.now())
        else:
            Notification.objects.create(message=text, created_at=datetime.datetime.now())
            #print(f'INFO: {text}')
    else:
        if text == '':
            print(f'ERRORS: всё гуд, ошибок нет')
        else:
            print(f'ERRORS: {text}')

def create_motherboardVendor(name):
    s = MotherboardVendor.objects.create(motherboardVendor_name=name)
    with open(r"D:\\otus2.txt", "w") as file:
        file.write(f'create mv: {s}')
    return s

def create_motherboardModel(name, vendor):
    s = MotherboardModel.objects.create(motherboardModel_name=name, motherboardVendor=vendor)
    return s

def create_motherboard(name, model, computer):
    s = Motherboard.objects.create(motherboard_name=name, motherboardModel=model, computer=computer)
    return s

def create_CPU_vendor(name):
    s = CPUVendor.objects.create(CPU_vendor_name=name)
    return s

def create_CPU_model(name, vendor):
    s = CPUModel.objects.create(CPU_model_name=name, CPUVendor=vendor)
    return s

def create_CPU(name, frequency, model, computer):
    if frequency is None:
        frequency = 0
    s = CPU.objects.create(CPU_name=name, CPU_frequency=frequency, CPUModel=model, computer=computer)
    return s

def create_storage_model(name, memory, s_vendor_id):
    s = StorageModel.objects.create(storage_model_name=name, storage_model_memory=memory, storageVendor_id=s_vendor_id)
    return s

def create_storage(name, serial, model, computer):
    # from django.db.models import Max
    # if serial is None:
    #     serial = Storage.objects.aaggregate(Max('id')) + 1 #пока так
    #s = None
    #if serial:
    s = Storage.objects.create(storage_name=name, storage_serial=serial, storageModel=model, computer=computer)
    return s

def create_videocard_model(name, memory, vendor):
    s = VideocardModel.objects.create(videocard_model_name=name, videocard_model_memory=memory)
    s.videocardVendors.set([vendor])
    return s

def create_videocard(name, model, computer):
    s = Videocard.objects.create(videocard_name=name, videocardModel=model, computer=computer)
    return s

def create_computer(name, inventory_number, arch):
    if arch is None:
        arch = ''
    s = Computer.objects.create(computer_name=name, computer_inventory_number=inventory_number, computer_arch=arch)
    return s

def create_ram(name, memory, frequency, computer):
    s = RAM.objects.create(ram_name=name, ram_memory=memory, ram_frequency=frequency, computer=computer)
    return s

def create_monitor(name, model, serial, resolution, computer):
    s = Monitor.objects.create(monitor_name=name, monitorModel=model, monitor_serial_number=serial, monitor_resolution=resolution, monitor_inventory_number='1', computer=computer)
    return s

def create_monitor_model(name, vendor):
    s = MonitorModel.objects.create(monitor_model_name=name, monitorVendor=vendor)
    return s

def create_monitor_vendor(name):
    s = MonitorVendor.objects.create(monitor_vendor_name=name)
    return s