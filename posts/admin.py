from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "fecha_creacion")
    search_fields = ("titulo", "contenido", "autor__username")
    list_filter = ("fecha_creacion",)
