



from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file', 'created_at_display']
    readonly_fields = ['created_at_display']
    list_filter = ['user']

    # Since your model does not have a created_at field, we can define a display method
    def created_at_display(self, obj):
        return obj.file.storage.get_created_time(obj.file.name) if obj.file else "N/A"

    created_at_display.short_description = 'Uploaded At'
