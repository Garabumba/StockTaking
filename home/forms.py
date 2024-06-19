import json
from typing import Mapping
from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.files.base import File
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.forms.utils import ErrorList
from users.models import Group
from itertools import chain
import helper

from users.models import Task, TaskStatus, User, User_Task

from .models import RAM, TV, Audience, AudienceType, CPUHistory, ColorPrinting, Computer, MotherboardHistory, PrintType, ProjectorType, Resolution, ResolutionFormat, Software, SoftwareType, StorageHistory, TVModel, TechniqueStatus, Monitor, MonitorModel, Motherboard, MotherboardModel, CPU, CPUModel, Printer, PrinterModel, Projector, ProjectorModel, RAMModel, RAMType, Storage, StorageModel, StorageType, TechniqueType, University, UniversityBody, Vendor, VendorType, Videocard, VideocardModel

class AddMotherboardForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=MotherboardModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.MOTHERBOARD), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Motherboard
        fields = ['vendor', 'model', 'name', 'can_installing', 'is_updating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'can_installing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_updating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Название',
            'model': 'Модель',
            'vendor': 'Производитель',
            'can_installing': 'Может быть установлена в другой компьютер',
            'is_updating': 'Обновляется',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        if instance and instance.pk:
            self.fields['vendor'].initial = instance.model.vendor

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddMotherboardModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.MOTHERBOARD), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = MotherboardModel
        fields = ['vendor', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 50 символов")
        return name
    
class AddMotherboardVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.MOTHERBOARD)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.MOTHERBOARD)
            vendor.vendor_type.add(vendor_type)
            return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class AddCPUForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=CPUModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.CPU), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = CPU
        fields = ['vendor', 'model', 'name', 'frequency', 'can_installing', 'is_updating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'can_installing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_updating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название',
            'can_installing': 'Может быть установлен в другой компьютер',
            'is_updating': 'Обновляется',
            'frequency': 'Частота',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        if instance and instance.pk:
            self.fields['vendor'].initial = instance.model.vendor

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_frequency(self):
        frequency = self.cleaned_data['frequency']
        if frequency <= 0:
            raise ValidationError("Частота не может нулём или быть отрицательным числом")
        return frequency
    
class AddCPUModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.CPU), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = CPUModel
        fields = ['vendor', 'name', 'cores', 'threads']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cores': forms.NumberInput(attrs={'class': 'form-control'}),
            'threads': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название',
            'cores': 'Количество ядер',
            'threads': 'Количество потоков'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return name
    
    def clean_cores(self):
        cores = self.cleaned_data['cores']
        if cores <= 0:
            raise ValidationError("Количество ядер не может быть нулём или отрицательным числом")
        return cores
    
    def clean_threads(self):
        threads = self.cleaned_data['threads']
        if threads <= 0:
            raise ValidationError("Количество потоков не может быть нулём или отрицательным числом")
        return threads
    
class AddCPUVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.CPU)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.CPU)
            vendor.vendor_type.add(vendor_type)
            return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddStorageForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=StorageModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.STORAGE), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Storage
        fields = ['vendor', 'model', 'name', 'serial_number', 'can_installing', 'is_updating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'can_installing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_updating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'name': 'Название',
            'serial_number': 'Серийный номер',
            'can_installing': 'Может быть установлен в другой компьютер',
            'is_updating': 'Обновляется',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['vendor'].initial = instance.model.vendor

        if instance and instance.serial_number:
            self.fields['serial_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_serial_number(self):
        serial_number = self.cleaned_data['serial_number']
        if len(serial_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return serial_number
    
class AddStorageModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.STORAGE), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    type = forms.ModelChoiceField(queryset=StorageType.objects.all(), empty_label="Тип не выбран", label="Тип", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = StorageModel
        fields = ['vendor', 'type', 'name', 'memory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'memory': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название',
            'memory': 'Объём памяти (МБ)',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_memory(self):
        memory = self.cleaned_data['memory']
        if memory <= 0:
            raise ValidationError("Объём памяти не может быть нулём или отрицательным числом")
        return memory
    
class AddStorageVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.STORAGE)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.STORAGE)
            vendor.vendor_type.add(vendor_type)
            return super().save()
    
class AddStorageTypeForm(forms.ModelForm):
    class Meta:
        model = StorageType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddVideocardForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=VideocardModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.VIDEOCARD), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Videocard
        fields = ['vendor', 'model', 'name', 'can_installing', 'is_updating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'can_installing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_updating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'name': 'Название',
            'can_installing': 'Может быть установлена в новый компьютер',
            'is_updating': 'Обновляется'
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['vendor'].initial = instance.model.vendor

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddVideocardModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.VIDEOCARD), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = VideocardModel
        fields = ['vendor', 'name', 'memory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'memory': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название',
            'memory': 'Объём памяти (МБ)'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_memory(self):
        memory = self.cleaned_data['memory']
        if memory <= 0:
            raise ValidationError("Объём памяти не может быть нулём или отрицательным числом")
        return memory
    
class AddVideocardVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.VIDEOCARD)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.VIDEOCARD)
            vendor.vendor_type.add(vendor_type)
            return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddRAMForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=RAMModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.RAM), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = RAM
        fields = ['vendor', 'model', 'name', 'slot', 'frequency', 'can_installing', 'is_updating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slot': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'can_installing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_updating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'name': 'Название',
            'slot': 'Слот',
            'frequency': 'Частота',
            'can_installing': 'Может быть установлена в другой компьютер',
            'is_updating': 'Обновляется',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['vendor'].initial = instance.model.vendor

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_slot(self):
        slot = self.cleaned_data['slot']
        if slot <= 0:
            raise ValidationError("Слот не может быть нулём или отрицательным числом")
        return slot
    
    def clean_frequency(self):
        frequency = self.cleaned_data['frequency']
        if frequency <= 0:
            raise ValidationError("Частота не может быть нулём или отрицательным числом")
        return frequency
    
class AddRAMModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.RAM), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    type = forms.ModelChoiceField(queryset=RAMType.objects.all(), empty_label="Тип не выбран", label="Тип", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = RAMModel
        fields = ['vendor', 'type', 'name', 'memory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'memory': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название',
            'memory': 'Объём памяти (МБ)'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_memory(self):
        memory = self.cleaned_data['memory']
        if memory <= 0:
            raise ValidationError("Объём памяти не может быть нулём или отрицательным числом")
        return memory
    
class AddRAMVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.RAM)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.RAM)
            vendor.vendor_type.add(vendor_type)
            return super().save()
    
