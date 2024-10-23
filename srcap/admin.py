from django.contrib import admin
from .models import *





# Register the Book model to be managed via the admin interface
@admin.register(ScrapyData)
class ScrapyDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_type', 'path', 'published_date', 'created_at', 'updated_at')
    search_fields = ('data_type', 'published_date')
    list_filter = ('published_date',)

# Or, if you don't need custom admin functionality, use:
# admin.site.register(Book)
