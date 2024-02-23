from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CPU, RAM, Audience, CPUModel, CPUVendor, Computer, Monitor, MonitorModel, MonitorVendor, Motherboard, MotherboardModel, MotherboardVendor, RAMModel, RAMType, RAMVendor, Storage, StorageModel, StorageType, StorageVendor, Videocard, VideocardModel, VideocardVendor
from django.views.generic import ListView, CreateView, UpdateView
from .forms import AddCPUForm, AddCPUModelForm, AddCPUVendorForm, AddMonitorForm, AddMonitorModelForm, AddMonitorVendorForm, AddMotherboardForm, AddMotherboardModelForm, AddMotherboardVendorForm, AddRAMForm, AddRAMModelForm, AddRAMTypeForm, AddRAMVendorForm, AddStorageForm, AddStorageModelForm, AddStorageTypeForm, AddStorageVendorForm, AddVideocardForm, AddVideocardModelForm, AddVideocardVendorForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
#from .models import MemoryManufacturer
import pandas as pd

def index(request):
    return render(request, 'home/index.html')

def test(request):
    lines = ["one", "two", "three"]
    with open(r"D:\\otus.txt", "w") as file:
        for  line in lines:
            file.write(line + '\n')

'''
Мат. платы
'''

class GetMotherboards(ListView):
    template_name = 'home/motherboard/motherboards.html'
    context_object_name = 'motherboards'
    title_page = 'Материнские платы'

    def get_queryset(self):
        vendor = self.request.GET.get('vendor')
        model = self.request.GET.get('model')

        print(f'model: {model}\nvendor: {vendor}')

        queryset = Motherboard.objects.all()

        if vendor:
            queryset = Motherboard.objects.filter(motherboardModel__motherboardVendor_id=vendor)
        
        if model:
            queryset = Motherboard.objects.filter(motherboardModel_id=model)

        print(queryset)
        return queryset
        #return Motherboard.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = MotherboardVendor.objects.all()
        context['models'] = MotherboardModel.objects.all()
        context['title'] = self.title_page
        return context

class AddMotherboard(LoginRequiredMixin, CreateView):
    form_class = AddMotherboardForm
    template_name = "home/motherboard/addmotherboard.html"
    title_page = 'Добавление материнской платы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    # def form_valid(self, form):
    #    form.save()
    #    return super().form_valid(form)
    
class UpdateMotherboard(LoginRequiredMixin, UpdateView):
    model = Motherboard
    form_class = AddMotherboardForm
    template_name = 'home/motherboard/addmotherboard.html'
    title_page = 'Редактирование материнской платы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Модели мат. плат
'''

class GetMotherboardModels(ListView):
    template_name = 'home/motherboard/motherboard_models.html'
    context_object_name = 'motherboard_models'
    title_page = 'Модели материнских плат'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return MotherboardModel.objects.all()

class AddMotherboardModel(LoginRequiredMixin, CreateView):
    form_class = AddMotherboardModelForm
    template_name = "home/motherboard/addmotherboardmodel.html"
    title_page = 'Добавление модели материнской платы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateMotherboardModel(LoginRequiredMixin, UpdateView):
    model = MotherboardModel
    form_class = AddMotherboardModelForm
    template_name = 'home/motherboard/addmotherboardmodel.html'
    title_page = 'Редактирование модели материнской платы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Производители мат. плат
'''

class GetMotherboardVendors(ListView):
    template_name = 'home/motherboard/motherboard_vendors.html'
    context_object_name = 'motherboard_vendors'
    title_page = 'Производители материнских плат'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return MotherboardVendor.objects.all()

class AddMotherboardVendor(LoginRequiredMixin, CreateView):
    form_class = AddMotherboardVendorForm
    template_name = "home/motherboard/addmotherboardvendor.html"
    title_page = 'Добавление производителя материнской платы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateMotherboardVendor(LoginRequiredMixin, UpdateView):
    model = MotherboardVendor
    form_class = AddMotherboardVendorForm
    template_name = 'home/motherboard/addmotherboardvendor.html'
    title_page = 'Редактирование производителя материнской платы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

