
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Simulation

# Form for handling image uploads and simulation creation/editing
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

class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['field1', 'field2', 'image']  # include your actual fields
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})