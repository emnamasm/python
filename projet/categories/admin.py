from django.contrib import admin

# Register your models here.
from .models import Category
#admin.site.register(le nom de la classe )
#apparition des modeles dans l'interface d'administration de Django.
class CategoryAdmin(admin.ModelAdmin):
    search_fields=('title',)
admin.site.register(Category,CategoryAdmin)
