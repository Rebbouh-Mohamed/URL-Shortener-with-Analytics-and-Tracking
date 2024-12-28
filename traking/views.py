from django.shortcuts import render,redirect,get_object_or_404
from .models import TrackedLink, Click
from django.utils import timezone
from django.http import HttpRequest,HttpResponseRedirect
from django.conf import settings
from user_agents import parse
from django.contrib.auth.decorators import login_required


def track_click(request: HttpRequest, slug: str):
    tracked_link = get_object_or_404(TrackedLink, slug=slug)

    # Record the click details
    Click.objects.create(
        tracked_link=tracked_link,
        timestamp=timezone.now(),
        ip_address=request.META.get('REMOTE_ADDR'),
        referrer=request.META.get('HTTP_REFERER', ''),
        user_agent=request.META.get('HTTP_USER_AGENT', '')

    )


    # Redirect to the original URL
    return HttpResponseRedirect(tracked_link.url)


@login_required
def tracked_link_detail(request, pk):
    tracked_link = get_object_or_404(TrackedLink, pk=pk)
    clicks = tracked_link.clicks.all()  # Retrieve all clicks related to this link
    context = {'tracked_link': tracked_link, 'clicks': clicks,'domain':settings.SITE_DOMAIN}
    return render(request, 'traking/tracked_link_detail.html', context)

@login_required
def create_tracked_link(request):
    if request.method=='POST':
        original_url = request.POST.get('url')
        name= request.POST.get('name')
        #Create a new TrackedLink instance
        tracked_link = TrackedLink.objects.create(user=request.user, url=original_url,url_name=name)
        redirect('tracked_link_detail',pk=tracked_link.pk)

    return render(request,'traking/create_link.html')

    
### later for extract city and ...
# def get_geo_location_from_headers(request):
#     return {
#         'country': request.META.get('HTTP_CF_IPCOUNTRY', None),
#         'region': request.META.get('HTTP_CF_REGION', None),
#         'city': request.META.get('HTTP_CF_CITY', None)
#     }