class AddRAMTypeForm(forms.ModelForm):
    class Meta:
        model = RAMType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddMonitorForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=MonitorModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.MONITOR), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    resolution = forms.ModelChoiceField(queryset=Resolution.objects.all(), empty_label="Разрешение не выбрано", label="Разрешение", widget=forms.Select(attrs={'class': 'form-control select2'}))
    #resolution_format = forms.ModelChoiceField(queryset=ResolutionFormat.objects.all(), empty_label="Соотношение сторон не выбрано", label="Соотношение сторон", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Monitor
        fields = ['vendor', 'model', 'name', 'serial_number', 'inventory_number', 'resolution', 'can_installing', 'is_updating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'resolution': forms.TextInput(attrs={'class': 'form-control'}),
            'can_installing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_updating': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'name': 'Название',
            'serial_number': 'Серийный номер',
            'inventory_number': 'Инвентарный номер',
            'resolution': 'Разрешение',
            'can_installing': 'Может быть установлен в другой компьютер',
            'is_updating': 'Обновляется',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if instance and instance.pk:
            self.fields['vendor'].initial = instance.model.vendor

        if instance and instance.serial_number:
            self.fields['serial_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Серийный номер')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_serial_number(self):
        serial_number = self.cleaned_data['serial_number']
        if len(serial_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return serial_number
    
    def clean_inventory_number(self):
        inventory_number = self.cleaned_data['inventory_number']
        if len(inventory_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return inventory_number
    
    def save(self):
        monitor = super().save(commit=False)
        monitor.technique_type_id = TechniqueType.Type.MONITOR
        return super().save()
    
    # def clean_resolution(self):
    #     resolution = self.cleaned_data['resolution']
    #     if len(resolution) > 50:
    #         raise ValidationError("Длина превышает 50 символов")
    #     return resolution
    
    # def clean_resolution_format(self):
    #     resolution_format = self.cleaned_data['resolution_format']
    #     if len(resolution_format) > 50:
    #         raise ValidationError("Длина превышает 50 символов")
    #     return resolution_format
        
class AddMonitorModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.MONITOR), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = MonitorModel
        fields = ['vendor', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddMonitorVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.MONITOR)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.MONITOR)
            vendor.vendor_type.add(vendor_type)
            return super().save()
    
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddComputerForm(forms.ModelForm):
    motherboard = forms.ModelChoiceField(queryset=Motherboard.objects.filter(computer=None), empty_label="Материнская плата не выбрана", label="Материнская плата", widget=forms.Select(attrs={'class': 'form-control select2'}))
    cpu = forms.ModelChoiceField(queryset=CPU.objects.filter(computer=None), empty_label="Процессор не выбран", label="Процессор", widget=forms.Select(attrs={'class': 'form-control select2'}))
    storages = forms.ModelMultipleChoiceField(queryset=Storage.objects.filter(computer=None), label="Накопители памяти", widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    rams = forms.ModelMultipleChoiceField(queryset=RAM.objects.filter(computer=None), label="Оперативная память", widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    videocards = forms.ModelMultipleChoiceField(queryset=Videocard.objects.filter(computer=None), label="Видеокарты", widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    monitors = forms.ModelMultipleChoiceField(queryset=Monitor.objects.filter(computer=None), label="Мониторы", widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    audience = forms.ModelChoiceField(queryset=Audience.objects.all(), empty_label="Аудитория не выбрана", label="Аудитория", required=False, widget=forms.Select(attrs={'class': 'form-control select2'}))
    status = forms.ModelChoiceField(queryset=TechniqueStatus.objects.all(), empty_label="Статус не выбран", label="Статус", required=False, widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Computer
        fields = ['inventory_number', 'name', 'arch', 'ip', 'motherboard', 'cpu', 'storages', 'rams', 'videocards', 'monitors', 'audience', 'status']
        widgets = {
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'arch': forms.TextInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'inventory_number': 'Инвентарный номер компьютера',
            'name': 'Название компьютера',
            'arch': 'Архитектура компьютера',
            'ip': 'IP',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        computer_id = kwargs.pop('computer_id', None)
        super().__init__(*args, **kwargs)
        if computer_id:
            self.fields['motherboard'].queryset = Motherboard.objects.filter(Q(computer=None) | Q(computer_id=computer_id))
            self.fields['cpu'].queryset = CPU.objects.filter(Q(computer=None) | Q(computer_id=computer_id))#(computer_id=computer_id)
            self.fields['storages'].queryset = Storage.objects.filter(Q(computer=None) | Q(computer_id=computer_id))
            self.fields['rams'].queryset = RAM.objects.filter(Q(computer=None) | Q(computer_id=computer_id))
            self.fields['videocards'].queryset = Videocard.objects.filter(computer_id=computer_id)
            self.fields['monitors'].queryset = Monitor.objects.filter(computer_id=computer_id)

        if instance and instance.inventory_number:
            self.fields['inventory_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Инвентарный номер')

    def clean_inventory_number(self):
        inventory_number = self.cleaned_data['inventory_number']
        if len(inventory_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return inventory_number
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_arch(self):
        arch = self.cleaned_data['arch']
        if len(arch) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return arch
    
    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if len(ip) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return ip
    
    def save(self):
        original_computer, old_audience = None, None
        #old_inventory_number = self.instance.__class__.objects.first().inventory_number
        if len(Computer.objects.filter(pk=self.instance.pk)) > 0:
            original_computer = self.instance.__class__.objects.get(pk=self.instance.pk)
            old_audience = original_computer.audience
        
        #if old_inventory_number != self.cleaned_data['inventory_number']:
        #    computer = None
        computer = super().save()

        #print(self.changed_data)
        #helper.update_rams(computer, original_computer.rams, self.cleaned_data['rams'])

        rams = self.cleaned_data['rams']
        for ram in rams:
           RAM.objects.filter(id=ram.id).update(computer=computer)

        videocards = self.cleaned_data['videocards']
        for videocard in videocards:
            Videocard.objects.filter(id=videocard.id).update(computer=computer)

        monitors = self.cleaned_data['monitors']
        for monitor in monitors:
            Monitor.objects.filter(inventory_number=monitor.inventory_number).update(computer=computer)

        audience = None

        if self.cleaned_data['audience']:
            audience = Audience.objects.filter(id=self.cleaned_data['audience'].id).first()
            if audience and Computer.objects.filter(audience=audience).count() > audience.max_computers:
                print('Ошибка добавления компьютера. Максимум!')
                audience = None
                computer.audience = audience
                computer.save()
        else:
            audience = old_audience
        
        if not self.cleaned_data['audience'] and audience:
            json_data = audience.state
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != computer.inventory_number]
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != original_computer.inventory_number]
            audience.state = json_data
            audience.save()
            return computer

        if audience and audience.state:
            helper.update_technique_image(audience, computer.inventory_number, self.cleaned_data['status'], TechniqueType.Type.COMPUTER)
            # json_data = audience.state
            # print(json_data)
            # for figure in json_data['objects']:
            #     if figure.get('figureId') == computer.inventory_number:
            #         figure['statusId'] = self.cleaned_data['status'].id

            #         if self.cleaned_data['status'].id == 1:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "pc.png"
            #             figure['src'] = '/'.join(picture)
            #         elif self.cleaned_data['status'].id == 2:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "broken_pc.png"
            #             figure['src'] = '/'.join(picture)

            #         break
            
            # audience.state = json_data
            # audience.save()

        return computer
        return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
'''
Университет
'''

class AddUniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название университета',
            'url': 'Ссылка на официальный сайт университета',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_url(self):
        url = self.cleaned_data['url']
        if len(url) > 1000:
            raise ValidationError("Длина превышает 1000 символов")
        return url
    
'''
Задача
'''

class AddTaskForm(forms.ModelForm):
    #users = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(group_id__in=Group.objects.filter(is_responsible=True).values('id')), label='Ответственные', required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    #status = forms.ModelChoiceField(queryset=TaskStatus.objects.all(), label='Статус задачи', empty_label='Статус не выбран', widget=forms.Select(attrs={'class': 'form-control select2'}))
    technique_status = forms.ModelChoiceField(queryset=TechniqueStatus.objects.all(), label='Статус техники', empty_label='Статус техники не выбран', widget=forms.Select(attrs={'class': 'form-control select2'}))

    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance', None)
    #     super().__init__(*args, **kwargs)

    #     if instance and instance.pk:
    #         self.fields['vendor'].initial = instance.model.vendor

    #     if instance and instance.serial_number:
    #         self.fields['serial_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Серийный номер')

    class Meta:
        model = Task
        fields = ['title', 'message', 'technique_status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок задачи',
            'message': 'Сообщение',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        all_inventory_numbers = list(chain(Computer.objects.values_list('inventory_number', flat=True), Printer.objects.values_list('inventory_number', flat=True), Projector.objects.values_list('inventory_number', flat=True), TV.objects.values_list('inventory_number', flat=True), Monitor.objects.values_list('inventory_number', flat=True)))
        
        #if not self.user.is_superuser:
        #    self.fields['users'] = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(group_id__in=Group.objects.filter(is_responsible=True).values('id')), label='', required=False, widget=forms.HiddenInput())

        result = tuple((value, value) for value in all_inventory_numbers)
        
        #if self.user.group.is_responsible:
        #    self.fields['status'] = forms.ModelChoiceField(queryset=TaskStatus.objects.all(), label='Статус задачи', empty_label='Статус не выбран', widget=forms.Select(attrs={'class': 'form-control select2'}))
        if self.user.is_superuser:
            self.fields['users'] = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(group_id__in=Group.objects.filter(is_responsible=True).values('id')), label='Ответственные', required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
        
        self.fields['inventory_number'] = forms.ChoiceField(label='Инвентарный номер', choices=result, widget=forms.Select(attrs={'class': 'form-control select2'}))
        if instance and instance.pk:
            self.fields['status'] = forms.ModelChoiceField(queryset=TaskStatus.objects.all(), label='Статус задачи', empty_label='Статус не выбран', widget=forms.Select(attrs={'class': 'form-control select2'}))
            if self.user.is_superuser:
                self.fields['users'] = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(group_id__in=Group.objects.filter(is_responsible=True).values('id')), label='Ответственные', required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

            if instance.computer:
                self.fields['inventory_number'].initial = instance.computer
            if instance.printer:
                self.fields['inventory_number'].initial = instance.printer
            if instance.projector:
                self.fields['inventory_number'].initial = instance.projector
            if instance.tv:
                self.fields['inventory_number'].initial = instance.tv
            if instance.monitor:
                self.fields['inventory_number'].initial = instance.monitor

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) > 500:
            raise ValidationError("Длина превышает 500 символов")
        return message
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if instance.id:
            instance.status = self.cleaned_data['status']
        else:
            instance.status_id = TaskStatus.Status.IN_PROGRESS

        if commit:
            technique = helper.get_technique_by_inventory_number(self.cleaned_data['inventory_number'])
            technique.status = self.cleaned_data['technique_status']
            technique.save()

            if technique.technique_type.id == TechniqueType.Type.COMPUTER:
                instance.computer = technique
                instance.save()
                users = technique.UsersComputers.all()
                try:
                    selected_users = self.cleaned_data['users']
                except:
                    selected_users = []
                helper.create_or_update_user_task(users, selected_users, instance, self.cleaned_data['inventory_number'], self.user)
                if instance.computer.audience:
                    helper.update_technique_image(instance.computer.audience, instance.computer.inventory_number, self.cleaned_data['technique_status'], technique.technique_type.id)

                return instance
            
            if technique.technique_type.id == TechniqueType.Type.PROJECTOR:
                instance.projector = technique
                instance.save()
                users = technique.UsersProjectors.all()
                try:
                    selected_users = self.cleaned_data['users']
                except:
                    selected_users = []
                helper.create_or_update_user_task(users, selected_users, instance, self.cleaned_data['inventory_number'], self.user)
                if instance.projector.audience:
                    helper.update_technique_image(instance.projector.audience, instance.projector.inventory_number, self.cleaned_data['technique_status'], technique.technique_type.id)

                return instance
            
            if technique.technique_type.id == TechniqueType.Type.PRINTER or technique.technique_type.id == TechniqueType.Type.MFU:
                instance.printer = technique
                instance.save()
                users = technique.UsersPrinters.all()
                try:
                    selected_users = self.cleaned_data['users']
                except:
                    selected_users = []
                helper.create_or_update_user_task(users, selected_users, instance, self.cleaned_data['inventory_number'], self.user)
                if instance.printer.audience:
                    helper.update_technique_image(instance.printer.audience, instance.printer.inventory_number, self.cleaned_data['technique_status'], technique.technique_type.id)

                return instance
            
            if technique.technique_type.id == TechniqueType.Type.TV:
                instance.tv = technique
                instance.save()
                users = technique.UsersTVs.all()
                try:
                    selected_users = self.cleaned_data['users']
                except:
                    selected_users = []
                helper.create_or_update_user_task(users, selected_users, instance, self.cleaned_data['inventory_number'], self.user)
                if instance.computer.audience:
                    helper.update_technique_image(instance.tv.audience, instance.tv.inventory_number, self.cleaned_data['technique_status'], technique.technique_type.id)

                return instance
            
            if technique.technique_type.id == TechniqueType.Type.MONITOR:
                instance.monitor = technique
                instance.save()
                users = technique.UsersMonitors.all()
                selected_users = self.cleaned_data['users']
                helper.create_or_update_user_task(users, selected_users, instance, self.cleaned_data['inventory_number'], self.user)
                # if len(users) == 0:
                #     helper.create_user_task(self.cleaned_data['users'], instance, self.cleaned_data['inventory_number'], self.user)
                #     return instance

                # helper.create_user_task(users, instance, self.cleaned_data['inventory_number'], self.user)
                return instance
            
        return instance

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddPrinterForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=PrinterModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.PRINTER), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    audience = forms.ModelChoiceField(queryset=Audience.objects.all(), empty_label="Аудитория не выбрана", label="Аудитория", required=False, widget=forms.Select(attrs={'class': 'form-control select2'}))
    print_type = forms.ModelChoiceField(queryset=PrintType.objects.all(), empty_label="Тип печати не выбран", label="Тип печати", widget=forms.Select(attrs={'class': 'form-control select2'}))
    color_printing = forms.ModelChoiceField(queryset=ColorPrinting.objects.all(), empty_label="Цветность печати не выбрана", label="Цветность печати", widget=forms.Select(attrs={'class': 'form-control select2'}))
    status = forms.ModelChoiceField(queryset=TechniqueStatus.objects.all(), empty_label="Статус не выбран", label="Статус", widget=forms.Select(attrs={'class': 'form-control select2'}))
    technique_type = forms.ModelChoiceField(queryset=TechniqueType.objects.filter(Q(id=TechniqueType.Type.PRINTER) | Q(id=TechniqueType.Type.MFU)), empty_label="Тип не выбран", label="Тип", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Printer
        fields = ['vendor', 'model', 'name', 'inventory_number', 'year_of_production', 'is_networking', 'print_type', 'color_printing', 'audience', 'status', 'technique_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_production': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_networking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'name': 'Имя принтера',
            'inventory_number': 'Инвентарный номер принтера',
            'year_of_production': 'Год производства',
            'is_networking': 'Сетевой',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(AddPrinterForm, self).__init__(*args, **kwargs)

        if instance and instance.inventory_number:
            self.fields['inventory_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Инвентарный номер')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_inventory_number(self):
        inventory_number = self.cleaned_data['inventory_number']
        if len(inventory_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return inventory_number
    
    def clean_year_of_production(self):
        year_of_production = self.cleaned_data['year_of_production']
        if year_of_production <= 0:
            raise ValidationError("Год производства не может быть нулём или отрицательным числом")
        return year_of_production
    
    def save(self):
        original_printer, old_audience = None, None
        #old_inventory_number = self.instance.__class__.objects.first().inventory_number
        if len(Printer.objects.filter(pk=self.instance.pk)) > 0:
            original_printer = self.instance.__class__.objects.get(pk=self.instance.pk)
            old_audience = original_printer.audience
        
        printer = super().save()

        audience = None

        if self.cleaned_data['audience']:
            audience = Audience.objects.filter(id=self.cleaned_data['audience'].id).first()
        else:
            audience = old_audience
        
        if not self.cleaned_data['audience'] and audience:
            json_data = audience.state
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != printer.inventory_number]
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != original_printer.inventory_number]
            audience.state = json_data
            audience.save()
            return printer

        if audience and audience.state:
            helper.update_technique_image(audience, printer.inventory_number, self.cleaned_data['status'], TechniqueType.Type.PRINTER)
            # json_data = audience.state
            # print(json_data)
            # for figure in json_data['objects']:
            #     if figure.get('figureId') == printer.inventory_number:
            #         figure['statusId'] = self.cleaned_data['status'].id

            #         if self.cleaned_data['status'].id == 1:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "printer.png"
            #             figure['src'] = '/'.join(picture)
            #         elif self.cleaned_data['status'].id == 2:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "broken_printer.png"
            #             figure['src'] = '/'.join(picture)

            #         break
            
            # audience.state = json_data
            # audience.save()

        return printer
    
class AddPrinterModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.PRINTER), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = PrinterModel
        fields = ['vendor', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddPrinterVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.PRINTER)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.PRINTER)
            vendor.vendor_type.add(vendor_type)
            return super().save()
    
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddProjectorForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=ProjectorModel.objects.all(), empty_label="Модель не выбрана", label="Модель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.PROJECTOR), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))
    audience = forms.ModelChoiceField(queryset=Audience.objects.all(), empty_label="Аудитория не выбрана", label="Аудитория", required=False, widget=forms.Select(attrs={'class': 'form-control select2'}))
    type = forms.ModelChoiceField(queryset=ProjectorType.objects.all(), empty_label="Тип не выбран", label="Тип", widget=forms.Select(attrs={'class': 'form-control select2'}))
    status = forms.ModelChoiceField(queryset=TechniqueStatus.objects.all(), empty_label="Статус не выбран", label="Статус", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Projector
        fields = ['vendor', 'model', 'name', 'inventory_number', 'year_of_production', 'with_remote_controller', 'type', 'audience', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_production': forms.NumberInput(attrs={'class': 'form-control'}),
            'with_remote_controller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'name': 'Название',
            'inventory_number': 'Инвентарный номер',
            'year_of_production': 'Год производства',
            'with_remote_controller': 'С пультом',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(AddProjectorForm, self).__init__(*args, **kwargs)

        if instance and instance.inventory_number:
            self.fields['inventory_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Инвентарный номер')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_inventory_number(self):
        inventory_number = self.cleaned_data['inventory_number']
        if len(inventory_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return inventory_number
    
    def clean_year_of_production(self):
        year_of_production = self.cleaned_data['year_of_production']
        if year_of_production <= 0:
            raise ValidationError("Год производства не может быть нулём или отрицательным числом")
        return year_of_production
    
    def save(self):
        original_projector, old_audience = None, None
        #old_inventory_number = self.instance.__class__.objects.first().inventory_number
        if len(Projector.objects.filter(pk=self.instance.pk)) > 0:
            original_projector = self.instance.__class__.objects.get(pk=self.instance.pk)
            old_audience = original_projector.audience
        
        projector = super().save(commit=False)
        projector.technique_type_id = TechniqueType.Type.PROJECTOR
        projector.save()

        audience = None

        if self.cleaned_data['audience']:
            audience = Audience.objects.filter(id=self.cleaned_data['audience'].id).first()
        else:
            audience = old_audience
        
        if not self.cleaned_data['audience'] and audience:
            json_data = audience.state
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != projector.inventory_number]
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != original_projector.inventory_number]
            audience.state = json_data
            audience.save()
            return projector

        if audience and audience.state:
            helper.update_technique_image(audience, projector.inventory_number, self.cleaned_data['status'], TechniqueType.Type.PROJECTOR)
            # json_data = audience.state
            # print(json_data)
            # for figure in json_data['objects']:
            #     if figure.get('figureId') == projector.inventory_number:
            #         figure['statusId'] = self.cleaned_data['status'].id

            #         if self.cleaned_data['status'].id == 1:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "projector.png"
            #             figure['src'] = '/'.join(picture)
            #         elif self.cleaned_data['status'].id == 2:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "broken_projector.png"
            #             figure['src'] = '/'.join(picture)

            #         break
            
            # audience.state = json_data
            # audience.save()

        return projector
    
class AddProjectorModelForm(forms.ModelForm):
    #vendor = forms.ModelChoiceField(queryset=ProjectorVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.PROJECTOR), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = ProjectorModel
        fields = ['name', 'vendor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddProjectorVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.PROJECTOR)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.PROJECTOR)
            vendor.vendor_type.add(vendor_type)
            return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class AddAudienceForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=AudienceType.objects.all(), empty_label='Тип не выбран', label='Тип', widget=forms.Select(attrs={'class': 'form-control select2'}))
    university_body = forms.ModelChoiceField(queryset=UniversityBody.objects.all(), empty_label='Корпус не выбран', label='Корпус', widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Audience
        fields = ['name', 'type', 'university_body', 'max_computers', 'max_places', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'max_computers': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_places': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'previewPhoto()'})
        }
        labels = {
            'name': 'Название аудитории',
            'max_computers': 'Максимальное количество комьютеров',
            'max_places': 'Вместимость (чел)'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return name
    
    def clean_max_computers(self):
        max_computers = self.cleaned_data['max_computers']
        if max_computers < 0:
            raise ValidationError("Максимальное количество комьютеров не может быть отрицательным числом")
        return max_computers
    
    def clean_max_places(self):
        max_places = self.cleaned_data['max_places']
        if max_places <= 0:
            raise ValidationError("Максимальная вместимость не может быть нулём или отрицательным числом")
        return max_places
    
    def save(self):
        instance = super().save(commit=False)

        if not instance.id:
            state = {
                "objects": [],
                "version": "5.2.1"
                }
            
            instance.state = state

        return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
'''
Корпус
'''

class AddUniversityBodyForm(forms.ModelForm):
    class Meta:
        model = UniversityBody
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название корпуса',
            'address': 'Адрес корпуса',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if len(address) > 1000:
            raise ValidationError("Длина превышает 1000 символов")
        return address
    
    def save(self):
        university_body = super().save(commit=False)
        university_body.university = University.objects.first()
        return super().save()

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
'''
Телевизор
'''

class AddTVForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset=TVModel.objects.all(), empty_label='Модель не выбрана', label='Модель', widget=forms.Select(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type=VendorType.Type.TV), empty_label='Производитель не выбран', label='Производитель', widget=forms.Select(attrs={'class': 'form-control select2'}))
    audience = forms.ModelChoiceField(queryset=Audience.objects.all(), empty_label='Аудитория не выбрана', label='Аудитория', widget=forms.Select(attrs={'class': 'form-control select2'}), required=False)
    status = forms.ModelChoiceField(queryset=TechniqueStatus.objects.all(), empty_label='Статус не выбран', label='Статус', widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = TV
        fields = ['vendor', 'model', 'inventory_number', 'name', 'diagonal', 'year_of_production', 'audience', 'status']
        widgets = {
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'diagonal': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_of_production': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'inventory_number': 'Инвентарный номер',
            'name': 'Название',
            'diagonal': 'Диагональ',
            'year_of_production': 'Год производства'
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(AddTVForm, self).__init__(*args, **kwargs)

        if instance and instance.inventory_number:
            self.fields['inventory_number'] = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Инвентарный номер')

    def clean_inventory_number(self):
        inventory_number = self.cleaned_data['inventory_number']
        if len(inventory_number) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return inventory_number
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name

    def clean_diagonal(self):
        diagonal = self.cleaned_data['diagonal']
        if diagonal <= 0:
            raise ValidationError("Диагональ не может быть нулём или отрицательным числом")
        return diagonal  
    
    def save(self):
        original_tv, old_audience = None, None
        #old_inventory_number = self.instance.__class__.objects.first().inventory_number
        if len(TV.objects.filter(pk=self.instance.pk)) > 0:
            original_tv = self.instance.__class__.objects.get(pk=self.instance.pk)
            old_audience = original_tv.audience
        
        tv = super().save(commit=False)
        tv.technique_type_id = TechniqueType.Type.TV
        tv.save()

        audience = None

        if self.cleaned_data['audience']:
            audience = Audience.objects.filter(id=self.cleaned_data['audience'].id).first()
        else:
            audience = old_audience
        
        if not self.cleaned_data['audience'] and audience:
            json_data = audience.state
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != tv.inventory_number]
            json_data['objects'] = [item for item in json_data['objects'] if item.get('figureId') != original_tv.inventory_number]
            audience.state = json_data
            audience.save()
            return tv

        if audience and audience.state:
            helper.update_technique_image(audience, tv.inventory_number, self.cleaned_data['status'], TechniqueType.Type.TV)
            # json_data = audience.state
            # print(json_data)
            # for figure in json_data['objects']:
            #     if figure.get('figureId') == tv.inventory_number:
            #         figure['statusId'] = self.cleaned_data['status'].id

            #         if self.cleaned_data['status'].id == 1:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "tv.png"
            #             figure['src'] = '/'.join(picture)
            #         elif self.cleaned_data['status'].id == 2:
            #             picture = figure['src'].split('/')
            #             picture[len(picture) - 1] = "broken_tv.png"
            #             figure['src'] = '/'.join(picture)

            #         break
            
            # audience.state = json_data
            # audience.save()

        return tv

class AddTVModelForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.TV), empty_label="Производитель не выбран", label="Производитель", widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = TVModel
        fields = ['name', 'vendor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddTVVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.TV)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.TV)
            vendor.vendor_type.add(vendor_type)
            return super().save()
    
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

'''
Программное обеспечение
'''

class AddSoftwareForm(forms.ModelForm):
    computer = forms.ModelMultipleChoiceField(queryset=Computer.objects.all(), label='Компьютеры', required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type__id=VendorType.Type.SOFTWARE), label='Издатель', empty_label='Издатель не выбран', widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = Software
        fields = ['vendor', 'name', 'computer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название программного обеспечения',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddSoftwareVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
    def save(self):
        vendor_type = VendorType.objects.get(id=VendorType.Type.SOFTWARE)
        try:
            vendor = Vendor.objects.get(name=self.cleaned_data['name'])
            if vendor_type not in vendor.vendor_type.all():
                vendor.vendor_type.add(vendor_type)
                vendor.save()
                return vendor
        except ObjectDoesNotExist:
            vendor = super().save()
            vendor_type = VendorType.objects.get(id=VendorType.Type.SOFTWARE)
            vendor.vendor_type.add(vendor_type)
            return super().save()

class AddAudienceTypeForm(forms.ModelForm):
    class Meta:
        model = AudienceType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name
    
class AddResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return name
    
class AddResolutionFormatForm(forms.ModelForm):
    resolution_format = forms.ModelChoiceField(queryset=ResolutionFormat.objects.all(), label='Соотношение сторон', empty_label='Соотношение сторон не выбрано', widget=forms.Select(attrs={'class': 'form-control select2'}))
    
    class Meta:
        model = ResolutionFormat
        fields = ['name', 'resolution_format']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Название'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return name
    
class AddSoftwareTypeForm(forms.ModelForm):
    class Meta:
        model = SoftwareType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 255:
            raise ValidationError("Длина превышает 255 символов")
        return name