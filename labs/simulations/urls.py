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
    path('quiz/', views.QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:simulation_id>/', views.quiz_question_view, name='quiz_question'),
    path('quiz/<int:simulation_id>/result/', views.quiz_result_view, name='quiz_result'),
    path('quiz/<int:current_simulation_id>/next/', views.next_quiz_view, name='next_quiz'),
    path('quiz/random/', views.random_quiz_view, name='random_quiz'),
]




