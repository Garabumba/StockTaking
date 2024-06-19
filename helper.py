import base64
import re

from django.http import JsonResponse
from home.models import TV, CPUHistory, CPUModel, Computer, Monitor, MonitorHistory, MotherboardHistory, OS_Computer, Printer, Projector, RAMHistory, RAMModel, Software, Software_Computer, StorageHistory, TechniqueType, Vendor, VendorType, VideocardHistory, VideocardModel
from users.models import Group, User_Task
from django.utils import timezone
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from asgiref.sync import sync_to_async

def update_computer(computer, name, ip, arch):
    info = ''
    
    if computer.name != name:
        info += f'Обновляем имя компьютера ({computer.name} -> {name})\n'
        computer.name = name
        
    if computer.ip != ip:
        info += f'Обновляем ip компьютера ({computer.ip} -> {ip})\n'
        computer.ip = ip

    if computer.arch != arch:
        info += f'Обновляем архитектуру компьютера ({computer.arch} -> {arch})\n'
        computer.arch = arch

    computer.update_date = timezone.now()

    computer.save()
    return computer, info

def update_motherboard(computer, old_motherboard, new_motherboard):
    info = f'Меняем материнскую плату ("{old_motherboard.name} -> {new_motherboard.name}")\n'
    old_motherboard.computer = None
    old_motherboard.can_installing = False
    old_motherboard.is_updating = False
    old_motherboard.save()
    MotherboardHistory.objects.filter(computer=computer, motherboard=old_motherboard).update(removed_date=timezone.now().isoformat())
    if len(MotherboardHistory.objects.filter(motherboard=new_motherboard, removed_date=None).values('motherboard_id').annotate(max_removed_date=Max('removed_date'))) < 1:
        MotherboardHistory.objects.create(computer=computer, motherboard=new_motherboard)

    new_motherboard.computer = computer
    new_motherboard.save()

    return info

def update_cpu(computer, old_cpu, new_cpu):
    info = ''
    
    if new_cpu:
        if old_cpu and old_cpu != new_cpu:
            info = f'Меняем материнскую плату ("{old_cpu.name} -> {new_cpu.name}")\n'
            old_cpu.computer = None
            old_cpu.can_installing = False
            old_cpu.is_updating = False
            old_cpu.save()
            CPUHistory.objects.filter(computer=computer, cpu=old_cpu).update(removed_date=timezone.now().isoformat())
            if len(CPUHistory.objects.filter(cpu=new_cpu, removed_date=None).values('cpu_id').annotate(max_removed_date=Max('removed_date'))) < 1:
                CPUHistory.objects.create(computer=computer, cpu=new_cpu)

            new_cpu.computer = computer
            new_cpu.save()

    return info

def update_storages(computer, old_storages, new_storages):
    info = f'Меняем накопители памяти ("{old_storages} -> {new_storages}")\n'
    if len(new_storages) > 0:
        for new_storage in new_storages:
            new_storage.computer = computer
            new_storage.save()
            if len(StorageHistory.objects.filter(storage=new_storage, removed_date=None).values('storage_id').annotate(max_removed_date=Max('removed_date'))) < 1:
                StorageHistory.objects.create(computer=computer, storage=new_storage)

        for old_storage in old_storages:
            if old_storage not in new_storages:
                old_storage.computer = None
                old_storage.can_installing = False
                old_storage.is_updating = False
                old_storage.save()
                StorageHistory.objects.filter(computer=computer, storage=old_storage).update(removed_date=timezone.now().isoformat())

    return info

def update_rams(computer, old_rams, new_rams):
    info = f'Меняем оперативную память ("{old_rams} -> {new_rams}")\n'
    for new_ram in new_rams:
        new_ram.computer = computer
        new_ram.save()
        if len(RAMHistory.objects.filter(ram=new_ram, removed_date=None).values('ram_id').annotate(max_removed_date=Max('removed_date'))) < 1:
            RAMHistory.objects.create(computer=computer, ram=new_ram)

    for old_ram in old_rams:
        if old_ram not in new_rams and old_ram.is_updating:
            old_ram.computer = None
            old_ram.can_installing = False
            old_ram.is_updating = False
            old_ram.save()
            RAMHistory.objects.filter(computer=computer, ram=old_ram).update(removed_date=timezone.now().isoformat())
    
    return info

def update_videocards(computer, old_videocards, new_videocards):
    info = f'Меняем видеокарты ("{old_videocards} -> {new_videocards}")\n'
    for new_videocard in new_videocards:
        new_videocard.computer = computer
        new_videocard.save()
        if len(VideocardHistory.objects.filter(videocard=new_videocard, removed_date=None).values('videocard_id').annotate(max_removed_date=Max('removed_date'))) < 1:
            VideocardHistory.objects.create(computer=computer, videocard=new_videocard)

    for old_videocard in old_videocards:
        if old_videocard not in new_videocards:
            old_videocard.computer = None
            old_videocard.can_installing = False
            old_videocard.is_updating = False
            old_videocard.save()
            VideocardHistory.objects.filter(computer=computer, videocard=old_videocard).update(removed_date=timezone.now().isoformat())
            
    return info

