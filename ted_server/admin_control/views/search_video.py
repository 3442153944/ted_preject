from .BaseApiView import BaseAPIView
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
import json


class SearchVideo(BaseAPIView):

    def post(self, request, *args, **kwargs):
        # 检查管理员权限
        admin_auth = self.check_admin_permission(request)
        if admin_auth:
            return admin_auth

        try:
            # 解析请求体数据
            data = json.loads(request.body.decode('utf-8'))
            search_type = data.get('search_type', None)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)

            # 参数校验
            if not search_type:
                return JsonResponse({"status": 400, 'msg': '缺少参数'}, status=400)

            # 处理搜索条件
            search_query = f"%{search_type}%"

            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 查询总数
                    total = self.get_total_count(cursor, search_query)

                    # 查询视频数据
                    result = self.get_video_results(cursor, search_query, limit, offset)

            return JsonResponse({"status": 200, 'msg': 'success', 'data': result, 'total': total}, status=200)

        except DatabaseError as db_err:
            return self.handle_database_error(request, db_err)
        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({"status": 500, 'msg': '服务器错误'}, status=500)

    def get_total_count(self, cursor, search_query):
        """
        获取符合条件的视频总数
        """
        count_sql = '''
            SELECT COUNT(*)
            FROM video_info
            LEFT JOIN auth_user ON auth_user.id = video_info.author_id
            WHERE video_info.id LIKE %s OR video_info.title LIKE %s 
                OR auth_user.id like %s OR auth_user.username LIKE %s
        '''
        cursor.execute(count_sql, (search_query, search_query, search_query, search_query))
        return cursor.fetchone()[0]

    def get_video_results(self, cursor, search_query, limit, offset):
        """
        获取符合条件的视频数据
        """
        search_video_sql = '''
            SELECT video_info.id AS video_id, video_info.title AS video_title, video_info.author,
                   video_info.author_id, video_info.introduce AS video_introduce, video_info.create_time, 
                   video_info.tags AS video_tags, video_info.video_file_path, video_info.video_status,
                   video_info.video_cover_path, auth_user.id AS user_id, auth_user.username, 
                   auth_user.avatar_path,
                   (SELECT COUNT(*) FROM watch_table WHERE video_id = video_info.id) AS watch_count,
                   (SELECT COUNT(*) FROM like_table WHERE video_id = video_info.id) AS like_count,
                   (SELECT COUNT(*) FROM collect_table WHERE video_id = video_info.id) AS collect_count
            FROM video_info
            LEFT JOIN auth_user ON auth_user.id = video_info.author_id
            WHERE video_info.id LIKE %s OR video_info.title LIKE %s 
                OR auth_user.id like %s OR auth_user.username LIKE %s
            LIMIT %s OFFSET %s
        '''
        cursor.execute(search_video_sql, (search_query, search_query, search_query, search_query, limit, offset))
        return self.format_result(cursor)
