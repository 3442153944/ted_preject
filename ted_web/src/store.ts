import { createStore } from 'vuex';
import { RootState } from './store.d'; // 引入RootState类型
import createPersistedState from 'vuex-persistedstate'; // 引入持久化插件

// 最大栈深度
const MAX_STACK_DEPTH = 500;

const store = createStore<RootState>({
    state: {
        pageStatus: {
            login_page_show: false,
            index_page_show: true,
            register_page_show: false,
        },
        content_page: {},
        pageStack: [],
        pushTimer: null,
        video_id: '',
        is_login: false,
        other_user_id: '',
        global_msg: '',//全局通知消息
        comment_msg: '',//评论消息
        main_comment_index:null,//如果是子评论将会记录父评论的索引
        user:localStorage.getItem('user')?JSON.parse(localStorage.getItem('user') as string):null,
    },
    mutations: {
        SET_SINGLE_PAGE_STATUS(state:any, { key = '', value = false }) {
            if (key === 'all') {
                for (const k in state.pageStatus) {
                    if (Object.prototype.hasOwnProperty.call(state.pageStatus, k) && typeof state.pageStatus[k] === 'boolean') {
                        state.pageStatus[k] = false;
                    }
                }
                return;
            }
            for (const k in state.pageStatus) {
                if (Object.prototype.hasOwnProperty.call(state.pageStatus, k) && typeof state.pageStatus[k] === 'boolean') {
                    state.pageStatus[k] = false;
                }
            }
            state.pageStatus[key] = value;
            const allFalse = Object.keys(state.pageStatus).every(k => typeof state.pageStatus[k] !== 'boolean' || state.pageStatus[k] === false);
            if (allFalse) {
                state.pageStatus.index_page = true;
            }
        },
        SET_CONTENT_PAGE(state:any, { key = '', value = false }) {
            for (const k in state.content_page) {
                if (Object.prototype.hasOwnProperty.call(state.content_page, k) && typeof state.content_page[k] === 'boolean') {
                    state.content_page[k] = false;
                }
            }
            state.content_page[key] = value;
        },
        PUSH_PAGE_STATE(state:any) {
            if (state.pageStack.length >= MAX_STACK_DEPTH) {
                state.pageStack.shift(); // 删除最早的记录
            }
            state.pageStack.push({
                pageStatus: JSON.parse(JSON.stringify(state.pageStatus)), // 深拷贝页面状态
                content_page: JSON.parse(JSON.stringify(state.content_page)), // 深拷贝内容页面状态
            });
        },
        POP_PAGE_STATE(state:any) {
            if (state.pageStack.length > 0) {
                const previousState = state.pageStack.pop();
                state.pageStatus = previousState.pageStatus;
                state.content_page = previousState.content_page;
            }
        },
        RESET_PAGE_STACK(state:any) {
            state.pageStack = [];
            state.pushTimer = null; // 清除定时器
        },
        set_video_id(state:any, video_id:any) {
            state.video_id = video_id;
        },
        set_login_status(state:any, is_login:any) {
            state.is_login = is_login;
        },
        set_other_user_id(state:any, other_user_id:any) {
            state.other_user_id = other_user_id;
        },
        set_global_msg(state:any, global_msg:any) {
            state.global_msg = global_msg;
        },
        set_comment_msg(state:any, comment_msg:any) {
            state.comment_msg = comment_msg;
        },
        set_main_comment_index(state:any, main_comment_index:any) {
            state.main_comment_index = main_comment_index;
        }
    },
    actions: {
        goBack({ commit }:{commit:Function}) {
            commit('POP_PAGE_STATE'); // 恢复上一个状态
        }
    },
    getters: {
        login_page_show: (state:any) => state.pageStatus.login_page_show,
        index_page_show: (state:any) => state.pageStatus.index_page_show,
        register_page_show: (state:any) => state.pageStatus.register_page_show,
        video_id: (state:any) => state.video_id,
        is_login: (state:any) => state.is_login,
        other_user_id: (state:any) => state.other_user_id,
        global_msg: (state:any) => state.global_msg,
        comment_msg: (state:any) => state.comment_msg,//评论内容
        main_comment_index: (state:any) => state.main_comment_index,//主评论索引，如果为主评论该项为null
        user:(state:any)=>state.user,//用户信息
    },
    // 添加持久化插件
    plugins: [
        createPersistedState({
            storage: window.localStorage, // 选择 localStorage 进行持久化存储
            // 可以根据需求选择哪些状态需要持久化
            reducer: (state) => ({
                pageStatus: state.pageStatus,
                video_id: state.video_id,
                is_login: state.is_login,
            }),
        }),
    ],
});

export default store;
