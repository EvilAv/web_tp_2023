from django.contrib import admin
from .models import Profile, Tag, Question, Answer, Rate

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Rate)