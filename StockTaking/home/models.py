from django.db import models
from django.urls import reverse_lazy

###############################################################################
###############################################################################
###############################################################################

'''
Материнская плата
'''

class Motherboard(models.Model):
    motherboard_name = models.CharField(max_length=255, default='')
    motherboardModel = models.ForeignKey('MotherboardModel', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.motherboard_name
    
    def get_absolute_url(self):
        return reverse_lazy('motherboards')

'''
Модель материнской платы
'''

class MotherboardModel(models.Model):
    motherboardModel_name = models.CharField(max_length=255, default='')
    motherboardVendor = models.ForeignKey('MotherboardVendor', on_delete=models.PROTECT, null=True)
    
    def __str__(self):
        return self.motherboardModel_name
    
    def get_absolute_url(self):
        return reverse_lazy('motherboard_models')

'''
Производитель материнской платы
'''

class MotherboardVendor(models.Model):
    motherboardVendor_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.motherboardVendor_name
    
    def get_absolute_url(self):
        return reverse_lazy('motherboard_vendors')
    
###############################################################################
###############################################################################
###############################################################################
    
'''
Процессор
'''

class CPU(models.Model):
    CPU_name = models.CharField(max_length=255, default='')
    CPU_frequency = models.FloatField()
    CPUModel = models.ForeignKey('CPUModel', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.CPU_name
    
    def get_absolute_url(self):
        return reverse_lazy('cpus')

'''
Модель процессора
'''

class CPUModel(models.Model):
    CPU_model_name = models.CharField(max_length=255, default='')
    CPUVendor = models.ForeignKey('CPUVendor', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.CPU_model_name
    
    def get_absolute_url(self):
        return reverse_lazy('cpu_models')

'''
Производитель процессора
'''

class CPUVendor(models.Model):
    CPU_vendor_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.CPU_vendor_name
    
    def get_absolute_url(self):
        return reverse_lazy('cpu_vendors')
    
###############################################################################
###############################################################################
###############################################################################

'''
Накопитель памяти
'''

class Storage(models.Model):
    storage_name = models.CharField(max_length=255, default='')
    storage_serial = models.CharField(max_length=255, default='')
    storageModel = models.ForeignKey('StorageModel', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.storage_name
    
    def get_absolute_url(self):
        return reverse_lazy('storages')

'''
Модель накопителя памяти
'''

class StorageModel(models.Model):
    storage_model_name = models.CharField(max_length=255, default='')
    storage_model_memory = models.FloatField()
    storageVendor = models.ForeignKey('StorageVendor', on_delete=models.PROTECT, null=True)
    storageType = models.ForeignKey('StorageType', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.storage_model_name
    
    def get_absolute_url(self):
        return reverse_lazy('storage_models')
    
'''
Производитель накопителя памяти
'''

class StorageVendor(models.Model):
    storage_vendor_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.storage_vendor_name
    
    def get_absolute_url(self):
        return reverse_lazy('storage_vendors')
    
'''
Тип накопителя памяти
'''

class StorageType(models.Model):
    storage_type_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.storage_type_name
    
    def get_absolute_url(self):
        return reverse_lazy('storage_types')
    
###############################################################################
###############################################################################
###############################################################################
    
'''
Видеокарта
'''

class Videocard(models.Model):
    videocard_name = models.CharField(max_length=255, default='')
    videocardModel = models.ForeignKey('VideocardModel', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.videocard_name
    
    def get_absolute_url(self):
        return reverse_lazy('videocards')
    
'''
Модель видеокарты
'''

class VideocardModel(models.Model):
    videocard_model_name = models.CharField(max_length=255, default='')
    videocard_model_memory = models.FloatField()
    #videocardVendor = models.ForeignKey('VideocardVendor', on_delete=models.PROTECT, null=True)
    videocardVendors = models.ManyToManyField('VideocardVendor', blank=True, related_name='videocardVendors')

    def __str__(self):
        return self.videocard_model_name
    
    def get_absolute_url(self):
        return reverse_lazy('videocard_models')
    
'''
Производитель видеокарты
'''

class VideocardVendor(models.Model):
    videocard_vendor_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.videocard_vendor_name
    
    def get_absolute_url(self):
        return reverse_lazy('videocard_vendors')
    
###############################################################################
###############################################################################
###############################################################################

'''
Оперативная память
'''

class RAM(models.Model):
    ram_name = models.CharField(max_length=255, default='', null=True)
    ram_memory = models.FloatField()
    ram_frequency = models.FloatField()
    ramModel = models.ForeignKey('RAMModel', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.ram_name
    
    def get_absolute_url(self):
        return reverse_lazy('rams')
    
'''
Модель оперативной памяти
'''

class RAMModel(models.Model):
    ram_model_name = models.CharField(max_length=255, default='')
    #storage_model_memory = models.FloatField()
    ramVendor = models.ForeignKey('RAMVendor', on_delete=models.PROTECT, null=True)
    ramType = models.ForeignKey('RAMType', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.ram_model_name
    
    def get_absolute_url(self):
        return reverse_lazy('ram_models')
    
'''
Производитель оперативной памяти
'''

class RAMVendor(models.Model):
    ram_vendor_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.ram_vendor_name
    
    def get_absolute_url(self):
        return reverse_lazy('ram_vendors')
    
'''
Тип оперативной памяти
'''

class RAMType(models.Model):
    ram_type_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.ram_type_name
    
    def get_absolute_url(self):
        return reverse_lazy('ram_types')

###############################################################################
###############################################################################
###############################################################################
    
'''
Компьютер
'''

class Computer(models.Model):
    computer_inventory_number = models.CharField(max_length=255, default='')
    computer_name = models.CharField(max_length=255, default='')
    computer_arch = models.CharField(max_length=255, default='')
    audience = models.ForeignKey('Audience', on_delete=models.PROTECT, null=True)

    # videocard_name = models.CharField(max_length=255, default='')
    # videocardModel = models.ForeignKey('VideocardModel', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.computer_inventory_number
    
    def get_absolute_url(self):
        return reverse_lazy('computers')

###############################################################################
###############################################################################
###############################################################################
    
'''
Монитор
'''

class Monitor(models.Model):
    monitor_inventory_number = models.CharField(max_length=255, default='')
    monitor_name = models.CharField(max_length=255, default='')
    monitor_serial_number = models.CharField(max_length=255, default='')
    monitor_resolution = models.CharField(max_length=255, default='')
    monitor_resolution_format = models.CharField(max_length=255, default='', null=True)
    monitorModel = models.ForeignKey('MonitorModel', on_delete=models.PROTECT, null=True)
    computer = models.ForeignKey('Computer', on_delete=models.PROTECT, null=True)
    
    # videocard_name = models.CharField(max_length=255, default='')
    # videocardModel = models.ForeignKey('VideocardModel', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.monitor_inventory_number
    
    def get_absolute_url(self):
        return reverse_lazy('monitors')
    
'''
Модель монитора
'''
    
class MonitorModel(models.Model):
    monitor_model_name = models.CharField(max_length=255, default='')
    monitorVendor = models.ForeignKey('MonitorVendor', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.monitor_model_name
    
    def get_absolute_url(self):
        return reverse_lazy('monitor_models')
    
'''
Производитель монитора
'''

class MonitorVendor(models.Model):
    monitor_vendor_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.monitor_vendor_name
    
    def get_absolute_url(self):
        return reverse_lazy('monitor_vendors')

###############################################################################
###############################################################################
###############################################################################

'''
Аудитория
'''

class Audience(models.Model):
    audience_name = models.CharField(max_length=255, default='')
    audience_state = models.JSONField(null=True)

    def __str__(self):
        return self.audience_name
    
    def get_absolute_url(self):
        return reverse_lazy('audiences')