__author__ = 'ian'
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import *
import time
import datetime
from django.utils import timezone

# ==================================================================================================
# =========================================== ACTIVITY LOG and STATISTICS ==========================
# ==================================================================================================

''' Displays the activity log '''
@login_required(login_url='/login/')
def view_activity_log(request, user):
    item = get_object_or_404(HospitalAdmin, pk=user)
    check_permissions(["HospitalAdmin"], user, request)
    create_event(user_actions[12], request.user, None, None, None)
    list_of_events = Event.objects.all()
    return render(request, 'main_site/systemStats.html', {
        'list_of_events': list_of_events,
        'item': item,
        'stats_dict' : get_system_stats(),
    })

def get_system_stats():
    stats_dict = {}
    # stats_dict['appointments today'] = get_appts_per_day()
    stats_dict['logins today'] = get_logins_per_day()
    stats_dict['checkins per week'] = checkins_per_week()
    stats_dict['appointments this week'] = get_appts_per_week()
    stats_dict['logins per week'] = get_logins_per_week()
    return stats_dict

def get_appts_per_day():
    t = time.strftime("%Y-%m-%d")
    appts_today = Appointment.objects.get(date = t)
    try:
        return len(appts_today)
    except Exception as e:
        print(e)
        return 0

def get_logins_per_day():
    logins_today = Event.objects.filter(activity = user_actions[1])
    logins_today1 = []
    for login in logins_today:
       if time_in_range(timezone.now() - datetime.timedelta(days = 1), timezone.now(), login.time):
           logins_today1.append(login)
    try:
        return len(logins_today1)
    except Exception as e:
        print(e)
        return 0

def get_appts_per_week():
    appts_this_week = Appointment.objects.all()
    appts_this_week1 = []
    for appt in appts_this_week:
        if time_in_range(datetime.datetime.now() - datetime.timedelta(days = 7),
                         datetime.datetime.now(),
                         datetime.datetime.strptime(parseDate(appt.date), "%Y-%m-%d")):
            appts_this_week1.append(appt)
    try:
        return len(appts_this_week1)
    except Exception as e:
        print(e)
        return 0

def get_logins_per_week():
    logins_this_week = Event.objects.filter(activity = user_actions[1])
    logins_this_week1 = []
    for login in logins_this_week:
       if time_in_range(timezone.now() - datetime.timedelta(days = 7), timezone.now(), login.time):
           logins_this_week1.append(login)
    try:
        return len(logins_this_week)
    except Exception as e:
        print(e)
        return 0

def checkins_per_week():
    checkins_this_week = Event.objects.filter(activity = user_actions[10])
    checkins_this_week1 = []
    for checkin in checkins_this_week:
       if time_in_range(timezone.now() - datetime.timedelta(days = 7), timezone.now(), checkin.time):
           checkins_this_week1.append(checkin)
    try:
        return len(checkins_this_week1)
    except Exception as e:
        print(e)
        return 0

# NOT MY CODE :: http://stackoverflow.com/questions/10747974/how-to-check-if-the-current-time-is-in-range-in-python
def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    return start < x and x < end

def parseDate(dateString):
    tempDate = dateString.split("/")
    formatDate = "20" + tempDate[2] + "-" + tempDate[0] + "-" + tempDate[1]
    return formatDate