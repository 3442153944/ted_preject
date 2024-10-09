from django.urls import path

from .views.edit_user_avatar import EditUserAvatar
from .views.edit_user_info import EditUserInfo
from .views.get_all_userinfo import GetAllUserInfo
from .views.get_userinfo import GetUserInfo
from .views.register import RegisterView
from .views.update_top_video import UpdateTopVideo

urlpatterns=[
    path('RegisterView/',RegisterView.as_view(),name='RegisterView'),
    #注册视图
    path('GetUserInfo/',GetUserInfo.as_view(),name='GetUserInfo'),
    #获取用户信息
    path('GetAllUserInfo/',GetAllUserInfo.as_view(),name='GetAllUserInfo'),
    #获取所有用户信息
    path('EditUserInfo/',EditUserInfo.as_view(),name='EditUserInfo'),
    #编辑用户信息
    path('EditUserAvatar/',EditUserAvatar.as_view(),name='EditUserAvatar'),
    #编辑用户头像
    path('UpdateTopVideo/',UpdateTopVideo.as_view(),name='UpdateTopVideo'),
    #更新置顶视频
]