from django.urls import path
# from django.views.generic import SimulationListView
from . import views

urlpatterns = [
    path(
        "",
        views.SimulationListView.as_view(),
        name="simulation-list"
    ),
    path(
        "new",
        views.SimulationCreateView.as_view(),
        name="simulation-create"
    ),
    path(
        "edit/<int:pk>",
        views.SimulationUpdateView.as_view(),
        name="simulation-update"
    ),
]