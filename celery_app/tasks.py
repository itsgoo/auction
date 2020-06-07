# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
# from quick_publisher.celery import app
from .models import Auctions, Prices, ScheduleAuction
from datetime import datetime, timedelta, time, date


from django.utils import timezone
from django.utils.timezone import pytz
from pytz import timezone as tze


from django.db.models import Q

from dateutil.tz import tzutc, tzlocal


# from .settings import TIME_ZONE
# from demoapp.models import Widget



@shared_task
def everyDaySchedule():
    # open 24 hours tasks
    # activate hour auction: status 2
    # deactivate previos auction: status 3
    auctions_meta = Auctions.objects.filter(start_auction = '0001-01-01', sort_auction__gt = 0 ).only('id', 'sort_auction')




    # last_hour = 23


    # p_del = ScheduleAuction.objects.all()
    # p_del.delete()


    # time_actual = time(0, 00)
    # local_dt = timezone.localtime(datetime.now(), pytz.timezone('Asia/Tel_Aviv'))
    
    # print('timezone.localtime(timezone.now())', timezone.localtime(datetime(2003, 9, 27, 12, 40, 12, 156379)))

    # tzutc = datetime(2003, 9, 27, 12, 40, 12, 156379, tzinfo=tzutc())
    # print('tzutc', tzutc)
    # tzlocal = tzlokal
    # print('tzlocal', tzlocal)
















    # get max active time date
    max_schedule_date_q = ScheduleAuction.objects.all().only('active_time').order_by('-active_time')[0]
    max_schedule_date = max_schedule_date_q.active_time

    #get today date
    test_1 = date.today()
    s_year = test_1.year
    s_month = test_1.month
    s_day = test_1.day + 1
    s_date_next_day = date(s_year, s_month, s_day)
    print('new format active_date_time', s_date_next_day)


    
    
    # get free time for automatic auctions
    schedule_test = ScheduleAuction.objects.filter(active_time__gte = s_date_next_day)




    busy_times_date = []
    busy_times_time = []
    free_num_list_in_day = []


    
    for i in schedule_test:
        if str(i.active_time) not in busy_times_date:
            busy_times_date.append(str(i.active_time))

    busy_times_date_full = []
    
    for busy in busy_times_date:
        busy_times_date_full.append([busy])
        for i in schedule_test:
            if busy == str(i.active_time):
                busy_times_time.append(int(i.active_date_time))

        busy_times_date_full[-1].append(busy_times_time)
        busy_times_time = []

                

    print('busy_times_date_full', busy_times_date_full)



    positive_values = []
    total_free_time_each_day = []
    for busy_full in busy_times_date_full:
        print('busy_full[0]', busy_full[0])

        total_free_time_each_day.append([busy_full[0]])
        print('busy_full[0]', busy_full[1])


        for i in range(0, 24):

            if i not in busy_full[1]:
                positive_values.append(i)
        
        total_free_time_each_day[-1].append(positive_values)
        positive_values = []

    print('total_free_time_each_day', total_free_time_each_day)









    for i in range(0, 24):

        if i not in busy_times_date:
            free_num_list_in_day.append(i)
    print('free_num_list_in_day', free_num_list_in_day)



    # get [[2020-06-08], [1, 2, 3], [2020-06-09], [1, 2, 3]]

    for i in auctions_meta:

        print('i.id', i.id)
        active_time_auction = s_date_next_day

        print('active_time_auction', active_time_auction)

        free_hour = free_num_list_in_day[0]

        print('free_hour', free_hour)


        s = ScheduleAuction(active_time = active_time_auction, auction = i, active_date_time = free_hour)
        # s.save()

        i.sort_auction = 0
        i.start_auction = active_time_auction
        i.start_auction_time = free_hour
        # i.save()
        print('i save sort_auction after ', i.sort_auction)
    
        del free_num_list_in_day[0]



    # s_date_next_day_next = s_date_next_day + timedelta(days=1)
    # print('new format s_date_next_day_next', s_date_next_day_next)


















        # # print('i.id', i.id)
        # # print('i.sort_auction before', i.sort_auction)
        # # print('hour', hour)

        # if hour < last_hour:
            
        #     active_time_auction = datetime(actual_year, actual_month, actual_day)
            
        #     # utc translate time
        #     u = active_time_auction.replace(tzinfo=pytz.utc)
        #     aware_time_utc_helper = u.astimezone(pytz.timezone('Asia/Tel_Aviv'))

        #     # print('active_time_auction', active_time_auction)
        #     # print('aware_time_utc_helper', aware_time_utc_helper)


        #     s = ScheduleAuction(active_time = aware_time_utc_helper, auction = i, active_date_time = hour)
        #     # s.save()

        #     i.sort_auction = 0
        #     # i.save()
        #     # print('i save sort_auction after ', i.sort_auction)
        
        #     hour += 1

        # elif hour >= last_hour:
        #     hour = 0
        #     # print('hour = 0 elif', hour)
            
        #     actual_day += 1
        #     # print('actual_day next elif', actual_day)
        
        #     active_time_auction = datetime(actual_year, actual_month, actual_day)
            
        #     # utc translate time
        #     u = active_time_auction.replace(tzinfo=pytz.utc)
        #     aware_time_utc_helper = u.astimezone(pytz.timezone('Asia/Tel_Aviv'))

        #     # print('active_time_auction', active_time_auction)
        #     # print('aware_time_utc_helper', aware_time_utc_helper)


        #     s = ScheduleAuction(active_time = aware_time_utc_helper, auction = i)
        #     # s.save()

        #     i.sort_auction = 0
        #     # i.save()
        #     # print('i save sort_auction after ', i.sort_auction)
        



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

