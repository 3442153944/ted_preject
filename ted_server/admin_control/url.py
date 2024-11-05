from django.urls import path

from .views.admin_check import AdminCheck
from .views.get_user_list import GetUserList

urlpatterns = [
    path('AdminCheck/', AdminCheck.as_view(), name='AdminCheck'),
    # 管理员权限检查
    path('GetUserList/', GetUserList.as_view(),name='GetUserList'),
    # 获取用户列表
]
