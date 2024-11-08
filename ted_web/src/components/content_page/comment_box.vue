<template>
  <div class="comment_box">
    <h2>评论</h2>
    <div class="content">
      <!-- 遍历主评论和子评论 -->
      <div class="comment_group" v-for="(mainComment, index) in displayedMainComments" :key="index">
        <!-- 主评论 -->
        <div class="main_comment">
          <div class="comment_info">
            <div class="user_box">
              <div class="avatar">
                <img :src="'http://localhost:8000/static/img/thumbnail/' + mainComment.avatar_path + '.png'" alt="用户头像">
              </div>
            </div>
            <div class="comment_content">
              <div class="username">
                <span @click="to_other_user_center(mainComment.user_id)">{{ mainComment.username }}</span>
                <div class="follow_btn" :class="mainComment.is_follow ? 'is_follow' : 'not_follow'"
                  @click="switch_follow_status('main', index, null)">
                  <span>{{ mainComment.is_follow ? '已关注' : '关注' }}</span>
                </div>
              </div>
              <p>{{ mainComment.comment_content }}</p>
              <div class="comment_interaction">
                <div class="interaction_box">
                  <div class="inter_box" @click="comm_interaction(mainComment.comment_id, 'comment', 'like')">
                    <img src="../../assets/svg/点赞.svg" alt="点赞">
                    <span>{{ mainComment.like_count }}</span>
                  </div>
                  <div class="inter_box" @click="comm_interaction(mainComment.comment_id, 'comment', 'not_like')">
                    <img src="../../assets/svg/踩.svg" alt="踩">
                    <span>{{ mainComment.not_like_count }}</span>
                  </div>
                  <div class="inter_box" @click="toggleReplyInput(index, 0)">
                    <img src="../../assets/svg/留言.svg" alt="回复">
                    <span>回复</span>
                  </div>
                </div>
                <span>{{ mainComment.send_time }}</span>
              </div>

              <!-- 主评论回复框 -->
              <comment_input_box v-if="comment_input_box_show[index][0]" :comment_type="'reply'"
                :comment_id="mainComment.comment_id" :video_id="video_id" />
            </div>
          </div>
        </div>

        <!-- 子评论 -->
        <div class="reply_comments" v-for="(reply, replyIndex) in displayedSubComments(index)" :key="reply.comment_id">
          <div class="reply_comment">
            <div class="comment_info">
              <div class="user_box">
                <div class="avatar">
                  <img :src="'http://localhost:8000/static/img/thumbnail/' + reply.avatar_path + '.png'" alt="用户头像">
                </div>
              </div>
              <div class="comment_content">
                <div class="username">
                  <span @click="to_other_user_center(reply.user_id)">{{ reply.username }}</span>
                  <div class="follow_btn" :class="reply.is_follow ? 'is_follow' : 'not_follow'"
                    @click="switch_follow_status('sub', index, replyIndex)">
                    <span>{{ reply.is_follow ? '已关注' : '关注' }}</span>
                  </div>
                </div>
                <p>回复:<span style="color: rgb(11,11,200);">@{{ reply.re_username }}</span> {{ reply.comment_content }}
                </p>
                <div class="comment_interaction">
                  <div class="interaction_box">
                    <div class="inter_box" @click="comm_interaction(reply.comment_id, 'reply', 'like')">
                      <img src="../../assets/svg/点赞.svg" alt="点赞">
                      <span>{{ reply.like_count }}</span>
                    </div>
                    <div class="inter_box" @click="comm_interaction(reply.comment_id, 'reply', 'not_like')">
                      <img src="../../assets/svg/踩.svg" alt="踩">
                      <span>{{ reply.not_like_count }}</span>
                    </div>
                    <div class="inter_box" @click="toggleReplyInput(index, replyIndex + 1)">
                      <img src="../../assets/svg/留言.svg" alt="回复">
                      <span>回复</span>
                    </div>
                  </div>
                  <span>{{ reply.send_time }}</span>
                </div>
                <!-- 子评论回复框 -->
                <comment_input_box v-if="comment_input_box_show[index][replyIndex + 1]" :comment_type="'reply'"
                  :video_id="video_id" :comment_id="reply.comment_id" />
              </div>
            </div>
          </div>
        </div>

        <!-- 子评论查看更多按钮 -->
        <div class="show_more_sub"
          v-if="sub_comment_list[index] && sub_comment_list[index].length >= sub_display_limit[index]">
          <span @click="loadMoreSubComments(index)">查看更多子评论</span>
        </div>
      </div>

      <!-- 主评论查看更多按钮 -->
      <div class="show_more" v-if="main_total > main_display_limit">
        <span @click="loadMoreMainComments">查看更多</span>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed,watch } from 'vue';
