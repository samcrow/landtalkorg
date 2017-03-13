from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound
from django.core import serializers

from .models import Submission
from .forms import SubmissionForm

from django.contrib.auth.models import User

def index(request):
	submissions = Submission.objects.all()
	return render(request, 'landtalkapp/index.html', {'submissions': submissions})

def faq(request):
	return render(request, 'landtalkapp/faq.html')

def about(request):
	return render(request, 'landtalkapp/about.html')

def submission_new(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            return redirect('submission_thankyou')
    else:
        form = SubmissionForm()
    return render(request, 'landtalkapp/submission_new.html', {'form': form})

def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if submission.pub is True:
    	return render(request, 'landtalkapp/submission_detail.html', {'submission': submission})
    else:
    	# return HttpResponseNotFound('<h1>Page not found</h1>')
    	return HttpResponseForbidden() #return HttpRedirect('/') #httpforbidden

def submission_edit(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = SubmissionForm(instance=submission)
    return render(request, 'landtalkapp/submission_new.html', {'form': form})

def submission_thankyou(request):
	return render(request, 'landtalkapp/submission_thankyou.html')

def map_query(request):
	submissions = Submission.objects.filter(pub = True)
	data = serializers.serialize("xml", submissions, fields=('location, lat, lng, videourl, privkey'))
	return HttpResponse(data, content_type="text/xml; charset=utf-8")