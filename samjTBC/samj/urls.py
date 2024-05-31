# samj/urls.py

from django.urls import path
from .views import TbcView, ZielnummernView, add_entry, edit_entry, delete_entry, copy_entry
urlpatterns = [
    path('tbc/', TbcView.as_view(), name='tbc'),
    path('tbc/zielnummern/', ZielnummernView.as_view(), name='zielnummern'),
    path('tbc/add/', add_entry, name='add_entry'),
    path('tbc/edit/<int:entry_id>/', edit_entry, name='edit_entry'),
    path('tbc/delete/<int:entry_id>/', delete_entry, name='delete_entry'),
    path('tbc/copy/<int:entry_id>/', copy_entry, name='copy_entry'),
]

