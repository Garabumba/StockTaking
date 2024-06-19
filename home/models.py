import datetime
import time
from django.utils import timezone
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse_lazy
import json

'''
Производители
'''
class Vendor(models.Model):
    name = models.CharField(max_length=255, default='')
    #vendor_type = models.ForeignKey('VendorType', on_delete=models.PROTECT, null=False)
    vendor_type = models.ManyToManyField('VendorType', blank=True, related_name='Vendor_VendorType')

    class Meta:
        verbose_name = "Производители"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.vendor_type.last().id == VendorType.Type.MOTHERBOARD:
            return reverse_lazy('motherboard_vendors')
        elif self.vendor_type.last().id == VendorType.Type.CPU:
            return reverse_lazy('cpu_vendors')
        elif self.vendor_type.last().id == VendorType.Type.STORAGE:
            return reverse_lazy('storage_vendors')
        elif self.vendor_type.last().id == VendorType.Type.RAM:
            return reverse_lazy('ram_vendors')
        elif self.vendor_type.last().id == VendorType.Type.MONITOR:
            return reverse_lazy('monitor_vendors')
        elif self.vendor_type.last().id == VendorType.Type.VIDEOCARD:
            return reverse_lazy('videocard_vendors')
        elif self.vendor_type.last().id == VendorType.Type.SOFTWARE:
            return reverse_lazy('software_vendors')
        elif self.vendor_type.last().id == VendorType.Type.PROJECTOR:
            return reverse_lazy('projector_vendors')
        elif self.vendor_type.last().id == VendorType.Type.PRINTER:
            return reverse_lazy('printer_vendors')
        elif self.vendor_type.last().id == VendorType.Type.TV:
            return reverse_lazy('tv_vendors')
        return reverse_lazy('')

'''
Тип производителя
'''

class VendorType(models.Model):
    class Type(models.IntegerChoices):
        MOTHERBOARD = 1, 'Материнская плата'
        CPU = 2, 'Процессор'
        STORAGE = 3, 'Накопитель памяти'
        VIDEOCARD = 4, 'Видеокарта'
        RAM = 5, 'Оперативная память'
        MONITOR = 6, 'Монитор'
        SOFTWARE = 7, 'Программное обеспечение'
        PROJECTOR = 8, 'Проектор'
        PRINTER = 9, 'Принтер'
        TV = 10, 'Телевизор'

    name = models.CharField(choices=Type.choices, max_length=255, default='')

    class Meta:
        verbose_name = "Типы производителей"
        verbose_name_plural = "Типы производителей"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('motherboards')

###############################################################################
###############################################################################
###############################################################################

'''
Материнская плата
'''

class MotherboardHistory(models.Model):
    motherboard = models.ForeignKey('Motherboard', on_delete=models.CASCADE, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, null=True)
    installed_date = models.DateTimeField(default=timezone.now)
    removed_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "История материнских плат"
        verbose_name_plural = "История материнских плат"

class CPUHistory(models.Model):
    cpu = models.ForeignKey('CPU', on_delete=models.CASCADE, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, null=True)
    installed_date = models.DateTimeField(default=timezone.now)
    removed_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "История процессоров"
        verbose_name_plural = "История процессоров"

class RAMHistory(models.Model):
    ram = models.ForeignKey('RAM', on_delete=models.CASCADE, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, null=True)
    installed_date = models.DateTimeField(default=timezone.now)
    removed_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "История оперативнй памяти"
        verbose_name_plural = "История оперативнй памяти"

class StorageHistory(models.Model):
    storage = models.ForeignKey('Storage', on_delete=models.CASCADE, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, null=True)
    installed_date = models.DateTimeField(default=timezone.now)
    removed_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "История накопителей памяти"
        verbose_name_plural = "История накопителей памяти"

class VideocardHistory(models.Model):
    videocard = models.ForeignKey('Videocard', on_delete=models.CASCADE, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, null=True)
    installed_date = models.DateTimeField(default=timezone.now)
    removed_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "История видеокарт"
        verbose_name_plural = "История видеокарт"

