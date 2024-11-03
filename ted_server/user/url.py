from django.urls import path

from .views.add_dynamic import AddDynamic
from .views.edit_base_userinfo import EditBaseUserInfo
from .views.edit_user_avatar import EditUserAvatar
from .views.edit_user_collect import EditUserCollect
from .views.edit_user_info import EditUserInfo
from .views.edit_user_password import EditUserPassword
from .views.get_all_userinfo import GetAllUserInfo
from .views.get_dynamic_list import GetDynamicList
from .views.get_other_user_info import GetOtherUserInfo
from .views.get_userinfo import GetUserInfo
from .views.get_watch_list import GetWatchList
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
    path('GetOtherUserInfo/', GetOtherUserInfo.as_view(), name='GetOtherUserInfo'),
    # 获取其他用户信息
    path('GetDynamicList/', GetDynamicList.as_view(), name='GetDynamicList'),
    # 获取指定用户的动态列表或者自身关注的用户的动态列表
    path('AddDynamic/', AddDynamic.as_view(), name='AddDynamic'),
    # 添加动态
    path('EditUserCollect/',EditUserCollect.as_view(),name='EditUserCollect'),
    # 编辑用户收藏
    path('GetWatchList/',GetWatchList.as_view(),name='GetWatchList'),
    # 获取用户观看历史列表
]
