from django.shortcuts import render, redirect
from django.views.generic.base import View
from .forms import RegisterUserForm, AuctionsForm, BidUpForm, ChangeUserData

from django.views.generic import CreateView

from django.urls import reverse_lazy


from django.contrib.auth.models import User, Group
from .models import Auctions, Bids, Prices, ImgForAuction, ScheduleAuction

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from django.core import serializers


from django.views.decorators.csrf import csrf_exempt

from django.core.files.base import ContentFile
from io import BytesIO
# Create your views here.

from django.shortcuts import get_object_or_404

import ast
from datetime import datetime, timedelta, time, date


from django.utils.timezone import pytz
from pytz import timezone as tze

class userGroups:
    def sellers(self):
        return User.objects.filter(groups = 1)

    def buyers(self):
        return User.objects.filter(groups = 2)



class Account_page(userGroups, View):

    def post(self, request):
        form = ChangeUserData(request.POST)

        if form.is_valid():
            print('valid change data form')

            user_data_form = get_object_or_404(User, id =request.user.id)

            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user_data_form.username = name
            user_data_form.email = email

            user_data_form.save()

            return redirect ('account_page')

    def get(self, request):


        user_data_form = get_object_or_404(User, id =request.user.id)
        form = ChangeUserData(instance = user_data_form)
        





        sellers_into_group = userGroups.sellers(self)

        # render for Sellers
        for i in sellers_into_group:
            if self.request.user.id == i.id:

                print('account seller')


                user_seller_auctions = Auctions.objects.filter(seller = self.request.user).order_by('-start_auction')
        

                # count the bids at auction
                bids = []
                winners = []
                count_bid = 0
                for auction in user_seller_auctions:
                    number_of_bids = Bids.objects.filter(auction = auction)
                    winner_buyer = Prices.objects.filter(auction = auction).filter(winner = 1)
                    for bid in number_of_bids:
                        # print('bid', bid.bid, bid.auction.id )
                        count_bid +=1

                
                    bids.append({auction.id: count_bid})
                    count_bid =0


                    for winner in winner_buyer:
                        
                        winners.append({winner.auction_id : 
                            {winner.new_price: winner.buyer_id}
                        })
                ctx = {
                    'form': form,
                    'groups_user_sellers': sellers_into_group,

                    'bids': bids,
                    'winners': winners,
                    'user_seller_auctions': user_seller_auctions,

                    
                }

        # render for Buyers
        buyers_into_group = userGroups.buyers(self)

        for i in buyers_into_group:
            if self.request.user.id == i.id:
                print('account buyer')
        
                

                user_auctions_short_from_prices = Prices.objects.filter(buyer_id = self.request.user.id, winner= 1, auction__status = 3).select_related('auction').prefetch_related('auction__seller').order_by('-auction__start_auction')

                
                user_auctions_short_from_prices_actual = Prices.objects.select_related('auction').filter(buyer_id = self.request.user.id, auction__status = 2).prefetch_related('auction__seller').order_by('-new_price_time')
                

                checked = []
                unique_actual_auctions_for_buyer = []
                # order preserving
                    
                for auctions in user_auctions_short_from_prices_actual:
                    if auctions.auction.id not in checked:
                        checked.append(auctions.auction.id)
                        unique_actual_auctions_for_buyer.append(auctions)

                

                print('f2', unique_actual_auctions_for_buyer)


                
                ctx = {
                    'form': form,
                    'buyers_into_group': buyers_into_group,
                    'unique_actual_auctions_for_buyer': unique_actual_auctions_for_buyer,

                    'user_auctions_short_from_prices_actual': user_auctions_short_from_prices_actual,
                    'user_auctions_short_from_prices': user_auctions_short_from_prices,
                }
        return render (request, 'account_page.html', ctx)




class CreateAuction(View):

    def post(self, request):

        form = AuctionsForm(request.POST, request.FILES)
        

        if form.is_valid():

            user_data_form = form.save(commit=True)


            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            seller = form.cleaned_data['seller']
            status = form.cleaned_data['status']
            start_price = form.cleaned_data['start_price']
            bid_up = form.cleaned_data['bid_up']
            start_auction = form.cleaned_data['start_auction']
            start_auction_time = form.cleaned_data['start_auction_time']
            sort_auction = form.cleaned_data['sort_auction']
            main_img = form.cleaned_data['main_img']


            user_data_form.title = title
            user_data_form.description = description
            user_data_form.seller = seller
            user_data_form.status = status
            user_data_form.start_price = start_price
            user_data_form.bid_up = bid_up
            user_data_form.start_auction = start_auction
            user_data_form.start_auction_time = start_auction_time
            user_data_form.sort_auction = sort_auction
            user_data_form.main_img = main_img



            user_data_form.save()



            # Get and Save additional images
            id_auction = user_data_form.pk
            auction = Auctions.objects.get(pk=id_auction)
            files = self.request.FILES.getlist('files')
            if files:
                for file in files:
                    fl = ImgForAuction(auction=auction, img = file)
                    print('fl', fl)
                    fl.save()



            if start_auction !=  date(1,1,1):
                s = ScheduleAuction(active_time = start_auction, auction = user_data_form, active_date_time = start_auction_time)
                
                s.save()
                print('schedule', s)
                


            return redirect ('index')

        else:
            print('form is invalid')
        
        return redirect('index')





    def get(self, request):
        
        form = AuctionsForm

        groups_user_sellers = User.objects.filter(groups=1)
        
        sort_query = Auctions.objects.only('sort_auction').order_by('-sort_auction')


        post_time = 0
        for i in sort_query:
            
            if i.sort_auction < post_time:
                pass
            elif i.sort_auction >= post_time:
                post_time = i.sort_auction


        post_time_ok = post_time + 1




        if self.request.is_ajax():
            date_dict = self.request.GET.get('start_auction', None)
            print('ok response success self', date_dict)
            
            leads_as_json = serializers.serialize('json', ScheduleAuction.objects.filter(active_time = date_dict).only('active_date_time').order_by('active_date_time'))
            






            print('acutal_dates_auctions', leads_as_json)

            return JsonResponse(dict(acutal_dates_auctions=leads_as_json), status=200)


        ctx = {
            'form': form,
            'post_time_ok': post_time_ok,
            'groups_user_sellers': groups_user_sellers,
        }

        return render(request, 'create_auction.html', ctx)











