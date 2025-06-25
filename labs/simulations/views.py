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


def simulation_detail(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        form = UserAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['useranswer']
            is_correct = simulation.save_user_answer(user_answer)
            # Handle the response based on correctness
    else:
        form = UserAnswerForm()
    
    context = {
        'simulation': simulation,
        'form': form,
    }
    return render(request, 'simulation_detail.html', context)


def simulation_detail(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        form = UserAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['useranswer']
            is_correct = simulation.save_user_answer(user_answer)
            # Handle the response based on correctness
    else:
        form = UserAnswerForm()
    
    context = {
        'simulation': simulation,
        'form': form,
    }
    return render(request, 'simulation_detail.html', context)


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Simulation
# from .forms import SimulationForm

def create_simulation(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST, request.FILES)
        if form.is_valid():
            simulation = form.save()
            messages.success(request, 'Simulation created successfully!')
            return redirect('simulation_detail', pk=simulation.pk)
    else:
        form = SimulationForm()
    
    return render(request, 'create_simulation.html', {'form': form})

def edit_simulation(request, pk):
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        form = SimulationForm(request.POST, request.FILES, instance=simulation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Simulation updated successfully!')
            return redirect('simulation_detail', pk=simulation.pk)
    else:
        form = SimulationForm(instance=simulation)
    
    return render(request, 'edit_simulation.html', {
        'form': form, 
        'simulation': simulation,
        'edit_mode': True
    })


# simulations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Simulation
# from .forms import SimulationForm, UserAnswerForm, SimulationSearchForm

def simulation_list(request):
    """Display list of all simulations with search and filter"""
    search_form = SimulationSearchForm(request.GET)
    simulations = Simulation.objects.all()
    
    # Apply search and filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        box_filter = search_form.cleaned_data.get('box_filter')
        
        if search_query:
            simulations = simulations.filter(
                Q(question__icontains=search_query) |
                Q(task__icontains=search_query) |
                Q(labanswer__icontains=search_query)
            )
        
        if box_filter:
            simulations = simulations.filter(box=box_filter)
    
    # Pagination
    paginator = Paginator(simulations, 10)  # Show 10 simulations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_simulations': simulations.count(),
    }
    return render(request, 'simulations/simulation_list.html', context)


def simulation_detail(request, pk):
    """Display a single simulation and handle user answers"""
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        form = UserAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['useranswer']
            is_correct = simulation.save_user_answer(user_answer)
            
            if is_correct:
                messages.success(request, '🎉 Correct! Well done!')
            else:
                messages.error(request, f'❌ Incorrect. The correct answer is: {simulation.labanswer}')
            
            return redirect('simulation_detail', pk=pk)
    else:
        # Pre-fill form with existing answer if available
        initial_data = {}
        if simulation.useranswer:
            initial_data['useranswer'] = simulation.useranswer
        form = UserAnswerForm(initial=initial_data)
    
    context = {
        'simulation': simulation,
        'form': form,
        'is_answered': simulation.is_answered,
        'is_correct': simulation.is_correct if simulation.is_answered else None,
    }
    return render(request, 'simulations/simulation_detail.html', context)


def create_simulation(request):
    """Create a new simulation"""
    if request.method == 'POST':
        form = SimulationForm(request.POST, request.FILES)
        if form.is_valid():
            simulation = form.save()
            messages.success(request, 'Simulation created successfully!')
            return redirect('simulation_detail', pk=simulation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SimulationForm()
    
    context = {
        'form': form,
        'title': 'Create New Simulation',
        'submit_text': 'Create Simulation',
        'edit_mode': False,
    }
    return render(request, 'simulations/simulation_form.html', context)


def edit_simulation(request, pk):
    """Edit an existing simulation"""
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        form = SimulationForm(request.POST, request.FILES, instance=simulation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Simulation updated successfully!')
            return redirect('simulation_detail', pk=simulation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SimulationForm(instance=simulation)
    
    context = {
        'form': form,
        'simulation': simulation,
        'title': f'Edit Simulation - Box {simulation.box}',
        'submit_text': 'Update Simulation',
        'edit_mode': True,
    }
    return render(request, 'simulations/simulation_form.html', context)


def delete_simulation(request, pk):
    """Delete a simulation"""
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        box_number = simulation.box
        simulation.delete()
        messages.success(request, f'Simulation from Box {box_number} has been deleted.')
        return redirect('simulation_list')
    
    context = {
        'simulation': simulation,
    }
    return render(request, 'simulations/simulation_confirm_delete.html', context)


@require_http_methods(["POST"])
def check_answer_ajax(request, pk):
    """AJAX endpoint to check user answer without page reload"""
    simulation = get_object_or_404(Simulation, pk=pk)
    
    if request.method == 'POST':
        form = UserAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['useranswer']
            is_correct = simulation.check_answer(user_answer)
            
            # Save the answer
            simulation.save_user_answer(user_answer)
            
            return JsonResponse({
                'success': True,
                'is_correct': is_correct,
                'correct_answer': simulation.labanswer,
                'message': '🎉 Correct! Well done!' if is_correct else '❌ Incorrect. Try again or see the correct answer.',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def simulation_by_box(request, box_number):
    """Display simulations for a specific box"""
    if box_number < 1 or box_number > 36:
        messages.error(request, 'Invalid box number. Please select a box between 1 and 36.')
        return redirect('simulation_list')
    
    simulations = Simulation.objects.filter(box=box_number).order_by('date_created')
    
    context = {
        'simulations': simulations,
        'box_number': box_number,
        'total_simulations': simulations.count(),
    }
    return render(request, 'simulations/simulation_by_box.html', context)


def dashboard(request):
    """Dashboard showing simulation statistics"""
    from django.db.models import Count
    
    # Get statistics
    total_simulations = Simulation.objects.count()
    answered_simulations = Simulation.objects.exclude(useranswer='').count()
    correct_answers = sum(1 for sim in Simulation.objects.exclude(useranswer='') if sim.is_correct)
    
    # Get simulations by box
    box_stats = []
    for box_num in range(1, 37):
        box_sims = Simulation.objects.filter(box=box_num)
        box_stats.append({
            'box': box_num,
            'total': box_sims.count(),
            'answered': box_sims.exclude(useranswer='').count(),
            'correct': sum(1 for sim in box_sims.exclude(useranswer='') if sim.is_correct),
        })
    
    # Recent simulations
    recent_simulations = Simulation.objects.order_by('-date_created')[:5]
    
    context = {
        'total_simulations': total_simulations,
        'answered_simulations': answered_simulations,
        'correct_answers': correct_answers,
        'accuracy_rate': (correct_answers / answered_simulations * 100) if answered_simulations > 0 else 0,
        'box_stats': box_stats,
        'recent_simulations': recent_simulations,
    }
    return render(request, 'simulations/dashboard.html', context)


def clear_user_answers(request):
    """Clear all user answers (for testing purposes)"""
    if request.method == 'POST':
        count = Simulation.objects.exclude(useranswer='').count()
        Simulation.objects.update(useranswer='')
        messages.success(request, f'Cleared {count} user answers.')
        return redirect('simulation_list')
    
    context = {
        'answered_count': Simulation.objects.exclude(useranswer='').count(),
    }
    return render(request, 'simulations/clear_answers_confirm.html', context)

def simulation_form_view(request, pk=None):
    if pk:
        simulation = get_object_or_404(Simulation, pk=pk)
        form = SimulationForm(request.POST or None, request.FILES or None, instance=simulation)
    else:
        form = SimulationForm(request.POST or None, request.FILES or None)
        simulation = None
    
    if form.is_valid():
        form.save()
        return redirect('simulation-list')
    
    return render(request, 'simulations/simulation_form.html', {
        'form': form,
        'simulation': simulation
    })