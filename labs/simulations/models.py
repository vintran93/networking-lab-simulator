from django.db import models
from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
import os

# Create your models here.
from django.db import models

NUM_BOXES = 36
BOXES = range(1, NUM_BOXES + 1)

def simulation_image_path(instance, filename):
    """
    Custom upload path for simulation images
    """
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename with box number
    safe_question = slugify(instance.question[:30]) if instance.question else 'question'
    new_filename = f"box_{instance.box}_{safe_question}.{ext}"
    return os.path.join('simulations', new_filename)

class Simulation(models.Model):
    # image = models.ImageField(
    #     upload_to=simulation_image_path,
    #     validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
    #     help_text="Upload an image file (JPG, PNG, GIF)",
    #     blank=True,
    #     null=True
    # )
    # image = models.ImageField(upload_to='simulations/')
    task = models.TextField(max_length=600)
    question = models.TextField(max_length=600)
    labanswer = models.TextField(max_length=600)
    useranswer = models.TextField(max_length=600)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['box', 'date_created']

    def __str__(self):
        return self.question

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


    


#stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-the-user