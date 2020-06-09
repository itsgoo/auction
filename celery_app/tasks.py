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
    auctions_meta = Auctions.objects.filter(start_auction = '0001-01-01', sort_auction__gte = 0 ).only('id', 'sort_auction')




    # last_hour = 23


    # p_del = ScheduleAuction.objects.all()
    # a_del = Auctions.objects.all()
    # # p_del.delete()


    # for d in p_del:
    #     if d.id == 119:
    #         d.active_date_time = 19
    #         d.save()

    # for a in a_del:
    #     if a.id == 90 or a.id == 91 or a.id == 93:
    #         a.start_auction_time = 0
    #         a.save()











    #get today date
    test_1 = date.today()
    s_year = test_1.year
    s_month = test_1.month
    s_day = test_1.day + 1
    s_date_next_day = date(s_year, s_month, s_day)
    print('new format active_date_time', s_date_next_day)


    
    
    # get free time for automatic auctions
    schedule_test = ScheduleAuction.objects.filter(active_time__gte = s_date_next_day).order_by('active_time')




    busy_times_date = []
    busy_times_time = []


    # get busy time
    for i in schedule_test:
        if str(i.active_time) not in busy_times_date:
            busy_times_date.append(str(i.active_time))

    print('busy_times_date', busy_times_date)
    busy_times_date_full = []
    
    for busy in busy_times_date:
        busy_times_date_full.append([busy])
        for i in schedule_test:
            if busy == str(i.active_time):
                busy_times_time.append(int(i.active_date_time))

        busy_times_date_full[-1].append(busy_times_time)
        busy_times_time = []

    print('busy_times_date_full', busy_times_date_full)




    # get free schedule time [[[2020-06-08], [1, 2, 3]], [[2020-06-09], [1, 2, 3]]]
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



    

    for i in auctions_meta:


        if total_free_time_each_day[0][1] == []:
            del total_free_time_each_day[0]

        print('i.id', i.id)
        active_time_auction = total_free_time_each_day[0][0]

        print('active_time_auction', active_time_auction)

        free_hour = total_free_time_each_day[0][1][0]

        print('free_hour', free_hour)


        s = ScheduleAuction(active_time = active_time_auction, auction = i, active_date_time = free_hour)
        s.save()

        i.sort_auction = 0
        i.start_auction = active_time_auction
        i.start_auction_time = free_hour
        i.save()
        print('i save sort_auction after ', i.sort_auction)
    


        del total_free_time_each_day[0][1][0]



        if total_free_time_each_day[0][1] == []:
            del total_free_time_each_day[0]

        print('total_free_time_each_day ', total_free_time_each_day)


















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
        



    return print('made schedule')










@shared_task
def update_post_status():

    

    



    #get today date
    test_1 = date.today()
    s_year = test_1.year
    s_month = test_1.month
    s_day = test_1.day 
    s_date_this_day = date(s_year, s_month, s_day)
    print('new format active_date_time', s_date_this_day)


    time_now = datetime.now() 
    actual_hour = time_now.hour
    
    print('s_hour', actual_hour)
    
    # get free time for automatic auctions
    schedule_test = ScheduleAuction.objects.filter(active_time = s_date_this_day)


    for actual_auction in schedule_test:

        # print('actual_auction.active_date_time', actual_auction.active_date_time)
        
        if actual_hour == int(actual_auction.active_date_time):
            current_auction_id = actual_auction.auction_id
            print('actual_auction', actual_auction.auction_id)



    change_auctions_status = Auctions.objects.all().only('id', 'status')


    # change last auction status(2) to 3
    # assign status to current auction

    for change_auctions in change_auctions_status:


        if change_auctions.status == 2 and change_auctions.id != current_auction_id:
            change_auctions.status = 3
            change_auctions.save()
            print('change_auctions.id status 3', change_auctions.id)
        elif change_auctions.id == current_auction_id:
            change_auctions.status = 2
            print('change_auctions.id status 2', change_auctions.id)
            change_auctions.save()



            p = Prices(new_price = change_auctions.start_price, auction=change_auctions, buyer_id=change_auctions.seller, winner=1)
            p.save()



        # if change_auctions.status == 2:
        #     change_auctions.status = 3
        #     change_auctions.save()
        #     print('change_auctions.id status 3', change_auctions.id)

        # if change_auctions.id == current_auction_id:
        #     if change_auctions.status != 2:
        #         change_auctions.status = 2
        #         print('change_auctions.id status 2', change_auctions.id)
        #         change_auctions.save()

        #         p = Prices(new_price = change_auctions.start_price, auction=change_auctions, buyer_id=change_auctions.seller, winner=1)
        #         p.save()











    # date = datetime.datetime.now()
    # dateyear = int(date.year)
    # datemonth = date.month
    # dateday = date.day - 1
    # yesterday = datetime.date(dateyear, datemonth, dateday)
    
    # today_auctions = Auctions.objects.filter(start_auction=date)

    # yesterday_auctions = Auctions.objects.filter(start_auction=yesterday)

    # print('yesterday date', yesterday)
    # for ya in yesterday_auctions:
    #     print('yesterday_auctions before', ya.id, ' ', ya.status)
    #     # ya.status = 3
    #     print('yesterday_auctions after', ya.status)
    #     # ya.save()

    # for i in today_auctions:
    #     if i.status != 2:
    #         print('today_auctions before', i.id, ' ', i.status)
    #         i.status = 2
    #         print('today_auctions after', i.status)
    #         # i.save()

    #         p = Prices(new_price = i.start_price, auction=i, buyer_id=i.seller, winner=1)
    #         # p.save()
    # # p_del = Prices.objects.get(id=159)
    # # p_del.delete()

    return print('status of yesterday auctions was update')




@shared_task
def update_auctions_with_no_bids_status():
    

    auctions_width_no_bids = Prices.objects.all().select_related('auction').prefetch_related('auction__seller')

    for price in auctions_width_no_bids:
        if price.winner == 1:
            if price.buyer_id.id == price.auction.seller.id:

                if price.auction.status != 2:
                    print('there is auction without bid', price.auction.id) 
                    price.auction.start_auction = '0001-01-01'
                    price.auction.save()

                    print('price.id delete', price.id)
                    price.delete()

                    try:
                        sh = ScheduleAuction.objects.get(auction_id = price.auction.id)
                        if sh:
                            sh.delete()
                    except:
                        pass
                



    return print('auctions who had no bids was moved to the end of the schedule list')
    




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

