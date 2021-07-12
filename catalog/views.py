from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import ComponentPrepTaskInstance, Part, StackingTaskInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.forms import RenewBookForm

def index(request):
    """View for the home page of the website"""
    
    #Generate counts for soe of the main objetcs
    num_CpTasks = ComponentPrepTaskInstance.objects.all().count()
    num_Stacking_Tasks = StackingTaskInstance.objects.all().count()
    
    #avalible tasks remaining
    tasks_remaning = ComponentPrepTaskInstance.objects.exclude(status__exact="c").count()
    
    #all() is implied by default
    num_parts = Part.objects.all().count()
    
    #Number of site visits by the current user    
    context = {
        "num_CpTasks": num_CpTasks,
        "num_parts": num_parts,  
        "tasks_remaning":tasks_remaning,
        "num_Stacking_Tasks": num_Stacking_Tasks,
        }
    
    #Render the HTML template index.html with the data in the context vairable
    return render(request, "index.html", context = context)


class CpTaskListView(generic.ListView):
    #permission_required = 'catalog.can_mark_returned'
    model = ComponentPrepTaskInstance
    context_object_name = "cptask_list"
    template_name = "cptask_list.html"
    paginate_by = 30
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_tasks_not_started = ComponentPrepTaskInstance.objects.filter(status__exact="a").count()
        tasks_remaining = ComponentPrepTaskInstance.objects.exclude(status__exact="c").count()
        tasks_complete = ComponentPrepTaskInstance.objects.filter(status__exact="c").count()
        tasks_on_hold = ComponentPrepTaskInstance.objects.filter(status__exact="h").count()
        context["num_tasks_not_started"] = num_tasks_not_started
        context["tasks_remaining"] = tasks_remaining
        context["tasks_complete"] = tasks_complete
        context["tasks_on_hold"] = tasks_on_hold
        return context
    
class StackingTaskListView(generic.ListView):
    model = StackingTaskInstance
    context_object_name = "stackingtask_list"
    template_name = "stackingtask/stackingtaskinstacne_list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         num_tasks_not_started = StackingTaskInstance.objects.filter(status__exact="a").count()
         tasks_remaining = StackingTaskInstance.objects.exclude(status__exact="c").count()
         component_prep_tasks = ComponentPrepTaskInstance.objects.all()
         counter = 0
         part = None
         Completedict = {}
         for task in ComponentPrepTaskInstance.objects.all():
             print(task)
             if task.part != part:
                 if counter != 0:
                     Completedict[task.part] = "Not Complete"
                 counter = 0
                 part = task.part
                 if task.status != "c":
                     counter += 1
             else:
                if task.status != "c":
                     counter += 1
         print(Completedict)

         context["num_tasks_not_started"] = num_tasks_not_started
         context["tasks_remaining"] = tasks_remaining
         context["component_prep_tasks"] = component_prep_tasks
         return context
     
class StackingTaskDetailView(generic.DetailView):
    model = StackingTaskInstance
    
class StackingTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = StackingTaskInstance
    fields = ['status'] 
    
class StackingTaskDelete(LoginRequiredMixin,DeleteView):
    model = StackingTaskInstance 
    success_url = reverse_lazy('stackingtasks')
    
class CPTaskDetailView(generic.DetailView):
    model = ComponentPrepTaskInstance
    
    
class PartListView(generic.ListView):
    model = Part
    context_object_name = "part_list"
    template_name = "parts/part_list.html"
    paginate_by = 10



class PartDetailView(generic.DetailView):
    model = Part
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part_component_prep_tasks = ComponentPrepTaskInstance.objects.all()
        part_stacking_tasks = StackingTaskInstance.objects.all()
        part_component_prep_tasks_complete = ComponentPrepTaskInstance.objects.exclude(status__exact="c").count()
        part_stacking_tasks_complete = StackingTaskInstance.objects.exclude(status__exact="c").count()
        context["part_component_prep_tasks_complete"] = part_component_prep_tasks_complete
        context["part_component_prep_tasks"] = part_component_prep_tasks
        context["part_stacking_tasks_complete"] = part_stacking_tasks_complete
        context["part_stacking_tasks"] = part_stacking_tasks
        return context
    
    
import datetime

from django.contrib.auth.decorators import login_required, permission_required
    
class PartCreate(LoginRequiredMixin,CreateView):
    model = Part 
    fields = ['title', 'team', 'Component_Prep_tasks','Stacking_tasks', 'pub_date']
    initial = {'pub_date': timezone.now}
    success_url = reverse_lazy('parts')
    
class PartUpdate(LoginRequiredMixin,UpdateView):
    model = Part 
    fields = '__all__'
    success_url = reverse_lazy('parts')
    
class PartDelete(LoginRequiredMixin,DeleteView):
    model = Part 
    success_url = reverse_lazy('parts')
    

class CPTaskStatusUpdate(LoginRequiredMixin,UpdateView):
    model = ComponentPrepTaskInstance
    fields = ['status'] 
    
class CPTaskDelete(LoginRequiredMixin,DeleteView):
    model = ComponentPrepTaskInstance 
    success_url = reverse_lazy('cptasks')