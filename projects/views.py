from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Tracker, Comment, Update

def index(request):
	latest_tracker_list = Tracker.objects.order_by('-create_date')[:5]
	context = {
		'latest_tracker_list': latest_tracker_list,
	}
	return render(request, 'projects/index.html', context)

def detail(request, tracker_id):
	tracker = get_object_or_404(Tracker, pk=tracker_id)
	return render(request, 'projects/detail.html', {'tracker': tracker}) 

def comments(request, tracker_id):
	tracker = get_object_or_404(Tracker, pk=tracker_id)
	return render(request, 'projects/comments.html', {'tracker': tracker})

def updates(request, tracker_id):
	tracker = get_object_or_404(Tracker, pk=tracker_id)
	return render(request, 'projects/updates.html', {'tracker': tracker})
