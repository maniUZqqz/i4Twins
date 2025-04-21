from django import forms
from .models import Chat, ChatFile, ChatUrl

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={
                # 'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4',
                'placeholder': 'نام چت خود را وارد کنید'
            }),
            'url': forms.URLInput(attrs={
                # 'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'placeholder': 'آدرس URL خود را وارد کنید'
            })
        }

class ChatFileForm(forms.ModelForm):
    class Meta:
        model = ChatFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                # 'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4',
            })
        }

class ChatUrlForm(forms.ModelForm):
    class Meta:
        model = ChatUrl
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={
                # 'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'placeholder': 'آدرس URL خود را وارد کنید'
            })
        }