'''
Процессоры
'''

class GetCPUs(ListView):
    template_name = 'home/cpu/cpus.html'
    context_object_name = 'cpus'
    title_page = 'Процессоры'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return CPU.objects.all()

class AddCPU(LoginRequiredMixin, CreateView):
    form_class = AddCPUForm
    template_name = "home/cpu/addcpu.html"
    title_page = 'Добавление процессора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateCPU(LoginRequiredMixin, UpdateView):
    model = CPU
    form_class = AddCPUForm
    template_name = 'home/cpu/addcpu.html'
    title_page = 'Редактирование процессора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Модели процессоров
'''

class GetCPUModels(ListView):
    template_name = 'home/cpu/cpu_models.html'
    context_object_name = 'cpu_models'
    title_page = 'Модели процессоров'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return CPUModel.objects.all()

class AddCPUModel(LoginRequiredMixin, CreateView):
    form_class = AddCPUModelForm
    template_name = "home/cpu/addcpumodel.html"
    title_page = 'Добавление модели процессора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateCPUModel(LoginRequiredMixin, UpdateView):
    model = CPUModel
    form_class = AddCPUModelForm
    template_name = 'home/cpu/addcpumodel.html'
    title_page = 'Редактирование модели процессора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Производители процессоров
'''

class GetCPUVendors(ListView):
    template_name = 'home/cpu/cpu_vendors.html'
    context_object_name = 'cpu_vendors'
    title_page = 'Производители процессоров'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return CPUVendor.objects.all()

class AddCPUVendor(LoginRequiredMixin, CreateView):
    form_class = AddCPUVendorForm
    template_name = "home/cpu/addcpuvendor.html"
    title_page = 'Добавление производителя процессора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateCPUVendor(LoginRequiredMixin, UpdateView):
    model = CPUVendor
    form_class = AddCPUVendorForm
    template_name = 'home/cpu/addcpuvendor.html'
    title_page = 'Редактирование производителя процессора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

from django.http import JsonResponse

def get_models(request, vendor_id):
    if vendor_id == 0:
        models = MotherboardModel.objects.none()
    else:
        models = MotherboardModel.objects.filter(motherboardVendor_id=vendor_id)
    model_list = list(models.values('id', 'motherboardModel_name'))
    return JsonResponse(model_list, safe=False)

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

'''
Накопители памяти
'''

class GetStorages(ListView):
    template_name = 'home/storage/storages.html'
    context_object_name = 'storages'
    title_page = 'Накопители памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Storage.objects.all()

class AddStorage(LoginRequiredMixin, CreateView):
    form_class = AddStorageForm
    template_name = "home/storage/addstorage.html"
    title_page = 'Добавление накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateStorage(LoginRequiredMixin, UpdateView):
    model = Storage
    form_class = AddStorageForm
    template_name = 'home/storage/addstorage.html'
    title_page = 'Редактирование накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Модели накопителей памяти
'''

class GetStorageModels(ListView):
    template_name = 'home/storage/storage_models.html'
    context_object_name = 'storage_models'
    title_page = 'Модели накопителей памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return StorageModel.objects.all()

class AddStorageModel(LoginRequiredMixin, CreateView):
    form_class = AddStorageModelForm
    template_name = "home/storage/addstorage.html"
    title_page = 'Добавление накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateStorageModel(LoginRequiredMixin, UpdateView):
    model = StorageModel
    form_class = AddStorageModelForm
    template_name = 'home/storage/addstorage.html'
    title_page = 'Редактирование накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context
    
'''
Производители накопителей памяти
'''

class GetStorageVendors(ListView):
    template_name = 'home/storage/storage_vendors.html'
    context_object_name = 'storage_vendors'
    title_page = 'Производители накопителей памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return StorageVendor.objects.all()

class AddStorageVendor(LoginRequiredMixin, CreateView):
    form_class = AddStorageVendorForm
    template_name = "home/storage/addstoragevendor.html"
    title_page = 'Добавление производителя накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateStorageVendor(LoginRequiredMixin, UpdateView):
    model = StorageVendor
    form_class = AddStorageVendorForm
    template_name = 'home/storage/addstoragevendor.html'
    title_page = 'Редактирование производителя накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Типы накопителей памяти
'''

