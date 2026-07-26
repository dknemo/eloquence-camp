<template>
  <view class="page jixun-page">
    <!-- 顶部标题 -->
    <view class="header">
      <text class="title">口才界集训打卡</text>
      <text class="subtitle">选择你想参加的集训活动</text>
    </view>

    <!-- 集训列表 -->
    <view class="event-list">
      <view 
        v-for="(event, index) in events" 
        :key="event.id"
        class="event-card"
        @click="goDetail(event.id)"
      >
        <view class="event-header">
          <text class="event-index">{{ index + 1 }}</text>
          <text class="event-title">{{ event.title }}</text>
        </view>
        <view class="event-meta">
          <view class="meta-item">
            <text class="meta-icon">👥</text>
            <text class="meta-text">{{ event.participant_count }}人参与</text>
          </view>
          <view class="meta-item">
            <text class="meta-icon">📅</text>
            <text class="meta-text">{{ event.total_days }}天</text>
          </view>
        </view>
        <view class="event-arrow">»</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBaseUrl } from '@/api/request.js'

const events = ref([])

onMounted(async () => {
  await loadEvents()
})

async function loadEvents() {
  try {
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/events`,
      method: 'GET'
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      events.value = res.data.data.events
    }
  } catch (err) {
    console.error('加载集训列表失败:', err)
  }
}

function goDetail(eventId) {
  uni.navigateTo({
    url: `/pages/jixun/detail?id=${eventId}`
  })
}
</script>

<style scoped lang="scss">
.jixun-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 100%);
  padding: 30rpx;
}

.header {
  margin-bottom: 40rpx;
  
  .title {
    font-size: 48rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
  }
  
  .subtitle {
    font-size: 28rpx;
    color: #666;
    display: block;
  }
}

.event-list {
  .event-card {
    background: #fff;
    border-radius: 16rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
    display: flex;
    align-items: center;
    position: relative;
    
    &:active {
      opacity: 0.8;
    }
    
    .event-header {
      flex: 1;
      display: flex;
      align-items: center;
      
      .event-index {
        width: 50rpx;
        height: 50rpx;
        background: #4CAF50;
        color: #fff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24rpx;
        font-weight: bold;
        margin-right: 20rpx;
        flex-shrink: 0;
      }
      
      .event-title {
        font-size: 30rpx;
        color: #333;
        font-weight: 500;
        line-height: 1.4;
      }
    }
    
    .event-meta {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 8rpx;
      margin-right: 10rpx;
      
      .meta-item {
        display: flex;
        align-items: center;
        
        .meta-icon {
          font-size: 24rpx;
          margin-right: 6rpx;
        }
        
        .meta-text {
          font-size: 22rpx;
          color: #666;
        }
      }
    }
    
    .event-arrow {
      font-size: 36rpx;
      color: #999;
      position: absolute;
      right: 20rpx;
      top: 50%;
      transform: translateY(-50%);
    }
  }
}
</style>
