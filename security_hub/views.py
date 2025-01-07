from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from security_hub.forms import AddWorkerForm
from security_hub.models import ScanLog, Worker


# Create your views here.
@login_required()
def index(request):
    context = {
        'scan_logs': ScanLog.objects.all(),
    }
    return render(request, 'security_hub/index.html', context)

@login_required()
def workers(request):
    context = {
        'workers': Worker.objects.all(),
    }
    return render(request, 'security_hub/workers.html', context)

@login_required()
def delete_worker(request, w_id):
    try:
        Worker.objects.get(id=w_id).delete()
    except Worker.DoesNotExist:
        pass
    return redirect(workers)


class AddWorker(LoginRequiredMixin, CreateView): # form is being sent to template via `form` key
    form_class = AddWorkerForm
    template_name = 'security_hub/add_worker.html'
    success_url = reverse_lazy('workers')
    title_page = "Add worker"

    def form_valid(self, form): # called when valid form data has been POSTed
        return super().form_valid(form)


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page not found :(</h1>')