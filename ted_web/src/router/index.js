import { createRouter, createWebHistory } from 'vue-router'
import index_recommend from '../components/index_com/index_recommend.vue'
import content_page from '../components/content_page/content_page.vue'
import login from '../components/login_page/login.vue'
import register from '../components/register_page/register.vue'
import root from '../components/root.vue'
import index_page from '../components/index_page.vue'
import user_center from '../components/user_center/user_center.vue'
import upload_page from '../components/video_upload_page/upload_page.vue'
import other_user_center from '../components/other_user_center/index_page.vue'
import dynamic_page from '../components/dynamic_page/dynamic_index.vue'
import history_page from '../components/head_page/history_page.vue'
import admin_index from '../components/admin_control/admin_index.vue'
import fans_list from '../components/head_page/components/fans_list.vue'
import follow_list from '../components/head_page/components/follow_list.vue'
import msg_box from '../components/head_page/components/msg_box.vue'

const routes = [
  {
    path: '/',
    component: root,
    children: [
      {
        path: '',  // 默认加载的子路由，当路径为 / 时，显示 index_page
        component: index_page,
        children: [
          {
            path: '',  // 当路径为 / 时显示推荐页面
            component: index_recommend
          },
          {
            path: 'content_page',
            name: 'content_page',
            component: content_page//内容页面
          },
          {
            path:'user_center',
            name:'user_center',
            component:user_center//用户中心
          },
          {
            path:'upload_page',
            name:'upload_page',
            component:upload_page//上传页面
          },
          {
            path:'other_user_center',
            name:'other_user_center',
            component:other_user_center//其他用户中心
          },
          {
           path:'dynamic_page',
           name:'dynamic_page',
           component:dynamic_page//动态页面
          },
          {
            path:'history_page',
            name:'history_page',
            component:history_page//历史页面
          },
          {
            path:'follow_list',
            name:'follow_list',
            component:follow_list//关注列表
          },
          {
            path:'fans_list',
            name:'fans_list',
            component:fans_list//粉丝列表
          },
          {
            path:'msg_box',
            name:'msg_box',
            component:msg_box//消息盒子
          }
        ]
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: login//登录页面
  },
  {
    path: '/register',
    name: 'register',
    component: register//注册页面
  },{
    path: '/admin',
    name: 'admin',
    component: admin_index//管理员页面
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
