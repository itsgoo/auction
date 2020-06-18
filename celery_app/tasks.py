# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import Auctions, Prices, ScheduleAuction, Notifications
from datetime import datetime, timedelta, time, date


from django.utils import timezone
from django.utils.timezone import pytz
from pytz import timezone as tze


from django.db.models import Q

from dateutil.tz import tzutc, tzlocal

from django.core.mail import send_mail

from django.contrib.auth.models import User




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

    current_auction_id = 'none'
    for actual_auction in schedule_test:

        # print('actual_auction.active_date_time', actual_auction.active_date_time)
        
        if actual_hour == int(actual_auction.active_date_time):
            current_auction_id = actual_auction.auction_id
            print('current_auction_id', current_auction_id)




    change_auctions_status = Auctions.objects.all().only('id', 'status', 'seller_id')



    # change last auction status(2) to 3
    # assign status to current auction

    for change_auctions in change_auctions_status:


        if change_auctions.id != current_auction_id:
            if change_auctions.status == 2: 
                change_auctions.status = 3
                change_auctions.save()

                notif_end_of_auciton.delay(change_auctions.id)

                print('change_auctions.id status 3', change_auctions.id)

        elif change_auctions.id == current_auction_id:
            change_auctions.status = 2
            print('change_auctions.id status 2', change_auctions.id)
            change_auctions.save()


            start_auction_to_seller.delay(change_auctions.seller_id)

            p = Prices(new_price = change_auctions.start_price, auction=change_auctions, buyer_id=change_auctions.seller, winner=1)
            p.save()

            notif_for_current_auction = Notifications.objects.filter(auction_id = change_auctions)
            print('notif_for_current_auction delete' , notif_for_current_auction)

            notif_for_current_auction.delete()


        # elif change_auctions.status != 2: 
        #     if change_auctions.id == current_auction_id:
        #         change_auctions.status = 2
        #         print('change_auctions.id status 2', change_auctions.id)
        #         change_auctions.save()




    return print('update_post_status')


















@shared_task
def update_auctions_with_no_bids_status():
    

    auctions_width_no_bids = Prices.objects.all().select_related('auction').prefetch_related('auction__seller')

    for price in auctions_width_no_bids:
        if price.winner == 1:
            print('price.winner == 1 in auction id', price.auction.id)

            if price.buyer_id.id == price.auction.seller.id:
                print('price.buyer_id.id == price.auction.seller.id', price.buyer_id.id)
                

                if price.auction.status != 2:
                    print('there is auction without bid', price.auction.id) 
                    price.auction.start_auction = '0001-01-01'
                    price.auction.status = 1
                    price.auction.save()

                    next_auction_schedule.delay(price.auction.id)

                    print('price.id delete', price.id)
                    price.delete()


                    try:
                        sh = ScheduleAuction.objects.get(auction_id = price.auction.id)
                        if sh:
                            sh.delete()
                    except:
                        pass
                

    return print('update_auctions_with_no_bids_status')
    




















@shared_task
def everyDaySchedule():
    # open 24 hours tasks
    # activate hour auction: status 2
    # deactivate previos auction: status 3
    auctions_meta = Auctions.objects.filter(start_auction = '0001-01-01', sort_auction__gte = 0 ).only('id', 'sort_auction')



    # p_del = ScheduleAuction.objects.all()
    # # p_del.delete()


    # for d in p_del:
    #     if d.id == 119:
    #         d.active_date_time = 19
    #         d.save()


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
        if i.active_time not in busy_times_date:
            busy_times_date.append(i.active_time)

    print('busy_times_date', busy_times_date)



    if busy_times_date == []:
        busy_times_date = [s_date_next_day]


    print('auctions_meta.lendth()', len(auctions_meta))



    new_days = []

    next_date = date(s_year, s_month, s_day)
    end_date = busy_times_date[-1]

    while next_date <= end_date:

        new_days.append(str(next_date))
        next_date = next_date + timedelta(days = 1)



        # for i in busy_times_date:
        #     sep = i.split('-')
        #     # print('i', sep)
        #     this_date = date(int(sep[0]), int(sep[1]), int(sep[2]))
        #     print('this_date', this_date)
        #     print('next_date', next_date)

        #     if this_date == next_date:
        #         # print('ok date', this_date)
        #         new_days.append(str(next_date))
        #         next_date = next_date + timedelta(days = 1)

        #     if this_date != next_date:
        #         new_days.append(str(next_date))
        #         next_date = next_date + timedelta(days = 1)
        





    print('new_days', new_days)


    busy_times_date_full = []
    
    for busy in new_days:
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

        auction_in_schedule.delay(i.id, str(active_time_auction), int(free_hour))

        i.sort_auction = 0
        i.start_auction = active_time_auction
        i.start_auction_time = free_hour
        i.save()
        print('i save sort_auction after ', i.sort_auction)
    
        del total_free_time_each_day[0][1][0]


        if total_free_time_each_day[0][1] == []:
            del total_free_time_each_day[0]

        print('total_free_time_each_day ', total_free_time_each_day)


    return print('everyDaySchedule')





















