class GetStorageTypes(ListView):
    template_name = 'home/storage/storage_types.html'
    context_object_name = 'storage_types'
    title_page = 'Типы накопителей памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return StorageType.objects.all()

class AddStorageType(LoginRequiredMixin, CreateView):
    form_class = AddStorageTypeForm
    template_name = "home/storage/addstoragetype.html"
    title_page = 'Добавление типа накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateStorageType(LoginRequiredMixin, UpdateView):
    model = StorageType
    form_class = AddStorageTypeForm
    template_name = 'home/storage/addstoragetype.html'
    title_page = 'Редактирование типа накопителя памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

'''
Видеокарты
'''

class GetVideocards(ListView):
    template_name = 'home/videocard/videocards.html'
    context_object_name = 'videocards'
    title_page = 'Видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Videocard.objects.all()

class AddVideocard(LoginRequiredMixin, CreateView):
    form_class = AddVideocardForm
    template_name = "home/videocard/addvideocard.html"
    title_page = 'Добавление видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateVideocard(LoginRequiredMixin, UpdateView):
    model = Videocard
    form_class = AddVideocardForm
    template_name = 'home/videocard/addvideocard.html'
    title_page = 'Редактирование видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Модели видеокарт
'''

class GetVideocardModels(ListView):
    template_name = 'home/videocard/videocard_models.html'
    context_object_name = 'videocard_models'
    title_page = 'Модели видеокарт'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return VideocardModel.objects.all()

class AddVideocardModel(LoginRequiredMixin, CreateView):
    form_class = AddVideocardModelForm
    template_name = "home/videocard/addvideocard.html"
    title_page = 'Добавление модели видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateVideocardModel(LoginRequiredMixin, UpdateView):
    model = VideocardModel
    form_class = AddVideocardModelForm
    template_name = 'home/videocard/addvideocard.html'
    title_page = 'Редактирование модели видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Производители видеокарт
'''

class GetVideocardVendors(ListView):
    template_name = 'home/videocard/videocard_vendors.html'
    context_object_name = 'videocard_vendors'
    title_page = 'Производители видеокарт'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return VideocardVendor.objects.all()

class AddVideocardVendor(LoginRequiredMixin, CreateView):
    form_class = AddVideocardVendorForm
    template_name = "home/videocard/addvideocardvendor.html"
    title_page = 'Добавление производителя видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateVideocardVendor(LoginRequiredMixin, UpdateView):
    model = VideocardVendor
    form_class = AddVideocardVendorForm
    template_name = 'home/videocard/addvideocardvendor.html'
    title_page = 'Редактирование производителя видеокарты'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
    
'''
Компьютеры
'''

class GetComputers(ListView):
    template_name = 'home/computer/computers.html'
    context_object_name = 'computers'
    title_page = 'Компьютеры'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Computer.objects.all()
    
'''
Аудитории
'''

class GetAudiences(ListView):
    template_name = 'home/audience/audiences.html'
    context_object_name = 'audiences'
    title_page = 'Аудитории'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Audience.objects.all()
    
class GetAudience(ListView):
    template_name = 'home/audience/audience.html'
    context_object_name = 'audience'
    title_page = 'Аудитория'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        audience_id = self.kwargs['pk']
        audience = Audience.objects.get(pk=audience_id)
        
        # Получаем информацию о компьютерах, привязанных к данной аудитории
        computers = Computer.objects.filter(audience_id=audience_id)
        
        # Добавляем информацию о компьютерах в контекст страницы
        context['title'] = self.title_page
        context['audience'] = audience
        context['computers'] = computers
        return context

    def get_queryset(self):
        return Audience.objects.filter(id=self.kwargs['pk']).first()
    
