from django.db import models
from django import forms

# Create your models here.
from django.db import models

NUM_BOXES = 36
BOXES = range(1, NUM_BOXES + 1)

class Simulation(models.Model):
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
    


    


#stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-the-user