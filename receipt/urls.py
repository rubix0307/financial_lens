from django.urls import path

from . import views

urlpatterns = [
    path('', views.receipt_list_view, name='receipt_list'),
    path('receipt/<int:receipt_id>/', views.receipt_detail_view, name='receipt_detail'),
    path('receipt/<int:receipt_id>/edit/', views.receipt_detail_view, name='receipt_edit'),
    path('receipt/<int:receipt_id>/delete/', views.receipt_delete_view, name='receipt_delete'),
]