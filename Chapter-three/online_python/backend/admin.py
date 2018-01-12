from django.contrib import admin
from .models import Code

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass
    
