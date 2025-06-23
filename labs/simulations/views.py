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