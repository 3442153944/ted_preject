from django.urls import path

from .views.admin_check import AdminCheck
from .views.edit_user_info import EditUserInfo
from .views.get_user_list import GetUserList
from .views.reset_user_avatar import ResetUserAvatar

urlpatterns = [
    path('AdminCheck/', AdminCheck.as_view(), name='AdminCheck'),
    # 管理员权限检查
    path('GetUserList/', GetUserList.as_view(), name='GetUserList'),
    # 获取用户列表
    path('EditUserInfo/', EditUserInfo.as_view(), name='EditUserInfo'),
    # 编辑用户信息
    path('ResetUserAvatar/',ResetUserAvatar.as_view(),name='ResetUserAvatar'),
    # 重置用户头像
]
