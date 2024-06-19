from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from StockTaking import settings
from django.db.models import Q
from users.models import Group, Task, TaskStatus, User_Task
from .models import CPU, OS, RAM, TV, Audience, AudienceType, CPUHistory, CPUModel, ColorPrinting, Computer, Drive, Monitor, MonitorHistory, MonitorModel, Motherboard, MotherboardHistory, MotherboardModel, OS_Computer, PrintType, Printer, PrinterModel, Projector, ProjectorModel, ProjectorType, RAMHistory, RAMModel, RAMType, Resolution, ResolutionFormat, Software, Software_Computer, SoftwareType, Storage, StorageHistory, StorageModel, StorageType, TVModel, TechniqueStatus, TechniqueType, University, UniversityBody, Vendor, VendorType, Videocard, VideocardHistory, VideocardModel
from django.views.generic import ListView, CreateView, UpdateView
from .forms import AddAudienceForm, AddAudienceTypeForm, AddCPUForm, AddCPUModelForm, AddCPUVendorForm, AddComputerForm, AddMonitorForm, AddMonitorModelForm, AddMonitorVendorForm, AddMotherboardForm, AddMotherboardModelForm, AddMotherboardVendorForm, AddPrinterForm, AddPrinterModelForm, AddPrinterVendorForm, AddProjectorForm, AddProjectorModelForm, AddProjectorVendorForm, AddRAMForm, AddRAMModelForm, AddRAMTypeForm, AddRAMVendorForm, AddResolutionForm, AddResolutionFormatForm, AddSoftwareForm, AddSoftwareTypeForm, AddSoftwareVendorForm, AddStorageForm, AddStorageModelForm, AddStorageTypeForm, AddStorageVendorForm, AddTVForm, AddTVModelForm, AddTVVendorForm, AddTaskForm, AddUniversityBodyForm, AddUniversityForm, AddVideocardForm, AddVideocardModelForm, AddVideocardVendorForm
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
import helper
from django.contrib.auth import get_user_model


def index(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    context = {
        'default_image': settings.DEFAULT_USER_IMAGE,
        'user': request.user
    }

    return render(request, 'home/index.html', context)

def linked_technique(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')

    queryset = list(chain(request.user.computers.all(), request.user.monitors.all(), request.user.printers.all(), request.user.projectors.all(), request.user.tvs.all()))

    selected_name = request.GET.get('name', '')
    selected_inventory_number = request.GET.get('inventory_number', '')
    selected_technique_type = request.GET.get('type', '')
    selected_audience = request.GET.get('audience', '')

    
    
    try:
        technique_type_id = int(selected_technique_type)
        technique_type_value = TechniqueType.objects.get(id=technique_type_id).name
    except:
        technique_type_value = 0

    try:
        audience_id = int(selected_audience)
        audience_value = Audience.objects.get(id=audience_id).name
    except:
        audience_value = 0

    def apply_filters(item):
        if selected_name and item.name != selected_name:
            return False
        if selected_inventory_number and item.inventory_number != selected_inventory_number:
            return False
        if selected_technique_type:
            try:
                if item.technique_type_id != int(selected_technique_type):
                    return False
            except:
                return False
        if selected_audience:
            try:
                if item.audience_id != int(selected_audience):
                    return False
            except:
                return False
        return True

    filtered_queryset = [item for item in queryset if apply_filters(item)]

    context = {
        'names': list(chain(request.user.computers.values_list('name', flat=True), request.user.monitors.values_list('name', flat=True), request.user.printers.values_list('name', flat=True), request.user.projectors.values_list('name', flat=True), request.user.tvs.values_list('name', flat=True))),
        'inventory_numbers': list(chain(request.user.computers.values_list('inventory_number', flat=True), request.user.monitors.values_list('inventory_number', flat=True), request.user.printers.values_list('inventory_number', flat=True), request.user.projectors.values_list('inventory_number', flat=True), request.user.tvs.values_list('inventory_number', flat=True))),
        'types': TechniqueType.objects.all(),
        'audiences': Audience.objects.all(),
        'selected_name': selected_name,
        'selected_inventory_number': selected_inventory_number,
        'selected_type': selected_technique_type,
        'selected_audience': selected_audience,
        'technique': filtered_queryset,
        'default_image': settings.DEFAULT_USER_IMAGE,
        'user': request.user,
        'title': 'Моя техника',
        'all_filters': [
            {
                'name': 'Название',
                'value': selected_name,
                'type': 'name'
            },
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number,
                'type': 'inventory_number'
            },
            {
                'name': 'Тип',
                'value': technique_type_value if technique_type_value else selected_technique_type,
                'type': 'type'
            },
            {
                'name': 'Аудитория',
                'value': audience_value if audience_value else selected_audience,
                'type': 'audience'
            },
        ]
    }

    return render(request, 'home/linked_technique.html', context)

'''
Мат. платы
'''

class GetMotherboards(PermissionRequiredMixin, ListView):
    model = Motherboard
    template_name = 'home/motherboard/motherboards.html'
    context_object_name = 'motherboards'
    title_page = 'Материнские платы'
    permission_required = 'home.view_motherboard'
    paginate_by = 10

    def get_queryset(self):
        queryset = Motherboard.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = queryset.filter(model__vendor_id=vendor)

        if model:
            try:
                model = int(model)
            except:
                return []
            queryset = queryset.filter(model_id=model)

        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        motherboard_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.MOTHERBOARD).all()
        motherboard_models = MotherboardModel.objects.all()
        selected_name = self.request.GET.get('name', '')
        selected_vendor = self.request.GET.get('vendor', '')
        selected_model = self.request.GET.get('model', '')
        selected_is_updating = self.request.GET.get('is_updating', '')
        selected_can_installing = self.request.GET.get('can_installing', '')

        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = motherboard_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        try:
            selected_model_id = int(selected_model)
            try:
                model_value = motherboard_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model

        context['names'] = set(Motherboard.objects.values_list('name', flat=True))
        context['vendors'] = motherboard_vendors
        context['models'] = motherboard_models
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_is_updating'] = selected_is_updating
        context['selected_can_installing'] = selected_can_installing
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлена',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

class AddMotherboard(PermissionRequiredMixin, CreateView):
    model = Motherboard
    form_class = AddMotherboardForm
    template_name = "home/motherboard/addmotherboard.html"
    title_page = 'Создание материнской платы'
    permission_required = 'home.add_motherboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateMotherboard(PermissionRequiredMixin, UpdateView):
    model = Motherboard
    form_class = AddMotherboardForm
    template_name = 'home/motherboard/addmotherboard.html'
    title_page = 'Редактирование материнской платы'
    permission_required = 'home.change_motherboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели мат. плат
'''

class GetMotherboardModels(PermissionRequiredMixin, ListView):
    model = MotherboardModel
    template_name = 'home/motherboard/motherboard_models.html'
    context_object_name = 'motherboard_models'
    title_page = 'Модели материнских плат'
    permission_required = 'home.view_motherboardmodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        motherboard_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.MOTHERBOARD).all()
        selected_vendor = self.request.GET.get('vendor', '')
        selected_name = self.request.GET.get('name', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = motherboard_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(MotherboardModel.objects.values_list('name', flat=True))
        context['vendors'] = motherboard_vendors
        context['selected_vendor'] = selected_vendor
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor'
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        
        return context

    def get_queryset(self):
        queryset = MotherboardModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)
        
        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = queryset.filter(vendor_id=vendor)

        return queryset

class AddMotherboardModel(PermissionRequiredMixin, CreateView):
    model = MotherboardModel
    form_class = AddMotherboardModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели материнской платы'
    permission_required = 'home.add_motherboardmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateMotherboardModel(PermissionRequiredMixin, UpdateView):
    model = MotherboardModel
    form_class = AddMotherboardModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели материнской платы'
    permission_required = 'home.change_motherboardmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители мат. плат
'''

class GetMotherboardVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/motherboard/motherboard_vendors.html'
    context_object_name = 'motherboard_vendors'
    title_page = 'Производители материнских плат'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = Vendor.objects.filter(vendor_type__id=VendorType.Type.MOTHERBOARD)
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.MOTHERBOARD)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddMotherboardVendor(PermissionRequiredMixin, CreateView):
    form_class = AddMotherboardVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя материнской платы'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateMotherboardVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddMotherboardVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя материнской платы'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Процессоры
'''

class GetCPUs(PermissionRequiredMixin, ListView):
    template_name = 'home/cpu/cpus.html'
    context_object_name = 'cpus'
    title_page = 'Процессоры'
    permission_required = 'home.view_cpu'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = CPU.objects.all()
        cpu_vendors = Vendor.objects.filter(vendor_type__id=VendorType.Type.CPU)
        cpu_models = CPUModel.objects.all()

        cores_value = 0
        threads_value = 0
        frequency_value = 0
        
        selected_name = self.request.GET.get('name', '')

        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = cpu_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_model = self.request.GET.get('model', '')
        try:
            selected_model_id = int(selected_model)
            try:
                model_value = cpu_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model
        
        selected_cores = self.request.GET.get('cores', '')
        try:
            selected_cores_id = int(selected_cores)
        except:
            cores_value = selected_cores

        selected_threads = self.request.GET.get('threads', '')
        try:
            selected_threads_id = int(selected_threads)
        except:
            threads_value = selected_threads

        selected_frequency = self.request.GET.get('frequency', '')
        try:
            selected_frequency_id = float(selected_frequency.replace(',', '.'))
        except:
            frequency_value = selected_frequency

        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(CPU.objects.values_list('name', flat=True))
        context['vendors'] = cpu_vendors
        context['models'] = cpu_models
        context['cores'] = set(CPUModel.objects.values_list('cores', flat=True))
        context['threads'] = set(CPUModel.objects.values_list('threads', flat=True))
        context['frequencies'] = set(CPU.objects.values_list('frequency', flat=True))
        context['selected_name'] = selected_name
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_cores'] = selected_cores
        context['selected_threads'] = selected_threads
        context['selected_frequency'] = selected_frequency
        context['selected_is_updating'] = self.request.GET.get('is_updating', '')
        context['selected_can_installing'] = self.request.GET.get('can_installing', '')
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model',
            }, 
            {
                'name': 'Ядра',
                'value': selected_cores if cores_value == 0 else cores_value,
                'type': 'cores', 
            },
            {
                'name': 'Потоки', 
                'value': selected_threads if threads_value == 0 else threads_value,
                'type': 'threads', 
            },
            {
                'name': 'Частота', 
                'value': selected_frequency if frequency_value == 0 else frequency_value,
                'type': 'frequency', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлен',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]

        return context

    def get_queryset(self):
        queryset = CPU.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        frequency = self.request.GET.get('frequency', '')
        cores = self.request.GET.get('cores', '')
        threads = self.request.GET.get('threads', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(model__vendor_id=vendor)
            except:
                return []
            
        if model:
            try:
                model = int(model)
                queryset = queryset.filter(model_id=model)
            except:
                return []
            
        if frequency:
            try:
                frequency = float(frequency.replace(',', '.'))
                queryset = queryset.filter(frequency=frequency)
            except:
                return []
            
        if cores:
            try:
                cores = int(cores)
                queryset = queryset.filter(cores=cores)
            except:
                return []
            
        if threads:
            try:
                threads = int(threads)
                queryset = queryset.filter(threads=threads)
            except:
                return []
            
        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset

class AddCPU(PermissionRequiredMixin, CreateView):
    form_class = AddCPUForm
    template_name = "home/cpu/addcpu.html"
    title_page = 'Создание процессора'
    permission_required = 'home.add_cpu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateCPU(PermissionRequiredMixin, UpdateView):
    model = CPU
    form_class = AddCPUForm
    template_name = 'home/cpu/addcpu.html'
    title_page = 'Редактирование процессора'
    permission_required = 'home.change_cpu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели процессоров
'''