import { get_comment_list, get_reply_comment_list } from './js/get_comment';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import comment_input_box from './comment_input_box.vue';
import interaction_comment from './js/interaction_comment';
import update_follow_status from './js/update_follow_status';

const store = useStore();
const router = useRouter();

let user=JSON.parse(localStorage.getItem('user'))

let now=new Date()
//主评论消息结构
/*let main_comment_msg=ref({
  "avatar_path":user.avatar_path,
  "send_user_id":user.id,
  "comment_content":"主评论",
  "comment_level":"0",
  "reply_comment_id":null,
  "send_time":now.toLocaleString(),
  "video_id":computed(() => store.getters.video_id),
  "comment_id":2,
  "user_id":user.id,
  "username":user.username,
  "like_count":"0",
  "not_like_count":"0",
  "is_follow":false
})

//子评论消息结构
let sub_comment_msg=ref({
  "avatar_path":user.avatar_path,
  "comment_level":"1",
  "comment_content":"子评论",
  "send_user_id":user.id,
  "reply_comment_id":2,
  "send_time":now.toLocaleString(),
  "belong_to_video_id":computed(() => store.getters.video_id),
  "comment_id":4,
  "video_id":computed(() => store.getters.video_id),
  "user_id":user.id,
  "username":user.username,
  "like_count":"0",
  "not_like_count":"0",
  "re_user_id":2,
  "re_username":"test_user",
  "is_follow":false
})*/

let main_comment_list = ref([]); // 主评论列表
let main_total = ref(0); // 主评论总数
let main_display_limit = ref(1); // 每次显示的主评论数量

let sub_comment_list = ref([]); // 存储每个主评论对应的子评论
let sub_total = ref([]); // 每个主评论的子评论总数
let sub_display_limit = ref([]); // 每个主评论的子评论显示数量

let video_id = computed(() => store.getters.video_id); // 视频 ID

let main_limit = ref(5); // 主评论加载数量
let main_offset = ref(0); // 主评论偏移量
let sub_limit = ref(10000); // 子评论加载数量

// 初始化回复框显示状态的二维数组
let comment_input_box_show = ref([]);

//获取全局消息中的新增评论
let temp_comment=computed(()=>store.getters.comment_msg)
//获取主评论索引,如果主评论索引存在则为子评论，否则为主评论
let main_index=computed(()=>store.getters.main_comment_index)

watch(temp_comment,()=>{
  if(main_index.value){
    //子评论，压入子评论中的栈顶
    sub_comment_list.value[main_index.value].push(temp_comment.value)
    store.commit('set_main_comment_index',null)
    store.commit('set_comment_msg',null)
  }
  else{
    //主评论，压入主评论中的栈顶
    main_comment_list.value.push(temp_comment.value)
    store.commit('set_comment_msg',null)
    store.commit('set_main_comment_index',null)
  }
})

// 获取主评论
async function getMainCommentList() {
  let res = await get_comment_list(video_id.value, main_limit.value, main_offset.value);
  if (res.status == 200) {
    res = res.data;
    console.log(res);
    main_comment_list.value.push(...res.rows);
    main_total.value = res.total;
    main_offset.value += main_limit.value;

    // 初始化每个主评论对应的子评论和显示限制
    res.rows.forEach((comment, index) => {
      sub_comment_list.value[index] = [];
      sub_display_limit.value[index] = 1; // 默认显示1条子评论
      comment_input_box_show.value[index] = [false]; // 主评论的回复框默认不显示
    });
  } else {
    console.warn('获取主评论失败');
  }
}

// 获取子评论
async function getSubCommentList(mainCommentId, index) {
  let res = await get_reply_comment_list(video_id.value, mainCommentId, sub_limit.value);
  if (res.status == 200) {
    res = res.data;
    console.log(res);
    sub_comment_list.value[index].push(...res.rows);

    // 初始化每个子评论的回复框显示状态
    for (let i = 0; i < res.rows.length; i++) {
      comment_input_box_show.value[index].push(false); // 子评论的回复框默认不显示
    }
  } else {
    console.warn('获取子评论失败');
  }
}

// 切换回复框显示状态
function toggleReplyInput(mainIndex, subIndex) {
  // 如果点击的是主评论，则只影响主评论的回复框显示状态
  comment_input_box_show.value[mainIndex].forEach((_, i) => {
    comment_input_box_show.value[mainIndex][i] = i === subIndex ? !comment_input_box_show.value[mainIndex][i] : false;
  });
}

