from django.contrib import admin
from django.utils.html import format_html
from .models import Simulation

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ['id', 'box', 'question_preview', 'has_image', 'image_preview', 'date_created']
    list_filter = ['box', 'date_created']
    search_fields = ['question', 'task']
    readonly_fields = ['image_preview']
    
    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = "Question"
    
    def has_image(self, obj):
        return "✅ Yes" if obj.image else "❌ No"
    has_image.short_description = "Has Image"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"