class GetCPUModels(PermissionRequiredMixin, ListView):
    template_name = 'home/cpu/cpu_models.html'
    context_object_name = 'cpu_models'
    title_page = 'Модели процессоров'
    permission_required = 'home.view_cpumodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        cpu_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.CPU)
        cores_value = 0
        threads_value = 0
        selected_name = self.request.GET.get('name', '')

        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = cpu_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor
        
        selected_cores = self.request.GET.get('cores', '')
        try:
            selected_cores_id = int(selected_cores)
        except:
            cores_value = selected_cores

        selected_threads = self.request.GET.get('threads', '')
        try:
            selected_threads_id = int(selected_threads)
        except:
            threads_value = selected_threads

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(CPUModel.objects.values_list('name', flat=True))
        context['vendors'] = cpu_vendors
        context['cores'] = set(CPUModel.objects.values_list('cores', flat=True))
        context['threads'] = set(CPUModel.objects.values_list('threads', flat=True))
        context['selected_vendor'] = selected_vendor
        context['selected_cores'] = selected_cores
        context['selected_threads'] = self.request.GET.get('threads', '')
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Ядра',
                'value': selected_cores if cores_value == 0 else cores_value,
                'type': 'cores', 
            },
            {
                'name': 'Потоки', 
                'value': selected_threads if threads_value == 0 else threads_value,
                'type': 'threads', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = CPUModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        cores = self.request.GET.get('cores', '')
        threads = self.request.GET.get('threads', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(vendor_id=vendor)
            except:
                return []

        if cores:
            try:
                cores = int(cores)
                queryset = queryset.filter(cores=cores)
            except:
                return []
        
        if threads:
            try:
                threads = int(threads)
                queryset = queryset.filter(threads=threads)
            except:            
                return []

        return queryset

class AddCPUModel(PermissionRequiredMixin, CreateView):
    form_class = AddCPUModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели процессора'
    permission_required = 'home.add_cpumodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateCPUModel(PermissionRequiredMixin, UpdateView):
    model = CPUModel
    form_class = AddCPUModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели процессора'
    permission_required = 'home.change_cpumodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители процессоров
'''

class GetCPUVendors(PermissionRequiredMixin, ListView):
    template_name = 'home/cpu/cpu_vendors.html'
    context_object_name = 'cpu_vendors'
    title_page = 'Производители процессоров'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        selected_name = self.request.GET.get('name', '')
        context['names'] = Vendor.objects.filter(vendor_type__id=VendorType.Type.CPU).values_list('name', flat=True)
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.CPU)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)
        
        return queryset

class AddCPUVendor(PermissionRequiredMixin, CreateView):
    form_class = AddCPUVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя процессора'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateCPUVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddCPUVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя процессора'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

def get_models(request, vendor_id):
    if vendor_id == 0:
        models = MotherboardModel.objects.none()
    else:
        models = MotherboardModel.objects.filter(motherboard_vendor_id=vendor_id)
    model_list = list(models.values('id', 'motherboard_model_name'))
    return JsonResponse(model_list, safe=False)

'''
Накопители памяти
'''

class GetStorages(PermissionRequiredMixin, ListView):
    template_name = 'home/storage/storages.html'
    context_object_name = 'storages'
    title_page = 'Накопители памяти'
    permission_required = 'home.view_storage'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        storage_vendors = Vendor.objects.filter(vendor_type__id=VendorType.Type.STORAGE)
        storage_models = StorageModel.objects.all()
        types = StorageType.objects.all()
        selected_name = self.request.GET.get('name', '')

        type_value = 0
        serial_number_value = 0
        
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = storage_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_model = self.request.GET.get('model', '')
        try:
            selected_model_id = int(selected_model)
            try:
                model_value = storage_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model
        
        selected_type = self.request.GET.get('type', '')
        try:
            selected_type_id = int(selected_type)
        except:
            type_value = selected_type

        selected_serial_number = self.request.GET.get('serial_number', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Storage.objects.values_list('name', flat=True))
        context['vendors'] = storage_vendors
        context['models'] = storage_models
        context['types'] = types
        context['serial_numbers'] = Storage.objects.values_list('serial_number', flat=True)
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_type'] = selected_type
        context['selected_serial_number'] = selected_serial_number
        context['selected_is_updating'] = self.request.GET.get('is_updating', '')
        context['selected_can_installing'] = self.request.GET.get('can_installing', '')
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model',
            }, 
            {
                'name': 'Тип',
                'value': type_value,
                'type': 'type', 
            },
            {
                'name': 'Серийный номер', 
                'value': selected_serial_number,
                'type': 'serial_number', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлен',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Storage.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        storage_type = self.request.GET.get('type', '')
        serial_number = self.request.GET.get('serial_number', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(model__vendor_id=vendor)
            except:
                return []
            
        if model:
            try:
                model = int(model)
                queryset = queryset.filter(model_id=model)
            except:
                return []
        
        if storage_type:
            try:
                storage_type = int(storage_type)
                queryset = queryset.filter(model__type_id=storage_type)
            except:
                return []
            
        if serial_number:
            queryset = queryset.filter(serial_number=serial_number)

        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset

class AddStorage(PermissionRequiredMixin, CreateView):
    form_class = AddStorageForm
    template_name = "home/storage/addstorage.html"
    title_page = 'Создание накопителя памяти'
    permission_required = 'home.add_storage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateStorage(PermissionRequiredMixin, UpdateView):
    model = Storage
    form_class = AddStorageForm
    template_name = 'home/storage/addstorage.html'
    title_page = 'Редактирование накопителя памяти'
    permission_required = 'home.change_storage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели накопителей памяти
'''

class GetStorageModels(PermissionRequiredMixin, ListView):
    template_name = 'home/storage/storage_models.html'
    context_object_name = 'storage_models'
    title_page = 'Модели накопителей памяти'
    permission_required = 'home.view_storagemodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        storage_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.STORAGE)
        storage_types = StorageType.objects.all()
        selected_name = self.request.GET.get('name', '')
        
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = storage_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_type = self.request.GET.get('type', '')
        try:
            selected_type_id = int(selected_type)
            try:
                type_value = storage_types.get(id=selected_type_id).name
            except ObjectDoesNotExist:
                type_value = selected_type
        except:
            type_value = selected_type

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(StorageModel.objects.values_list('name', flat=True))
        context['vendors'] = storage_vendors
        context['types'] = storage_types
        context['selected_vendor'] = selected_vendor
        context['selected_type'] = selected_type
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Тип',
                'value': type_value,
                'type': 'type', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = StorageModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        type = self.request.GET.get('type', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(vendor_id=vendor)
            except:
                return []
            
        if type:
            try:
                type = int(type)
                queryset = queryset.filter(type_id=type)
            except:
                return []
    
        return queryset
    

class AddStorageModel(PermissionRequiredMixin, CreateView):
    form_class = AddStorageModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание накопителя памяти'
    permission_required = 'home.add_storagemodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateStorageModel(PermissionRequiredMixin, UpdateView):
    model = StorageModel
    form_class = AddStorageModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование накопителя памяти'
    permission_required = 'home.change_storagemodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
'''
Производители накопителей памяти
'''

class GetStorageVendors(PermissionRequiredMixin, ListView):
    template_name = 'home/storage/storage_vendors.html'
    context_object_name = 'storage_vendors'
    title_page = 'Производители накопителей памяти'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.STORAGE).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.STORAGE)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddStorageVendor(PermissionRequiredMixin, CreateView):
    form_class = AddStorageVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя накопителя памяти'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateStorageVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddStorageVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя накопителя памяти'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Типы накопителей памяти
'''

class GetStorageTypes(PermissionRequiredMixin, ListView):
    template_name = 'home/storage/storage_types.html'
    context_object_name = 'storage_types'
    title_page = 'Типы накопителей памяти'
    permission_required = 'home.view_storagetype'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(StorageType.objects.values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = StorageType.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddStorageType(PermissionRequiredMixin, CreateView):
    form_class = AddStorageTypeForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание типа накопителя памяти'
    permission_required = 'home.add_storagetype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateStorageType(PermissionRequiredMixin, UpdateView):
    model = StorageType
    form_class = AddStorageTypeForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование типа накопителя памяти'
    permission_required = 'home.change_storagetype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Видеокарты
'''

class GetVideocards(PermissionRequiredMixin, ListView):
    template_name = 'home/videocard/videocards.html'
    context_object_name = 'videocards'
    title_page = 'Видеокарты'
    permission_required = 'home.view_videocard'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        videocard_vendors = Vendor.objects.filter(vendor_type__id=VendorType.Type.VIDEOCARD)
        videocard_models = VideocardModel.objects.all()
        selected_name = self.request.GET.get('name', '')
        
        memory_value = 0
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = videocard_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_model = self.request.GET.get('model', '')
        try:
            selected_model_id = int(selected_model)
            try:
                model_value = videocard_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model
        
        selected_memory = self.request.GET.get('memory', '')
        try:
            selected_memory_id = int(selected_memory)
        except:
            memory_value = selected_memory
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Videocard.objects.values_list('name', flat=True))
        context['vendors'] = videocard_vendors
        context['models'] = videocard_models
        context['memories'] = set(VideocardModel.objects.values_list('memory', flat=True))
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_memory'] = selected_memory
        context['selected_is_updating'] = self.request.GET.get('is_updating', '')
        context['selected_can_installing'] = self.request.GET.get('can_installing', '')
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model',
            }, 
            {
                'name': 'Обёъм памяти',
                'value': selected_memory if memory_value == 0 else memory_value,
                'type': 'memory', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлен',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Videocard.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        memory = self.request.GET.get('memory', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(model__vendor_id=vendor)
            except:
                return []
            
        if model:
            try:
                model = int(model)
                queryset = queryset.filter(model_id=model)
            except:
                return []
            
        if memory:
            try:
                memory = float(memory.replace(',', '.'))
                queryset = queryset.filter(model__memory=memory)
            except:
                return []
            
        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset

class AddVideocard(PermissionRequiredMixin, CreateView):
    form_class = AddVideocardForm
    template_name = "home/videocard/addvideocard.html"
    title_page = 'Создание видеокарты'
    permission_required = 'home.add_videocard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateVideocard(PermissionRequiredMixin, UpdateView):
    model = Videocard
    form_class = AddVideocardForm
    template_name = 'home/videocard/addvideocard.html'
    title_page = 'Редактирование видеокарты'
    permission_required = 'home.change_videocard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели видеокарт
'''

class GetVideocardModels(PermissionRequiredMixin, ListView):
    template_name = 'home/videocard/videocard_models.html'
    context_object_name = 'videocard_models'
    title_page = 'Модели видеокарт'
    permission_required = 'home.view_videocardmodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        videocard_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.VIDEOCARD)
        memory_value = 0
        
        selected_name = self.request.GET.get('name', '')
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = videocard_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_memory = self.request.GET.get('memory', '')
        try:
            selected_memory_id = float(selected_memory.replace(',', '.'))
        except:
            memory_value = selected_memory
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(VideocardModel.objects.values_list('name', flat=True))
        context['vendors'] = videocard_vendors
        context['memories'] = set(VideocardModel.objects.values_list('memory', flat=True))
        context['selected_vendor'] = selected_vendor
        context['selected_memory'] = selected_memory
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            },
            {
                'name': 'Объём памяти',
                'value': memory_value if memory_value else selected_memory,
                'type': 'memory', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = VideocardModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        memory = self.request.GET.get('memory', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(vendor_id=vendor)
            except:
                return []
            
        if memory:
            try:
                memory = float(memory.replace(',', '.'))
                queryset = queryset.filter(memory=memory)
            except:
                return []
    
        return queryset

class AddVideocardModel(PermissionRequiredMixin, CreateView):
    form_class = AddVideocardModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели видеокарты'
    permission_required = 'home.add_videocardmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateVideocardModel(PermissionRequiredMixin, UpdateView):
    model = VideocardModel
    form_class = AddVideocardModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели видеокарты'
    permission_required = 'home.change_videocardmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители видеокарт
'''

class GetVideocardVendors(PermissionRequiredMixin, ListView):
    template_name = 'home/videocard/videocard_vendors.html'
    context_object_name = 'videocard_vendors'
    title_page = 'Производители видеокарт'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.VIDEOCARD).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.VIDEOCARD)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddVideocardVendor(PermissionRequiredMixin, CreateView):
    form_class = AddVideocardVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя видеокарты'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateVideocardVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddVideocardVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя видеокарты'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
