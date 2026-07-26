<template>
<view class="page home-page">
  <!-- 顶部标题栏 -->
  <view class="top-bar">
    <text class="top-title">口才界多维班</text>
  </view>

  <!-- AI答疑搜索框 -->
  <view class="search-section">
    <view class="search-box">
      <view class="ri-icon ri-size-sm ri-search-line" style="color:#999"></view>
      <input class="search-input" placeholder="请输入想问的问题" />
      <view class="ai-btn">AI答疑</view>
    </view>
  </view>

  <!-- 功能模块区域（7个卡片） -->
  <view class="module-grid">
    <view class="module-card" @tap="goModule('集训打卡')">
      <text class="module-name">集训打卡</text>
      <view class="module-arrow">›</view>
    </view>
    <view class="module-card" @tap="goModule('约课')">
      <text class="module-name">约课</text>
      <view class="module-arrow">›</view>
    </view>
    <view class="module-card" @tap="goModule('习惯打卡')">
      <text class="module-name">习惯打卡</text>
      <view class="module-arrow">›</view>
    </view>
    <view class="module-card" @tap="goModule('今日打卡')">
      <text class="module-name">今日打卡</text>
      <view class="module-arrow">›</view>
    </view>
    <view class="module-card" @tap="goModule('自由练习')">
      <text class="module-name">自由练习</text>
      <view class="module-arrow">›</view>
    </view>
    <view class="module-card" @tap="goModule('闯关练习')">
      <text class="module-name">闯关练习</text>
      <view class="module-arrow">›</view>
    </view>
    <view class="module-card" @tap="goModule('挑战练习')">
      <text class="module-name">挑战练习</text>
      <view class="module-arrow">›</view>
    </view>
  </view>

  <!-- 开始训练按钮 -->
  <view class="start-train-btn" @tap="goTraining">
    <text>开始训练</text>
  </view>

  <!-- 首页快捷功能（4个卡片） -->
  <view class="quick-section">
    <text class="section-title">首页快捷功能</text>
    <view class="quick-grid">
      <view class="quick-card" @tap="goQuick('manage')">
        <view class="ri-icon ri-size-lg ri-settings-3-line" style="color:#4F46E5"></view>
        <text class="quick-label">管理</text>
      </view>
      <view class="quick-card" @tap="goQuick('circle')">
        <view class="ri-icon ri-size-lg ri-group-line" style="color:#10B981"></view>
        <text class="quick-label">圈子</text>
      </view>
      <view class="quick-card" @tap="goQuick('review')">
        <view class="ri-icon ri-size-lg ri-file-list-3-line" style="color:#F59E0B"></view>
        <text class="quick-label">高效能复盘</text>
      </view>
      <view class="quick-card" @tap="goQuick('cognitive')">
        <view class="ri-icon ri-size-lg ri-brain-line" style="color:#8B5CF6"></view>
        <text class="quick-label">认知管理</text>
      </view>
      <view class="quick-card" @tap="goQuick('solve')">
        <view class="ri-icon ri-size-lg ri-lightbulb-line" style="color:#EF4444"></view>
        <text class="quick-label">解决问题</text>
      </view>
      <view class="quick-card" @tap="goQuick('tutor')">
        <view class="ri-icon ri-size-lg ri-robot-3-line" style="color:#6366F1"></view>
        <text class="quick-label">AI私教</text>
      </view>
    </view>
  </view>

  <!-- 挑战榜单（3个榜单） -->
  <view class="rank-section">
    <text class="section-title">挑战榜单</text>
    <view class="rank-cards">
      <view class="rank-card" @tap="goRank('ai')">
        <view class="ri-icon ri-size-md ri-crown-line" style="color:#F59E0B"></view>
        <text class="rank-label">AI点评次数榜</text>
      </view>
      <view class="rank-card" @tap="goRank('success')">
        <view class="ri-icon ri-size-md ri-trophy-line" style="color:#10B981"></view>
        <text class="rank-label">成功练习榜</text>
      </view>
      <view class="rank-card" @tap="goRank('days')">
        <view class="ri-icon ri-size-md ri-calendar-event-line" style="color:#4F46E5"></view>
        <text class="rank-label">练习总天数榜</text>
      </view>
    </view>
  </view>

  <view class="bottom-spacer"></view>
</view>
</template>

<script setup>
import { onShow } from '@dcloudio/uni-app'

function goModule(name) {
  if (name === '集训打卡') {
    uni.navigateTo({ url: '/pages/jixun/index' })
  } else if (name === '今日打卡') {
    uni.switchTab({ url: '/pages/checkin/index' })
  } else if (name === '习惯打卡') {
    uni.navigateTo({ url: '/pages/checkin/calendar' })
  } else {
    uni.showToast({ title: `${name} 功能开发中`, icon: 'none' })
  }
}

function goTraining() {
  uni.switchTab({ url: '/pages/training/index' })
}

function goQuick(type) {
  const map = {
    circle: '/pages/discover/index',
    review: '/pages/review/index',
    tutor: '/pages/ai-tools/index',
  }
  if (map[type]) {
    uni.switchTab({ url: map[type] })
  } else {
    uni.showToast({ title: `${type} 功能开发中`, icon: 'none' })
  }
}

function goRank(type) {
  uni.navigateTo({ url: '/pages/training/leaderboard' })
}

onShow(() => {})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 30%, #F8F9FC 100%);
  padding: 0 24rpx;
}

/* 顶部标题栏 */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24rpx 0 12rpx;
}
.top-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
}

/* AI答疑搜索框 */
.search-section {
  margin: 16rpx 0 24rpx;
}
.search-box {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 40rpx;
  padding: 0 24rpx;
  height: 72rpx;
  box-shadow: 0 4rpx 20rpx rgba(0,0,0,.06);
  gap: 12rpx;
}
.search-input {
  flex: 1;
  font-size: 26rpx;
  color: #333;
  height: 72rpx;
}
.ai-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: #fff;
  font-size: 24rpx;
  font-weight: 600;
  padding: 8rpx 24rpx;
  border-radius: 24rpx;
  white-space: nowrap;
}

/* 功能模块网格（7个卡片，2列布局） */
.module-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16rpx;
  margin-bottom: 24rpx;
}
.module-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx 20rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.module-card:active {
  opacity: .85;
}
.module-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
}
.module-arrow {
  font-size: 36rpx;
  color: #4CAF50;
  font-weight: bold;
}

/* 开始训练按钮 */
.start-train-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 48rpx;
  padding: 24rpx 0;
  text-align: center;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(76,175,80,.3);
}
.start-train-btn text {
  font-size: 32rpx;
  font-weight: 700;
  color: #fff;
}

/* 首页快捷功能 */
.quick-section {
  margin-bottom: 24rpx;
}
.section-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #333;
  margin-bottom: 16rpx;
  display: block;
}
.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
}
.quick-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.quick-card:active {
  opacity: .85;
}
.quick-label {
  font-size: 24rpx;
  color: #333;
  text-align: center;
}

/* 挑战榜单 */
.rank-section {
  margin-bottom: 24rpx;
}
.rank-cards {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}
.rank-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  gap: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.rank-card:active {
  opacity: .85;
}
.rank-label {
  font-size: 26rpx;
  color: #333;
  font-weight: 500;
  flex: 1;
}

.bottom-spacer {
  height: 60rpx;
}
</style>