def update_monitors(computer, old_monitors, new_monitors):
    info = f'Меняем мониторы ("{old_monitors} -> {new_monitors}")\n'
    for new_monitor in new_monitors:
        new_monitor.computer = computer
        new_monitor.save()
        
        if len(MonitorHistory.objects.filter(monitor=new_monitor, removed_date=None).values('monitor_id').annotate(max_removed_date=Max('removed_date'))) < 1:
            MonitorHistory.objects.create(computer=computer, monitor=new_monitor)

    for old_monitor in old_monitors:
        if old_monitor not in new_monitors:
            old_monitor.computer = None
            old_monitor.can_installing = False
            old_monitor.is_updating = False
            old_monitor.save()
            MonitorHistory.objects.filter(computer=computer, monitor=old_monitor).update(removed_date=timezone.now().isoformat())
    
    return info

def get_technique_by_inventory_number(inventory_number, models=[Computer, Projector, Printer, TV, Monitor]):
    for model in models:
        try:
            return model.objects.get(inventory_number=inventory_number)
        except ObjectDoesNotExist:
            continue

    raise ObjectDoesNotExist
    
def __get_computer_video_memory(computer):
    try:
        return VideocardModel.objects.filter(videocard__computer=computer).aggregate(Sum('memory'))['memory__sum']
    except:
        return 0

def __get_computer_memory(computer):
    try:
        return RAMModel.objects.filter(ram__computer=computer).aggregate(Sum('memory'))['memory__sum']
    except:
        return 0
    
def __get_computer_cpu_cores(computer):
    try:
        return computer.cpu_set.first().model.cores
    except:
        return 0
    
def __get_computer_os(computer):
    try:
        return OS_Computer.objects.get(computer=computer)
    except:
        return None
    
def compare_cores(computer, cores):
    computer_cores = __get_computer_cpu_cores(computer)
    return computer_cores == cores
    
def compare_memory(computer, memory):
    computer_memory = __get_computer_memory(computer)
    return computer_memory == memory

def computer_have_videocard(computer, with_videocard):
    return with_videocard == computer.videocard_set.exists()

def compare_os(computer, os):
    computer_os = __get_computer_os(computer)
    
    if computer_os:
        return computer_os.os.name == os
    return False

def compare_video_memory(computer, memory):
    video_memory = __get_computer_video_memory(computer)
    return video_memory == memory

def computer_contains_software(computer, softwares):
    for software in softwares:
        try:
            Software_Computer.objects.get(software__name=software, computer=computer)
        except ObjectDoesNotExist:
            return False
    return True

def compare_computers_count_and_places(audience, max_computers, max_places):
    if not max_computers and not max_places:
        return True
    
    if max_computers and max_places:
        return audience.max_computers == max_computers and audience.max_places == max_places
    
    if not max_computers:
        return audience.max_places == max_places
    
    if not max_places:
        return audience.max_computers == max_computers
    
def audience_have_projector(audience, with_projector):
    try:
        Projector.objects.get(audience=audience)
        return with_projector == True
    except ObjectDoesNotExist:
        return with_projector == False
    
def check_auth_and_permissions(request, permissions=None):
    if not request.user.is_authenticated:
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).decode('utf-8').split(':', 1)
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    request.user = user
                    if permissions:
                        if user.user_permissions.all() in Permission.objects.filter(codename__in=permissions):
                            return False
                if user is None:
                    return False  
        else:
            return False
            
    return True

def search_add_vendor(vendor_name, vendor_type_id, is_unknown_name=False):
    result = None
    vendor_types = []
    vendor_created = False
    
    vendor = None
    vendor_type = VendorType.objects.get(id=vendor_type_id)

    if is_unknown_name:
        vendor = Vendor.objects.get(name__icontains=vendor_name, vendor_type=vendor_type)
    else:
        vendor, vendor_created = Vendor.objects.get_or_create(name=vendor_name)

    if vendor_type not in vendor.vendor_type.all():
        vendor_types.append(str(vendor_type))
        vendor.vendor_type.add(vendor_type)
        vendor.save()

    if len(vendor_types) > 0:
        result = {'name': vendor_name, 'types': vendor_types}

    return vendor, result