'''
Компьютеры
'''

class GetComputers(LoginRequiredMixin, ListView):
    template_name = 'home/computer/computers.html'
    context_object_name = 'computers'
    title_page = 'Компьютеры'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        statuses = TechniqueStatus.objects.all()
        audiences = Audience.objects.all()
        inventory_numbers = Computer.objects.values_list('inventory_number', flat=True)
        selected_status = self.request.GET.get('status', '')
        selected_ip = self.request.GET.get('ip', '')
        selected_arch = self.request.GET.get('arch', '')
        selected_audience = self.request.GET.get('audience', '')
        selected_inventory_number = self.request.GET.get('inventory_number', '')
        selected_name = self.request.GET.get('name', '')

        ip_value = ''
        arch_value = ''

        try:
            selected_status_id = int(selected_status)
            try:
                status_value = statuses.get(id=int(selected_status_id)).name
            except ObjectDoesNotExist:
                status_value = selected_status
        except:
            status_value = selected_status

        try:
            selected_ip_id = int(selected_ip)
        except:
            ip_value = selected_ip

        try:
            selected_arch_id = int(selected_arch)
        except:
            arch_value = selected_arch

        try:
            selected_audience_id = int(selected_audience)
            try:
                audience_value = audiences.get(id=int(selected_audience_id)).name
            except ObjectDoesNotExist:
                audience_value = selected_audience
        except:
            audience_value = selected_audience

        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Computer.objects.values_list('name', flat=True))
        context['inventory_numbers'] = inventory_numbers
        context['statuses'] = statuses
        context['ips'] = Computer.objects.values_list('ip', flat=True)
        context['archs'] = Computer.objects.values_list('arch', flat=True)
        context['audiences'] = audiences
        context['selected_inventory_number'] = selected_inventory_number
        context['selected_status'] = selected_status
        context['selected_ip'] = selected_ip
        context['selected_arch'] = selected_arch
        context['selected_audience'] = selected_audience
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number,
                'type': 'inventory_number', 
            },
            {
                'name': 'Статус',
                'value': status_value,
                'type': 'status', 
            },
            {
                'name': 'ip',
                'value': ip_value if ip_value else selected_ip,
                'type': 'ip', 
            },
            {
                'name': 'Архитектура',
                'value': arch_value if arch_value else selected_arch,
                'type': 'arch', 
            },
            {
                'name': 'Аудитория',
                'value': audience_value,
                'type': 'audience', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Computer.objects.all()
        vendor = self.request.GET.get('vendor', '')
        status = self.request.GET.get('status', '')
        arch = self.request.GET.get('arch', '')
        audience = self.request.GET.get('audience', '')
        ip = self.request.GET.get('ip', '')
        inventory_number = self.request.GET.get('inventory_number', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if inventory_number:
            queryset = queryset.filter(inventory_number=inventory_number)

        # if vendor:
        #     try:
        #         vendor = int(vendor)
        #     except:
        #         return []
        #     queryset = queryset.filter(model__vendor_id=vendor)

        if status:
            try:
                status = int(status)
            except:
                return []
            queryset = queryset.filter(status_id=status)

        if ip:
            queryset = queryset.filter(ip=ip)

        if arch:
            queryset = queryset.filter(arch=arch)

        if audience:
            try:
                audience = int(audience)
            except:
                return []
            queryset = queryset.filter(audience_id=audience)

        return queryset
    
class AddComputer(PermissionRequiredMixin, CreateView):
    model = Computer
    form_class = AddComputerForm
    template_name = "home/computer/addcomputer.html"
    title_page = 'Создание компьютера'
    permission_required = 'home.add_computer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context
    
class UpdateComputer(PermissionRequiredMixin, UpdateView):
    model = Computer
    form_class = AddComputerForm
    template_name = "home/computer/addcomputer.html"
    title_page = 'Редактирование компьютера'
    permission_required = 'home.change_computer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(UpdateComputer, self).get_form_kwargs()
        kwargs['computer_id'] = self.kwargs['pk']
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        computer = self.get_object()
        initial['motherboard'] = computer.motherboard_set.first()
        initial['cpu'] = computer.cpu_set.first()
        initial['storages'] = computer.storage_set.all()
        initial['rams'] = computer.ram_set.all()
        initial['videocards'] = computer.videocard_set.all()
        initial['monitors'] = computer.monitor_set.all()

        return initial
    
    def form_valid(self, form):
        response = super().form_valid(form)
        computer = self.object
        new_motherboard = form.cleaned_data.get('motherboard')
        new_cpu = form.cleaned_data.get('cpu')
        new_storages = form.cleaned_data.get('storages')
        new_rams = form.cleaned_data.get('rams')
        new_videocards = form.cleaned_data.get('videocards')
        new_monitors = form.cleaned_data.get('monitors')

        helper.update_motherboard(computer, computer.motherboard_set.first(), new_motherboard)
        helper.update_cpu(computer, computer.cpu_set.first(), new_cpu)
        helper.update_storages(computer, computer.storage_set.all(), new_storages)
        helper.update_rams(computer, computer.ram_set.all(), new_rams)
        helper.update_videocards(computer, computer.videocard_set.all(), new_videocards)
        helper.update_monitors(computer, computer.monitor_set.all(), new_monitors)         

        return response

'''
Аудитории
'''

class AddAudience(PermissionRequiredMixin, CreateView):
    model = Audience
    form_class = AddAudienceForm
    template_name = "home/audience/addaudience.html"
    title_page = 'Создание аудитории'
    permission_required = 'home.add_audience'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context
    
class UpdateAudience(PermissionRequiredMixin, UpdateView):
    model = Audience
    form_class = AddAudienceForm
    template_name = "home/audience/addaudience.html"
    title_page = 'Редактирование аудитории'
    permission_required = 'home.change_audience'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

class GetAudiences(PermissionRequiredMixin, ListView):
    template_name = 'home/audience/audiences.html'
    context_object_name = 'audiences'
    title_page = 'Аудитории'
    permission_required = 'home.view_audience'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        university_bodies = UniversityBody.objects.all()
        audience_types = AudienceType.objects.all()

        selected_university_body = self.request.GET.get('university_body', '')
        selected_audience_type = self.request.GET.get('type', '')
        selected_max_computers = self.request.GET.get('max_computers', '')
        selected_max_places = self.request.GET.get('max_places', '')
        selected_name = self.request.GET.get('name', '')

        max_computers_value = 0
        max_places_value = 0

        try:
            selected_university_body_id = int(selected_university_body)
            try:
                university_body_value = university_bodies.get(id=selected_university_body_id).name
            except ObjectDoesNotExist:
                university_body_value = selected_university_body
        except:
            university_body_value = selected_university_body

        try:
            selected_audience_type_id = int(selected_audience_type)
            try:
                audience_type_value = audience_types.get(id=int(selected_audience_type_id)).name
            except ObjectDoesNotExist:
                audience_type_value = selected_audience_type
        except:
            audience_type_value = selected_audience_type

        try:
            selected_max_computers_id = int(selected_max_computers)
        except:
            max_computers_value = selected_max_computers

        try:
            selected_max_places_id = int(selected_max_places)
        except:
            max_places_value = selected_max_places

        context['university_bodies'] = university_bodies
        context['audience_types'] = audience_types
        context['max_computers_list'] = set(Audience.objects.values_list('max_computers', flat=True))
        context['max_places_list'] = set(Audience.objects.values_list('max_places', flat=True))
        context['types'] = audience_types
        context['title'] = self.title_page
        context['names'] = set(Audience.objects.values_list('name', flat=True))
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['selected_university_body'] = selected_university_body
        context['selected_audience_type'] = selected_audience_type
        context['selected_max_computers'] = selected_max_computers
        context['selected_max_places'] = selected_max_places
        context['selected_type'] = selected_audience_type
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Корпус',
                'value': university_body_value,
                'type': 'university_body',
            }, 
            {
                'name': 'Тип',
                'value': audience_type_value,
                'type': 'type', 
            },
            {
                'name': 'Макс. кол-во компьютеров',
                'value': max_computers_value if max_computers_value else selected_max_computers, 
                'type': 'max_computers', 
            },
            {
                'name': 'Вместимость',
                'value': max_places_value if max_places_value else selected_max_places, 
                'type': 'max_places', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Audience.objects.all()
        university_body = self.request.GET.get('university_body', '')
        audience_type = self.request.GET.get('type', '')
        max_computers = self.request.GET.get('max_computers', '')
        max_places = self.request.GET.get('max_places', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if university_body:
            try:
                university_body = int(university_body)
            except:
                return []
            queryset = queryset.filter(university_body_id=university_body)

        if audience_type:
            try:
                audience_type = int(audience_type)
            except:
                return []
            queryset = queryset.filter(type_id=audience_type)

        if max_computers:
            try:
                max_computers = int(max_computers)
            except:
                return []
            queryset = queryset.filter(max_computers=max_computers)

        if max_places:
            try:
                max_places = int(max_places)
            except:
                return []
            queryset = queryset.filter(max_places=max_places)

        return queryset

class GetAudience(PermissionRequiredMixin, ListView):
    template_name = 'home/audience/audience.html'
    context_object_name = 'audience'
    title_page = 'Аудитория'
    permission_required = 'home.view_audience'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        audience_id = self.kwargs['pk']
        audience = Audience.objects.get(pk=audience_id)
        computers = Computer.objects.filter(audience_id=audience_id)
        printers = Printer.objects.filter(audience_id=audience_id)
        projectors = Projector.objects.filter(audience_id=audience_id)
        tvs = TV.objects.filter(audience_id=audience_id)
        
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['audience'] = audience
        context['technique'] = list(chain(computers, printers, projectors, tvs))
        context['technique_types'] = TechniqueType.objects.all()
                
        return context

    def get_queryset(self):
        queryset = Audience.objects.filter(id=self.kwargs['pk']).first()
    
class GetComputer(PermissionRequiredMixin, ListView):
    template_name = 'home/computer/computer.html'
    context_object_name = 'computer'
    title_page = 'Компьютер'
    permission_required = 'home.view_computer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        computer = Computer.objects.filter(inventory_number=self.kwargs['pk']).first()
        storage_models = Storage.objects.filter(computer=computer).values('model_id')
        
        try:
            total_storage_memory = round(StorageModel.objects.filter(id__in=storage_models).aggregate(Sum('memory'))['memory__sum'] / 1024, 2)
        except:
            total_storage_memory = 0

        try:
            ram_memory = int(round(RAMModel.objects.filter(ram__in=RAM.objects.filter(computer=computer)).aggregate(Sum('memory'))['memory__sum'] / 1024, 0))
        except:
            ram_memory = 0

        context['computer'] = computer
        context['cpu'] = CPU.objects.filter(computer=computer).first()
        context['motherboard'] = Motherboard.objects.filter(computer=computer).first()
        context['monitors'] = Monitor.objects.filter(computer=computer)
        context['rams'] = RAM.objects.filter(computer=computer)
        context['storages'] = Storage.objects.filter(computer=computer)
        context['videocards'] = Videocard.objects.filter(computer=computer)
        context['total_storage_memory'] = total_storage_memory
        context['ram_memory'] = ram_memory
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['softwares'] = Software_Computer.objects.filter(computer=computer)
        context['drives'] = Drive.objects.filter(computer=computer)
        context['old_motherboards'] = MotherboardHistory.objects.filter(computer=computer)
        context['old_cpus'] = CPUHistory.objects.filter(computer=computer)
        context['old_rams'] = RAMHistory.objects.filter(computer=computer)
        context['old_storages'] = StorageHistory.objects.filter(computer=computer)
        context['old_videocards'] = VideocardHistory.objects.filter(computer=computer)
        context['old_monitors'] = MonitorHistory.objects.filter(computer=computer)
        context['oss'] = OS_Computer.objects.filter(computer=computer)
        return context

    def get_queryset(self):
        return Computer.objects.filter(inventory_number=self.kwargs['pk']).first()

'''
Оперативная память
'''

class GetRAMs(PermissionRequiredMixin, ListView):
    template_name = 'home/ram/rams.html'
    context_object_name = 'rams'
    title_page = 'Оперативная память'
    permission_required = 'home.view_ram'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        queryset = RAM.objects.all()
        ram_vendors = Vendor.objects.filter(vendor_type__id=VendorType.Type.RAM)
        ram_models = RAMModel.objects.all()
        ram_types = RAMType.objects.all()
        selected_name = self.request.GET.get('name', '')

        memory_value = 0
        frequency_value = 0
        
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = ram_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_model = self.request.GET.get('model', '')
        try:
            selected_model_id = int(selected_model)
            try:
                model_value = ram_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model
        
        selected_memory = self.request.GET.get('memory', '')
        try:
            selected_memory_id = int(selected_memory)
        except:
            memory_value = selected_memory

        selected_type = self.request.GET.get('type', '')
        try:
            selected_type_id = int(selected_type)
            try:
                type_value = ram_types.get(id=int(selected_type_id)).name
            except ObjectDoesNotExist:
                type_value = selected_type
        except:
            type_value = selected_type

        selected_frequency = self.request.GET.get('frequency', '')
        try:
            selected_frequency_id = float(selected_frequency.replace(',', '.'))
        except:
            frequency_value = selected_frequency


        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(RAM.objects.values_list('name', flat=True))
        context['vendors'] = ram_vendors
        context['models'] = ram_models
        context['memories'] = set(RAMModel.objects.values_list('memory', flat=True))
        context['types'] = ram_types
        context['frequencies'] = set(RAM.objects.values_list('frequency', flat=True))
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_memory'] = selected_memory
        context['selected_type'] = selected_type
        context['selected_frequency'] = selected_frequency
        context['selected_is_updating'] = self.request.GET.get('is_updating', '')
        context['selected_can_installing'] = self.request.GET.get('can_installing', '')
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model',
            }, 
            {
                'name': 'Обёъм памяти',
                'value': selected_memory if memory_value == 0 else memory_value,
                'type': 'memory', 
            },
            {
                'name': 'Тип', 
                'value': type_value,
                'type': 'type', 
            },
            {
                'name': 'Частота', 
                'value': selected_frequency if frequency_value == 0 else frequency_value,
                'type': 'frequency', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлен',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = RAM.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        frequency = self.request.GET.get('frequency', '')
        memory = self.request.GET.get('memory', '')
        ram_type = self.request.GET.get('type', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(model__vendor_id=vendor)
            except:
                return []
            
        if model:
            try:
                model = int(model)
                queryset = queryset.filter(model_id=model)
            except:
                return []
            
        if ram_type:
            try:
                ram_type = int(ram_type)
                queryset = queryset.filter(model__type_id=ram_type)
            except:
                return []
            
        if frequency:
            try:
                frequency = float(frequency.replace(',', '.'))
                queryset = queryset.filter(frequency=frequency)
            except:
                return []
            
        if memory:
            try:
                memory = float(memory.replace(',', '.'))
                queryset = queryset.filter(model__memory=memory)
            except:
                return []
            
        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset

class AddRAM(PermissionRequiredMixin, CreateView):
    form_class = AddRAMForm
    template_name = "home/ram/addram.html"
    title_page = 'Создание оперативной памяти'
    permission_required = 'home.add_ram'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateRAM(PermissionRequiredMixin, UpdateView):
    model = RAM
    form_class = AddRAMForm
    template_name = 'home/ram/addram.html'
    title_page = 'Редактирование оперативной памяти'
    permission_required = 'home.change_ram'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели оперативной памяти
'''

class GetRAMModels(PermissionRequiredMixin, ListView):
    model = RAMModel
    template_name = 'home/ram/ram_models.html'
    context_object_name = 'ram_models'
    title_page = 'Модели оперативной памяти'
    permission_required = 'home.view_rammodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ram_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.RAM)
        ram_types = RAMType.objects.all()
        memory_value = 0
        selected_name = self.request.GET.get('name', '')
        
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = ram_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_type = self.request.GET.get('type', '')
        try:
            selected_type_id = int(selected_type)
            try:
                type_value = ram_types.get(id=selected_type_id).name
            except ObjectDoesNotExist:
                type_value = selected_type
        except:
            type_value = selected_type

        selected_memory = self.request.GET.get('memory', '')
        try:
            selected_memory_id = float(selected_memory.replace(',', '.'))
        except:
            memory_value = selected_memory
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(RAMModel.objects.values_list('name', flat=True))
        context['vendors'] = ram_vendors
        context['types'] = ram_types
        context['memories'] = set(RAMModel.objects.values_list('memory', flat=True))
        context['selected_vendor'] = selected_vendor
        context['selected_type'] = selected_type
        context['selected_memory'] = selected_memory
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Тип',
                'value': type_value,
                'type': 'type', 
            },
            {
                'name': 'Объём памяти',
                'value': memory_value if memory_value else selected_memory,
                'type': 'memory', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = RAMModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        ram_type = self.request.GET.get('type', '')
        memory = self.request.GET.get('memory', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(vendor_id=vendor)
            except:
                return []
            
        if ram_type:
            try:
                ram_type = int(ram_type)
                queryset = queryset.filter(type_id=ram_type)
            except:
                return []
            
        if memory:
            try:
                memory = float(memory.replace(',', '.'))
                queryset = queryset.filter(memory=memory)
            except:
                return []
    
        return queryset

class AddRAMModel(PermissionRequiredMixin, CreateView):
    model = RAMModel
    form_class = AddRAMModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели оперативной памяти'
    permission_required = 'home.add_rammodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateRAMModel(PermissionRequiredMixin, UpdateView):
    model = RAMModel
    form_class = AddRAMModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели оперативной памяти'
    permission_required = 'home.change_rammodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
'''
Производители оперативной памяти
'''

class GetRAMVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/ram/ram_vendors.html'
    context_object_name = 'ram_vendors'
    title_page = 'Производители оперативной памяти'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.RAM).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.RAM)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddRAMVendor(PermissionRequiredMixin, CreateView):
    model = Vendor
    form_class = AddRAMVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя оперативной памяти'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateRAMVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddRAMVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя оперативной памяти'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Типы оперативной памяти
'''

class GetRAMTypes(PermissionRequiredMixin, ListView):
    model = RAMType
    template_name = 'home/ram/ram_types.html'
    context_object_name = 'ram_types'
    title_page = 'Типы оперативной памяти'
    permission_required = 'home.view_ramtype'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(RAMType.objects.values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = RAMType.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddRAMType(PermissionRequiredMixin, CreateView):
    model = RAMType
    form_class = AddRAMTypeForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание типа оперативной памяти'
    permission_required = 'home.add_ramtype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateRAMType(PermissionRequiredMixin, UpdateView):
    model = RAMType
    form_class = AddRAMTypeForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование типа оперативной памяти'
    permission_required = 'home.change_ramtype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Мониторы
'''

class GetMonitors(PermissionRequiredMixin, ListView):
    model = Monitor
    template_name = 'home/monitor/monitors.html'
    context_object_name = 'monitors'
    title_page = 'Мониторы'
    permission_required = 'home.view_monitor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        monitor_vendors = Vendor.objects.filter(vendor_type__id=VendorType.Type.MONITOR)
        monitor_models = MonitorModel.objects.all()
        monitor_resolutions = Resolution.objects.all()
        monitor_resolution_formats = ResolutionFormat.objects.all()
        
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = monitor_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        selected_model = self.request.GET.get('model', '')
        try:
            selected_model_id = int(selected_model)
            try:
                model_value = monitor_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model
        
        selected_resolution = self.request.GET.get('resolution', '')
        try:
            selected_resolution_id = int(selected_resolution)
            try:
                resolution_value = monitor_resolutions.get(id=int(selected_resolution_id)).name
            except ObjectDoesNotExist:
                resolution_value = selected_resolution
        except:
            resolution_value = selected_resolution

        selected_resolution_format = self.request.GET.get('resolution_format', '')
        try:
            selected_resolution_format_id = int(selected_resolution_format)
            try:
                resolution_format_value = monitor_resolution_formats.get(id=int(selected_resolution_format_id)).name
            except ObjectDoesNotExist:
                resolution_format_value = selected_resolution_format
        except:
            resolution_format_value = selected_resolution_format

        selected_serial_number = self.request.GET.get('serial_number', '')
        selected_inventory_number = self.request.GET.get('inventory_number', '')
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Monitor.objects.values_list('name', flat=True))
        context['vendors'] = monitor_vendors
        context['models'] = monitor_models
        context['resolutions'] = set(monitor_resolutions)
        context['resolution_formats'] = set(monitor_resolution_formats)
        context['inventory_numbers'] = Monitor.objects.values_list('inventory_number', flat=True)
        context['serial_numbers'] = Monitor.objects.values_list('serial_number', flat=True)
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_inventory_number'] = selected_inventory_number
        context['selected_serial_number'] = selected_serial_number
        context['selected_resolution'] = selected_resolution
        context['selected_resolution_format'] = selected_resolution_format
        context['selected_is_updating'] = self.request.GET.get('is_updating', '')
        context['selected_can_installing'] = self.request.GET.get('can_installing', '')
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model',
            }, 
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number,
                'type': 'inventory_number', 
            },
            {
                'name': 'Серийный номер', 
                'value': selected_serial_number,
                'type': 'serial_number', 
            },
            {
                'name': 'Разрешение', 
                'value': resolution_value,
                'type': 'resolution', 
            },
            {
                'name': 'Соотношение сторон', 
                'value': resolution_format_value,
                'type': 'resolution_format', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлен',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Monitor.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        inventory_number = self.request.GET.get('inventory_number', '')
        serial_number = self.request.GET.get('serial_number', '')
        resolution = self.request.GET.get('resolution', '')
        resolution_format = self.request.GET.get('resolution_format', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(model__vendor_id=vendor)
            except:
                return []
            
        if model:
            try:
                model = int(model)
                queryset = queryset.filter(model_id=model)
            except:
                return []

        if inventory_number:
            queryset = queryset.filter(inventory_number=inventory_number)

        if serial_number:
            queryset = queryset.filter(serial_number=serial_number)

        if resolution:
            try:
                resolution = int(resolution)
                queryset = queryset.filter(resolution_id=resolution)
            except:
                return []

        if resolution_format:
            try:
                resolution_format = int(resolution_format)
                queryset = queryset.filter(resolution__resolution_format_id=resolution_format)
            except:
                return []

        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset

class AddMonitor(PermissionRequiredMixin, CreateView):
    model = Monitor
    form_class = AddMonitorForm
    template_name = "home/monitor/addmonitor.html"
    title_page = 'Создание монитора'
    permission_required = 'home.add_monitor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateMonitor(PermissionRequiredMixin, UpdateView):
    model = Monitor
    form_class = AddMonitorForm
    template_name = 'home/monitor/addmonitor.html'
    title_page = 'Редактирование монитора'
    permission_required = 'home.change_monitor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели мониторов
'''

class GetMonitorModels(PermissionRequiredMixin, ListView):
    model = MonitorModel
    template_name = 'home/monitor/monitor_models.html'
    context_object_name = 'monitor_models'
    title_page = 'Модели мониторов'
    permission_required = 'home.view_monitormodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        monitor_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.MONITOR)
        
        selected_name = self.request.GET.get('name', '')
        selected_vendor = self.request.GET.get('vendor', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = monitor_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(MonitorModel.objects.values_list('name', flat=True))
        context['vendors'] = monitor_vendors
        context['selected_vendor'] = selected_vendor
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = MonitorModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(vendor_id=vendor)
            except:
                return []
    
        return queryset

class AddMonitorModel(PermissionRequiredMixin, CreateView):
    model = MonitorModel
    form_class = AddMonitorModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели монитора'
    permission_required = 'home.add_monitormodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateMonitorModel(PermissionRequiredMixin, UpdateView):
    model = MonitorModel
    form_class = AddMonitorModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели монитора'
    permission_required = 'home.change_monitormodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители мониторов
'''

class GetMonitorVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/monitor/monitor_vendors.html'
    context_object_name = 'monitor_vendors'
    title_page = 'Производители мониторов'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.MONITOR).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.MONITOR)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddMonitorVendor(PermissionRequiredMixin, CreateView):
    model = Vendor
    form_class = AddMonitorVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя монитора'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateMonitorVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddMonitorVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя монитора'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Университет
'''

class AddUniversity(PermissionRequiredMixin, CreateView):
    model = University
    form_class = AddUniversityForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание университета'
    permission_required = 'home.add_university'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['exists'] = len(University.objects.all()) > 0
        context['button_text'] = 'Создать'
        return context
    
class GetUniversity(PermissionRequiredMixin, ListView):
    model = University
    template_name = 'home/university/university.html'
    context_object_name = 'university'
    title_page = 'Университет'
    permission_required = 'home.view_university'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['university'] = University.objects.first()
        context['exists'] = len(University.objects.all()) > 0

        data = []
        for university_body in UniversityBody.objects.all():
            data.append({
                'name': university_body.name,
                'address': university_body.address,
                'audiences': [{
                    'id': audience.id, 
                    'name': audience.name 
                    } for audience in university_body.audience_set.all()]
                })

        context['university_bodies'] = data
        return context

    def get_queryset(self):
        return University.objects.first()
    
'''
Программное обеспечение
'''

class GetSoftwares(PermissionRequiredMixin, ListView):
    model = Software
    template_name = 'home/software/softwares.html'
    context_object_name = 'softwares'
    title_page = 'Программное обеспечение'
    permission_required = 'home.view_software'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')
        selected_vendor = self.request.GET.get('vendor', '')
        selected_type = self.request.GET.get('type', '')
        software_vendors = Vendor.objects.filter(vendor_type__id=VendorType.Type.SOFTWARE)
        software_types = SoftwareType.objects.all()
        
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = software_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        try:
            selected_type_id = int(selected_type)
            try:
                type_value = software_types.get(id=selected_type_id).name
            except ObjectDoesNotExist:
                type_value = selected_type
        except:
            type_value = selected_type

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Software.objects.values_list('name', flat=True))
        context['vendors'] = software_vendors
        context['types'] = software_types
        context['selected_name'] = selected_name
        context['selected_vendor'] = selected_vendor
        context['selected_type'] = selected_type
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Тип',
                'value': type_value,
                'type': 'type',
            }, 
        ]
        return context

    def get_queryset(self):
        queryset = Software.objects.all()
        name = self.request.GET.get('name', '')
        vendor = self.request.GET.get('vendor', '')
        software_type = self.request.GET.get('software_type', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
                queryset = queryset.filter(vendor_id=vendor)
            except:
                return []
            
        if software_type:
            try:
                software_type = int(software_type)
                queryset = queryset.filter(type_id=software_type)
            except:
                return []

        return queryset
    
'''
Производители программного обеспечения
'''

class GetSoftwareVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/software/software_vendors.html'
    context_object_name = 'software_vendors'
    title_page = 'Производители программного обеспечения'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.SOFTWARE).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):        
        queryset = Vendor.objects.filter(vendor_type__id=VendorType.Type.SOFTWARE)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

'''
Задачи
'''

class GetTasks(PermissionRequiredMixin, ListView):
    model = Task
    template_name = 'home/task/tasks.html'
    context_object_name = 'tasks'
    title_page = 'Задачи'
    permission_required = 'users.view_task'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')
        selected_status = self.request.GET.get('status', '')
        selected_inventory_number = self.request.GET.get('inventory_number', '')

        try:
            status_id = int(selected_status)
            try:
                status_value = TaskStatus.objects.get(id=status_id).status_name
            except ObjectDoesNotExist:
                status_value = selected_status
        except:
            status_value = selected_status

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['user_tasks'] = User_Task.objects.all()
        context['names'] = set(Task.objects.values_list('title', flat=True))
        context['inventory_numbers'] = list(chain(Computer.objects.values_list('inventory_number', flat=True), Printer.objects.values_list('inventory_number', flat=True), Projector.objects.values_list('inventory_number', flat=True), TV.objects.values_list('inventory_number', flat=True), Monitor.objects.values_list('inventory_number', flat=True)))
        context['statuses'] = TaskStatus.objects.all()
        context['selected_name'] = selected_name
        context['selected_status'] = selected_status
        context['selected_inventory_number'] = selected_inventory_number
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
            {
                'name': 'Статус',
                'value': status_value, 
                'type': 'status', 
            },
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number, 
                'type': 'inventory_number', 
            },
        ]
        
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Task.objects.all()
        else:
            if self.request.user.group.is_responsible:
                queryset = Task.objects.filter(id__in=User_Task.objects.filter(user_id=self.request.user.id).values_list('task_id', flat=True))
            else:    
                queryset = Task.objects.filter(id__in=User_Task.objects.filter(user_id=self.request.user.id, owner=True).values_list('task_id', flat=True))

        name = self.request.GET.get('name', '')
        status = self.request.GET.get('status', '')
        inventory_number = self.request.GET.get('inventory_number', '')

        if name:
            queryset = queryset.filter(title=name)

        if inventory_number:
            try:
                tehnique = helper.get_technique_by_inventory_number(inventory_number)
                if tehnique.technique_type_id == TechniqueType.Type.COMPUTER:
                    queryset = queryset.filter(computer_id=inventory_number)
                elif tehnique.technique_type_id == TechniqueType.Type.MONITOR:
                    queryset = queryset.filter(monitor_id=inventory_number)
                elif tehnique.technique_type_id == TechniqueType.Type.PRINTER:
                    queryset = queryset.filter(printer_id=inventory_number)
                elif tehnique.technique_type_id == TechniqueType.Type.PROJECTOR:
                    queryset = queryset.filter(projector_id=inventory_number)
                elif tehnique.technique_type_id == TechniqueType.Type.TV:
                    queryset = queryset.filter(tv_id=inventory_number)
            except ObjectDoesNotExist:
                return []

        if status:
            try:
                status = int(status)
                queryset = queryset.filter(status__id=status)
            except:
                return []

        return queryset

