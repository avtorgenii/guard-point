from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

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


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page not found :(</h1>')