// 查看更多主评论
function loadMoreMainComments() {
  main_display_limit.value += 3; // 每次显示3条主评论
  getMainCommentList();
}

// 查看更多子评论
function loadMoreSubComments(index) {
  sub_display_limit.value[index] += 3; // 每次显示3条子评论
}

// 计算当前显示的主评论
const displayedMainComments = computed(() => {
  return main_comment_list.value.slice(0, main_display_limit.value);
});

// 计算当前显示的子评论
function displayedSubComments(index) {
  if (sub_comment_list.value[index]) {
    return sub_comment_list.value[index].slice(0, sub_display_limit.value[index]);
  }
  return [];
}

//接收临时前端主评论直接压入栈顶
function add_temp_main_comment(comment) {
  main_comment_list.value.unshift(comment);
  main_total.value++;
  main_display_limit.value++;
  sub_comment_list.value.unshift([]);
  sub_display_limit.value.unshift(1);
  comment_input_box_show.value.unshift([false]);
}

//接收临时子评论并压入对应主评轮下的子评论的栈顶
function add_temp_sub_comment(comment, mainIndex) {
  sub_comment_list.value[mainIndex].unshift(comment);
  sub_display_limit.value[mainIndex]++;
  comment_input_box_show.value[mainIndex].unshift(false);
}

//评论交互
async function comm_interaction(comment_id, comment_type, interaction_type) {
  const res = await interaction_comment(comment_id, interaction_type, comment_type);
  if (res.status == 200) {
    console.log(res)
  }
  else {
    console.log(res)
  }
}

//其他用户的用户中心跳转
const to_other_user_center = (id) => {
  router.push('/other_user_center');
  store.commit('set_other_user_id', id);
}

// 切换关注状态
async function switch_follow_status(leave_type, main_index, sub_index) {
  // 确定目标用户和关注状态
  let target_user_id;
  let follow_status;

  if (leave_type === 'main') {
    target_user_id = main_comment_list.value[main_index].user_id;
    follow_status = main_comment_list.value[main_index].is_follow;
  } else if (leave_type === 'sub') {
    target_user_id = sub_comment_list.value[main_index][sub_index].user_id;
    follow_status = sub_comment_list.value[main_index][sub_index].is_follow;
  } else {
    return; // 如果leave_type不符合，直接返回
  }

  // 切换关注状态
  const action = follow_status ? 'cancel' : 'add';
  const res = await update_follow_status(target_user_id, action);

  // 更新状态和提示消息
  if (res.status === 200) {
    store.commit('set_global_msg', res.msg);
  } else {
    store.commit('set_global_msg', res.msg);
  }

  // 更新对应的关注状态
  if (leave_type === 'main') {
    main_comment_list.value[main_index].is_follow = !follow_status;
  } else {
    sub_comment_list.value[main_index][sub_index].is_follow = !follow_status;
  }
}


// 初始化评论加载
onMounted(async () => {
  await getMainCommentList();
  for (let i = 0; i < main_comment_list.value.length; i++) {
    await getSubCommentList(main_comment_list.value[i].comment_id, i);
  }
});
</script>


<style scoped>
.comment_box {
  width: 100%;
  margin: 20px 0;
}

h2 {
  margin-bottom: 10px;
}

.content {
  width: 100%;
}

.comment_group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment_info {
  display: flex;
  align-items: flex-start;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.user_box {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.username {
  margin-left: 10px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  gap: 10px;
}

.follow_btn {
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  color: white;
  max-width: 70px;
}

.follow_btn:hover {
  opacity: 0.8;
  transition: all 0.3s ease-in-out;
  transform: scale(1.05);
  transform: translateY(-2px);
}

.is_follow {
  background-color: rgba(133, 133, 133, 1);
}

.not_follow {
  background-color: rgba(0, 150, 250, 1);
}

.comment_content {
  flex: 1;
}

.comment_interaction {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.interaction_box {
  width: auto;
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: center;
}

.inter_box {
  display: flex;
  cursor: pointer;
  padding: 5px;
  align-items: center;
  gap: 5px;
}

.inter_box:hover {
  border-radius: 50%;
  background-color: rgba(133, 133, 133, 1);
}

.inter_box img {
  width: 20px;
  height: 20px;
  object-fit: cover;
}

.reply_comment {
  margin-left: 40px;
}

.show_more {
  text-align: center;
  margin-top: 20px;
  cursor: pointer;
}

.show_more:hover {
  text-decoration: underline;
}

.show_more span {
  color: #007bff;
  width: 80px;
}

.show_more_sub {
  cursor: pointer;
  width: 150px;
}

.show_more_sub:hover {
  text-decoration: underline;
}
</style>
