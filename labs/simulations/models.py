# from django.db import models
# from django import forms
# from django.core.validators import FileExtensionValidator
# from django.utils.text import slugify
# import os

# # Create your models here.
# from django.db import models

# NUM_BOXES = 36
# BOXES = range(1, NUM_BOXES + 1)

# def simulation_image_path(instance, filename):
#     ext = filename.split('.')[-1]
#     # Create filename with box number
#     safe_question = slugify(instance.question[:30]) if instance.question else 'question'
#     new_filename = f"box_{instance.box}_{safe_question}.{ext}"
#     return os.path.join('simulations', new_filename)

# class Simulation(models.Model):
#     task = models.TextField(max_length=600)
#     question = models.TextField(max_length=600)
#     labanswer = models.TextField(max_length=600)
#     useranswer = models.TextField(max_length=600)
#     box = models.IntegerField(
#         choices=zip(BOXES, BOXES),
#         default=BOXES[0],
#     )
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.question
    
#     class Meta:
#         ordering = ['box', 'date_created']

#     def __str__(self):
#         return self.question

#     @property
#     def has_image(self):
#         """Check if simulation has an image"""
#         return bool(self.image)

#     @property
#     def image_url(self):
#         """Get image URL safely"""
#         if self.image:
#             return self.image.url
#         return None

#     @property
#     def is_answered(self):
#         """Check if user has answered"""
#         return bool(self.useranswer.strip())

#     @property
#     def is_correct(self):
#         """Check if user answer matches lab answer"""
#         if not self.is_answered:
#             return False
#         return self.useranswer.strip().lower() == self.labanswer.strip().lower()

#     def check_answer(self, user_input):
#         """
#         Check if provided answer is correct
#         Returns True if correct, False otherwise
#         """
#         return user_input.strip().lower() == self.labanswer.strip().lower()

#     def save_user_answer(self, answer):
#         """
#         Save user's answer and return if it's correct
#         """
#         self.useranswer = answer.strip()
#         self.save()
#         return self.is_correct


    


# #stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-the-user



# # Add these to your settings.py

# import os
# from pathlib import Path

# # ... your existing settings ...

# # Media files (uploaded files)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Make sure you have this in your INSTALLED_APPS
# INSTALLED_APPS = [
#     # ... your other apps ...
#     'your_app_name',  # Replace with your actual app name
# ]

# # In your main urls.py (project level), add this:
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('your_app_name.urls')),  # Replace with your app name
# ]

# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.db import models
from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
import os
from django.utils import timezone

# Create your models here.
from django.db import models

NUM_BOXES = 36
BOXES = range(1, NUM_BOXES + 1)

def simulation_image_path(instance, filename):
    ext = filename.split('.')[-1]
    # Create filename with box number
    safe_question = slugify(instance.question[:30]) if instance.question else 'question'
    new_filename = f"box_{instance.box}_{safe_question}.{ext}"
    return os.path.join('simulations', new_filename)

class Simulation(models.Model):
    task = models.TextField(max_length=600)
    question = models.TextField(max_length=600)
    labanswer = models.TextField(max_length=600)
    useranswer = models.TextField(max_length=600, blank=True)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    # Add image field
    image = models.ImageField(
        upload_to=simulation_image_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        help_text='Upload an image for this simulation (JPG, PNG, GIF formats allowed)'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['box', 'date_created']

    @property
    def has_image(self):
        """Check if simulation has an image"""
        return bool(self.image)

    @property
    def image_url(self):
        """Get image URL safely"""
        if self.image:
            return self.image.url
        return None

    @property
    def is_answered(self):
        """Check if user has answered"""
        return bool(self.useranswer.strip())

    @property
    def is_correct(self):
        """Check if user answer matches lab answer"""
        if not self.is_answered:
            return False
        return self.useranswer.strip().lower() == self.labanswer.strip().lower()

    def check_answer(self, user_input):
        """
        Check if provided answer is correct
        Returns True if correct, False otherwise
        """
        return user_input.strip().lower() == self.labanswer.strip().lower()

    def save_user_answer(self, answer):
        """
        Save user's answer and return if it's correct
        """
        self.useranswer = answer.strip()
        self.save()
        return self.is_correct


# Form for handling image uploads
class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['task', 'question', 'labanswer', 'box', 'image']
        widgets = {
            'task': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'question': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'labanswer': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'box': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class UserAnswerForm(forms.Form):
    useranswer = forms.CharField(
        max_length=600,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Enter your answer here...'}),
        label='Your Answer'
    )


class Simulation(models.Model):
    box = models.IntegerField(default=1)
    question = models.TextField(default="")
    task = models.TextField(blank=True, null=True)
    useranswer = models.TextField(blank=True, null=True)
    labanswer = models.TextField(blank=True, null=True)  # Add this field
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='simulation_images/', blank=True, null=True)
    
    def __str__(self):
        return f"Simulation {self.id} - Box {self.box}"