class AddTask(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = AddTaskForm
    template_name = 'home/task/addtask.html'
    title_page = 'Создание задачи'
    permission_required = 'users.add_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    # model = Task
    # permission_required = 'users.add_task'

    # def get(self, request):
    #     form = AddTaskForm()
    #     template_name = "home/task/addtask.html"
    #     title_page = 'Создание задачи'
    #     users = get_user_model().objects.filter(group_id__in=Group.objects.filter(is_responsible=True))
    #     return render(request, template_name, {'form': form, 'title': title_page, 'users': users})

    # def post(self, request):
    #     form = AddTaskForm(request.POST, user=request.user)
    #     #print(form.errors)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect("/tasks/")
        
    #     return render(request, 'home/task/addtask.html', {'form': form})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = self.title_page
    #     context['default_image'] = settings.DEFAULT_USER_IMAGE
    #     context['button_text'] = 'Создать'
    #     return context
    
class UpdateTask(PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = AddTaskForm
    template_name = 'home/task/addtask.html'
    title_page = 'Редактирование задачи'
    permission_required = 'users.change_task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

'''
Принтеры
'''

class GetPrinters(PermissionRequiredMixin, ListView):
    model = Printer
    template_name = 'home/printer/printers.html'
    context_object_name = 'printers'
    title_page = 'Принтеры'
    permission_required = 'home.view_printer'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        printer_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.PRINTER)
        printer_models = PrinterModel.objects.all()
        color_printings = ColorPrinting.objects.all()
        print_types = PrintType.objects.all()
        statuses = TechniqueStatus.objects.all()
        audiences = Audience.objects.all()
        types = TechniqueType.objects.filter(Q(id = TechniqueType.Type.PRINTER) | Q(id = TechniqueType.Type.MFU))
        inventory_numbers = Printer.objects.values_list('inventory_number', flat=True)
        selected_vendor = self.request.GET.get('vendor', '')
        selected_model = self.request.GET.get('model', '')
        selected_color_printing = self.request.GET.get('color_printing', '')
        selected_print_type = self.request.GET.get('print_type', '')
        selected_status = self.request.GET.get('status', '')
        selected_is_networking = self.request.GET.get('is_networking', '')
        selected_year_of_production = self.request.GET.get('year_of_production', '')
        selected_audience = self.request.GET.get('audience', '')
        selected_type = self.request.GET.get('type', '')
        selected_inventory_number = self.request.GET.get('inventory_number', '')

        year_of_production_value = 0

        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = printer_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        try:
            selected_model_id = int(selected_model)
            try:
                model_value = printer_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model

        try:
            selected_color_printing_id = int(selected_color_printing)
            try:
                color_printing_value = color_printings.get(id=int(selected_color_printing_id)).name
            except ObjectDoesNotExist:
                color_printing_value = selected_color_printing
        except:
            color_printing_value = selected_color_printing

        try:
            selected_print_type_id = int(selected_print_type)
            try:
                print_type_value = print_types.get(id=int(selected_print_type_id)).name
            except ObjectDoesNotExist:
                print_type_value = selected_print_type
        except:
            print_type_value = selected_print_type

        try:
            selected_status_id = int(selected_status)
            try:
                status_value = statuses.get(id=int(selected_status_id)).name
            except ObjectDoesNotExist:
                status_value = selected_status
        except:
            status_value = selected_status

        try:
            selected_year_of_production_id = int(selected_year_of_production)
        except:
            year_of_production_value = selected_year_of_production

        try:
            selected_audience_id = int(selected_audience)
            try:
                audience_value = audiences.get(id=int(selected_audience_id)).name
            except ObjectDoesNotExist:
                audience_value = selected_audience
        except:
            audience_value = selected_audience

        try:
            selected_type_id = int(selected_type)
            try:
                type_value = types.get(id=int(selected_type_id)).name
            except ObjectDoesNotExist:
                type_value = selected_type
        except:
            type_value = selected_type

        selected_name = self.request.GET.get('name', '')

        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['inventory_numbers'] = inventory_numbers
        context['names'] = set(Printer.objects.values_list('name', flat=True))
        context['vendors'] = printer_vendors
        context['models'] = printer_models
        context['color_printings'] = color_printings
        context['print_types'] = print_types
        context['statuses'] = statuses
        context['year_of_productions'] = set(Printer.objects.values_list('year_of_production', flat=True))
        context['audiences'] = audiences
        context['types'] = types
        context['selected_inventory_number'] = selected_inventory_number
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_color_printing'] = selected_color_printing
        context['selected_print_type'] = selected_print_type
        context['selected_status'] = selected_status
        context['selected_year_of_production'] = selected_year_of_production
        context['selected_audience'] = selected_audience
        context['selected_is_networking'] = self.request.GET.get('is_networking', '')
        context['selected_type'] = selected_type
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number,
                'type': 'inventory_number', 
            },
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model', 
            },
            {
                'name': 'Цветность печати',
                'value': color_printing_value,
                'type': 'color_printing', 
            },
            {
                'name': 'Тип печати',
                'value': print_type_value,
                'type': 'print_type', 
            },
            {
                'name': 'Статус',
                'value': status_value,
                'type': 'status', 
            },
            {
                'name': 'Сетевой',
                'value': self.request.GET.get('is_networking', ''), 
                'type': 'is_networking', 
            },
            {
                'name': 'Год производства',
                'value': year_of_production_value if year_of_production_value else selected_year_of_production,
                'type': 'year_of_production', 
            },
            {
                'name': 'Аудитория',
                'value': audience_value,
                'type': 'audience', 
            },
            {
                'name': 'Тип',
                'value': type_value,
                'type': 'type', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Printer.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        color_printing = self.request.GET.get('color_printing', '')
        print_type = self.request.GET.get('print_type', '')
        status = self.request.GET.get('status', '')
        is_networking = self.request.GET.get('is_networking', '')
        year_of_production = self.request.GET.get('year_of_production', '')
        audience = self.request.GET.get('audience', '')
        technique_type = self.request.GET.get('type', '')
        inventory_number = self.request.GET.get('inventory_number', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if inventory_number:
            queryset = queryset.filter(inventory_number=inventory_number)

        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = queryset.filter(model__vendor_id=vendor)

        if model:
            try:
                model = int(model)
            except:
                return []
            queryset = queryset.filter(model_id=model)

        if color_printing:
            try:
                color_printing = int(color_printing)
            except:
                return []
            queryset = queryset.filter(color_printing_id=color_printing)

        if print_type:
            try:
                print_type = int(print_type)
            except:
                return []
            queryset = queryset.filter(print_type_id=print_type)

        if status:
            try:
                status = int(status)
            except:
                return []
            queryset = queryset.filter(status_id=status)

        if is_networking != None and is_networking != '':
            if is_networking != 'True':
                if is_networking != 'False':
                    return []
            queryset = queryset.filter(is_networking=is_networking)

        if year_of_production:
            try:
                year_of_production = int(year_of_production)
            except:
                return []
            queryset = queryset.filter(year_of_production=year_of_production)

        if technique_type:
            try:
                technique_type = int(technique_type)
            except:
                return []
            queryset = queryset.filter(technique_type=technique_type)

        if audience:
            try:
                audience = int(audience)
            except:
                return []
            queryset = queryset.filter(audience_id=audience)

        return queryset

class AddPrinter(PermissionRequiredMixin, CreateView):
    model = Printer
    form_class = AddPrinterForm
    template_name = "home/printer/addprinter.html"
    title_page = 'Создание принтера'
    permission_required = 'home.add_printer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdatePrinter(PermissionRequiredMixin, UpdateView):
    model = Printer
    form_class = AddPrinterForm
    template_name = 'home/printer/addprinter.html'
    title_page = 'Редактирование принтера'
    permission_required = 'home.change_printer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели принтеров
'''

class GetPrinterModels(PermissionRequiredMixin, ListView):
    model = PrinterModel
    template_name = 'home/printer/printer_models.html'
    context_object_name = 'printer_models'
    title_page = 'Модели принетров'
    permission_required = 'home.view_printermodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        printer_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.PRINTER).all()
        selected_vendor = self.request.GET.get('vendor', '')
        selected_name = self.request.GET.get('name', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = printer_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(PrinterModel.objects.values_list('name', flat=True))
        context['vendors'] = printer_vendors
        context['selected_vendor'] = selected_vendor
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor'
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        
        return context

    def get_queryset(self):
        queryset = PrinterModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)
        
        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = PrinterModel.objects.filter(vendor_id=vendor)

        return queryset

class AddPrinterModel(PermissionRequiredMixin, CreateView):
    model = PrinterModel
    form_class = AddPrinterModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели принтера'
    permission_required = 'home.add_printermodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdatePrinterModel(PermissionRequiredMixin, UpdateView):
    model = PrinterModel
    form_class = AddPrinterModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели принтера'
    permission_required = 'home.change_printermodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители принтеров
'''

class GetPrinterVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/printer/printer_vendors.html'
    context_object_name = 'printer_vendors'
    title_page = 'Производители принтеров'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type=VendorType.Type.PRINTER).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.PRINTER)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddPrinterVendor(PermissionRequiredMixin, CreateView):
    model = Vendor
    form_class = AddPrinterVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя принтера'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdatePrinterVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddPrinterVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя принтера'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Корпус
