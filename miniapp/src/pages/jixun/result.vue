<template>
  <view class="page result-page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="back-btn" @click="goBack">
        <text class="icon">←</text>
      </view>
      <text class="nav-title">打卡结果</text>
      <view class="menu-btn">⋯</view>
    </view>

    <!-- 提交成功提示 -->
    <view class="success-section">
      <view class="success-icon">✓</view>
      <text class="success-text">打卡成功！</text>
      <text class="success-subtitle">你的努力被记录下来了</text>
    </view>

    <!-- 同学作业列表 -->
    <view class="homework-section">
      <view class="section-header">
        <text class="section-title">同学作业</text>
        <text class="section-count">{{ total }}条作业</text>
      </view>
      
      <view class="homework-list">
        <view 
          v-for="item in homeworkList" 
          :key="item.id"
          class="homework-card"
        >
          <view class="user-info">
            <image 
              class="avatar" 
              :src="item.user.avatar_url || '/static/default-avatar.png'" 
              mode="aspectFill"
            />
            <text class="nickname">{{ item.user.nickname }}</text>
          </view>
          
          <view class="content-info">
            <text class="day-badge">第{{ item.day_number }}天</text>
            <text class="content-text">{{ item.content_text.substring(0, 100) }}...</text>
          </view>
          
          <view class="media-info" v-if="item.audio_url" @click="playHomeworkAudio(item)">
            <view class="play-btn-small">
              <text class="play-icon-small">{{ item.isPlaying ? '⏸' : '▶️' }}</text>
            </view>
            <text class="audio-duration">{{ formatAudioDuration(item.audio_duration) }}</text>
          </view>
          
          <view class="action-bar">
            <view class="action-item" @click="likeHomework(item)">
              <text class="action-icon">{{ item.liked ? '❤️' : '🤍' }}</text>
              <text class="action-count">{{ item.likes_count }}</text>
            </view>
            <view class="action-item" @click="commentHomework(item)">
              <text class="action-icon">💬</text>
              <text class="action-count">{{ item.comments_count }}</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore">
        <text class="load-more-text" @click="loadMore">加载更多</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBaseUrl } from '@/api/request.js'

const eventId = ref(null)
const homeworkList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const hasMore = ref(true)

// 音频播放器
let audioContext = null

function getAudioContext() {
  if (!audioContext) {
    audioContext = uni.createInnerAudioContext()
    audioContext.obeyMuteSwitch = false
    audioContext.onPlay(() => {})
    audioContext.onPause(() => {})
    audioContext.onStop(() => {})
    audioContext.onEnded(() => {})
    audioContext.onError((err) => {
      console.error('播放作业音频失败', err)
      uni.showToast({ title: '播放失败', icon: 'none' })
    })
  }
  return audioContext
}

function playHomeworkAudio(item) {
  const ctx = getAudioContext()
  
  // 停止其他正在播放的音频
  homeworkList.value.forEach(h => {
    if (h.id !== item.id && h.isPlaying) {
      h.isPlaying = false
    }
  })
  
  if (item.isPlaying) {
    ctx.pause()
    item.isPlaying = false
  } else {
    ctx.src = item.audio_url
    ctx.play()
    item.isPlaying = true
  }
}

function formatAudioDuration(seconds) {
  if (!seconds || seconds === 0) return '00:00'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

onMounted(async () => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  eventId.value = currentPage.options.id
  
  await loadHomework()
})

async function loadHomework() {
  try {
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/checkin/${eventId.value}?page=${page.value}&page_size=${pageSize}`,
      method: 'GET'
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      homeworkList.value = res.data.data.items
      total.value = res.data.data.pagination.total
      hasMore.value = res.data.data.pagination.page * pageSize < total.value
    }
  } catch (err) {
    console.error('加载作业列表失败:', err)
  }
}

function likeHomework(item) {
  // TODO: 点赞功能
  if (!item.liked) {
    item.likes_count++
    item.liked = true
  }
}

function commentHomework(item) {
  // TODO: 评论功能
  uni.navigateTo({
    url: `/pages/jixun/comment?recordId=${item.id}`
  })
}

function loadMore() {
  page.value++
  loadHomework()
}

function goBack() {
  uni.navigateBack()
}
</script>

<style scoped lang="scss">
.result-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 100%);
  padding-bottom: 120rpx;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  
  .back-btn {
    font-size: 40rpx;
    color: #333;
  }
  
  .nav-title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
  }
  
  .menu-btn {
    font-size: 40rpx;
    color: #666;
  }
}

.success-section {
  text-align: center;
  padding: 60rpx 30rpx;
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  
  .success-icon {
    width: 100rpx;
    height: 100rpx;
    background: #4CAF50;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 60rpx;
    margin: 0 auto 20rpx;
  }
  
  .success-text {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
  }
  
  .success-subtitle {
    font-size: 26rpx;
    color: #666;
    display: block;
  }
}

.homework-section {
  margin: 20rpx 30rpx;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
    
    .section-title {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
    }
    
    .section-count {
      font-size: 24rpx;
      color: #999;
    }
  }
  
  .homework-list {
    .homework-card {
      background: #fff;
      border-radius: 16rpx;
      padding: 30rpx;
      margin-bottom: 20rpx;
      box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
      
      .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 20rpx;
        
        .avatar {
          width: 60rpx;
          height: 60rpx;
          border-radius: 50%;
          margin-right: 16rpx;
        }
        
        .nickname {
          font-size: 28rpx;
          color: #333;
          font-weight: 500;
        }
      }
      
      .content-info {
        margin-bottom: 16rpx;
        
        .day-badge {
          display: inline-block;
          background: #4CAF50;
          color: #fff;
          padding: 4rpx 12rpx;
          border-radius: 8rpx;
          font-size: 22rpx;
          margin-bottom: 12rpx;
        }
        
        .content-text {
          font-size: 26rpx;
          color: #666;
          line-height: 1.5;
        }
      }
      
      .media-info {
        display: flex;
        align-items: center;
        gap: 12rpx;
        margin-bottom: 16rpx;
        padding: 16rpx 20rpx;
        background: #f5f5f5;
        border-radius: 12rpx;
        
        .play-btn-small {
          width: 48rpx;
          height: 48rpx;
          background: #4CAF50;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          
          .play-icon-small {
            font-size: 20rpx;
            color: #fff;
          }
        }
        
        .audio-duration {
          font-size: 24rpx;
          color: #4CAF50;
          font-weight: 500;
        }
      }
      
      .action-bar {
        display: flex;
        gap: 40rpx;
        
        .action-item {
          display: flex;
          align-items: center;
          
          .action-icon {
            font-size: 28rpx;
            margin-right: 8rpx;
          }
          
          .action-count {
            font-size: 24rpx;
            color: #666;
          }
        }
      }
    }
  }
  
  .load-more {
    text-align: center;
    padding: 30rpx 0;
    
    .load-more-text {
      font-size: 26rpx;
      color: #4CAF50;
    }
  }
}
</style>
