from rest_framework import serializers
from home.models import CPU, OS, RAM, TV, Audience, AudienceType, CPUModel, ColorPrinting, Computer, Drive, Monitor, MonitorModel, Motherboard, MotherboardModel, OSVersion, PrintType, Printer, PrinterModel, Projector, ProjectorModel, ProjectorType, RAMModel, RAMType, Resolution, ResolutionFormat, Software, SoftwareType, Storage, StorageModel, StorageType, TVModel, TechniqueStatus, TechniqueType, UniversityBody, Vendor, VendorType, Videocard, VideocardModel
from users.models import Task, TaskStatus, User, User_Task, Group
from django.contrib.auth import get_user_model
import helper

class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = ('id', 'name', 'model')
        depth = 2

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = ('id', 'name', 'model')
        depth = 2

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = ('id', 'name', 'model')
        depth = 2

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('name', 'serial_number', 'model')
        depth = 2

class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        fields = ('id', 'letter', 'total_memory', 'free_memory')

class VideocardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videocard
        fields = ('id', 'name', 'model')
        depth = 2

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ('inventory_number', 'name', 'serial_number', 'resolution', 'model')
        depth = 2

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = ('inventory_number', 'name', 'arch', 'technique_type_id', 'audience', 'status')
        depth = 1

    def to_representation(self, value):
        data = super().to_representation(value)
        if isinstance(value, Computer):
            data['motherboard'] = MotherboardSerializer(value.motherboard_set.first()).data
            data['cpu'] = CPUSerializer(value.cpu_set.first()).data
            data['rams'] = RAMSerializer(value.ram_set, many=True).data
            data['storages'] = StorageSerializer(value.storage_set, many=True).data
            data['drives'] = DriveSerializer(value.drive_set, many=True).data
            data['videocards'] = VideocardSerializer(value.videocard_set, many=True).data
            data['monitors'] = MonitorSerializer(value.monitor_set, many=True).data

        return data

class ProjectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projector
        fields = ('inventory_number', 'name', 'model', 'with_remote_controller', 'year_of_production', 'audience', 'status', 'technique_type_id')
        depth = 2

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('inventory_number', 'name', 'model', 'is_networking', 'year_of_production', 'audience', 'color_printing', 'print_type', 'status', 'technique_type_id')
        depth = 2

class TechniqueSerializer(serializers.Serializer):
    motherboard = MotherboardSerializer()
    cpu = CPUSerializer()
    rams = RAMSerializer(many=True)
    storages = StorageSerializer(many=True)
    drives = DriveSerializer(many=True)
    videocards = VideocardSerializer(many=True)
    monitors = MonitorSerializer(many=True)
    computer = ComputerSerializer()

class MotherboardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherboardModel
        fields = ('id', 'name')

class CPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUModel
        fields = ('id', 'name')

class StorageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModel
        fields = ('id', 'name')

class RAMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMModel
        fields = ('id', 'name')

class VideocardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideocardModel
        fields = ('id', 'name')

class MonitorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorModel
        fields = ('id', 'name')

class ProjectorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectorModel
        fields = ('id', 'name')

class PrinterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterModel
        fields = ('id', 'name')

class TVModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVModel
        fields = ('id', 'name')

class AnalyzeComputerSerializer(serializers.Serializer):
    ram = serializers.FloatField(allow_null=True)
    cores = serializers.IntegerField(allow_null=True)
    with_videocard = serializers.BooleanField()
    os_name = serializers.CharField(allow_null=True, allow_blank=True)
    softwares = serializers.ListField(child=serializers.CharField(allow_blank=True))
    video_memory = serializers.FloatField(allow_null=True)

class AnalyzeAudienceSerializer(serializers.Serializer):
    max_computers = serializers.IntegerField(allow_null=True)
    max_places = serializers.IntegerField(allow_null=True)
    with_projector = serializers.BooleanField()

class RequestSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField()
    
    def validate_owner_id(self, value):
        if not value:
            raise serializers.ValidationError("custom_field не может быть пустым")
        return value

    class Meta:
        model = Task
        fields = ['title', 'message', 'computer', 'printer', 'projector', 'tv', 'users', 'status', 'owner_id']
    
    def create(self, validated_data):
        owner = get_user_model().objects.get(id=validated_data.get('owner_id'))
        instance = Task.objects.create(title=validated_data.get('title'), 
                                       message=validated_data.get('message'),
                                       computer=validated_data.get('computer'),
                                       projector=validated_data.get('projector'),
                                       printer=validated_data.get('printer'),
                                       tv=validated_data.get('tv'),
                                       status=validated_data.get('status'))

        technique = validated_data.get('computer')
        if not technique:
            technique = validated_data.get('printer')
            if not technique:
                technique = validated_data.get('projector')
                if not technique:
                    technique = validated_data.get('tv')

        if technique.technique_type.id == TechniqueType.Type.COMPUTER:
            instance.computer = technique
            instance.status_id = TaskStatus.Status.IN_PROGRESS
            instance.save()
            users = technique.UsersComputers.all()
            
            helper.create_or_update_user_task(users, [], instance, technique.inventory_number, owner)

            return instance
        
        if technique.technique_type.id == TechniqueType.Type.PROJECTOR:
            instance.projector = technique
            instance.status_id = TaskStatus.Status.IN_PROGRESS
            instance.save()
            users = technique.UsersProjectors.all()
            
            helper.create_or_update_user_task(users, [], instance, technique.inventory_number, owner)
            return instance
        
        if technique.technique_type.id == TechniqueType.Type.PRINTER or technique.technique_type.id == TechniqueType.Type.MFU:
            instance.printer = technique
            instance.status_id = TaskStatus.Status.IN_PROGRESS
            instance.save()
            users = technique.UsersPrinters.all()
            
            helper.create_or_update_user_task(users, [], instance, technique.inventory_number, owner)
            return instance
        
        if technique.technique_type.id == TechniqueType.Type.TV:
            instance.tv = technique
            instance.status_id = TaskStatus.Status.IN_PROGRESS
            instance.save()
            users = technique.UsersTVs.all()
            
            helper.create_or_update_user_task(users, [], instance, technique.inventory_number, owner)
            return instance
        return instance

class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ['id', 'name', 'state', 'photo']

class StorageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageType
        fields = '__all__'

class RAMTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAMType
        fields = '__all__'

class TechniqueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueStatus
        fields = '__all__'

class ResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolution
        fields = '__all__'

class ResolutionFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResolutionFormat
        fields = '__all__'

class UniversityBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityBody
        fields = '__all__'

class AudienceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudienceType
        fields = '__all__'

class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = '__all__'

class SoftwareTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareType
        fields = '__all__'

class PrintTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintType
        fields = '__all__'

class ColorPrintingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorPrinting
        fields = '__all__'

class ProjectorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectorType
        fields = '__all__'

class TechniqueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueType
        fields = '__all__'

class TVSerializer(serializers.ModelSerializer):
    class Meta:
        model = TV
        fields = ('inventory_number', 'name', 'model', 'diagonal', 'year_of_production', 'audience', 'status', 'technique_type_id')
        depth = 2

class OSSerializer(serializers.ModelSerializer):
    class Meta:
        model = OS
        fields = '__all__'

class OSVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OSVersion
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'