class MonitorHistory(models.Model):
    monitor = models.ForeignKey('Monitor', on_delete=models.CASCADE, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE, null=True)
    installed_date = models.DateTimeField(default=timezone.now)
    removed_date = models.DateTimeField(null=True, default=None)

    class Meta:
        verbose_name = "История мониторов"
        verbose_name_plural = "История мониторов"

class Motherboard(models.Model):
    name = models.CharField(max_length=255, default='')
    model = models.ForeignKey('MotherboardModel', on_delete=models.PROTECT)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    is_updating = models.BooleanField(default=True)
    can_installing = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Материнские платы"
        verbose_name_plural = "Материнские платы"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('motherboards')

'''
Модель материнской платы
'''

class MotherboardModel(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Модели материнских плат"
        verbose_name_plural = "Модели материнских плат"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('motherboard_models')

'''
Производитель материнской платы
'''

# class MotherboardVendor(models.Model):
#     motherboard_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.motherboard_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('motherboard_vendors')
    
###############################################################################
###############################################################################
###############################################################################
    
'''
Процессор
'''

class CPU(models.Model):
    name = models.CharField(max_length=255, default='')
    model = models.ForeignKey('CPUModel', on_delete=models.PROTECT)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    frequency = models.FloatField()
    is_updating = models.BooleanField(default=True)
    can_installing = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Процессоры"
        verbose_name_plural = "Процессоры"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('cpus')

'''
Модель процессора
'''

class CPUModel(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)
    cores = models.IntegerField()
    threads = models.IntegerField()

    class Meta:
        verbose_name = "Модели процессоров"
        verbose_name_plural = "Модели процессоров"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('cpu_models')

'''
Производитель процессора
'''

# class CPUVendor(models.Model):
#     cpu_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.cpu_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('cpu_vendors')
    
###############################################################################
###############################################################################
###############################################################################

'''
Накопитель памяти
'''

class Storage(models.Model):
    serial_number = models.CharField(max_length=255, default='', primary_key=True)
    name = models.CharField(max_length=255, default='')
    model = models.ForeignKey('StorageModel', on_delete=models.PROTECT)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    is_updating = models.BooleanField(default=True)
    can_installing = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Накопители памяти"
        verbose_name_plural = "Накопители памяти"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('storages')

'''
Модель накопителя памяти
'''

class StorageModel(models.Model):
    name = models.CharField(max_length=255, default='')
    memory = models.FloatField()
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)
    type = models.ForeignKey('StorageType', on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Модели накопителей памяти"
        verbose_name_plural = "Модели накопителей памяти"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('storage_models')
    
'''
Производитель накопителя памяти
'''

# class StorageVendor(models.Model):
#     storage_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.storage_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('storage_vendors')
    
'''
Тип накопителя памяти
'''

class StorageType(models.Model):
    name = models.CharField(max_length=50, default='')

    class Meta:
        verbose_name = "Типы накопителей памяти"
        verbose_name_plural = "Типы накопителей памяти"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('storage_types')
    
###############################################################################
###############################################################################
###############################################################################
    
'''
Видеокарта
'''

class Videocard(models.Model):
    name = models.CharField(max_length=255, default='')
    model = models.ForeignKey('VideocardModel', on_delete=models.PROTECT)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    is_updating = models.BooleanField(default=True)
    can_installing = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Видеокарты"
        verbose_name_plural = "Видеокарты"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('videocards')
    
'''
Модель видеокарты
'''

class VideocardModel(models.Model):
    name = models.CharField(max_length=255, default='')
    memory = models.FloatField()
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)
    #videocard_vendors = models.ManyToManyField('Vendor', blank=True, related_name='videocardVendors')

    class Meta:
        verbose_name = "Модели видеокарт"
        verbose_name_plural = "Модели видеокарт"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('videocard_models')
    
'''
Производитель видеокарты
'''

# class VideocardVendor(models.Model):
#     videocard_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.videocard_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('videocard_vendors')
    
###############################################################################
###############################################################################
###############################################################################

'''
Оперативная память
'''

class RAM(models.Model):
    name = models.CharField(max_length=255, default='')
    frequency = models.FloatField()
    slot = models.IntegerField()
    model = models.ForeignKey('RAMModel', on_delete=models.PROTECT)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    is_updating = models.BooleanField(default=True)
    can_installing = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Оперативная память"
        verbose_name_plural = "Оперативная память"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('rams')
    