class GetComputer(ListView):
    template_name = 'home/computer/computer.html'
    context_object_name = 'computer'
    title_page = 'Компьютер'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     computer_id = self.kwargs['invent']
    #     computer = Computer.objects.get(computer_inventory_number=computer_id)
        
    #     # Получаем информацию о компьютерах, привязанных к данной аудитории
    #     #computers = Computer.objects.filter(audience_id=audience_id)
        
    #     # Добавляем информацию о компьютерах в контекст страницы
    #     context['title'] = self.title_page
    #     context['computer'] = computer
    #     #context['computers'] = computers
    #     return context
    
    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        context = super().get_context_data(**kwargs)
        computer = Computer.objects.filter(computer_inventory_number=self.kwargs['invent']).first()
        storage_models = Storage.objects.filter(computer=computer).values('storageModel_id')
        rams = RAM.objects.filter(computer=computer).values('id')
        context['computer'] = computer
        context['monitors'] = Monitor.objects.filter(computer=computer)
        context['rams'] = RAM.objects.filter(computer=computer)
        context['storages'] = Storage.objects.filter(computer=computer)
        context['total_storage_memory'] =round(StorageModel.objects.filter(id__in=storage_models).aggregate(Sum('storage_model_memory'))['storage_model_memory__sum'] / 1024, 2)
        context['ram_memory'] = int(round(RAM.objects.filter(id__in=rams).aggregate(Sum('ram_memory'))['ram_memory__sum'] / 1024, 0))
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Computer.objects.filter(computer_inventory_number=self.kwargs['invent']).first()
    
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

'''
Оперативная память
'''

class GetRAMs(ListView):
    template_name = 'home/ram/rams.html'
    context_object_name = 'rams'
    title_page = 'Оперативная память'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return RAM.objects.all()

class AddRAM(LoginRequiredMixin, CreateView):
    form_class = AddRAMForm
    template_name = "home/ram/addram.html"
    title_page = 'Добавление оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateRAM(LoginRequiredMixin, UpdateView):
    model = RAM
    form_class = AddRAMForm
    template_name = 'home/ram/addram.html'
    title_page = 'Редактирование оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Модели оперативной памяти
'''

class GetRAMModels(ListView):
    template_name = 'home/ram/ram_models.html'
    context_object_name = 'ram_models'
    title_page = 'Модели оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return RAMModel.objects.all()

class AddRAMModel(LoginRequiredMixin, CreateView):
    form_class = AddRAMModelForm
    template_name = "home/ram/addram.html"
    title_page = 'Добавление модели оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateRAMModel(LoginRequiredMixin, UpdateView):
    model = RAMModel
    form_class = AddRAMModelForm
    template_name = 'home/ram/addram.html'
    title_page = 'Редактирование модели оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context
    
'''
Производители оперативной памяти
'''

class GetRAMVendors(ListView):
    template_name = 'home/ram/ram_vendors.html'
    context_object_name = 'ram_vendors'
    title_page = 'Производители оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return RAMVendor.objects.all()

class AddRAMVendor(LoginRequiredMixin, CreateView):
    form_class = AddRAMVendorForm
    template_name = "home/ram/addramvendor.html"
    title_page = 'Добавление производителя оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateRAMVendor(LoginRequiredMixin, UpdateView):
    model = RAMVendor
    form_class = AddRAMVendorForm
    template_name = 'home/ram/addramvendor.html'
    title_page = 'Редактирование производителя оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Типы оперативной памяти
'''

class GetRAMTypes(ListView):
    template_name = 'home/ram/ram_types.html'
    context_object_name = 'ram_types'
    title_page = 'Типы оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return RAMType.objects.all()

