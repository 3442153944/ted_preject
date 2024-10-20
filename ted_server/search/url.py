from django.urls import path

from .view.search import Search

urlpatterns=[
    path('Search/',Search.as_view(),name='search'),
    # 搜索接口
]