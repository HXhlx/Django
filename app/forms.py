from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User, Profile, Schedule


class RegisterForm(UserCreationForm):
    """注册表单"""

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': _('用户名'),
        }


class ProfileForm(forms.ModelForm):
    """个人信息表单"""

    class Meta:
        model = Profile
        fields = ['name', 'sex', 'birth', 'phone', 'email', 'address']
        labels = {
            'name': _('姓名'),
            'sex': _('性别'),
            'birth': _('出生日期'),
            'phone': _('电话'),
            'email': _('邮箱'),
            'address': _('地址'),
        }
        widgets = {
            'birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError(_('请输入姓名'))
        if len(name) < 2:
            raise forms.ValidationError(_('姓名至少需要 2 个字符'))
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError(_('请输入电话号码'))
        import re
        if not re.match(r'^\+?[0-9\s\-()]{7,20}$', phone):
            raise forms.ValidationError(_('请输入有效的电话号码（支持国际格式，如 +86 13800138000）'))
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 7 or len(digits) > 15:
            raise forms.ValidationError(_('电话号码长度应在 7-15 位之间'))
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if email:
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                raise forms.ValidationError(_('请输入有效的邮箱地址'))
        return email


class ScheduleForm(forms.ModelForm):
    """日程表单"""
    start_date = forms.DateField(label=_('开始日期'), required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    start_time = forms.TimeField(label=_('开始时间'), required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    end_date = forms.DateField(label=_('结束日期'), required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_time = forms.TimeField(label=_('结束时间'), required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))

    class Meta:
        model = Schedule
        fields = ['title', 'text']
        labels = {
            'title': _('标题'),
            'text': _('内容'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.start_time:
                self.fields['start_date'].initial = self.instance.start_time.date()
                self.fields['start_time'].initial = self.instance.start_time.time().strftime('%H:%M')
            if self.instance.end_time:
                self.fields['end_date'].initial = self.instance.end_time.date()
                self.fields['end_time'].initial = self.instance.end_time.time().strftime('%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time')

        import datetime
        if start_date and start_time:
            cleaned_data['start_time'] = datetime.datetime.combine(start_date, start_time)
        elif start_date or start_time:
            cleaned_data['start_time'] = None

        if end_date and end_time:
            cleaned_data['end_time'] = datetime.datetime.combine(end_date, end_time)
        elif end_date or end_time:
            cleaned_data['end_time'] = None

        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise ValidationError(_('结束时间必须晚于开始时间'))
        return cleaned_data