def create_user_task(users, instance, inventory_number, owner):
    if len(users) == 0:
        print("Не нашли ответственных за технику")
    
    responsible_groups = Group.objects.filter(is_responsible=True).values_list('name', flat=True)
    current_groups = []
    for user in users:
        if user.group.is_responsible:
            try:
                user_exists = User_Task.objects.get(user=user, task=instance, owner=False)
            except ObjectDoesNotExist:
                User_Task.objects.create(user=user, task=instance, owner=False)
            current_groups.append(user.group.name)

    unsearched_groups = [x for x in responsible_groups if x not in current_groups]

    if len(unsearched_groups) > 0:
        print(f"Не нашли ответственных к технике: '{inventory_number}' с ролями: \"{', '.join(unsearched_groups)}\"")
    
    try:
        owner_exists = User_Task.objects.get(task=instance, owner=True)
    except:    
        User_Task.objects.create(user=owner, task=instance, owner=True)

def create_or_update_user_task(users, selected_users, instance, inventory_number, owner):
    if len(users) == 0 and len(selected_users) == 0:
        print("Не нашли ответственных за технику")
    
    responsible_groups = Group.objects.filter(is_responsible=True).values_list('name', flat=True)
    current_groups = []

    if len(selected_users) < 1 or users == selected_users:
        __delete_users(users, instance)
        __add_existing_users(users, instance, current_groups)
        # for user in instance.users:
        #     if user not in users:
        #         User_Task.objects.filter(user=user, task=instance).delete()
        
    else:
        __delete_users(selected_users, instance)
        __add_existing_users(selected_users, instance, current_groups)
        #for current_user in users:
        #    if current_user not in selected_users:
        #        User_Task.objects.filter(user=current_user, task=instance).delete()
            # try:
            #     user_exists = User_Task.objects.get(user=current_user, task=instance, owner=False)
            # except ObjectDoesNotExist:
            #     User_Task.objects.create(user=current_user, task=instance, owner=False)

        # for selected_user in selected_users:
        #     try:
        #         User_Task.objects.get(user=selected_user, task=instance, owner=False)
        #     except ObjectDoesNotExist:
        #         User_Task.objects.create(user=selected_user, task=instance, owner=False)

    unsearched_groups = [x for x in responsible_groups if x not in current_groups]

    if len(unsearched_groups) > 0:
        print(f"Не нашли ответственных к технике: \"{inventory_number}\" с ролями: \"{', '.join(unsearched_groups)}\"")
    
    try:
        User_Task.objects.get(task=instance, owner=True)
    except ObjectDoesNotExist:    
        User_Task.objects.create(user=owner, task=instance, owner=True)

def __add_existing_users(users, instance, current_groups):
    for user in users:
        if user.group.is_responsible:
            try:
                user_exists = User_Task.objects.get(user=user, task=instance, owner=False)
            except ObjectDoesNotExist:
                User_Task.objects.create(user=user, task=instance, owner=False)
            current_groups.append(user.group.name)

def __delete_users(users, instance):
    for user in User_Task.objects.filter(task=instance, owner=False).values_list('user'):
        if user not in users:
            User_Task.objects.filter(user=user, task=instance).delete()

PERMISSION_TRANSLATIONS = {
    'Can add': 'Может добавлять',
    'Can change': 'Может редактировать',
    'Can delete': 'Может удалять',
    'Can view': 'Может просматривать',
    # Добавьте все необходимые переводы здесь
}

def get_permission_name(permission_codename):
    print(permission_codename)
    permission_codename = permission_codename.replace('Can add', 'Может добавлять').replace('Can change', 'Может редактировать').replace('Can delete', 'Может удалять').replace('Can view', 'Может просматривать')
    print(permission_codename)
    return permission_codename

def update_technique_image(audience, inventory_number, status, technique_type):
    json_data = audience.state
    #print(json_data)
    for figure in json_data['objects']:
        if figure.get('figureId') == inventory_number:
            figure['statusId'] = status.id

            if status.id == 1:
                picture = figure['src'].split('/')
                if technique_type == TechniqueType.Type.COMPUTER:
                    picture[len(picture) - 1] = "pc.png"
                elif technique_type == TechniqueType.Type.PRINTER or technique_type == TechniqueType.Type.MFU:
                    picture[len(picture) - 1] = "printer.png"
                if technique_type == TechniqueType.Type.PROJECTOR:
                    picture[len(picture) - 1] = "projector.png"
                if technique_type == TechniqueType.Type.TV:
                    picture[len(picture) - 1] = "tv.png"
                figure['src'] = '/'.join(picture)
            elif status.id == 2:
                picture = figure['src'].split('/')
                if technique_type == TechniqueType.Type.COMPUTER:
                    picture[len(picture) - 1] = "broken_pc.png"
                elif technique_type == TechniqueType.Type.PRINTER or technique_type == TechniqueType.Type.MFU:
                    picture[len(picture) - 1] = "broken_printer.png"
                if technique_type == TechniqueType.Type.PROJECTOR:
                    picture[len(picture) - 1] = "broken_projector.png"
                if technique_type == TechniqueType.Type.TV:
                    picture[len(picture) - 1] = "broken_tv.png"
                figure['src'] = '/'.join(picture)

            break
    
    audience.state = json_data
    audience.save()