from django.conf.urls import url
from django.urls import re_path, path, include
from .views import Index, CreateAuction, RegisterUserView, Account_page, Reports, UserReports, Company
# from .views import LoginUserView, LogOutUserView
from django.conf.urls.static import static
from celery_proj.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    re_path(r'^$', Index.as_view(), name='index'),

    path('company', Company.as_view(), name='company_page'),
    path('account-page', Account_page.as_view(), name='account_page'),
    path('reports', Reports.as_view(), name='reports_page'),
    re_path(r'^reports/id/(?P<pk>\d+)$', UserReports.as_view(), name='user_reports_page'),
    
    url('create', CreateAuction.as_view(), name='create_auction'),
    url('register', RegisterUserView.as_view(), name='register_page'),

    path('accounts/', include('django.contrib.auth.urls')),
    # path('silk/', include('silk.urls', namespace='silk')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

