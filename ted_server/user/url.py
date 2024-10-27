from django.urls import path

from .views.edit_base_userinfo import EditBaseUserInfo
from .views.edit_user_avatar import EditUserAvatar
from .views.edit_user_info import EditUserInfo
from .views.edit_user_password import EditUserPassword
from .views.get_all_userinfo import GetAllUserInfo
from .views.get_userinfo import GetUserInfo
from .views.register import RegisterView
from .views.update_follow import UpdateFollow
from .views.update_top_video import UpdateTopVideo

urlpatterns = [
    path('RegisterView/', RegisterView.as_view(), name='RegisterView'),
    # 注册视图
    path('GetUserInfo/', GetUserInfo.as_view(), name='GetUserInfo'),
    # 获取用户信息
    path('GetAllUserInfo/', GetAllUserInfo.as_view(), name='GetAllUserInfo'),
    # 获取所有用户信息
    path('EditUserInfo/', EditUserInfo.as_view(), name='EditUserInfo'),
    # 编辑用户信息
    path('EditUserAvatar/', EditUserAvatar.as_view(), name='EditUserAvatar'),
    # 编辑用户头像
    path('UpdateTopVideo/', UpdateTopVideo.as_view(), name='UpdateTopVideo'),
    # 更新置顶视频
    path('EditBaseUserInfo/', EditBaseUserInfo.as_view(), name='EditBaseUserInfo'),
    # 更新用户基础信息
    path('EditUserPassword/', EditUserPassword.as_view(), name='EditUserPassword'),
    # 更新用户密码
    path('UpdateFollow/', UpdateFollow.as_view(), name='UpdateFollow'),
    # 更新关注状态
]