'''

class AddUniversityBody(PermissionRequiredMixin, CreateView):
    model = UniversityBody
    form_class = AddUniversityBodyForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание корпуса'
    permission_required = 'home.add_universitybody'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context
    
class UpdateUniversityBody(PermissionRequiredMixin, UpdateView):
    model = UniversityBody
    form_class = AddUniversityBodyForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование корпуса'
    permission_required = 'home.change_universitybody'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
class GetUniversityBodies(PermissionRequiredMixin, ListView):
    model = UniversityBody
    template_name = 'home/university_body/universitybodies.html'
    context_object_name = 'university_bodies'
    title_page = 'Корпуса'
    permission_required = 'home.view_universitybody'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(UniversityBody.objects.values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context
    
    def get_queryset(self):
        queryset = UniversityBody.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset
    
'''
Проекторы
'''

class GetProjectors(PermissionRequiredMixin, ListView):
    model = Projector
    template_name = 'home/projector/projectors.html'
    context_object_name = 'projectors'
    title_page = 'Проекторы'
    permission_required = 'home.view_projector'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        projector_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.PRINTER)
        projector_models = ProjectorModel.objects.all()
        statuses = TechniqueStatus.objects.all()
        audiences = Audience.objects.all()
        types = ProjectorType.objects.all()
        inventory_numbers = Projector.objects.values_list('inventory_number', flat=True)
        selected_vendor = self.request.GET.get('vendor', '')
        selected_model = self.request.GET.get('model', '')
        selected_status = self.request.GET.get('status', '')
        selected_with_remote_controller = self.request.GET.get('with_remote_controller', '')
        selected_year_of_production = self.request.GET.get('year_of_production', '')
        selected_audience = self.request.GET.get('audience', '')
        selected_type = self.request.GET.get('type', '')
        selected_inventory_number = self.request.GET.get('inventory_number', '')

        year_of_production_value = 0

        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = projector_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        try:
            selected_model_id = int(selected_model)
            try:
                model_value = projector_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model

        try:
            selected_status_id = int(selected_status)
            try:
                status_value = statuses.get(id=int(selected_status_id)).name
            except ObjectDoesNotExist:
                status_value = selected_status
        except:
            status_value = selected_status

        try:
            selected_year_of_production_id = int(selected_year_of_production)
        except:
            year_of_production_value = selected_year_of_production

        try:
            selected_audience_id = int(selected_audience)
            try:
                audience_value = audiences.get(id=int(selected_audience_id)).name
            except ObjectDoesNotExist:
                audience_value = selected_audience
        except:
            audience_value = selected_audience

        try:
            selected_type_id = int(selected_type)
            try:
                type_value = types.get(id=int(selected_type_id)).name
            except ObjectDoesNotExist:
                type_value = selected_type
        except:
            type_value = selected_type

        selected_name = self.request.GET.get('name', '')

        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Projector.objects.values_list('name', flat=True))
        context['inventory_numbers'] = inventory_numbers
        context['vendors'] = projector_vendors
        context['models'] = projector_models
        context['statuses'] = statuses
        context['year_of_productions'] = set(Projector.objects.values_list('year_of_production', flat=True))
        context['audiences'] = audiences
        context['types'] = types
        context['selected_inventory_number'] = selected_inventory_number
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_status'] = selected_status
        context['selected_year_of_production'] = selected_year_of_production
        context['selected_audience'] = selected_audience
        context['selected_with_remote_controller'] = self.request.GET.get('with_remote_controller', '')
        context['selected_type'] = selected_type
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number,
                'type': 'inventory_number', 
            },
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model', 
            },
            {
                'name': 'Статус',
                'value': status_value,
                'type': 'status', 
            },
            {
                'name': 'Сетевой',
                'value': self.request.GET.get('with_remote_controller', ''), 
                'type': 'with_remote_controller', 
            },
            {
                'name': 'Год производства',
                'value': year_of_production_value if year_of_production_value else selected_year_of_production,
                'type': 'year_of_production', 
            },
            {
                'name': 'Аудитория',
                'value': audience_value,
                'type': 'audience', 
            },
            {
                'name': 'Тип',
                'value': type_value,
                'type': 'type', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Projector.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        status = self.request.GET.get('status', '')
        with_remote_controller = self.request.GET.get('with_remote_controller', '')
        year_of_production = self.request.GET.get('year_of_production', '')
        audience = self.request.GET.get('audience', '')
        inventory_number = self.request.GET.get('inventory_number', '')
        projector_type = self.request.GET.get('type', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if inventory_number:
            queryset = queryset.filter(inventory_number=inventory_number)

        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = queryset.filter(model__vendor_id=vendor)

        if model:
            try:
                model = int(model)
            except:
                return []
            queryset = queryset.filter(model_id=model)

        if status:
            try:
                status = int(status)
            except:
                return []
            queryset = queryset.filter(status_id=status)

        if with_remote_controller != None and with_remote_controller != '':
            if with_remote_controller != 'True':
                if with_remote_controller != 'False':
                    return []
            queryset = queryset.filter(with_remote_controller=with_remote_controller)

        if year_of_production:
            try:
                year_of_production = int(year_of_production)
            except:
                return []
            queryset = queryset.filter(year_of_production=year_of_production)

        if audience:
            try:
                audience = int(audience)
            except:
                return []
            queryset = queryset.filter(audience_id=audience)

        if projector_type:
            try:
                projector_type = int(projector_type)
            except:
                return []
            queryset = queryset.filter(type_id=projector_type)

        return queryset

class AddProjector(PermissionRequiredMixin, CreateView):
    model = Projector
    form_class = AddProjectorForm
    template_name = "home/projector/addprojector.html"
    title_page = 'Создание проектора'
    permission_required = 'home.add_projector'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateProjector(PermissionRequiredMixin, UpdateView):
    model = Projector
    form_class = AddProjectorForm
    template_name = 'home/projector/addprojector.html'
    title_page = 'Редактирование проектора'
    permission_required = 'home.change_projector'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Модели проекторов
'''

