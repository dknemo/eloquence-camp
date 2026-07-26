<template>
<view class="page pre-page">
  <view class="pre-card" v-if="item">
    <!-- 题目信息 -->
    <view class="pre-header">
      <text class="pre-title">{{ item.title }}</text>
      <text class="pre-cat">{{ cl(item.category) }} · {{ '★'.repeat(item.difficulty) }}</text>
    </view>

    <!-- 参考文本 -->
    <view class="pre-text" v-if="item.sample_text">
      <text class="pre-label">练习内容</text>
      <text class="pre-content">{{ item.sample_text }}</text>
    </view>

    <!-- 配置项 -->
    <view class="config-section">
      <text class="config-title">训练配置</text>

      <!-- 难度 -->
      <view class="config-row">
        <text class="config-label">能力等级</text>
        <view class="config-options">
          <text
            v-for="l in levels"
            :key="l.value"
            class="co-pill"
            :class="{ active: config.level === l.value }"
            @tap="config.level = l.value"
          >{{ l.label }}</text>
        </view>
      </view>

      <!-- 倒计时 -->
      <view class="config-row">
        <text class="config-label">倒计时</text>
        <view class="config-options">
          <text
            v-for="t in countdowns"
            :key="t.value"
            class="co-pill"
            :class="{ active: config.countdown === t.value }"
            @tap="config.countdown = t.value"
          >{{ t.label }}</text>
        </view>
      </view>

      <!-- 构思时间 -->
      <view class="config-row">
        <text class="config-label">构思时间</text>
        <view class="config-options">
          <text
            v-for="t in thinkTimes"
            :key="t.value"
            class="co-pill"
            :class="{ active: config.thinkTime === t.value }"
            @tap="config.thinkTime = t.value"
          >{{ t.label }}</text>
        </view>
      </view>

      <!-- 尝试次数 -->
      <view class="config-row">
        <text class="config-label">尝试次数</text>
        <view class="config-options">
          <text
            v-for="t in attempts"
            :key="t.value"
            class="co-pill"
            :class="{ active: config.attempts === t.value }"
            @tap="config.attempts = t.value"
          >{{ t.label }}</text>
        </view>
      </view>
    </view>

    <!-- 开始按钮 -->
    <view class="start-btn" @tap="startTraining">
      <text>开始训练</text>
    </view>
  </view>

  <view v-else class="loading">加载中...</view>
</view>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import api from '@/api/request'
import { catLabel } from '@/utils/category'

const item = ref(null)
const itemId = ref('')

const levels = [
  { label: '入门', value: 1 },
  { label: '基础', value: 2 },
  { label: '进阶', value: 3 },
  { label: '挑战', value: 4 },
]
const countdowns = [
  { label: '1 分钟', value: 60 },
  { label: '2 分钟', value: 120 },
  { label: '3 分钟', value: 180 },
  { label: '5 分钟', value: 300 },
]
const thinkTimes = [
  { label: '无', value: 0 },
  { label: '15 秒', value: 15 },
  { label: '30 秒', value: 30 },
  { label: '60 秒', value: 60 },
]
const attempts = [
  { label: '1 次', value: 1 },
  { label: '2 次', value: 2 },
  { label: '3 次', value: 3 },
  { label: '不限', value: 0 },
]

const config = reactive({
  level: 2,
  countdown: 120,
  thinkTime: 15,
  attempts: 2,
})

const cl = catLabel

function startTraining() {
  const params = [
    `id=${itemId.value}`,
    `level=${config.level}`,
    `countdown=${config.countdown}`,
    `think=${config.thinkTime}`,
    `attempts=${config.attempts}`,
  ]
  uni.navigateTo({ url: `/pages/training/detail?${params.join('&')}` })
}

onLoad(async (opt) => {
  if (opt?.id) {
    itemId.value = opt.id
    try { item.value = await api.get(`/training/items/${opt.id}`) } catch (e) {}
  }
})
</script>

<style scoped>
.pre-page {
  min-height: 100vh;
  background: #F8F9FC;
  padding: 24rpx;
}

.pre-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;
  box-shadow: 0 4rpx 24rpx rgba(0,0,0,.04);
}

.pre-header {
  margin-bottom: 20rpx;
}
.pre-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #1A1A2E;
  display: block;
}
.pre-cat {
  font-size: 22rpx;
  color: #999;
  margin-top: 8rpx;
}

.pre-text {
  background: #F8F9FC;
  border-radius: 16rpx;
  padding: 20rpx;
  margin-bottom: 24rpx;
}
.pre-label {
  font-size: 22rpx;
  color: #999;
  display: block;
  margin-bottom: 8rpx;
}
.pre-content {
  font-size: 26rpx;
  color: #333;
  line-height: 1.8;
  word-break: break-all;
}

.config-section {
  margin-bottom: 24rpx;
}
.config-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #1A1A2E;
  display: block;
  margin-bottom: 20rpx;
}

.config-row {
  margin-bottom: 20rpx;
}
.config-label {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 10rpx;
}
.config-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}
.co-pill {
  font-size: 24rpx;
  padding: 10rpx 24rpx;
  border-radius: 24rpx;
  background: #F3F4F6;
  color: #666;
  transition: all .15s;
}
.co-pill.active {
  background: #4F46E5;
  color: #fff;
}

.start-btn {
  background: linear-gradient(135deg, #4F46E5, #6366F1);
  border-radius: 48rpx;
  padding: 24rpx;
  text-align: center;
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
  box-shadow: 0 8rpx 24rpx rgba(79,70,229,.3);
  margin-top: 16rpx;
}
.start-btn:active { opacity: .85; }

.loading {
  text-align: center;
  color: #999;
  padding: 200rpx 0;
}
</style>
