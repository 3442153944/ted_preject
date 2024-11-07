from django.urls import path

from .views.admin_check import AdminCheck
from .views.delete_comment import DeleteComment
from .views.delete_user import DeleteUser
from .views.delete_video import DeleteVideo
from .views.edit_user_info import EditUserInfo
from .views.get_comment_list import GetCommentList
from .views.get_user_list import GetUserList
from .views.get_video_list import GetVideoList
from .views.reset_user_avatar import ResetUserAvatar
from .views.search_comment import SearchComment
from .views.search_user import SearchUser
from .views.search_video import SearchVideo

urlpatterns = [
    path('AdminCheck/', AdminCheck.as_view(), name='AdminCheck'),
    # 管理员权限检查
    path('GetUserList/', GetUserList.as_view(), name='GetUserList'),
    # 获取用户列表
    path('EditUserInfo/', EditUserInfo.as_view(), name='EditUserInfo'),
    # 编辑用户信息
    path('ResetUserAvatar/', ResetUserAvatar.as_view(), name='ResetUserAvatar'),
    # 重置用户头像
    path('SearchUser/', SearchUser.as_view(), name='SearchUser'),
    # 搜索用户
    path('GetVideoList/', GetVideoList.as_view(), name='GetVideoList'),
    # 获取视频列表
    path('DeleteUser/', DeleteUser.as_view(), name='DeleteUser'),
    # 删除用户
    path('DeleteVideo/', DeleteVideo.as_view(), name='DeleteVideo'),
    # 删除视频
    path('SearchVideo/', SearchVideo.as_view(), name='SearchVideo'),
    # 搜索视频
    path('GetCommentList/', GetCommentList.as_view(), name='GetCommentList'),
    # 获取评论列表
    path('SearchComment/', SearchComment.as_view(), name='SearchComment'),
    # 搜索评论
    path('DeleteComment/', DeleteComment.as_view(), name='DeleteComment'),
    # 删除评论
]