class GetProjectorModels(PermissionRequiredMixin, ListView):
    model = ProjectorModel
    template_name = 'home/projector/projector_models.html'
    context_object_name = 'projector_models'
    title_page = 'Модели проекторов'
    permission_required = 'home.view_projectormodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        projector_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.PROJECTOR).all()
        selected_vendor = self.request.GET.get('vendor', '')
        selected_name = self.request.GET.get('name', '')
        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = projector_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(ProjectorModel.objects.values_list('name', flat=True))
        context['vendors'] = projector_vendors
        context['selected_vendor'] = selected_vendor
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor'
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        
        return context

    def get_queryset(self):
        queryset = ProjectorModel.objects.all()
        vendor = self.request.GET.get('vendor', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)
        
        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = ProjectorModel.objects.filter(vendor_id=vendor)

        return queryset

class AddProjectorModel(PermissionRequiredMixin, CreateView):
    model = ProjectorModel
    form_class = AddProjectorModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели проектора'
    permission_required = 'home.add_projectormodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateProjectorModel(PermissionRequiredMixin, UpdateView):
    model = ProjectorModel
    form_class = AddProjectorModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели проектора'
    permission_required = 'home.change_projectormodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители проекторов
'''

class GetProjectorVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/projector/projector_vendors.html'
    context_object_name = 'projector_vendors'
    title_page = 'Производители проекторов'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.PROJECTOR).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.PROJECTOR)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddProjectorVendor(PermissionRequiredMixin, CreateView):
    model = Vendor
    form_class = AddProjectorVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя проектора'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateProjectorVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddProjectorVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя проектора'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Телевизоры
'''

