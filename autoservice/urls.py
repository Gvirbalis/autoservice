from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymas'),
    path('uzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas-detail'),
    path('search/', views.search, name='search'),
    path('about/' ,views.about,name='about'),
    path('akcijos/' ,views.akcijos,name='akcijos'),
    path('manoautomobiliai/', views.LoanedUzsakymaiByUserListView.as_view(), name='mano-uzsakymai'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('main/', views.profilis2, name='main'),
]