from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from traking.models import TrackedLink, Click
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate

@login_required
def dashboard_overview(request):
    # Get all tracked links for the current user
    tracked_links = TrackedLink.objects.filter(user=request.user)

    # Calculate summary stats
    total_clicks = Click.objects.filter(tracked_link__user=request.user).count()
    recent_clicks = Click.objects.filter(
        tracked_link__user=request.user,
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).count()
    tracked_links = TrackedLink.objects.filter(user=request.user).annotate(click_count=Count('clicks'))
    context = {
        'tracked_links': tracked_links,
        'total_clicks': total_clicks,
        'recent_clicks': recent_clicks,
    }
    return render(request, 'dashboard/overview.html', context)

@login_required
def link_detail(request, link_id):
    tracked_link = get_object_or_404(TrackedLink, id=link_id, user=request.user)

    # Use TruncDate to group clicks by date and count them
    daily_clicks = Click.objects.filter(tracked_link=tracked_link) \
        .annotate(day=TruncDate('timestamp')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')

    # Convert data to lists for Chart.js
    days = [click['day'].strftime('%Y-%m-%d') for click in daily_clicks]
    counts = [click['count'] for click in daily_clicks]

    context = {
        'tracked_link': tracked_link,
        'days': days,
        'counts': counts,
    }
    return render(request, 'dashboard/link_detail.html', context)
