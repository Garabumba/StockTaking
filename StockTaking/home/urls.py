#from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('test', views.test, name='test'),
    path('motherboards/', views.GetMotherboards.as_view(), name='motherboards'),
    path('motherboards/add_motherboard/', views.AddMotherboard.as_view(), name='add_motherboard'),
    path('motherboards/<int:pk>/edit_motherboard/', views.UpdateMotherboard.as_view(), name='edit_motherboard'),
    ############################################################################################################
    path('motherboard_models/', views.GetMotherboardModels.as_view(), name='motherboard_models'),
    path('motherboard_models/add_motherboard_model/', views.AddMotherboardModel.as_view(), name='add_motherboard_model'),
    path('motherboard_models/<int:pk>/edit_motherboard_model/', views.UpdateMotherboardModel.as_view(), name='edit_motherboard_model'),
    ############################################################################################################
    path('motherboard_vendors/', views.GetMotherboardVendors.as_view(), name='motherboard_vendors'),
    path('motherboard_vendors/add_motherboard_vendor/', views.AddMotherboardVendor.as_view(), name='add_motherboard_vendor'),
    path('motherboard_vendors/<int:pk>/edit_motherboard_vendor/', views.UpdateMotherboardVendor.as_view(), name='edit_motherboard_vendor'),
    ############################################################################################################
    path('cpu_models/', views.GetCPUModels.as_view(), name='cpu_models'),
    path('cpu_models/add_cpu_model/', views.AddCPUModel.as_view(), name='add_cpu_model'),
    path('cpu_models/<int:pk>/edit_cpu_model/', views.UpdateCPUModel.as_view(), name='edit_cpu_model'),
    ############################################################################################################
    path('cpu_vendors/', views.GetCPUVendors.as_view(), name='cpu_vendors'),
    path('cpu_vendors/add_cpu_vendor/', views.AddCPUVendor.as_view(), name='add_cpu_vendor'),
    path('cpu_vendors/<int:pk>/edit_cpu_vendor/', views.UpdateCPUVendor.as_view(), name='edit_cpu_vendor'),
    ############################################################################################################
    path('cpus/', views.GetCPUs.as_view(), name='cpus'),
    path('cpus/add_cpu/', views.AddCPU.as_view(), name='add_cpu'),
    path('cpus/<int:pk>/edit_cpu/', views.UpdateCPU.as_view(), name='edit_cpu'),
    path('get_models/<int:vendor_id>/', views.get_models, name='get_models'),
    path('upload/', views.upload_file, name='upload_file'),
    path('uploadv/', views.upload_filev, name='upload_filev'),
    ############################################################################################################
    path('storages/', views.GetStorages.as_view(), name='storages'),
    path('storages/add_storage/', views.AddStorage.as_view(), name='add_storage'),
    path('storages/<int:pk>/edit_storage/', views.UpdateStorage.as_view(), name='edit_storage'),
    ############################################################################################################
    path('storage_models/', views.GetStorageModels.as_view(), name='storage_models'),
    path('storage_models/add_storage_model/', views.AddStorageModel.as_view(), name='add_storage_model'),
    path('storage_models/<int:pk>/edit_storage_model/', views.UpdateStorageModel.as_view(), name='edit_storage_model'),
    ############################################################################################################
    path('storage_vendors/', views.GetStorageVendors.as_view(), name='storage_vendors'),
    path('storage_vendors/add_storage_vendor/', views.AddStorageVendor.as_view(), name='add_storage_vendor'),
    path('storage_vendors/<int:pk>/edit_storage_vendor/', views.UpdateStorageVendor.as_view(), name='edit_storage_vendor'),
    ############################################################################################################
    path('storage_types/', views.GetStorageTypes.as_view(), name='storage_types'),
    path('storage_types/add_storage_type/', views.AddStorageType.as_view(), name='add_storage_type'),
    path('storage_types/<int:pk>/edit_storage_type/', views.UpdateStorageType.as_view(), name='edit_storage_type'),
    ############################################################################################################
    path('videocard_models/', views.GetVideocardModels.as_view(), name='videocard_models'),
    path('videocard_models/add_videocard_model/', views.AddVideocardModel.as_view(), name='add_videocard_model'),
    path('videocard_models/<int:pk>/edit_videocard_model/', views.UpdateVideocardModel.as_view(), name='edit_videocard_model'),
    ############################################################################################################
    path('videocard_vendors/', views.GetVideocardVendors.as_view(), name='videocard_vendors'),
    path('videocard_vendors/add_videocard_vendor/', views.AddVideocardVendor.as_view(), name='add_videocard_vendor'),
    path('videocard_vendors/<int:pk>/edit_videocard_vendor/', views.UpdateVideocardVendor.as_view(), name='edit_videocard_vendor'),
    ############################################################################################################
    path('videocards/', views.GetVideocards.as_view(), name='videocards'),
    path('videocards/add_videocard/', views.AddVideocard.as_view(), name='add_videocard'),
    path('videocards/<int:pk>/edit_videocard/', views.UpdateVideocard.as_view(), name='edit_videocard'),
    ############################################################################################################
    path('computers/', views.GetComputers.as_view(), name='computers'),
    path('audiences/', views.GetAudiences.as_view(), name='audiences'),
    path('audience/<int:pk>/', views.GetAudience.as_view(), name='audiecne'),
    path('audience/get_state/<int:aud_id>/', views.get_state, name='get_state'),
    path('audience/change_state/', views.change_state, name='change_state'),
    #path('computer/<int:pk>/', views.GetComputer.as_view(), name='computer'),
    path('computer/<slug:invent>/', views.GetComputer.as_view(), name='computer'),
    ############################################################################################################
    path('rams/', views.GetRAMs.as_view(), name='rams'),
    path('rams/add_ram/', views.AddRAM.as_view(), name='add_ram'),
    path('rams/<int:pk>/edit_ram/', views.UpdateRAM.as_view(), name='edit_ram'),
    ############################################################################################################
    path('ram_models/', views.GetRAMModels.as_view(), name='ram_models'),
    path('ram_models/add_ram_model/', views.AddRAMModel.as_view(), name='add_ram_model'),
    path('ram_models/<int:pk>/edit_ram_model/', views.UpdateRAMModel.as_view(), name='edit_ram_model'),
    ############################################################################################################
    path('ram_vendors/', views.GetRAMVendors.as_view(), name='ram_vendors'),
    path('ram_vendors/add_ram_vendor/', views.AddRAMVendor.as_view(), name='add_ram_vendor'),
    path('ram_vendors/<int:pk>/edit_ram_vendor/', views.UpdateRAMVendor.as_view(), name='edit_ram_vendor'),
    ############################################################################################################
    path('ram_types/', views.GetRAMTypes.as_view(), name='ram_types'),
    path('ram_types/add_ram_type/', views.AddRAMType.as_view(), name='add_ram_type'),
    path('ram_types/<int:pk>/edit_ram_type/', views.UpdateRAMType.as_view(), name='edit_ram_type'),
    ############################################################################################################
    path('monitor_models/', views.GetMonitorModels.as_view(), name='monitor_models'),
    path('monitor_models/add_monitor_model/', views.AddMonitorModel.as_view(), name='add_monitor_model'),
    path('monitor_models/<int:pk>/edit_monitor_model/', views.UpdateMonitorModel.as_view(), name='edit_monitor_model'),
    ############################################################################################################
    path('monitor_vendors/', views.GetMonitorVendors.as_view(), name='monitor_vendors'),
    path('monitor_vendors/add_monitor_vendor/', views.AddMonitorVendor.as_view(), name='add_monitor_vendor'),
    path('monitor_vendors/<int:pk>/edit_monitor_vendor/', views.UpdateMonitorVendor.as_view(), name='edit_monitor_vendor'),
    ############################################################################################################
    path('monitors/', views.GetMonitors.as_view(), name='monitors'),
    path('monitors/add_monitor/', views.AddMonitor.as_view(), name='add_monitor'),
    path('monitors/<int:pk>/edit_monitor/', views.UpdateMonitor.as_view(), name='edit_monitor'),
    #path('update_model_dropdown/', views.update_model_dropdown, name='update_model_dropdown'),
    #path('ajax/load-models/', views.load_models, name='ajax_load_models'),
    #path('login/', views.LoginUser.as_view(), name='login'),
    #path('logout/', views.logout_user, name='logout'),
]