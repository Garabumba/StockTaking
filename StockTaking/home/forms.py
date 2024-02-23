from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .models import RAM, Monitor, MonitorModel, MonitorVendor, Motherboard, MotherboardModel, MotherboardVendor, CPU, CPUModel, CPUVendor, RAMModel, RAMType, RAMVendor, Storage, StorageModel, StorageType, StorageVendor, Videocard, VideocardModel, VideocardVendor

class AddMotherboardForm(forms.ModelForm):
    motherboardModel = forms.ModelChoiceField(queryset=MotherboardModel.objects.all(), empty_label="Модель не выбрана", label="Модель")#, disabled=True)
    motherboardVendor = forms.ModelChoiceField(queryset=MotherboardVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = Motherboard
        fields = ['motherboard_name', 'motherboardModel', 'motherboardVendor']
        widgets = {
            'motherboard_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_motherboard_name(self):
        motherboard_name = self.cleaned_data['motherboard_name']
        if len(motherboard_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return motherboard_name
    
class AddMotherboardModelForm(forms.ModelForm):
    motherboardVendor = forms.ModelChoiceField(queryset=MotherboardVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = MotherboardModel
        fields = ['motherboardModel_name', 'motherboardVendor']
        widgets = {
            'motherboardModel_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_motherboardModel_name(self):
        motherboardModel_name = self.cleaned_data['motherboardModel_name']
        if len(motherboardModel_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return motherboardModel_name
    
class AddMotherboardVendorForm(forms.ModelForm):
    class Meta:
        model = MotherboardVendor
        fields = ['motherboardVendor_name']
        widgets = {
            'motherboardVendor_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_motherboardVendor_name(self):
        motherboardVendor_name = self.cleaned_data['motherboardVendor_name']
        if len(motherboardVendor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return motherboardVendor_name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class AddCPUForm(forms.ModelForm):
    CPUModel = forms.ModelChoiceField(queryset=CPUModel.objects.all(), empty_label="Модель не выбрана", label="Модель")
    CPUVendor = forms.ModelChoiceField(queryset=CPUVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = CPU
        fields = ['CPU_name', 'CPU_frequency', 'CPUModel', 'CPUVendor']
        widgets = {
            'CPU_name': forms.TextInput(attrs={'class': 'form-input'}),
            'CPU_frequency': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean_cpu_name(self):
        CPU_name = self.cleaned_data['CPU_name']
        if len(CPU_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return CPU_name
    
class AddCPUModelForm(forms.ModelForm):
    CPUVendor = forms.ModelChoiceField(queryset=CPUVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = CPUModel
        fields = ['CPU_model_name', 'CPUVendor']
        widgets = {
            'CPU_model_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_CPU_model_name(self):
        CPU_model_name = self.cleaned_data['CPU_model_name']
        if len(CPU_model_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return CPU_model_name
    
class AddCPUVendorForm(forms.ModelForm):
    class Meta:
        model = CPUVendor
        fields = ['CPU_vendor_name']
        widgets = {
            'CPU_vendor_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_CPU_vendor_name(self):
        CPU_vendor_name = self.cleaned_data['CPU_vendor_name']
        if len(CPU_vendor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return CPU_vendor_name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddStorageForm(forms.ModelForm):
    storageModel = forms.ModelChoiceField(queryset=StorageModel.objects.all(), empty_label="Модель не выбрана", label="Модель")
    storageVendor = forms.ModelChoiceField(queryset=StorageVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = Storage
        fields = ['storage_name', 'storage_serial', 'storageModel', 'storageVendor']
        widgets = {
            'storage_name': forms.TextInput(attrs={'class': 'form-input'}),
            'storage_serial': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_storage_name(self):
        storage_name = self.cleaned_data['storage_name']
        if len(storage_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return storage_name
    
    def clean_storage_serial(self):
        storage_serial = self.cleaned_data['storage_serial']
        if len(storage_serial) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return storage_serial
    
class AddStorageModelForm(forms.ModelForm):
    storageVendor = forms.ModelChoiceField(queryset=StorageVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")
    storageType = forms.ModelChoiceField(queryset=StorageType.objects.all(), empty_label="Тип не выбран", label="Тип")

    class Meta:
        model = StorageModel
        fields = ['storage_model_name', 'storage_model_memory', 'storageVendor', 'storageType']
        widgets = {
            'storage_model_name': forms.TextInput(attrs={'class': 'form-input'}),
            'storage_model_memory': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean_storage_model_name(self):
        storage_model_name = self.cleaned_data['storage_model_name']
        if len(storage_model_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return storage_model_name
    
class AddStorageVendorForm(forms.ModelForm):
    class Meta:
        model = StorageVendor
        fields = ['storage_vendor_name']
        widgets = {
            'storage_vendor_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_storage_vendor_name(self):
        storage_vendor_name = self.cleaned_data['storage_vendor_name']
        if len(storage_vendor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return storage_vendor_name
    
class AddStorageTypeForm(forms.ModelForm):
    class Meta:
        model = StorageType
        fields = ['storage_type_name']
        widgets = {
            'storage_type_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_storage_type_name(self):
        storage_type_name = self.cleaned_data['storage_type_name']
        if len(storage_type_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return storage_type_name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddVideocardForm(forms.ModelForm):
    videocardModel = forms.ModelChoiceField(queryset=VideocardModel.objects.all(), empty_label="Модель не выбрана", label="Модель")
    videocardVendor = forms.ModelChoiceField(queryset=VideocardVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = Videocard
        fields = ['videocard_name', 'videocardModel', 'videocardVendor']
        widgets = {
            'videocard_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_videocard_name(self):
        videocard_name = self.cleaned_data['videocard_name']
        if len(videocard_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return videocard_name
    
class AddVideocardModelForm(forms.ModelForm):
    videocardVendors = forms.ModelChoiceField(queryset=VideocardVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = VideocardModel
        fields = ['videocard_model_name', 'videocard_model_memory', 'videocardVendors']
        widgets = {
            'videocard_model_name': forms.TextInput(attrs={'class': 'form-input'}),
            'videocard_model_memory': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean_videocard_model_name(self):
        videocard_model_name = self.cleaned_data['videocard_model_name']
        if len(videocard_model_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return videocard_model_name
    
class AddVideocardVendorForm(forms.ModelForm):
    class Meta:
        model = VideocardVendor
        fields = ['videocard_vendor_name']
        widgets = {
            'videocard_vendor_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_videocard_vendor_name(self):
        videocard_vendor_name = self.cleaned_data['videocard_vendor_name']
        if len(videocard_vendor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return videocard_vendor_name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddRAMForm(forms.ModelForm):
    ramModel = forms.ModelChoiceField(queryset=RAMModel.objects.all(), empty_label="Модель не выбрана", label="Модель")
    ramVendor = forms.ModelChoiceField(queryset=RAMVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = RAM
        fields = ['ram_name', 'ram_memory', 'ram_frequency', 'ramModel', 'ramVendor']
        widgets = {
            'ram_name': forms.TextInput(attrs={'class': 'form-input'}),
            'ram_memory': forms.NumberInput(attrs={'class': 'form-input'}),
            'ram_frequency': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def clean_ram_name(self):
        ram_name = self.cleaned_data['ram_name']
        if len(ram_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return ram_name
    
class AddRAMModelForm(forms.ModelForm):
    ramVendor = forms.ModelChoiceField(queryset=RAMVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")
    ramType = forms.ModelChoiceField(queryset=RAMType.objects.all(), empty_label="Тип не выбран", label="Тип")

    class Meta:
        model = RAMModel
        fields = ['ram_model_name', 'ramVendor', 'ramType']
        widgets = {
            'ram_model_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_ram_model_name(self):
        ram_model_name = self.cleaned_data['ram_model_name']
        if len(ram_model_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return ram_model_name
    
class AddRAMVendorForm(forms.ModelForm):
    class Meta:
        model = RAMVendor
        fields = ['ram_vendor_name']
        widgets = {
            'ram_vendor_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_ram_vendor_name(self):
        ram_vendor_name = self.cleaned_data['ram_vendor_name']
        if len(ram_vendor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return ram_vendor_name
    
class AddRAMTypeForm(forms.ModelForm):
    class Meta:
        model = RAMType
        fields = ['ram_type_name']
        widgets = {
            'ram_type_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_ram_type_name(self):
        ram_type_name = self.cleaned_data['ram_type_name']
        if len(ram_type_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return ram_type_name

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
    
class AddMonitorForm(forms.ModelForm):
    monitorModel = forms.ModelChoiceField(queryset=MonitorModel.objects.all(), empty_label="Модель не выбрана", label="Модель")
    monitorVendor = forms.ModelChoiceField(queryset=MonitorVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = Monitor
        fields = ['monitor_name', 'monitor_serial_number', 'monitor_resolution', 'monitor_resolution_format', 'monitorModel', 'monitorVendor']
        widgets = {
            'monitor_name': forms.TextInput(attrs={'class': 'form-input'}),
            'monitor_serial_number': forms.TextInput(attrs={'class': 'form-input'}),
            'monitor_resolution': forms.TextInput(attrs={'class': 'form-input'}),
            'monitor_resolution_format': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_monitor_name(self):
        monitor_name = self.cleaned_data['monitor_name']
        if len(monitor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return monitor_name
    
    def clean_monitor_serial_number(self):
        monitor_serial_number = self.cleaned_data['monitor_serial_number']
        if len(monitor_serial_number) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return monitor_serial_number
    
    def clean_monitor_resolution(self):
        monitor_resolution = self.cleaned_data['monitor_resolution']
        if len(monitor_resolution) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return monitor_resolution
    
    def clean_monitor_resolution_format(self):
        monitor_resolution_format = self.cleaned_data['monitor_resolution_format']
        if len(monitor_resolution_format) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return monitor_resolution_format
    
class AddMonitorModelForm(forms.ModelForm):
    monitorVendor = forms.ModelChoiceField(queryset=MonitorVendor.objects.all(), empty_label="Производитель не выбран", label="Производитель")

    class Meta:
        model = MonitorModel
        fields = ['monitor_model_name', 'monitorVendor']
        widgets = {
            'monitor_model_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_monitor_model_name(self):
        monitor_model_name = self.cleaned_data['monitor_model_name']
        if len(monitor_model_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return monitor_model_name
    
class AddMonitorVendorForm(forms.ModelForm):
    class Meta:
        model = MonitorVendor
        fields = ['monitor_vendor_name']
        widgets = {
            'monitor_vendor_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_monitor_vendor_name(self):
        monitor_vendor_name = self.cleaned_data['monitor_vendor_name']
        if len(monitor_vendor_name) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return monitor_vendor_name

class UploadFileForm(forms.Form):
    file = forms.FileField()