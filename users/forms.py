
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from users.models import Group
from itertools import chain
import helper

from home.models import TV, Computer, Monitor, Printer, Projector, TechniqueType
from users.models import User

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Роль', widget=forms.Select(attrs={'class': 'form-control select2'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'password1', 'password2', 'group']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'group': 'Роль',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.valid_technique = []
        all_inventory_numbers = list(chain(Computer.objects.values_list('inventory_number', flat=True), Printer.objects.values_list('inventory_number', flat=True), Projector.objects.values_list('inventory_number', flat=True), TV.objects.values_list('inventory_number', flat=True), Monitor.objects.values_list('inventory_number', flat=True)))
        result = tuple((value, value) for index, value in enumerate(all_inventory_numbers))
        self.fields['inventory_numbers'] = forms.MultipleChoiceField(label='Инвентарные номера', choices=result, required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует')
        return email
    
    def clean_inventory_numbers(self):
        inventory_numbers = self.cleaned_data['inventory_numbers']
        role = self.cleaned_data['group']

        if role.is_responsible:
            error_msgs = []
            for inventory_number in inventory_numbers:
                if Computer.objects.filter(inventory_number=inventory_number, UsersComputers__group=role).exists():
                    error_msgs.append(f'Компьютер с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                if Printer.objects.filter(inventory_number=inventory_number, UsersPrinters__group=role).exists():
                    error_msgs.append(f'Принтер с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                if Projector.objects.filter(inventory_number=inventory_number, UsersProjectors__group=role).exists():
                    error_msgs.append(f'Проектор с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                if TV.objects.filter(inventory_number=inventory_number, UsersTVs__group=role).exists():
                    error_msgs.append(f'Телевизор с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
                if Monitor.objects.filter(inventory_number=inventory_number, UsersMonitors__group=role).exists():
                    error_msgs.append(f'Монитор с инвентарным номером {inventory_number} уже зарегистрирован на другого пользователя')
            
            if error_msgs:
                raise forms.ValidationError(error_msgs)

        return inventory_numbers

    def save(self, commit=True):
        user = super().save()
        role = self.cleaned_data['group']
        user.user_permissions.set(role.permissions.all())
        #user.groups.set([role.id])

        if role.is_responsible:
            for inventory_number in self.cleaned_data['inventory_numbers']:
                technique = helper.get_technique_by_inventory_number(inventory_number)

                if technique.technique_type.id == TechniqueType.Type.COMPUTER:
                    user.computers.add(technique)
                if technique.technique_type.id == TechniqueType.Type.PRINTER:
                    user.printers.add(technique)
                if technique.technique_type.id == TechniqueType.Type.PROJECTOR or technique.technique_type == TechniqueType.Type.MFU:
                    user.projectors.add(technique)
                if technique.technique_type.id == TechniqueType.Type.TV:
                    user.tvs.add(technique)
                if technique.technique_type.id == TechniqueType.Type.MONITOR:
                    user.monitors.add(technique)

            self.save_m2m()

        return user
    
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'patronymic']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'previewPhoto()'})
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class GetUsersForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'group']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'group': 'Роль',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
        }



class AddGroupForm(forms.ModelForm):
    #permissions = forms.ModelMultipleChoiceField(
    #    queryset=Permission.objects.all(),
    #    label="Права"
    #)
    
    class Meta:
        model = Group
        fields = ['name', 'permissions', 'is_responsible']
        # labels = {
        #     'name': 'Name',
        #     'permissions': 'Permissions',
        # }

        # filter_horizontal = ['permissions']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.all()
        self.fields['permissions'].label_from_instance = self.get_permission_name

    def get_permission_name(self, permission):
        name = permission.name
        name = name.replace('Can add ', 'Добавление элемента в справочник "')
        name = name.replace('Can change ', 'Редактирование элемента в справочнике "')
        name = name.replace('Can delete ', 'Удаление элемента в справочнике "')
        name = name.replace('Can view ', 'Просмотр элемента в справочнике "')
        return name + '"'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        instance.save()
        
        self.save_m2m()

        perms = instance.permissions.all()
        users = instance.user_set.all()

        for user in users:
            user.user_permissions.clear()

        for user in users:
            user.user_permissions.set(perms)

        if commit:
            instance.save()

        return instance