class GetTVs(PermissionRequiredMixin, ListView):
    model = TV
    template_name = 'home/tv/tvs.html'
    context_object_name = 'tvs'
    title_page = 'Телевизоры'
    permission_required = 'home.view_tv'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tv_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.TV)
        tv_models = TVModel.objects.all()
        statuses = TechniqueStatus.objects.all()
        audiences = Audience.objects.all()
        inventory_numbers = TV.objects.values_list('inventory_number', flat=True)
        diagonales = set(TV.objects.values_list('diagonal', flat=True))
        selected_vendor = self.request.GET.get('vendor', '')
        selected_model = self.request.GET.get('model', '')
        selected_status = self.request.GET.get('status', '')
        selected_diagonal = self.request.GET.get('diagonal', '')
        selected_year_of_production = self.request.GET.get('year_of_production', '')
        selected_audience = self.request.GET.get('audience', '')
        selected_inventory_number = self.request.GET.get('inventory_number', '')

        year_of_production_value = 0
        diagonal_value = 0

        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = tv_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        try:
            selected_model_id = int(selected_model)
            try:
                model_value = tv_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model

        try:
            selected_status_id = int(selected_status)
            try:
                status_value = statuses.get(id=int(selected_status_id)).name
            except ObjectDoesNotExist:
                status_value = selected_status
        except:
            status_value = selected_status

        try:
            selected_year_of_production_id = int(selected_year_of_production)
        except:
            year_of_production_value = selected_year_of_production

        try:
            selected_audience_id = int(selected_audience)
            try:
                audience_value = audiences.get(id=int(selected_audience_id)).name
            except ObjectDoesNotExist:
                audience_value = selected_audience
        except:
            audience_value = selected_audience

        try:
            selected_diagonal_id = int(selected_diagonal)
        except:
            diagonal_value = selected_diagonal

        selected_name = self.request.GET.get('name', '')

        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(TV.objects.values_list('name', flat=True))
        context['inventory_numbers'] = inventory_numbers
        context['vendors'] = tv_vendors
        context['models'] = tv_models
        context['statuses'] = statuses
        context['year_of_productions'] = set(TV.objects.values_list('year_of_production', flat=True))
        context['audiences'] = audiences
        context['diagonales'] = diagonales
        context['selected_inventory_number'] = selected_inventory_number
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_status'] = selected_status
        context['selected_year_of_production'] = selected_year_of_production
        context['selected_audience'] = selected_audience
        context['selected_with_remote_controller'] = self.request.GET.get('with_remote_controller', '')
        context['selected_diagonal'] = selected_diagonal
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Инвентарный номер',
                'value': selected_inventory_number,
                'type': 'inventory_number', 
            },
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model', 
            },
            {
                'name': 'Статус',
                'value': status_value,
                'type': 'status', 
            },
            {
                'name': 'Сетевой',
                'value': self.request.GET.get('with_remote_controller', ''), 
                'type': 'with_remote_controller', 
            },
            {
                'name': 'Год производства',
                'value': year_of_production_value if year_of_production_value else selected_year_of_production,
                'type': 'year_of_production', 
            },
            {
                'name': 'Аудитория',
                'value': audience_value,
                'type': 'audience', 
            },
            {
                'name': 'Диагональ',
                'value': diagonal_value if diagonal_value else selected_diagonal,
                'type': 'diagonal', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = TV.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        status = self.request.GET.get('status', '')
        year_of_production = self.request.GET.get('year_of_production', '')
        audience = self.request.GET.get('audience', '')
        diagonal = self.request.GET.get('diagonal', '')
        inventory_number = self.request.GET.get('inventory_number', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if inventory_number:
            queryset = queryset.filter(inventory_number=inventory_number)

        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = queryset.filter(model__vendor_id=vendor)

        if model:
            try:
                model = int(model)
            except:
                return []
            queryset = queryset.filter(model_id=model)

        if status:
            try:
                status = int(status)
            except:
                return []
            queryset = queryset.filter(status_id=status)

        if diagonal:
            try:
                diagonal = float(diagonal.replace(',', '.'))
            except:
                return []
            queryset = queryset.filter(diagonal=diagonal)

        if year_of_production:
            try:
                year_of_production = int(year_of_production)
            except:
                return []
            queryset = queryset.filter(year_of_production=year_of_production)

        if audience:
            try:
                audience = int(audience)
            except:
                return []
            queryset = queryset.filter(audience_id=audience)

        return queryset

class AddTV(PermissionRequiredMixin, CreateView):
    model = TV
    form_class = AddTVForm
    template_name = "home/tv/addtv.html"
    title_page = 'Создание телевизора'
    permission_required = 'home.add_tv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateTV(PermissionRequiredMixin, UpdateView):
    model = TV
    form_class = AddTVForm
    template_name = 'home/tv/addtv.html'
    title_page = 'Редактирование телевизора'
    permission_required = 'home.change_tv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
'''
Модели телевизоров
'''

class GetTVModels(PermissionRequiredMixin, ListView):
    model = TVModel
    template_name = 'home/tv/tv_models.html'
    context_object_name = 'tv_models'
    title_page = 'Модели телевизоров'
    permission_required = 'home.view_tvmodel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(TVModel.objects.values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = TVModel.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddTVModel(PermissionRequiredMixin, CreateView):
    model = TVModel
    form_class = AddTVModelForm
    template_name = "home/add_model.html"
    title_page = 'Создание модели телевизора'
    permission_required = 'home.add_tvmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateTVModel(PermissionRequiredMixin, UpdateView):
    model = TVModel
    form_class = AddTVModelForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование модели телевизора'
    permission_required = 'home.change_tvmodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Производители телевизоров
'''

class GetTVVendors(PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'home/tv/tv_vendors.html'
    context_object_name = 'tv_vendors'
    title_page = 'Производители телевизоров'
    permission_required = 'home.view_vendor'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Vendor.objects.filter(vendor_type__id=VendorType.Type.TV).values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Vendor.objects.filter(vendor_type=VendorType.Type.TV)
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddTVVendor(PermissionRequiredMixin, CreateView):
    model = Vendor
    form_class = AddTVVendorForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание производителя телевизора'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateTVVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddTVVendorForm
    template_name = 'home/add_vendor.html'
    title_page = 'Редактирование производителя телевизора'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

'''
Программное обеспечение
'''

class AddSoftware(PermissionRequiredMixin, CreateView):
    model = Software
    form_class = AddSoftwareForm
    template_name = 'home/add_model.html'
    title_page = 'Создание программного обеспечение'
    permission_required = 'home.add_software'

    # def get(self, request):
    #     form = AddSoftwareForm()
    #     template_name = "home/add_model.html"
    #     title_page = 'Создание программного обеспечения'
    #     return render(request, template_name, {'form': form, 'title': title_page})

    # def post(self, request):
    #     form = AddSoftwareForm(request.POST, user=request.user)
    #     print(form.errors)
    #     if form.is_valid():
    #         form.save()
            
    #         return HttpResponseRedirect("/softwares/")
    #     return render(request, 'home/add_edit_form.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context
    
class UpdateSoftware(PermissionRequiredMixin, UpdateView):
    model = Software
    form_class = AddSoftwareForm
    template_name = 'home/add_model.html'
    title_page = 'Редактирование программного обеспечения'
    permission_required = 'home.change_software'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context

class AddSoftwareVendor(PermissionRequiredMixin, CreateView):
    model = Vendor
    form_class = AddSoftwareVendorForm
    template_name = "home/add_edit_form.html"
    title_page = 'Создание производителя программного обеспечения'
    permission_required = 'home.add_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateSoftwareVendor(PermissionRequiredMixin, UpdateView):
    model = Vendor
    form_class = AddSoftwareVendorForm
    template_name = 'home/add_edit_form.html'
    title_page = 'Редактирование производителя программного обеспечения'
    permission_required = 'home.change_vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
class GetAudienceTypes(PermissionRequiredMixin, ListView):
    model = AudienceType
    template_name = 'home/audience/audience_types.html'
    context_object_name = 'audience_types'
    title_page = 'Типы аудиторий'
    permission_required = 'home.view_audiencetype'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')
        
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(AudienceType.objects.values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]

        return context

    def get_queryset(self):
        queryset = AudienceType.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)
        
        return queryset

class AddAudienceType(PermissionRequiredMixin, CreateView):
    form_class = AddAudienceTypeForm
    template_name = "home/add_vendor.html"
    title_page = 'Создание типа аудитории'
    permission_required = 'home.add_audiencetype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateAudienceType(PermissionRequiredMixin, UpdateView):
    model = AudienceType
    form_class = AddAudienceTypeForm
    template_name = "home/add_vendor.html"
    title_page = 'Редактирование типа аудитории'
    permission_required = 'home.change_audiencetype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
class GetResolutions(PermissionRequiredMixin, ListView):
    model = Resolution
    template_name = 'home/resolution/resolutions.html'
    context_object_name = 'resolutions'
    title_page = 'Разрешения'
    permission_required = 'home.view_resolution'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')
        selected_aspect_ratio = self.request.GET.get('aspect_ratio', '')
        aspect_ratios = ResolutionFormat.objects.all()

        aspect_ratio_value = 0

        try:
            selected_aspect_ratio_id = int(selected_aspect_ratio)
            try:
                aspect_ratio_value = aspect_ratios.get(id=int(selected_aspect_ratio_id)).name
            except ObjectDoesNotExist:
                aspect_ratio_value = selected_aspect_ratio
        except:
            aspect_ratio_value = selected_aspect_ratio

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(Resolution.objects.values_list('name', flat=True))
        context['aspect_ratios'] = aspect_ratios
        context['selected_name'] = selected_name
        context['selected_aspect_ratio'] = selected_aspect_ratio
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
            {
                'name': 'Соотношение сторон',
                'value': aspect_ratio_value if aspect_ratio_value else selected_aspect_ratio, 
                'type': 'aspect_ratio', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = Resolution.objects.all()
        name = self.request.GET.get('name', '')
        aspect_ratio = self.request.GET.get('aspect_ratio', '')

        if aspect_ratio:
            try:
                aspect_ratio = int(aspect_ratio)
            except:
                return []
            queryset = queryset.filter(resolution_format_id=aspect_ratio)

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddResolution(PermissionRequiredMixin, CreateView):
    form_class = AddResolutionForm
    template_name = "home/resolution/addresolution.html"
    title_page = 'Создание разрешения'
    permission_required = 'home.add_resolution'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateResolution(PermissionRequiredMixin, UpdateView):
    model = Resolution
    form_class = AddResolutionForm
    template_name = "home/resolution/addresolution.html"
    title_page = 'Редактирование разрешения'
    permission_required = 'home.add_resolution'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
class GetResolutionFormats(PermissionRequiredMixin, ListView):
    model = ResolutionFormat
    template_name = 'home/resolution_format/resolution_formats.html'
    context_object_name = 'resolution_formats'
    title_page = 'Соотношения сторон'
    permission_required = 'home.view_resolutionformat'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = ResolutionFormat.objects.values_list('name', flat=True)
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = ResolutionFormat.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddResolutionFormat(PermissionRequiredMixin, CreateView):
    form_class = AddResolutionFormatForm
    template_name = "home/resolution_format/addresolutionformat.html"
    title_page = 'Создание соотношения сторон'
    permission_required = 'home.add_resolutionformat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateResolutionFormat(PermissionRequiredMixin, UpdateView):
    model = ResolutionFormat
    form_class = AddResolutionFormatForm
    template_name = "home/resolution_format/addresolutionformat.html"
    title_page = 'Редактирование соотношения сторон'
    permission_required = 'home.add_resolutionformat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
class GetSoftwareTypes(PermissionRequiredMixin, ListView):
    model = SoftwareType
    template_name = 'home/software/software_types.html'
    context_object_name = 'software_types'
    title_page = 'Типы программного обеспечения'
    permission_required = 'home.view_softwaretype'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        selected_name = self.request.GET.get('name', '')

        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['names'] = set(SoftwareType.objects.values_list('name', flat=True))
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context

    def get_queryset(self):
        queryset = SoftwareType.objects.all()
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

class AddSoftwareType(PermissionRequiredMixin, CreateView):
    form_class = AddSoftwareTypeForm
    template_name = "home/software/addsoftwaretype.html"
    title_page = 'Создание типа программного обеспечения'
    permission_required = 'home.add_softwaretype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Создать'
        return context

class UpdateSoftwareType(PermissionRequiredMixin, UpdateView):
    model = SoftwareType
    form_class = AddSoftwareTypeForm
    template_name = "home/software/addsoftwaretype.html"
    title_page = 'Редактирование типа программного обеспечения'
    permission_required = 'home.change_softwaretype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['button_text'] = 'Сохранить'
        return context
    
class GetOS(PermissionRequiredMixin, ListView):
    model = OS
    template_name = 'home/os/os.html'
    context_object_name = 'oss'
    title_page = 'Операционные системы'
    permission_required = 'home.view_os'
    paginate_by = 10

    def get_queryset(self):
        queryset = OS.objects.all()
        vendor = self.request.GET.get('vendor', '')
        model = self.request.GET.get('model', '')
        can_installing = self.request.GET.get('can_installing', '')
        is_updating = self.request.GET.get('is_updating', '')
        name = self.request.GET.get('name', '')

        if name:
            queryset = queryset.filter(name=name)

        if vendor:
            try:
                vendor = int(vendor)
            except:
                return []
            queryset = queryset.filter(model__vendor_id=vendor)

        if model:
            try:
                model = int(model)
            except:
                return []
            queryset = queryset.filter(model_id=model)

        if can_installing != None and can_installing != '':
            if can_installing != 'True':
                if can_installing != 'False':
                    return []
            queryset = queryset.filter(can_installing=can_installing)

        if is_updating != None and is_updating != "":
            if is_updating != "True":
                if is_updating != "False":
                    return []
            queryset = queryset.filter(is_updating=is_updating)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        motherboard_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.MOTHERBOARD).all()
        motherboard_models = MotherboardModel.objects.all()
        selected_name = self.request.GET.get('name', '')
        selected_vendor = self.request.GET.get('vendor', '')
        selected_model = self.request.GET.get('model', '')
        selected_is_updating = self.request.GET.get('is_updating', '')
        selected_can_installing = self.request.GET.get('can_installing', '')

        try:
            selected_vendor_id = int(selected_vendor)
            try:
                vendor_value = motherboard_vendors.get(id=selected_vendor_id).name
            except ObjectDoesNotExist:
                vendor_value = selected_vendor
        except:
            vendor_value = selected_vendor

        try:
            selected_model_id = int(selected_model)
            try:
                model_value = motherboard_models.get(id=int(selected_model_id)).name
            except ObjectDoesNotExist:
                model_value = selected_model
        except:
            model_value = selected_model

        context['names'] = set(Motherboard.objects.values_list('name', flat=True))
        context['vendors'] = motherboard_vendors
        context['models'] = motherboard_models
        context['title'] = self.title_page
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['selected_vendor'] = selected_vendor
        context['selected_model'] = selected_model
        context['selected_is_updating'] = selected_is_updating
        context['selected_can_installing'] = selected_can_installing
        context['selected_name'] = selected_name
        context['all_filters'] = [
            {
                'name': 'Производитель',
                'value': vendor_value,
                'type': 'vendor',
            }, 
            {
                'name': 'Модель',
                'value': model_value,
                'type': 'model', 
            },
            {
                'name': 'Обновляется',
                'value': self.request.GET.get('is_updating', ''), 
                'type': 'is_updating', 
            },
            {
                'name': 'Может быть установлена',
                'value': self.request.GET.get('can_installing', ''), 
                'type': 'can_installing', 
            },
            {
                'name': 'Название',
                'value': selected_name, 
                'type': 'name', 
            },
        ]
        return context
    
def analytic(request):
    m_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.MOTHERBOARD)
    s_vendors = Vendor.objects.filter(vendor_type=VendorType.Type.STORAGE)

    rams = set()
    cores = set()
    video_memories = set()
    free_memories = set()
    cpu_frequencies = set()
    
    ram_values = RAM.objects.exclude(computer_id__isnull=True).values('computer_id').annotate(total_memory=Sum('model__memory') / 1024.0)
    letter_values = Drive.objects.exclude(computer_id__isnull=True).values('computer_id').annotate(total_memory=Sum('free_memory') / 1024.0)
    
    video_memory_values = Videocard.objects.exclude(computer_id__isnull=True).values('computer_id').annotate(total_memory=Sum('model__memory') / 1024.0)
    core_values = CPUModel.objects.all().values('cores')
    os_values = OS.objects.all()
    software_values = Software.objects.all()
    
    max_computers = set()
    max_places = set()
    
    for ram in ram_values:    
        rams.add(round(ram['total_memory'], 2))

    for core in core_values:
        cores.add(core['cores'])

    for video_memory in video_memory_values:
        video_memories.add(round(video_memory['total_memory'], 2))

    for free_memory in letter_values:
        free_memories.add(round(free_memory['total_memory'], 2))
    
    for audience in Audience.objects.all():
        max_computers.add(audience.max_computers)
        max_places.add(audience.max_places)
        
    return render(request, 'home/analytic/analytic.html', context={
        'motherboard_vendors': m_vendors, 
        'storage_vendors': s_vendors, 
        'rams': rams,
        'cores': cores,
        'video_memories': video_memories,
        'free_memories': free_memories,
        'oss': os_values,
        'softwares': software_values,
        'max_computers': max_computers,
        'max_places': max_places,
        'default_image': settings.DEFAULT_USER_IMAGE,
        'user': request.user
    })

def get_softwares(request):
    if request.method == 'GET':
        softwares = []
        for software in Software.objects.values('name'):
            softwares.append(software)
        return JsonResponse(data={'softwares': softwares})

def upload_information(request):
    if not request.user.is_authenticated:
        return redirect('/users/login/')
    
    context = {
        'default_image': settings.DEFAULT_USER_IMAGE,
        'user': request.user
    }

    return render(request, 'home/upload_information.html', context)

def success(request):
    return render(request, 'home/success.html')