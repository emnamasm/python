from django.urls import path
from .views import *
urlpatterns=[
    path('list/',conferenceList,name="listconf"),
    path('listViewconference/',ConferenceListView.as_view(),name="listviewconf"),
    path('details/<int:pk>/',DetailsViewConference.as_view(),name="detailConf"),
]
#toujous le name="detailConf" on l utilise dans la page html dans les urls