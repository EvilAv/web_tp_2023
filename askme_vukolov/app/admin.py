from django.contrib import admin
from .models import Profile, Tag, Question, Answer, RateToQuestion, RateToAnswer

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(RateToQuestion)
admin.site.register(RateToAnswer)