class AddRAMType(LoginRequiredMixin, CreateView):
    form_class = AddRAMTypeForm
    template_name = "home/ram/addramtype.html"
    title_page = 'Добавление типа оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateRAMType(LoginRequiredMixin, UpdateView):
    model = RAMType
    form_class = AddRAMTypeForm
    template_name = 'home/ram/addramtype.html'
    title_page = 'Редактирование типа оперативной памяти'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

'''
Мониторы
'''

class GetMonitors(ListView):
    template_name = 'home/monitor/monitors.html'
    context_object_name = 'monitors'
    title_page = 'Мониторы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return Monitor.objects.all()

class AddMonitor(LoginRequiredMixin, CreateView):
    form_class = AddMonitorForm
    template_name = "home/monitor/addmonitor.html"
    title_page = 'Добавление монитора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateMonitor(LoginRequiredMixin, UpdateView):
    model = Monitor
    form_class = AddMonitorForm
    template_name = 'home/monitor/addmonitor.html'
    title_page = 'Редактирование монитора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Модели мониторов
'''

class GetMonitorModels(ListView):
    template_name = 'home/monitor/monitor_models.html'
    context_object_name = 'monitor_models'
    title_page = 'Модели мониторов'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return MonitorModel.objects.all()

class AddMonitorModel(LoginRequiredMixin, CreateView):
    form_class = AddMonitorModelForm
    template_name = "home/monitor/addmonitor.html"
    title_page = 'Добавление модели монитора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateMonitorModel(LoginRequiredMixin, UpdateView):
    model = MonitorModel
    form_class = AddMonitorModelForm
    template_name = 'home/monitor/addmonitor.html'
    title_page = 'Редактирование модели монитора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

'''
Производители мониторов
'''

class GetMonitorVendors(ListView):
    template_name = 'home/monitor/monitor_vendors.html'
    context_object_name = 'monitor_vendors'
    title_page = 'Производители мониторов'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

    def get_queryset(self):
        return MonitorVendor.objects.all()

class AddMonitorVendor(LoginRequiredMixin, CreateView):
    form_class = AddMonitorVendorForm
    template_name = "home/monitor/addmonitorvendor.html"
    title_page = 'Добавление производителя монитора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context

class UpdateMonitorVendor(LoginRequiredMixin, UpdateView):
    model = MonitorVendor
    form_class = AddMonitorVendorForm
    template_name = 'home/monitor/addmonitorvendor.html'
    title_page = 'Редактирование производителя монитора'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title_page
        return context



















#class GetAudienceState(ListView):    
def get_state(request, aud_id):
    if aud_id == 0:
        audience = Audience.objects.none()
    else:
        audience = Audience.objects.filter(id=aud_id).first()
        
    return JsonResponse(audience.audience_state, safe=False)

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def change_state(request):
    if request.method == 'PUT':
        try:
            json_data = json.loads(request.body)
            m = Audience.objects.filter(id=2).first()
            m.audience_state = json_data
            m.save()
            return JsonResponse({'success': True}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)













def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            storage_vendors = df['Производитель накопителя памяти'].tolist()
            for storage_vendor in storage_vendors:
                if StorageVendor.objects.filter(storage_vendor_name=storage_vendor):
                    continue
                StorageVendor.objects.create(storage_vendor_name=storage_vendor)
                #MemoryManufacturer.objects.create(name=manufacturer)
                #print(manufacturer)
            return HttpResponseRedirect('/')  # Redirect after successful upload
    else:
        form = UploadFileForm()
    return render(request, 'home/upload.html', {'form': form})

def upload_filev(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)
            videocard_vendors = df['Производитель видеокарты'].tolist()
            for videocard_vendor in videocard_vendors:
                if VideocardVendor.objects.filter(videocard_vendor_name=videocard_vendor):
                    continue
                VideocardVendor.objects.create(videocard_vendor_name=videocard_vendor)
                #MemoryManufacturer.objects.create(name=manufacturer)
                #print(manufacturer)
            return HttpResponseRedirect('/')  # Redirect after successful upload
    else:
        form = UploadFileForm()
    return render(request, 'home/upload.html', {'form': form})

def success(request):
    return render(request, 'home/success.html')