# class CreateAuction(LoginRequiredMixin, CreateView):
#     model = Auctions
#     template_name = 'create_auction.html'
#     form_class = AuctionsForm
#     success_url = reverse_lazy('index')
#     success_msg = 'Auction was created'


#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super(CreateAuction, self).get_context_data(**kwargs)
#         # Add in a QuerySet of all the posts


#         context['groups_user_sellers'] = User.objects.filter(groups=1)
        
#         sort_query = Auctions.objects.only('sort_auction').order_by('-sort_auction')


#         post_time = 0
#         for i in sort_query:
            
#             if i.sort_auction < post_time:
#                 pass
#             elif i.sort_auction >= post_time:
#                 post_time = i.sort_auction




#         context['post_time_ok'] = post_time + 1
        
#         return context

#     def form_valid(self, form):
#         form_valid = super().form_valid(form)

#         # Get and Save additional images
#         id = form.save().pk
#         auction = Auctions.objects.get(pk=id)
#         files = self.request.FILES.getlist('files')
#         if files:
#             for file in files:
#                 fl = ImgForAuction(auction=auction, img = file)
#                 print('fl', fl)
#                 fl.save()


        
#         return form_valid



    




class Index(View):

    def post(self, request):
        bidup_form = BidUpForm(request.POST)
        print('bidup_form view')
        if bidup_form.is_valid():
            print('bidup_form.cleaned_data[bid]')

            bid_data = bidup_form.save(commit=True)

            print('bid_data', bid_data)

            new_bid = bidup_form.cleaned_data['bid']
            auction = bidup_form.cleaned_data['auction']
            buyer = bidup_form.cleaned_data['buyer_id']

            print('auction', auction.id)
            prices = Prices.objects.filter(auction_id = auction.id)
            print('prices', prices)
            winner= 1

            price_for_main = new_bid
            for exist_price in prices:

                if new_bid < exist_price.new_price:
                    print('exist_price.new_price', exist_price.new_price, '> new_bid', new_bid)
                    winner=0
                    price_for_main = 'none'



            if winner == 1:
                winner_price = Prices.objects.filter(winner = 1, auction_id = auction.id)
                for win_old in winner_price:
                    win_old.winner=0
                    win_old.save()
                
                    
            new_price = Prices(new_price = new_bid, auction=auction, buyer_id=buyer, winner=winner)
            new_price.save()

            dict_bid_data = model_to_dict(bid_data)

            if price_for_main != 'none':
                dict_bid_data.update({"new_bid": price_for_main})
            print('model_to_dict(bid_data)', dict_bid_data)


        # return redirect('index')
        return JsonResponse({'bid_data': dict_bid_data}, status=200)


    def get(self, request):

















        winners = Prices.objects.filter(winner=1)
        additional_img = ImgForAuction.objects.all() 
        groups_user_buyers = User.objects.filter(groups = 2)
        form = BidUpForm
        groups_user_sellers = User.objects.filter(groups = 1)

        auctions_tomorrow = Auctions.objects.filter(status=1).order_by('-start_auction')
        auctions_today = Auctions.objects.filter(status=2).order_by('-start_auction')
        auctions_yesterday = Auctions.objects.filter(status=3).order_by('-start_auction')

        prices = Prices.objects.filter()

        current_user = request.user
        auction_bids = Bids.objects.all()

        # for i in auctions_today:
        #     i.id 


        ctx ={
            'form': form,
            'winners': winners,
            'current_user': current_user,
            'additional_img': additional_img,
            'prices': prices,
            'auctions_today': auctions_today,
            'auctions_tomorrow': auctions_tomorrow,
            'auctions_yesterday': auctions_yesterday,
            'auction_bids': auction_bids,
            'groups_user_buyers': groups_user_buyers,
            'groups_user_sellers': groups_user_sellers,
        }
        return render(request, 'index.html', ctx)



# old registration
#
# class LoginUserView(LoginView):
#     template_name = 'login.html'
#     form_class = AuthUserForm
#     success_url = reverse_lazy('index')
#     success_msg = 'Hi, User'
#     def get_success_url(self):
#         return self.success_url
#
# class LogOutUserView(LogoutView):
#     next_page = reverse_lazy('index')

class RegisterUserView(CreateView):
    model = User
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')
    success_msg = 'User was created'


    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        group = form.cleaned_data["groups"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)

        group_id = group[0].id
        my_group = Group.objects.get(id = group_id)
        print('User.id', self.request.user.id)
        my_group.user_set.add(self.request.user.id)
        return form_valid





# class RegisterUserView(CreateView):
#     model = User
#     template_name = 'register_user.html'
#     form_class = RegisterUserForm
#     success_url = reverse_lazy('index')
#     success_msg = 'User was created'


#     def form_valid(self, form):
#         form_valid = super().form_valid(form)
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]
#         group = form.cleaned_data["groups"]
#         auth_user = authenticate(username=username, password=password)
#         login(self.request, auth_user)

#         group_id = group[0].id
#         my_group = Group.objects.get(id = group_id)
#         print('User.id', self.request.user.id)
#         my_group.user_set.add(self.request.user.id)
#         return form_valid
