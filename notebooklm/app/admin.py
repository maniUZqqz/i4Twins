from django.contrib import admin
from .models import Chat, ChatFile, ChatUrl, Message

class ChatFileInline(admin.TabularInline):
    model = ChatFile
    extra = 1  # تعداد فرم‌های خالی برای افزودن فایل جدید

class ChatUrlInline(admin.TabularInline):  # نمایش URLها در داخل صفحه چت
    model = ChatUrl
    extra = 1  # تعداد فرم‌های خالی برای افزودن URL جدید

class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # نمایش نام چت و زمان ایجاد آن
    search_fields = ('name',)  # جستجو در نام چت‌ها
    inlines = [ChatFileInline, ChatUrlInline]  # نمایش فایل‌ها و URLها به صورت درون‌خطی

admin.site.register(Chat, ChatAdmin)


admin.site.register(Message)


