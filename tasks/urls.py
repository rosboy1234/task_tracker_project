from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskDetailView, SignUpView, 
    add_subtask, toggle_subtask
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    
    path('<int:pk>/subtask/add/', add_subtask, name='add_subtask'),
    path('<int:pk>/subtask/<int:subtask_id>/toggle/', toggle_subtask, name='toggle_subtask'),
]