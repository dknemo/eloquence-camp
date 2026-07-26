<template>
<view class="page jixun-page">
  <!-- 顶部标题栏 -->
  <view class="top-bar">
    <view class="ri-icon ri-size-lg ri-arrow-left-s-line" @tap="goBack" style="color:#333"></view>
    <text class="page-title">集训打卡</text>
    <view class="top-actions">
      <view class="ri-icon ri-size-md ri-dots-vertical" style="color:#333"></view>
      <view class="ri-icon ri-size-md ri-minimize" style="color:#333"></view>
      <view class="ri-icon ri-size-md ri-circle-dot" style="color:#333"></view>
    </view>
  </view>

  <!-- 数据表格区域 -->
  <view class="table-container">
    <!-- 表头 -->
    <view class="table-header">
      <text class="col col-index">序号</text>
      <text class="col col-topic">主题</text>
      <text class="col col-count">参与人数</text>
      <text class="col col-days">打卡天数</text>
    </view>

    <!-- 表格行 -->
    <view
      class="table-row"
      v-for="(item, index) in trainingList"
      :key="item.id"
      @tap="goDetail(item)"
    >
      <text class="col col-index">{{ index + 1 }}</text>
      <text class="col col-topic ellipsis">{{ item.topic }}</text>
      <text class="col col-count">{{ item.participants }}</text>
      <text class="col col-days">{{ item.checkinDays }}</text>
      <view class="col col-action">
        <text class="arrow">»</text>
      </view>
    </view>
  </view>

  <view class="bottom-spacer"></view>
</view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'

const trainingList = ref([
  { id: 1, topic: '7月7天批判性思维（独立思考）打卡集训', participants: 0, checkinDays: 0 },
  { id: 2, topic: '7月7天"结构划分"打卡集训', participants: 5, checkinDays: 0 },
  { id: 3, topic: '2026-8月美文朗读', participants: 0, checkinDays: 0 },
  { id: 4, topic: '2026-7月美文朗读', participants: 83, checkinDays: 0 },
  { id: 5, topic: '热点新闻评述', participants: 3035, checkinDays: 0 },
  { id: 6, topic: '"述思用"共读集训', participants: 1804, checkinDays: 0 },
])

function goBack() {
  uni.navigateBack()
}

function goDetail(item) {
  uni.navigateTo({ url: `/pages/training/detail?id=${item.id}` })
}

onShow(() => {})
</script>

<style scoped>
.jixun-page {
  min-height: 100vh;
  background: #fff;
}

/* 顶部导航栏 */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 24rpx;
  background: linear-gradient(135deg, #E0F7FA, #B2EBF2);
  border-bottom: 1rpx solid #e0e0e0;
}
.page-title {
  font-size: 34rpx;
  font-weight: 700;
  color: #333333;
}
.top-actions {
  display: flex;
  gap: 16rpx;
  align-items: center;
}

/* 表格容器 */
.table-container {
  background: #fff;
}

/* 表头 */
.table-header {
  display: flex;
  align-items: center;
  padding: 20rpx 24rpx;
  background: #f8f9fc;
  border-bottom: 2rpx solid #e0e0e0;
}
.col {
  font-size: 24rpx;
  color: #666666;
  font-weight: 500;
}
.col-index {
  width: 60rpx;
  text-align: center;
  flex-shrink: 0;
}
.col-topic {
  flex: 1;
  min-width: 0;
}
.col-count {
  width: 100rpx;
  text-align: center;
  flex-shrink: 0;
}
.col-days {
  width: 100rpx;
  text-align: center;
  flex-shrink: 0;
}
.col-action {
  width: 50rpx;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 表格行 */
.table-row {
  display: flex;
  align-items: center;
  padding: 24rpx 24rpx;
  border-bottom: 1rpx solid #eeeeee;
}
.table-row:active {
  background: #f5f5f5;
}
.arrow {
  font-size: 32rpx;
  color: #333333;
  font-weight: bold;
}

.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
  max-width: 300rpx;
}

.bottom-spacer {
  height: 60rpx;
}
</style>
