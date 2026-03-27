from django.urls import path
from . import views

urlpatterns = [
    # Keyword endpoints
    path('keywords/', views.KeywordListCreateView.as_view(), name='keyword-list'),
    path('keywords/<int:pk>/', views.KeywordDetailView.as_view(), name='keyword-detail'),
    
    # Scan endpoints
    path('scan/', views.ScanTriggerView.as_view(), name='scan-trigger'),
    path('rescan/<int:content_item_id>/', views.RescanContentItemView.as_view(), name='rescan'),
    
    # Flag endpoints
    path('flags/', views.FlagListView.as_view(), name='flag-list'),
    path('flags/<int:pk>/', views.FlagUpdateView.as_view(), name='flag-update'),
]