'''
Модель оперативной памяти
'''

class RAMModel(models.Model):
    name = models.CharField(max_length=255, default='')
    memory = models.FloatField(null=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)
    type = models.ForeignKey('RAMType', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Модели оперативной памяти"
        verbose_name_plural = "Модели оперативной памяти"

    #memory = models.FloatField()
    #frequency = models.FloatField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('ram_models')
    
'''
Производитель оперативной памяти
'''

# class RAMVendor(models.Model):
#     ram_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.ram_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('ram_vendors')
    
'''
Тип оперативной памяти
'''

class RAMType(models.Model):
    name = models.CharField(max_length=50, default='')

    class Meta:
        verbose_name = "Типы оперативной памяти"
        verbose_name_plural = "Типы оперативной памяти"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('ram_types')

###############################################################################
###############################################################################
###############################################################################
    
'''
Компьютер
'''

class Computer(models.Model):
    inventory_number = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, default='')
    arch = models.CharField(max_length=50, default='')
    ip = models.CharField(max_length=50, default='', null=True)
    audience = models.ForeignKey('Audience', on_delete=models.PROTECT, null=True)
    status = models.ForeignKey('TechniqueStatus', on_delete=models.PROTECT)
    technique_type = models.ForeignKey('TechniqueType', on_delete=models.PROTECT)
    update_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Компьютеры"
        verbose_name_plural = "Компьютеры"

    def __str__(self):
        return self.inventory_number
    
    def get_absolute_url(self):
        return reverse_lazy('computers')

###############################################################################
###############################################################################
###############################################################################
    
'''
Статусы техники
'''

class TechniqueStatus(models.Model):
    class Status(models.IntegerChoices):
        OK = 1, 'Исправен',
        BROKEN = 2, 'Сломан',
        DECOMMISSIONED = 3, 'Списан',

    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Статусы техники"
        verbose_name_plural = "Статусы техники"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('computer_statuses')

###############################################################################
###############################################################################
###############################################################################

