from django.contrib import admin
from django.urls import path
from crawler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search_page, name = 'search_page'),
    path('results/<str:tribunal_choice>/<str:process_number>/', views.results_page, name = 'results_page')
]
