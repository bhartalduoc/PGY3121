from django.contrib import admin
from .models import Estado,Categoria,Noticia

# Register your models here.
admin.site.register(Estado)
admin.site.register(Categoria)
admin.site.register(Noticia)