class Resolution(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)
    resolution_format = models.ForeignKey('ResolutionFormat', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('resolutions')

class ResolutionFormat(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('resolution_formats')

'''
Монитор
'''

class Monitor(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=255, default='')
    inventory_number = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    resolution = models.ForeignKey('Resolution', on_delete=models.PROTECT)
    technique_type = models.ForeignKey('TechniqueType', on_delete=models.PROTECT)
    model = models.ForeignKey('MonitorModel', on_delete=models.PROTECT)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    is_updating = models.BooleanField(default=True)
    can_installing = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Мониторы"
        verbose_name_plural = "Мониторы"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('monitors')
    
'''
Модель монитора
'''
    
class MonitorModel(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Модели мониторов"
        verbose_name_plural = "Модели мониторов"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('monitor_models')
    
'''
Производитель монитора
'''

# class MonitorVendor(models.Model):
#     monitor_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.monitor_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('monitor_vendors')

###############################################################################
###############################################################################
###############################################################################

'''
Университет
'''

class University(models.Model):
    name = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=1000, default='')

    class Meta:
        verbose_name = "Университеты"
        verbose_name_plural = "Университеты"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('')

###############################################################################
###############################################################################
###############################################################################
    
'''
Корпус
'''

class UniversityBody(models.Model):
    name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=1000, default='')
    university = models.ForeignKey('University', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Корпуса"
        verbose_name_plural = "Корпуса"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('university_bodies')
    
###############################################################################
###############################################################################
###############################################################################

'''
Аудитория
'''

class Audience(models.Model):
    name = models.CharField(max_length=100, default='')
    state = models.JSONField(null=True)
    type = models.ForeignKey('AudienceType', on_delete=models.PROTECT)
    university_body = models.ForeignKey('UniversityBody', on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="home/audiences/", blank=True, null=True, verbose_name="Вид сверху")
    max_computers = models.IntegerField()
    max_places = models.IntegerField()

    class Meta:
        verbose_name = "Аудитории"
        verbose_name_plural = "Аудитории"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('audiences')
    
'''
Тип аудитории
'''

class AudienceType(models.Model):
    name = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Типы аудитории"
        verbose_name_plural = "Типы аудитории"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('audience_types')

###############################################################################
###############################################################################
###############################################################################
    
'''
Программное обеспечение
'''

class Software(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=True)
    computer = models.ManyToManyField('Computer', through="Software_Computer")
    license = models.ManyToManyField('SoftwareLicense', blank=True, related_name='SoftwareLicense')
    type = models.ForeignKey('SoftwareType', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Программное обеспечение"
        verbose_name_plural = "Программное обеспечение"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('softwares')
    
class SoftwareType(models.Model):
    name = models.CharField(max_length=255, default='')

    class Meta:
        verbose_name = "Типы программного обеспечения"
        verbose_name_plural = "Типы программного обеспечения"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('software_types')
    
class SoftwareLicense(models.Model):
    name = models.CharField(max_length=100, default='')
    activation_date = models.DateTimeField(default=None)
    expiration_date = models.DateTimeField(default=None)

    class Meta:
        verbose_name = "Лицензии программного обеспечения"
        verbose_name_plural = "Лицензии программного обеспечения"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('software_licenses')

# class SoftwareVendor(models.Model):
#     software_vendor_name = models.CharField(max_length=1000, default='')

#     def __str__(self):
#         return self.software_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('software_vendors')
    
class Software_Computer(models.Model):
    software = models.ForeignKey('Software', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
    version = models.CharField(max_length=1000, default='', null=True)
    install_date = models.DateField(null=True)
    folder = models.CharField(max_length=1000, default='', null=True)

    class Meta:
        verbose_name = "Программное обеспечение компьютеров"
        verbose_name_plural = "Программное обеспечение компьютеров"

###############################################################################
###############################################################################
###############################################################################

'''
Разделы накопителей памяти
'''

class Drive(models.Model):
    letter = models.CharField(max_length=50, default='')
    total_memory = models.FloatField()
    free_memory = models.FloatField()
    computer = models.ForeignKey('Computer', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Разделы накопителей памяти"
        verbose_name_plural = "Разделы накопителей памяти"

###############################################################################
###############################################################################
###############################################################################

'''
Тип печати
'''

class PrintType(models.Model):
    name = models.CharField(max_length=100, default='', null=False)

    class Meta:
        verbose_name = "Типы печати (принтер)"
        verbose_name_plural = "Типы печати (принтер)"

    def __str__(self):
        return self.name

'''
Цветность печати
'''

class ColorPrinting(models.Model):
    name = models.CharField(max_length=100, default='', null=False)

    class Meta:
        verbose_name = "Цветность печати (принтер)"
        verbose_name_plural = "Цветность печати (принтер)"

    def __str__(self):
        return self.name

'''
Модель принтера
'''
    
class PrinterModel(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Модели принтеров"
        verbose_name_plural = "Модели принтеров"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('printer_models')
    
'''
Производитель принтера
'''

# class PrinterVendor(models.Model):
#     printer_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.printer_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('printer_vendors')

'''
Принтер
'''

class Printer(models.Model):
    inventory_number = models.CharField(max_length=255, default='', null=False, primary_key=True)
    year_of_production = models.IntegerField()
    is_networking = models.BooleanField()
    name = models.CharField(max_length=255, default='')
    print_type = models.ForeignKey('PrintType', on_delete=models.PROTECT)
    color_printing = models.ForeignKey('ColorPrinting', on_delete=models.PROTECT)
    model = models.ForeignKey('PrinterModel', on_delete=models.PROTECT)
    technique_type = models.ForeignKey('TechniqueType', on_delete=models.PROTECT)
    audience = models.ForeignKey('Audience', on_delete=models.PROTECT, null=True)
    status = models.ForeignKey('TechniqueStatus', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Принтеры"
        verbose_name_plural = "Принтеры"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('printers')
    
###############################################################################
###############################################################################
###############################################################################
    
'''
Тип проектора
'''

class ProjectorType(models.Model):
    name = models.CharField(max_length=50, default='', null=False)

    class Meta:
        verbose_name = "Типы проекторов"
        verbose_name_plural = "Типы проекторов"

    def __str__(self):
        return self.name

'''
Модель проектора
'''
    
class ProjectorModel(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT, null=False)

    class Meta:
        verbose_name = "Модели проекторов"
        verbose_name_plural = "Модели проекторов"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('projector_models')
    
'''
Производитель проектора
'''

# class ProjectorVendor(models.Model):
#     projector_vendor_name = models.CharField(max_length=255, default='')

#     def __str__(self):
#         return self.projector_vendor_name
    
#     def get_absolute_url(self):
#         return reverse_lazy('projector_vendors')

'''
Проектор
'''

class Projector(models.Model):
    name = models.CharField(max_length=255, default='', null=False)
    inventory_number = models.CharField(max_length=255, default='', null=False, primary_key=True)
    year_of_production = models.IntegerField()
    with_remote_controller = models.BooleanField()
    type = models.ForeignKey('ProjectorType', on_delete=models.PROTECT)
    model = models.ForeignKey('ProjectorModel', on_delete=models.PROTECT)
    technique_type = models.ForeignKey('TechniqueType', on_delete=models.PROTECT)
    audience = models.ForeignKey('Audience', on_delete=models.PROTECT, null=True)
    status = models.ForeignKey('TechniqueStatus', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Проекторы"
        verbose_name_plural = "Проекторы"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('projectors')
    
'''
Тип техники
'''

class TechniqueType(models.Model):
    class Type(models.IntegerChoices):
        COMPUTER = 1, 'Компьютер',
        PROJECTOR = 2, 'Проектор',
        PRINTER = 3, 'Принтер',
        MFU = 4, 'МФУ',
        TV = 5, 'Телевизор'
        MONITOR = 6, 'Монитор'

    name = models.CharField(max_length=100, default='', null=False)

    class Meta:
        verbose_name = "Типы техники"
        verbose_name_plural = "Типы техники"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('techique_types')
    
###############################################################################
###############################################################################
###############################################################################

'''
Телевизор
'''

class TV(models.Model):
    inventory_number = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, default='')
    technique_type = models.ForeignKey('TechniqueType', on_delete=models.PROTECT)
    model = models.ForeignKey('TVModel', on_delete=models.PROTECT)
    audience = models.ForeignKey('Audience', on_delete=models.PROTECT, null=True)
    status = models.ForeignKey('TechniqueStatus', on_delete=models.PROTECT)
    diagonal = models.FloatField()
    year_of_production = models.IntegerField()

    class Meta:
        verbose_name = "Телевизоры"
        verbose_name_plural = "Телевизоры"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('tvs')

class TVModel(models.Model):
    name = models.CharField(max_length=255, default='')
    vendor = models.ForeignKey('Vendor', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Модели телевизоров"
        verbose_name_plural = "Модели телевизоров"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('tv_models')
    
###############################################################################
###############################################################################
###############################################################################
    
'''
Операционная система
'''

class OS(models.Model):
    name = models.CharField(max_length=100, default='')
    version = models.ManyToManyField('OSVersion', blank=True, related_name='OSOSVersion')

    class Meta:
        verbose_name = "Операционные системы"
        verbose_name_plural = "Операционные системы"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('os')
    
class OSVersion(models.Model):
    name = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name = "Версии операционных систем"
        verbose_name_plural = "Версии операционных систем"

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('os_versions')
    
# class OS_Computer(models.Model):
#     computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True)
#     os = models.ForeignKey('OS', on_delete=models.PROTECT)
#     license_key = models.CharField(max_length=255, default='', null=True)
#     # os_version = models.ForeignKey('OSVersion', on_delete=models.PROTECT)
#     # software = models.ForeignKey('Software', on_delete=models.PROTECT, null=True)
#     # computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)
#     # version = models.CharField(max_length=1000, default='', null=True)
#     # install_date = models.DateField(null=True)
#     # folder = models.CharField(max_length=1000, default='', null=True)

#     class Meta:
#         verbose_name = "Операционные системы компьютеров"
#         verbose_name_plural = "Операционные системы компьютеров"

class OS_Computer(models.Model):
    os = models.ForeignKey(OS, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=100, null=True)
    version = models.ForeignKey(OSVersion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Операционные системы компьютеров"
        verbose_name_plural = "Операционные системы компьютеров"