from django.db import models

class Chat(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)  # اضافه کردن فیلد URL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatFile(models.Model):
    chat = models.ForeignKey(Chat, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='chat_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    pdf_content = models.TextField(blank=True, null=True)
    excel_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'File for {self.chat.name}'


class ChatUrl(models.Model):
    chat = models.ForeignKey(Chat, related_name='urls', on_delete=models.CASCADE)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)  # اضافه کردن فیلد برای محتوا
    def __str__(self):
        return self.url



class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


# python manage.py makemigrations
# python manage.py migrate

