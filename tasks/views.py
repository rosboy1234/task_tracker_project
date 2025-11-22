from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from .models import Task, Comment
from .forms import TaskForm, CommentForm, SignUpForm
from django.db.models import Q
from datetime import date

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        due = self.request.GET.get('due')
        if due == 'overdue':
            queryset = queryset.filter(due_date__lt=date.today(), status__ne=Task.Status.DONE)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context['filter_params'] = get_params.urlencode()
        context['status_choices'] = Task.Status.choices
        context['priority_choices'] = Task.Priority.choices
        context['user_today'] = date.today()
        return context


class TaskDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    form_class = CommentForm

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'comment_form' not in context:
            context['comment_form'] = self.get_form()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST, request.FILES)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(comment_form=form))

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.task = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'tasks/signup.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('task_list')