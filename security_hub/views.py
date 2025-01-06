from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render

from security_hub.models import ScanLog


# Create your views here.
@login_required()
def index(request):
    context = {
        'scan_logs': ScanLog.objects.all(),
    }
    return render(request, 'security_hub/index.html', context)





def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page not found :(</h1>')