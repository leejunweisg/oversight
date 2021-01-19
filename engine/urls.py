from django.urls import path
from . import views # import views defined in views.py

# for profile pics
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # default home page
    path('dashboard-refresh/', views.dashboard_refresh, name='dashboard-refresh'), # for AJAX refresh
    path('create-stock/', views.StockCreateView.as_view(), name='create-stock'),
    path('delete-stock/<int:pk>/', views.StockDeleteView.as_view(), name='delete-stock'), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)