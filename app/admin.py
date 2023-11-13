from django.contrib import admin

# Register your models here.
#
from .models import Tag, Profile, Question, Answer, LikeAnswer, LikeQuestion

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(LikeAnswer)
admin.site.register(LikeQuestion)
