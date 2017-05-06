"""rpdSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rpdesign import views

urlpatterns = [
    url(r'^$', views.index_view),
    url(r'^admin/', admin.site.urls),
    url(r'^addVisit/', views.addVisit),
    url(r'^showVisit/', views.showVisit),
    url(r'^newVisit/', views.newVisit),
    url(r'^editTeeth/', views.editTeeth),
    url(r'^visitList/', views.showVisitList),
    url(r'^login/', views.login_post),
    url(r'^logout/', views.logout_get),
    url(r'^showPatient/', views.showPatient),
    url(r'^editPatient/', views.editPatient),
    url(r'^newStaff/', views.newStaff),
    url(r'^addStaff/', views.addStaff),
    url(r'^deleteVisit/', views.deleteVisits),
]
