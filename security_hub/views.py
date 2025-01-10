import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from security_hub.forms import AddWorkerForm
from security_hub.models import ScanLog, Worker, CardChange



ENTRANCE_TERMINAL_ID = "T0"
EXIT_TERMINAL_ID = "T1"

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
    title_page = "Add worker"

    def form_valid(self, form):
        worker = form.save()
        worker_id = worker.id
        return redirect('add_worker_card', w_id=worker_id)


# View for the web interface
@require_http_methods(["GET"])
def worker_card(request, w_id):
    worker = get_object_or_404(Worker, id=w_id)

    CardChange.objects.filter(worker=worker).delete()

    # Proceed with rendering the worker's card information
    response = render(request, 'security_hub/worker_card.html', {
        'w_id': w_id,
        'full_name': f"{worker.name} {worker.surname}",
        'card': worker.card or False,
    })
    return response

@require_http_methods(["GET"])
def add_worker_card(request, w_id):
    worker = get_object_or_404(Worker, id=w_id)

    # Create or update the CardChange record
    card_change, created = CardChange.objects.update_or_create(
        worker=worker, defaults={'card_change_in_progress': True}
    )

    # Pass the card_change object to the template
    response = render(request, 'security_hub/add_worker_card.html', {
        'w_id': w_id,
        'full_name': f"{worker.name} {worker.surname}",
        'card_change': card_change  # Pass the CardChange object
    })
    return response

# API endpoint for the Raspberry Pi
@csrf_exempt
@require_http_methods(["POST"])
def register_card(request, card):
    # Retrieve the CardChange record to see if card change is in progress
    card_change = CardChange.objects.filter(card_change_in_progress=True).first()
    if not card_change:
        return JsonResponse({
            'status': 'error',
            'message': 'No card change in progress'
        }, status=400)

    if Worker.objects.filter(card=card).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Card already registered'
        })

    worker = card_change.worker
    worker.card = card
    worker.save()

    # Mark the card change as complete by updating the record
    card_change.card_change_in_progress = False
    card_change.save()

    return JsonResponse({
        'status': 'success',
        'worker_id': worker.id,
        'card': card
    })

from django.http import JsonResponse

@require_http_methods(["GET"])
def check_card_status(request, card_change_id):
    try:
        card_change = CardChange.objects.get(id=card_change_id)
        return JsonResponse({
            'card_change_in_progress': card_change.card_change_in_progress,
            'card': card_change.worker.card,
        })
    except CardChange.DoesNotExist:
        return JsonResponse({
            'card_change_in_progress': False  # If the CardChange doesn't exist, assume it's not in progress
        }, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def validate_card_scan(request):
    def log_scan(card, scan_type, scan_result, worker=None):
        """Helper to create a ScanLog entry."""
        ScanLog.objects.create(
            card=card,
            scan_type=scan_type,
            scan_result=scan_result,
            worker=worker,
            worker_full_name=f"{worker.name} {worker.surname}" if worker else None,
        )

    def get_last_scan_type(card):
        """Helper to get the last scan type or None if no logs exist."""
        last_log = ScanLog.objects.filter(card=card).first()
        return last_log.scan_type if last_log else None

    request_data = json.loads(request.body)
    terminal_id = request_data.get('terminal_id')
    card = request_data.get('card')

    if not card:
        return JsonResponse({
            'status': 'error',
            'message': 'Card is required'
        })

    try:
        worker = Worker.objects.get(card=card)
    except Worker.DoesNotExist:
        log_scan(card, ScanLog.ScanType.ENTRANCE if terminal_id == ENTRANCE_TERMINAL_ID else ScanLog.ScanType.EXIT,
                 ScanLog.ScanResult.DENIED)
        return JsonResponse({
            'status': 'error',
            'message': 'Card is not registered'
        })

    last_scan_type = get_last_scan_type(card)

    if terminal_id == ENTRANCE_TERMINAL_ID:
        if last_scan_type == ScanLog.ScanType.ENTRANCE:
            log_scan(card, ScanLog.ScanType.ENTRANCE, ScanLog.ScanResult.DENIED, worker)
            return JsonResponse({
                'status': 'error',
                'message': 'Worker already entered',
                'worker_name': f"{worker.name} {worker.surname}"
            })
        else:
            log_scan(card, ScanLog.ScanType.ENTRANCE, ScanLog.ScanResult.SUCCESSFUL, worker)
            return JsonResponse({
                'status': 'success',
                'worker_name': f"{worker.name} {worker.surname}"
            })

    elif terminal_id == EXIT_TERMINAL_ID:
        if last_scan_type == ScanLog.ScanType.EXIT:
            log_scan(card, ScanLog.ScanType.EXIT, ScanLog.ScanResult.DENIED, worker)
            return JsonResponse({
                'status': 'error',
                'message': 'Worker already leaved',
                'worker_name': f"{worker.name} {worker.surname}"
            })
        else:
            log_scan(card, ScanLog.ScanType.EXIT, ScanLog.ScanResult.SUCCESSFUL, worker)
            return JsonResponse({
                'status': 'success',
                'worker_name': f"{worker.name} {worker.surname}"
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid terminal id'
    })


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Page not found :(</h1>')


