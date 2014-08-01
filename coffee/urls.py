from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^$', views.CoffeeList.as_view(), name='coffee-list'),
    url(
        r'^(?P<coffee_id>\d+)/$', 
        views.CoffeeRoastProfileList.as_view(), 
        name='coffeeroastprofile-list'
    ),
    url(r'^create/$', views.GreenCoffeeCreate.as_view(), name='greencoffee-new'),
    url(r'^component/create/$', views.CoffeeComponentCreate.as_view(), name='coffeecomponent-new'),
    url(r'^blend/create/$', views.CoffeeCreate.as_view(), name='coffee-new'),
)