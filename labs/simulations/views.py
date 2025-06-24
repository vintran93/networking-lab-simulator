from django.urls import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
)

from .models import Simulation

class SimulationListView(ListView):
    model = Simulation
    queryset = Simulation.objects.all().order_by("box", "-date_created")

class SimulationCreateView(CreateView):
    model = Simulation
    fields = ["task", "question", "labanswer", "useranswer"]
    success_url = reverse_lazy("simulation-create")

class SimulationUpdateView(SimulationCreateView, UpdateView):
    success_url = reverse_lazy("simulation-list")

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from .models import Simulation
from django import forms


class QuizAnswerForm(forms.Form):
    """Form for submitting quiz answers"""
    answer = forms.CharField(
        max_length=600,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your answer...',
            'required': True
        }),
        label='Your Answer'
    )


def quiz_question_view(request, simulation_id):
    """
    Display a quiz question and handle answer submission
    """
    simulation = get_object_or_404(Simulation, id=simulation_id)
    
    if request.method == 'POST':
        form = QuizAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer'].strip()
            
            # Save the user's answer to the simulation
            simulation.useranswer = user_answer
            simulation.save()
            
            # Check if the answer is correct (case-insensitive comparison)
            if user_answer.lower() == simulation.labanswer.lower():
                messages.success(request, 'Correct! Well done.')
                return redirect('quiz_result', simulation_id=simulation.id)
            else:
                messages.error(request, 'Incorrect answer. Please try again.')
                return redirect('quiz_question', simulation_id=simulation.id)
    else:
        form = QuizAnswerForm()
    
    context = {
        'simulation': simulation,
        'form': form,
    }
    return render(request, 'quiz/question.html', context)


def quiz_result_view(request, simulation_id):
    """
    Display the quiz result after answering
    """
    simulation = get_object_or_404(Simulation, id=simulation_id)
    
    # Check if user has answered
    if not simulation.useranswer:
        return redirect('quiz_question', simulation_id=simulation.id)
    
    is_correct = simulation.useranswer.lower() == simulation.labanswer.lower()
    
    context = {
        'simulation': simulation,
        'is_correct': is_correct,
    }
    return render(request, 'quiz/result.html', context)


class QuizListView(ListView):
    """
    Display list of all available quiz questions
    """
    model = Simulation
    template_name = 'quiz/list.html'
    context_object_name = 'simulations'
    ordering = ['box', 'date_created']


class QuizView(View):
    """
    Class-based view alternative for handling quiz questions
    """
    def get(self, request, simulation_id):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        form = QuizAnswerForm()
        
        context = {
            'simulation': simulation,
            'form': form,
        }
        return render(request, 'quiz/question.html', context)
    
    def post(self, request, simulation_id):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        form = QuizAnswerForm(request.POST)
        
        if form.is_valid():
            user_answer = form.cleaned_data['answer'].strip()
            simulation.useranswer = user_answer
            simulation.save()
            
            if user_answer.lower() == simulation.labanswer.lower():
                messages.success(request, 'Correct! Well done.')
                return redirect('quiz_result', simulation_id=simulation.id)
            else:
                messages.error(request, 'Incorrect answer. Please try again.')
        
        context = {
            'simulation': simulation,
            'form': form,
        }
        return render(request, 'quiz/question.html', context)


def next_quiz_view(request, current_simulation_id):
    """
    Navigate to the next quiz question
    """
    current_simulation = get_object_or_404(Simulation, id=current_simulation_id)
    
    # Get next simulation by box number or date
    next_simulation = Simulation.objects.filter(
        box__gt=current_simulation.box
    ).order_by('box', 'date_created').first()
    
    if not next_simulation:
        # If no next simulation by box, get the first one with higher date
        next_simulation = Simulation.objects.filter(
            date_created__gt=current_simulation.date_created
        ).order_by('date_created').first()
    
    if next_simulation:
        return redirect('quiz_question', simulation_id=next_simulation.id)
    else:
        messages.info(request, 'You have completed all available quizzes!')
        return redirect('quiz_list')


def random_quiz_view(request):
    """
    Display a random quiz question
    """
    simulation = Simulation.objects.order_by('?').first()
    
    if simulation:
        return redirect('quiz_question', simulation_id=simulation.id)
    else:
        messages.error(request, 'No quiz questions available.')
        return redirect('quiz_list')