@shared_task
def auction_in_schedule(auction_id, active_time_auction, free_hour):

    auction = Auctions.objects.get(id = auction_id)
    email = auction.seller.email
    auction_name = auction.title
    text = 'your auction: %s will in schedule at %s and %d hour' %(auction_name, active_time_auction, free_hour)

    send_mail(
        'your auction in schedule!',
        text,
        'admin@onehourbid.com',
        [email],
    )
    print('notif auction_in_schedule id', auction_id)











@shared_task
def start_auction_notification():
    #get today date
    test_1 = date.today()
    s_year = test_1.year
    s_month = test_1.month
    s_day = test_1.day
    s_date_this_day = date(s_year, s_month, s_day)
    print('new format active_date_time', s_date_this_day)

    time_now = datetime.now() 
    next_hour = int(time_now.hour) + 1

    minutes_left = 60 - int(time_now.minute)

    print('minutes_left', minutes_left)

    next_auction = ScheduleAuction.objects.filter(active_time = s_date_this_day).get(active_date_time = next_hour)

    print(next_auction)

    current_notifications = Notifications.objects.filter(auction_id = next_auction.auction_id)

    print('current_notifications', current_notifications)
    current_subscribers = []
    for all_sub in current_notifications:
        if all_sub.subscriber.email not in current_subscribers:
            current_subscribers.append(all_sub.subscriber.email)

    for notif in current_notifications:

        if notif.subscriber.email in current_subscribers:
            text = 'Auction - %s will start in %d minutes' %(notif.auction_id, minutes_left)

            print('notif auction.seller_id', notif.subscriber.email)
            
            send_mail(
                'next auction will start soon!',
                text,
                'admin@onehourbid.com',
                [notif.subscriber.email],
            )
            current_subscribers.remove(notif.subscriber.email)
    






@shared_task
def new_registration(email):
    
    text = 'Welcome to auction 10bid area!'
    
    print('notif new_registration', email)
    send_mail(
        'Congratulation!',
        text,
        'admin@onehourbid.com',
        [email],
    )




@shared_task
def start_auction_to_seller(seller_id):
    
    user = User.objects.get(id = seller_id)

    text = 'Your auction was start'
    email = user.email
    
    print('notif start_auction_to_seller', email)
    send_mail(
        'Congratulation!',
        text,
        'admin@onehourbid.com',
        [email],
    )



@shared_task
def auction_to_schedule(email):
    
    text = 'Your auction was start at '
    
    print('notif auction_to_schedule', email)
    send_mail(
        'Congratulation!',
        text,
        'admin@onehourbid.com',
        [email],
    )



@shared_task
def notif_end_of_auciton(auction_id):

    auctions_width_no_bids = Prices.objects.filter(auction_id = auction_id).select_related('auction').prefetch_related('auction__seller').order_by('new_price_time')

    players = []
    for price in auctions_width_no_bids:

        if price.buyer_id.id == price.auction.seller.id:
            if price.winner == 1:
                # wasnt bid
                email = price.auction.seller.email
                text = 'wasnt bid'
                print('notif_end_of_auciton wasnt bid', auction_id)
                send_mail(
                    'Congratulation!',
                    text,
                    'admin@onehourbid.com',
                    [email],
                )

                break

        elif price.buyer_id.id != price.auction.seller.id:
            if price.winner == 1:
                # winner!
                email = price.buyer_id.email
                text = 'you are a winner!'

                print('notif notif_end_of_auciton winner', email)
                send_mail(
                    'Congratulation!',
                    text,
                    'admin@onehourbid.com',
                    [email],
                )



                print('notif notif_end_of_auciton winner', price.auction.seller.email)
                send_mail(
                    'Congratulations!',
                    'your auction was sold for %d' %price.new_price,
                    'admin@onehourbid.com',
                    [price.auction.seller.email],
                )

                # add athis email to players array

            elif price.winner != 1:
                # players!
                if price.buyer_id.email not in players:
                    email = price.buyer_id.email
                    text = 'you arent a winner, try again!'

                    print('notif notif_end_of_auciton not a winner', email)
                    send_mail(
                        'Congratulation!',
                        text,
                        'admin@onehourbid.com',
                        [email],
                    )

                    players.append(price.buyer_id.email)



@shared_task
def next_auction_schedule(auction_id):
    print('next_auction_schedule', auction_id)




@shared_task
def sending_email_about_new_price(buyer_id, auction_title, bid, email):

    text = 'User %d has new leader of the aution %s, with highest bid %d' %( buyer_id, auction_title, bid)

    print('notif sending_email_about_new_price buyer email', email)
    send_mail(
        'new bid at the auction you are interested in!',
        text,
        'admin@onehourbid.com',
        [email],
    )






















@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

