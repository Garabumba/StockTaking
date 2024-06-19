import json
import os
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
import pandas as pd
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from django.conf import settings

from users.models import Task, TaskStatus, User
from .serializers import AnalyzeAudienceSerializer, AnalyzeComputerSerializer, AudienceSerializer, AudienceTypeSerializer, CPUModelSerializer, CPUSerializer, ColorPrintingSerializer, ComputerSerializer, DriveSerializer, MonitorModelSerializer, MonitorSerializer, MotherboardModelSerializer, MotherboardSerializer, OSSerializer, OSVersionSerializer, PrintTypeSerializer, PrinterModelSerializer, PrinterSerializer, ProjectorModelSerializer, ProjectorSerializer, ProjectorTypeSerializer, RAMModelSerializer, RAMSerializer, RAMTypeSerializer, RequestSerializer, ResolutionSerializer, SoftwareSerializer, SoftwareTypeSerializer, StorageModelSerializer, StorageSerializer, StorageTypeSerializer, TVModelSerializer, TVSerializer, TaskSerializer, TechniqueStatusSerializer, TechniqueTypeSerializer, UniversityBodySerializer, UserSerializer, VendorSerializer, VideocardModelSerializer, VideocardSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError as DRFValidationError
from django.db.models import ProtectedError
from itertools import chain
import helper

from home.models import CPU, OS, RAM, TV, Audience, AudienceType, CPUModel, ColorPrinting, Computer, Drive, Monitor, MonitorModel, Motherboard, MotherboardModel, OS_Computer, OSVersion, PrintType, Printer, PrinterModel, Projector, ProjectorModel, ProjectorType, RAMModel, RAMType, Resolution, ResolutionFormat, Software, SoftwareType, Storage, StorageModel, StorageType, TVModel, TechniqueStatus, TechniqueType, UniversityBody, Vendor, VendorType, Videocard, VideocardModel

class MotherboardModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_motherboard_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = MotherboardModelSerializer(MotherboardModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class CPUModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_cpu_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = CPUModelSerializer(CPUModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class StorageModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_storage_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = StorageModelSerializer(StorageModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)

class RAMModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_ram_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = RAMModelSerializer(RAMModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class VideocardModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_videocard_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = VideocardModelSerializer(VideocardModel.objects.filter(vendor__id=vendor_id), many=True)
        return Response(serializer.data)
    
class MonitorModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_monitor_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = MonitorModelSerializer(MonitorModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class ProjectorModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_projector_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = ProjectorModelSerializer(ProjectorModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class PrinterModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_printer_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = PrinterModelSerializer(PrinterModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class TVModelsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        if not request.user.has_perm('home.view_tv_model'):
            return JsonResponse({'success': False}, status=403)
        
        serializer = TVModelSerializer(TVModel.objects.filter(vendor_id=vendor_id), many=True)
        return Response(serializer.data)
    
class TechniqueList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        inventory_number = request.GET.get('inventory_number')
        serializer = None
        try:
            technique = helper.get_technique_by_inventory_number(inventory_number)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': "invalid 'inventory_number'"})

        if inventory_number is None:
            return JsonResponse({'success': False, 'message': "param 'inventory_number' is required"}, status=400)
        
        if technique.technique_type.id == TechniqueType.Type.COMPUTER:
            serializer = ComputerSerializer(technique)
        elif technique.technique_type.id == TechniqueType.Type.PROJECTOR:
            serializer = ProjectorSerializer(technique)
        elif technique.technique_type.id == TechniqueType.Type.PRINTER or technique.technique_type.id == TechniqueType.Type.MFU:
            serializer = PrinterSerializer(technique)
        elif technique.technique_type.id == TechniqueType.Type.TV:
            serializer = TVSerializer(technique)
        return Response(serializer.data)
    
class Analyze(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        res = {}
        situable_elements = []
        analizing_type = request.GET.get('analizing_type', 'computers')

        if analizing_type == 'computers':
            serializer = AnalyzeComputerSerializer(data=request.data)

            if serializer.is_valid():
                ram = serializer.validated_data.get('ram')
                cores = serializer.validated_data.get('cores')
                with_videocard = serializer.validated_data.get('with_videocard')
                video_memory = serializer.validated_data.get('video_memory')
                os = serializer.validated_data.get('os_name')
                softwares = serializer.validated_data.get('softwares')
            else:
                return JsonResponse({'errors': serializer.errors}, status=400)

            for computer in Computer.objects.all():
                if _is_situable_computer(computer, cores, ram, with_videocard, os, softwares, video_memory):
                    situable_elements.append({'name': computer.inventory_number, 'audience': computer.audience})
            
            for item in situable_elements:
                audience = str(item['audience']) if item['audience'] else "Без аудитории"
                
                if audience not in res:
                    res[audience] = {'computers': [], 'count': 0, 'total_count': Computer.objects.filter(audience=None if audience == 'Без аудитории' else item['audience'].id).count()}
                res[audience]['computers'].append(item['name'])
                res[audience]['count'] += 1
        elif analizing_type == 'audiences':
            serializer = AnalyzeAudienceSerializer(data=request.data)

            if serializer.is_valid():
                max_computers = serializer.validated_data.get('max_computers')
                max_places = serializer.validated_data.get('max_places')
                with_projector = serializer.validated_data.get('with_projector')
            else:
                return JsonResponse({'errors': serializer.errors}, status=400)
            
            for audience in Audience.objects.all():
                if _is_situable_audience(audience, max_computers, max_places, with_projector):
                    situable_elements.append({'university_body': audience.university_body.name, 'audience': audience.name, 'audience_id': audience.id })

            for item in situable_elements:
                university_body = str(item['university_body']) if item['university_body'] else "None"
                if university_body not in res:
                    res[university_body] = {'audiences': []}
                res[university_body]['audiences'].append({'id': item['audience_id'], 'name': item['audience']})

        return JsonResponse({"result": res}, status=200)

class CreateRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_title = request.data.get('request').get('title')
        request_message = request.data.get('request').get('message')
        request_inventory_number = request.data.get('request').get('inventory_number')

        technique = helper.get_technique_by_inventory_number(request_inventory_number)
        
        if technique.technique_type.id == TechniqueType.Type.COMPUTER:
            data = {
                'title': request_title,
                'message': request_message,
                'computer': technique,
                'projector': None,
                'printer': None,
                'tv': None,
                'owner_id': request.user.id,
            }
        elif technique.technique_type.id == TechniqueType.Type.PROJECTOR:
            data = {
                'title': request_title,
                'message': request_message,
                'computer': None,
                'projector': technique,
                'printer': None,
                'tv': None,
                'owner_id': request.user.id,
            }
        elif technique.technique_type.id == TechniqueType.Type.PRINTER or technique.technique_type.id == TechniqueType.Type.MFU:
            data = {
                'title': request_title,
                'message': request_message,
                'computer': None,
                'projector': None,
                'printer': technique,
                'tv': None,
                'owner_id': request.user.id,
            }
        elif technique.technique_type.id == TechniqueType.Type.TV:
            data = {
                'title': request_title,
                'message': request_message,
                'computer': None,
                'projector': None,
                'printer': None,
                'tv': technique,
                'owner_id': request.user.id,
            }

        serializer = RequestSerializer(data=data)
        
        if serializer.is_valid():
            req = serializer.save()
            
        else:
            print(serializer.errors)
        return JsonResponse({'success': True}, status=200)

class GetState(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):        
        serializer = AudienceSerializer(Audience.objects.get(id=pk))
        return Response(serializer.data)
    
class ChangeState(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        serializer = AudienceSerializer(Audience.objects.get(id=pk), data={'state': request.data})
        if serializer.is_valid():
            serializer.update(instance=Audience.objects.get(id=pk), validated_data={'state': request.data})
            return JsonResponse({"succcess": True})
                
        return JsonResponse({"succcess": True})

class DeleteMotherboardModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = MotherboardModel.objects.all()
    serializer_class = MotherboardModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_motherboard_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к материнским платам: {", ".join(Motherboard.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteMotherboard(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Motherboard.objects.all()
    serializer_class = MotherboardSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_motherboard'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная материнская плата привязана к компьютеру: {instance.computer}')

class DeleteCPUModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CPUModel.objects.all()
    serializer_class = CPUModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_cpu_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к процессорам: {", ".join(CPU.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteCPU(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CPU.objects.all()
    serializer_class = CPUSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_cpu'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный процессор привязан к компьютеру: {instance.computer}')
        
class DeleteStorageModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = StorageModel.objects.all()
    serializer_class = StorageModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_storage_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к накопителям памяти: {", ".join(Storage.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteStorage(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_storage'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный накопитель памяти привязан к компьютеру: {instance.computer}')
        
class DeleteStorageType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = StorageType.objects.all()
    serializer_class = StorageTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_storage'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный тип накопителя памяти привязан к моделям накопителей памяти: {", ".join(StorageModel.objects.filter(type__id=instance.id).values_list("name", flat=True))}')
        
class DeleteVideocardModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = VideocardModel.objects.all()
    serializer_class = VideocardModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_videocard_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к видеокартам: {", ".join(Videocard.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteVideocard(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Videocard.objects.all()
    serializer_class = VideocardSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_videocard'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная видеокарта привязана к компьютеру: {instance.computer}')

class DeleteRAMModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = RAMModel.objects.all()
    serializer_class = RAMModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_ram_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к оперативной памяти: {", ".join(RAM.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteRAM(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = RAM.objects.all()
    serializer_class = RAMSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_ram'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная оперативная память привязана к компьютеру: {instance.computer}')
        
class DeleteRAMType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = RAMType.objects.all()
    serializer_class = RAMTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_ram'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный тип оперативной памяти привязан к оперативной памяти: {", ".join(RAM.objects.filter(type__id=instance.id).values_list("name", flat=True))}')
        
class DeleteComputer(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_computer'):
            raise PermissionDenied("Недостаточно прав")
        #try:
        instance.delete()
        #except ProtectedError:
        #    raise DRFValidationError(f'Данный накопитель памяти привязан к компьютеру: {instance.computer}')

class DeleteTechniqueStatus(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = TechniqueStatus.objects.all()
    serializer_class = TechniqueStatusSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_technique_status'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError: #ДОДЕЛАТЬ!
            technique = list(chain(Computer.objects.filter(status__id=instance.id).values_list('inventory_number', flat=True), Printer.objects.filter(status__id=instance.id).values_list('inventory_number', flat=True), Projector.objects.filter(status__id=instance.id).values_list('inventory_number', flat=True), TV.objects.filter(status__id=instance.id).values_list('inventory_number', flat=True), Monitor.objects.filter(status__id=instance.id).values_list('inventory_number', flat=True)))
            raise DRFValidationError(f'Данный статус привязан к технике: {", ".join(technique)}')
        
class DeleteResolution(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Resolution.objects.all()
    serializer_class = ResolutionSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_resolution'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данное разрешение привязано к монитроам: {", ".join(Monitor.objects.filter(resolution__id=instance.id).values_list("name", flat=True))}')
        
class DeleteMonitorModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = MonitorModel.objects.all()
    serializer_class = MonitorModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_monitor_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к монитрам: {", ".join(Monitor.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteMonitor(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_monitor'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный монитор привязан к компьютеру: {instance.monitor}')
        
class DeleteUniversityBody(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = UniversityBody.objects.all()
    serializer_class = UniversityBodySerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_university_body'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный корпус привязан к аудиториям: {", ".join(Audience.objects.filter(university_body__id=instance.id).values_list("name", flat=True))}')
        
class DeleteAudience(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_audience'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЕЛАТЬ!
            technique = list(chain(Computer.objects.filter(audience__id=instance.id).values_list('inventory_number', flat=True), Printer.objects.filter(audience__id=instance.id).values_list('inventory_number', flat=True), Projector.objects.filter(audience__id=instance.id).values_list('inventory_number', flat=True), TV.objects.filter(audience__id=instance.id).values_list('inventory_number', flat=True)))
            raise DRFValidationError(f'В данной аудитории находится техника: {", ".join(technique)}')
        
class DeleteAudienceType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = AudienceType.objects.all()
    serializer_class = AudienceTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_audience'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный тип аудитории привязан к аудиториям: {", ".join(Audience.objects.filter(type__id=instance.id).values_list("name", flat=True))}')

class DeleteSoftware(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_software'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данное программное обеспеченние привязано к компьютерам: \"{",".join(instance.computer.values_list('name', flat=True))}\"')

class DeleteSoftwareType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = SoftwareType.objects.all()
    serializer_class = SoftwareTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_software'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный тип программного обеспечния привязан к программному обеспечению: {", ".join(Software.objects.filter(type__id=instance.id).values_list("name", flat=True))}')
        
class DeleteDrive(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Drive.objects.all()
    serializer_class = DriveSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_drive'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный раздел памяти привязан к компьютеру: {instance.computer}')
        
class DeletePrintType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = PrintType.objects.all()
    serializer_class = PrintTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_print'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЕЛАТЬ!
            raise DRFValidationError(f'Данный тип печати привязан к технике: {", ".join(Printer.objects.filter(print_type__id=instance.id).values_list("inventory_number", flat=True))}')
        
class DeleteColorPrinting(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ColorPrinting.objects.all()
    serializer_class = ColorPrintingSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_color_printing'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЕЛАТЬ!
            raise DRFValidationError(f'Даннпя цветность печати привязан к технике: {", ".join(Printer.objects.filter(color_printing__id=instance.id).values_list("inventory_number", flat=True))}')
        
class DeletePrinterModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = PrinterModel.objects.all()
    serializer_class = PrinterModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_printer_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЕЛАТЬ
            raise DRFValidationError(f'Данная модель привязана к технике: {", ".join(Printer.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeletePrinter(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_printer'):
            raise PermissionDenied("Недостаточно прав")
        instance.delete()

class DeleteProjectorModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ProjectorModel.objects.all()
    serializer_class = ProjectorModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_projector_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к проекторам: {", ".join(Projector.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteProjector(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Projector.objects.all()
    serializer_class = ProjectorSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_projector'):
            raise PermissionDenied("Недостаточно прав")
        instance.delete()

class DeleteProjectorType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ProjectorType.objects.all()
    serializer_class = ProjectorTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_projector_type'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данный тип проектора привязан к проекторам: {", ".join(Projector.objects.filter(type__id=instance.id).values_list("name", flat=True))}')

class DeleteTechniqueType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = TechniqueType.objects.all()
    serializer_class = TechniqueTypeSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_technique_type'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЕЛАТЬ!
            technique = list(chain(Computer.objects.filter(technique__id=instance.id).values_list('inventory_number', flat=True), Printer.objects.filter(technique__id=instance.id).values_list('inventory_number', flat=True), Projector.objects.filter(technique__id=instance.id).values_list('inventory_number', flat=True), TV.objects.filter(technique__id=instance.id).values_list('inventory_number', flat=True), Monitor.objects.filter(technique__id=instance.id).values_list('inventory_number', flat=True)))
            raise DRFValidationError(f'Данный тип техники привязан к технике: {", ".join(technique)}')

class DeleteTVModel(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = TVModel.objects.all()
    serializer_class = TVModelSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_tv_model'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(f'Данная модель привязана к телевизорам: {", ".join(TV.objects.filter(model__id=instance.id).values_list("name", flat=True))}')

class DeleteTV(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = TV.objects.all()
    serializer_class = TVSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_tv'):
            raise PermissionDenied("Недостаточно прав")
        instance.delete()
        
class DeleteOS(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = OS.objects.all()
    serializer_class = OSSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_os'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЕЛАТЬ!
            raise DRFValidationError(f'Данная операционная систем привязана к компьютерам: {OS_Computer.objects.filter(os__id=instance.id).values_list("computer", flat=True)}')
        
class DeleteOSVersion(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = OSVersion.objects.all()
    serializer_class = OSVersionSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_os_version'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЛЕАТЬ!
            raise DRFValidationError(f'Данная версия ОС привязана к ОС: {instance.os_version}')
        
class DeleteVendor(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_vendor'):
            raise PermissionDenied("Недостаточно прав")
        try:
            instance.delete()
        except ProtectedError:#ДОДЛЕАТЬ!
            related_models = {
                VendorType.Type.CPU: CPUModel,
                VendorType.Type.MONITOR: MonitorModel,
                VendorType.Type.MOTHERBOARD: MotherboardModel,
                VendorType.Type.PRINTER: PrinterModel,
                VendorType.Type.PROJECTOR: ProjectorModel,
                VendorType.Type.RAM: RAMModel,
                VendorType.Type.SOFTWARE: Software,
                VendorType.Type.STORAGE: StorageModel,
                VendorType.Type.TV: TVModel,
                VendorType.Type.VIDEOCARD: VideocardModel,
            }
            related_objects = []

            for vendor_type in instance.vendor_type.all():
                model = related_models.get(vendor_type.id)
                if model:
                    related_objects.extend(
                        model.objects.filter(vendor=instance).values_list('name', flat=True)
                    )
            raise DRFValidationError(f'Данный производитель привязан к: {", ".join(related_objects)}')
        
class DeleteTask(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('home.delete_task'):
            raise PermissionDenied("Недостаточно прав")
        if instance.status_id == TaskStatus.Status.FINISHED:
            instance.delete()
        else:
            raise DRFValidationError(f'Данная задача имеет статус: {instance.status}')
        
class DeleteComputer(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer

    def perform_destroy(self, instance):
        delete_related = self.request.query_params.get('delete_related', 'false').lower() == 'true'
        if delete_related:
            instance.motherboard_set.all().delete()
            instance.cpu_set.all().delete()
            instance.storage_set.all().delete()
            instance.videocard_set.all().delete()
            instance.ram_set.all().delete()
            instance.monitor_set.all().delete()
        instance.delete()

class DeleteLinkedTechnique(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        technique_type = self.kwargs.get('technique_type')
        if technique_type == TechniqueType.Type.COMPUTER:
            return Computer.objects.all()
        elif technique_type == TechniqueType.Type.PRINTER or technique_type == TechniqueType.Type.MFU:
            return Printer.objects.all()
        elif technique_type == TechniqueType.Type.PROJECTOR:
            return Projector.objects.all()
        elif technique_type == TechniqueType.Type.MONITOR:
            return Monitor.objects.all()
        elif technique_type == TechniqueType.Type.TV:
            return TV.objects.all()

    def get_serializer_class(self):
        technique_type = self.kwargs.get('technique_type')
        if technique_type == TechniqueType.Type.COMPUTER:
            return ComputerSerializer
        elif technique_type == TechniqueType.Type.PRINTER or technique_type == TechniqueType.Type.MFU:
            return PrinterSerializer
        elif technique_type == TechniqueType.Type.PROJECTOR:
            return ProjectorSerializer
        elif technique_type == TechniqueType.Type.MONITOR:
            return MonitorSerializer
        elif technique_type == TechniqueType.Type.TV:
            return TVSerializer
        
    def perform_destroy(self, instance):
        technique_type = self.kwargs.get('technique_type')
        if technique_type == TechniqueType.Type.COMPUTER:
            self.request.user.computers.remove(instance)
        elif technique_type == TechniqueType.Type.PRINTER or technique_type == TechniqueType.Type.MFU:
            self.request.user.printers.remove(instance)
        elif technique_type == TechniqueType.Type.PROJECTOR:
            self.request.user.projectors.remove(instance)
        elif technique_type == TechniqueType.Type.MONITOR:
            self.request.user.monitors.remove(instance)
        elif technique_type == TechniqueType.Type.TV:
            self.request.user.tvs.remove(instance)

class DeleteUser(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UploadVendors(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
        except Exception as ex:
            return JsonResponse({"success": False, "message": str(ex)}, status=400)
        result = []
        errors = []
        all_vendor_types = VendorType.objects.values_list('name', flat=True)
        
        for new_vendor in df.to_dict(orient='records'):
            vendor_types = VendorType.objects.filter(name__in=new_vendor['Типы производителей'].split(','))
            vendor, vendor_created = Vendor.objects.get_or_create(name=new_vendor['Производитель'])
            vendor.vendor_type.set(vendor_types)
            if vendor_created:
                result.append({'vendor': str(vendor), 'vendor_types': list(vendor_types.values_list('name', flat=True))})

            for vendor_type in new_vendor['Типы производителей'].split(','):
                if vendor_type.strip() not in all_vendor_types:
                    errors.append(f"Не создали производителя '{vendor}' для '{vendor_type}', так как не нашли такой тип производителя")

        if errors:
            return JsonResponse({'success': True, 'created': result, 'errors': errors}, status=207)
        
        return JsonResponse({"succcess": True, "created": result})

class UploadUsers(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
        except Exception as ex:
            return JsonResponse({"success": False, "message": str(ex)}, status=400)
        result = []
        errors = []
        email_validator = EmailValidator()

        for user in df.to_dict(orient='records'):
            name = user['Имя']
            surname = user['Фамилия']
            lastname = user['Отчество']
            login = user['Логин']
            email = user['Почта']
            password = user['Пароль']
            group_name = user['Роль']

            try:
                email_validator(email)
            except ValidationError:
                errors.append(f'Некорректный e-mail для пользователя {login}: {email}')
                continue

            try:
                validate_password(password)
            except ValidationError as e:
                errors.append(f'Некорректный пароль для пользователя {login}: {"; ".join(e.messages)}')
                continue

            if get_user_model().objects.filter(email=email).exists():
                errors.append(f'Пользователь с e-mail: {email} уже существует')
                continue

            if get_user_model().objects.filter(username=login).exists():
                errors.append(f'Пользователь с логином: {login} уже существует')
                continue

            new_user = get_user_model()(first_name=name, last_name=surname, patronymic=lastname, email=email, username=login)
            new_user.set_password(password)
            new_user.save()

            if group_name:
                try:
                    group = Group.objects.get(name=group_name)
                    new_user.groups.add(group)
                    new_user.save()
                except:
                    errors.append(f'Роль: {group_name} не найдена. Пользователь: {str(new_user)} создан без роли')
            
            result.append(new_user)

        if errors:
            return JsonResponse({'success': True, 'created': [str(u) for u in result], 'errors': errors}, status=207)
        
        return JsonResponse({'success': True, 'created': [str(u) for u in result]}, status=200)
    
class UploadUserTechnique(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
        except Exception as ex:
            return JsonResponse({"success": False, "message": str(ex)}, status=400)
        result = []
        errors = []

        for user in df.to_dict(orient='records'):
            user_login_or_email = user['Логин/Почта']
            inventory_number = user['Инвентарный номер']
            try:
                current_user = get_user_model().objects.get(username=user_login_or_email)
            except ObjectDoesNotExist:
                try:
                    current_user = get_user_model().objects.get(email=user_login_or_email)
                except ObjectDoesNotExist:
                    errors.append(f'Не нашли пользователя с логином/почтой: {user_login_or_email}')
                    continue

            if not current_user.groups.first().is_responsible or not current_user.groups.first():
                errors.append(f'Роль: {current_user.groups.first()} у пользователя: {current_user} не подразумевает прикрепления к технике')
                continue

            if Computer.objects.filter(inventory_number=inventory_number, UsersComputers__groups=current_user.groups.first()).exists():
                errors.append(f'Компьютер с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                continue
            if Printer.objects.filter(inventory_number=inventory_number, UsersPrinters__groups=current_user.groups.first()).exists():
                errors.append(f'Принтер с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                continue
            if Projector.objects.filter(inventory_number=inventory_number, UsersProjectors__groups=current_user.groups.first()).exists():
                errors.append(f'Проектор с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                continue
            if TV.objects.filter(inventory_number=inventory_number, UsersTVs__groups=current_user.groups.first()).exists():
                errors.append(f'Телевизор с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                continue

            try:
                technique = helper.get_technique_by_inventory_number(inventory_number)
            except ObjectDoesNotExist:
                errors.append(f'Не нашли технику с инвентарным номером: {inventory_number}')

            if technique.technique_type.id == TechniqueType.Type.COMPUTER:
                current_user.computers.add(technique)
            if technique.technique_type.id == TechniqueType.Type.PRINTER:
                current_user.printers.add(technique)
            if technique.technique_type.id == TechniqueType.Type.PROJECTOR or technique.technique_type == TechniqueType.Type.MFU:
                current_user.projectors.add(technique)
            if technique.technique_type.id == TechniqueType.Type.TV:
                current_user.tvs.add(technique)
                
            current_user.save()
            result.append(current_user)

        if errors:
            return JsonResponse({'success': True, 'created': [str(u) for u in result], 'errors': errors}, status=207)
        
        return JsonResponse({'success': True, 'created': [str(u) for u in result]}, status=200)
    
class UploadAudiences(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
        except Exception as ex:
            return JsonResponse({"success": False, "message": str(ex)}, status=400)
        result = []
        errors = []

        for audience in df.to_dict(orient='records'):
            name = audience['Название']
            audience_type = audience['Тип']
            university_body = audience['Корпус']
            max_computers = audience['Максимальное количество компьютеров']
            max_places = audience['Вместимость (чел)']

            current_audience_type, current_audience_type_created = AudienceType.objects.get_or_create(name=audience_type)
            
            try:
                current_university_body = UniversityBody.objects.get(name=university_body.strip())
            except ObjectDoesNotExist:
                errors.append(f"Не нашли корпус: '{university_body}' для аудитории: '{name}'")
                continue

            try:
                max_computers = int(max_computers)
            except:
                errors.append(f'Некорректное максимальное количество компьютеров: {max_computers}')
                continue

            try:
                max_places = int(max_places)
            except:
                errors.append(f'Некорректная вместимость: {max_places}')
                continue

            result.append(Audience(name=name, type=current_audience_type, university_body=current_university_body, max_computers=max_computers, max_places=max_places))
            
        Audience.objects.bulk_create(result)

        if errors:
            return JsonResponse({'success': True, 'created': [str(u) for u in result], 'errors': errors}, status=207)
        
        return JsonResponse({'success': True, 'created': [str(u) for u in result]}, status=200)

class UploadResolutions(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
        except Exception as ex:
            return JsonResponse({"success": False, "message": str(ex)}, status=400)

        resolutions_to_create = []
        errors = []

        for index, row in df.iterrows():
            resolution_name = row['Разрешение']
            resolution_format_name = row['Соотношение сторон']

            try:
                resolution = Resolution.objects.get(name=resolution_name)
            except ObjectDoesNotExist:
                try:
                    resolution_format = ResolutionFormat.objects.get(name=resolution_format_name)
                    resolutions_to_create.append(Resolution(name=resolution_name, resolution_format=resolution_format))
                except ObjectDoesNotExist:
                    errors.append(f"Не создали разрешение '{resolution_name}', т.к. не нашли соотношение сторон '{resolution_format_name}'")
                    continue

        if resolutions_to_create:
            Resolution.objects.bulk_create(resolutions_to_create)
            result = [{'resolution': res.name, 'resolution_format': str(res.resolution_format)} for res in resolutions_to_create]
        else:
            result = []

        response_data = {'success': True, 'created': result}
        if errors:
            response_data['errors'] = errors
            return JsonResponse(response_data, status=207)

        return JsonResponse(response_data, status=200)
    
class UploadResolutionFormats(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)
        except Exception as ex:
            return JsonResponse({"success": False, "message": str(ex)}, status=400)

        errors = []
        resolution_format_to_create = []

        for resolution_format in set(df['Соотношение сторон'].tolist()):
            #try:
            #    ResolutionFormat.objects.get(name=resolution_format)
            #    continue
            #except ObjectDoesNotExist:
            resolution_format_to_create.append(ResolutionFormat(name=resolution_format))

        if resolution_format_to_create:
            ResolutionFormat.objects.bulk_create(resolution_format_to_create, ignore_conflicts=True)
            result = [{'resolution_format': str(res_format.name)} for res_format in resolution_format_to_create]
        else:
            result = []

        response_data = {'success': True, 'created': result}
        if errors:
            response_data['errors'] = errors
            return JsonResponse(response_data, status=207)

        return JsonResponse(response_data, status=200)

class DownloadUsersTemplate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'templates_files', 'users_template.xlsx')
        return _download_template(file_path, 'users_template.xlsx')

class DownloadVendorsTemplate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'templates_files', 'vendors_template.xlsx')
        return _download_template(file_path, 'vendors_template.xlsx')

class DownloadUsersTechniqueTemplate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'templates_files', 'users_technique_template.xlsx')
        return _download_template(file_path, 'users_technique_template.xlsx')
    
class DownloadAudiencesTemplate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'templates_files', 'audiences_template.xlsx')
        return _download_template(file_path, 'audiences_template.xlsx')

def _download_template(file_path, filename):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
    else:
        return HttpResponse(status=404)

def _is_situable_computer(computer, cores, total_memory, with_videocard, os, softwares, video_memory):
    is_searched = False

    if cores:
        is_searched = helper.compare_cores(computer, cores)
        if not is_searched:
            return False
    
    if total_memory:
        is_searched = helper.compare_memory(computer, total_memory)
        if not is_searched:
            return False
    
    is_searched = helper.computer_have_videocard(computer, with_videocard)
    if not is_searched:
        return False
    
    if os:
        is_searched = helper.compare_os(computer, os)
        if not is_searched:
            return False
    
    if len(softwares) > 0:
        is_searched = helper.computer_contains_software(computer, softwares)
        if not is_searched:
            return False
        
    if video_memory:
        is_searched = helper.compare_video_memory(computer, video_memory)
        if not is_searched:
            return False

    return True

def _is_situable_audience(audience, max_computers, max_places, with_projector):
    is_searched = True

    is_searched = helper.compare_computers_count_and_places(audience, max_computers, max_places)
    if not is_searched:
        return False
    
    is_searched = helper.audience_have_projector(audience, with_projector)

    return is_searched