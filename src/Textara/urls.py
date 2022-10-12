"""Textara URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home_app.views import *
from users_app.views import *
from otherfeatures_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('recognize', recognize, name='recognize'),
    path('home/recognize', recognize, name='recognize'),
    path('contact/', contact_view, name='contact'),
    path('about_us/', about_us_view, name='about_us'),
    path('other_features/', other_features_view, name='other_features'),
    path('login/', login_view, name='login'),
    path('login/login', login, name='login'),
    path('login/', login, name='login'),
    path('register/', register_view, name='register'),
    # path('register/login/', login_view, name='login'),
    path('register/register1', register1, name='register'),
    path('your_activities/', user_dashboard_view, name='your_activities'),
    path('logout/', logout, name='logout'),
    path('save_activity', save_activity, name='save_activity'),
    path('your_activities/delete/<int:id>',
         delete_activity, name='delete'),
    path('your_activities/save_as_doc/<text>&<id>',
         save_as_doc, name='save_as_doc'),
    path('your_activities/save_as_doc/save_as_pdf/<text>&<id>',
         save_as_pdf, name='save_as_pdf'),
    path('your_activities/save_as_doc/save_as_txt/<text>&<id>',
         save_as_txt, name='save_as_txt'),
    path('your_activities/save_as_doc/save_as_word/<text>&<id>',
         save_as_word, name='save_as_word'),
    path('save_as_doc_from_home/', save_as_doc_from_home,
         name='save_as_doc_from_home'),
    path('translator/', translator, name='translator'),
    path('translator/translate/', translate, name='translate'),
    path('contact/messagesent/', contact, name='contact1'),
    path('contact/messagesent/', contact, name='contact'),
    path('google_search/', google_search, name='google_search'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
