# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
# from quick_publisher.celery import app
from .models import Auctions, Prices, ScheduleAuction
from datetime import datetime, timedelta, time, date


from django.utils import timezone
from django.utils.timezone import pytz

from django.db.models import Q

# from .settings import TIME_ZONE
# from demoapp.models import Widget



@shared_task
def everyDaySchedule():
    # open 24 hours tasks
    # activate hour auction: status 2
    # deactivate previos auction: status 3
    auctions_meta = Auctions.objects.filter(start_auction = datetime.now(), sort_auction__gt = 0 ).only('id', 'sort_auction')



    date = datetime.now()   
    dateyear = int(date.year)
    datemonth = date.month
    dateday = date.day

    last_hour = 23


    # p_del = ScheduleAuction.objects.all()
    # p_del.delete()


    # time_actual = time(0, 00)
    # local_dt = timezone.localtime(datetime.now(), pytz.timezone('Asia/Tel_Aviv'))
    
    print('timezone.localtime(timezone.now())', timezone.localtime(timezone.now()))


    schedule_max_hour = ScheduleAuction.objects.all().only('active_time').order_by('-active_time')[0]
    print('schedule_max_hour', schedule_max_hour)

    last_auction_time = schedule_max_hour.active_time.time()
    hour = int(str(last_auction_time).split(':')[0])
    actual_hour = hour + 1

    # schedule_up_hour = schedule_max_hour.active_time + timedelta(minutes=60)


    active_time_auction = datetime(dateyear, datemonth, dateday, hour= actual_hour, tzinfo=timezone.utc)

    print('active_time_auction', active_time_auction)

    for i in auctions_meta:

        if hour < last_hour:
            
            print('i.id', i.id)
            print('i.sort_auction before', i.sort_auction)

            
            active_time_auction = datetime(dateyear, datemonth, dateday, hour= actual_hour, tzinfo=timezone.utc)
            
        
            print('active_time_auction', active_time_auction)
            
            s = ScheduleAuction(active_time = active_time_auction, auction = i)
            # s.save()

            i.sort_auction = 0
            # i.save()
            print('i save sort_auction after ', i.sort_auction)
        
            actual_hour += 1

        elif  hour >= last_hour:
            hour = 0
            dateday += 1
        




    return print('cron it works! 2')

@shared_task
def update_post_status():
    date = datetime.datetime.now()
    dateyear = int(date.year)
    datemonth = date.month
    dateday = date.day - 1
    yesterday = datetime.date(dateyear, datemonth, dateday)
    
    today_auctions = Auctions.objects.filter(start_auction=date)

    yesterday_auctions = Auctions.objects.filter(start_auction=yesterday)

    print('yesterday date', yesterday)
    for ya in yesterday_auctions:
        print('yesterday_auctions before', ya.id, ' ', ya.status)
        ya.status = 3
        print('yesterday_auctions after', ya.status)
        ya.save()

    for i in today_auctions:
        if i.status != 2:
            print('today_auctions before', i.id, ' ', i.status)
            i.status = 2
            print('today_auctions after', i.status)
            i.save()

            p = Prices(new_price = i.start_price, auction=i, buyer_id=i.seller, winner=1)
            p.save()
    # p_del = Prices.objects.get(id=159)
    # p_del.delete()

    return print('status of yesterday auctions was update')




@shared_task
def add_first_price():
    pass



@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

