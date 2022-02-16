from django.contrib import admin
from tutorial.models import Material,Subject,Comment,Reply,Student_Model

# Register your models here.

admin.site.register(Material)
admin.site.register(Subject)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Student_Model)
