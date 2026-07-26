<template>
  <view class="page jixun-detail-page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="back-btn" @click="goBack">
        <text class="icon">←</text>
      </view>
      <text class="nav-title">集训详情</text>
      <view class="menu-btn">⋯</view>
    </view>

    <!-- 活动标题 -->
    <view class="event-header" v-if="event">
      <text class="event-title">{{ event.title }}</text>
      <text class="event-date">{{ event.start_date }} 至 {{ event.end_date }}</text>
    </view>

    <!-- 详情介绍 -->
    <view class="section" v-if="event">
      <view class="section-header">
        <text class="section-title">详情介绍</text>
        <text class="expand-btn" @click="toggleExpand">{{ expanded ? '收起' : '展开所有' }} ▼</text>
      </view>
      <view class="section-content">
        <text class="description-text" user-select>{{ expanded ? (event.description || '') : (event.description || '').substring(0, 150) + '...' }}</text>
      </view>
    </view>

    <!-- 报名条件 -->
    <view class="section" v-if="event">
      <view class="section-header">
        <text class="section-title">报名条件</text>
      </view>
      <view class="section-content">
        <text class="requirement-text">{{ event.signup_requirement }}</text>
      </view>
    </view>

    <!-- 集训时间 -->
    <view class="section" v-if="event">
      <view class="section-header">
        <text class="section-title">集训时间</text>
      </view>
      <view class="section-content">
        <text class="time-text">共 {{ event.total_days }} 天</text>
      </view>
    </view>

    <!-- 打卡日历 -->
    <view class="section" v-if="event && event.has_calendar">
      <view class="section-header">
        <text class="section-title">打卡日历</text>
      </view>
      <view class="calendar-container">
        <view class="calendar-header">
          <text class="month-text">{{ currentMonth }}月</text>
        </view>
        <view class="calendar-grid">
          <view 
            v-for="day in calendarDays" 
            :key="day.day"
            class="calendar-day"
            :class="{
              'today': day.isToday,
              'checked': day.isChecked,
              'future': day.isFuture
            }"
            @click="day.isChecked ? viewDayRecord(day) : null"
          >
            <text class="day-number">{{ day.day }}</text>
            <text class="day-status" v-if="day.isChecked">✓</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 配置选择 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">配置选择</text>
      </view>
      <view class="config-item" @click="showCountdownPicker = true">
        <text class="config-label">倒计时时间</text>
        <text class="config-value">{{ countdown }}分钟 ›</text>
      </view>
      <view class="config-item" @click="showThinkTimePicker = true">
        <text class="config-label">构思时间</text>
        <text class="config-value">{{ thinkTime }}分钟 ›</text>
      </view>
      <view class="config-item" @click="showAttemptsPicker = true">
        <text class="config-label">尝试次数</text>
        <text class="config-value">{{ attempts }}次 ›</text>
      </view>
    </view>

    <!-- 底部按钮 -->
    <view class="bottom-bar">
      <button 
        class="signup-btn" 
        :class="{ 'signed-up': isSignedUp }"
        @click="handleSignup"
      >
        {{ isSignedUp ? '去打卡' : '报名并打卡' }}
      </button>
    </view>

    <!-- 配置选择器 -->
    <view class="picker-overlay" v-if="showCountdownPicker" @click="showCountdownPicker = false">
      <view class="picker-panel" @click.stop>
        <view class="picker-header">
          <text class="picker-title">选择倒计时时间</text>
          <text class="picker-close" @click="showCountdownPicker = false">✕</text>
        </view>
        <scroll-view scroll-y class="picker-list">
          <view 
            v-for="val in countdownOptions" 
            :key="val"
            class="picker-option"
            :class="{ active: countdown === val }"
            @click="selectCountdown(val)"
          >
            <text>{{ val }}分钟</text>
          </view>
        </scroll-view>
      </view>
    </view>

    <view class="picker-overlay" v-if="showThinkTimePicker" @click="showThinkTimePicker = false">
      <view class="picker-panel" @click.stop>
        <view class="picker-header">
          <text class="picker-title">选择构思时间</text>
          <text class="picker-close" @click="showThinkTimePicker = false">✕</text>
        </view>
        <scroll-view scroll-y class="picker-list">
          <view 
            v-for="val in thinkTimeOptions" 
            :key="val"
            class="picker-option"
            :class="{ active: thinkTime === val }"
            @click="selectThinkTime(val)"
          >
            <text>{{ val }}分钟</text>
          </view>
        </scroll-view>
      </view>
    </view>

    <view class="picker-overlay" v-if="showAttemptsPicker" @click="showAttemptsPicker = false">
      <view class="picker-panel" @click.stop>
        <view class="picker-header">
          <text class="picker-title">选择尝试次数</text>
          <text class="picker-close" @click="showAttemptsPicker = false">✕</text>
        </view>
        <scroll-view scroll-y class="picker-list">
          <view 
            v-for="val in attemptsOptions" 
            :key="val"
            class="picker-option"
            :class="{ active: attempts === val }"
            @click="selectAttempts(val)"
          >
            <text>{{ val }}次</text>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getBaseUrl } from '@/api/request.js'

const eventId = ref(null)
const event = ref(null)
const isSignedUp = ref(false)
const countdown = ref(45)
const thinkTime = ref(30)
const attempts = ref(8)
const expanded = ref(false)
const currentMonth = ref('')
const calendarDays = ref([])

// 配置选项
const countdownOptions = ref([5, 10, 15, 20, 25, 30, 35, 40, 45])
const thinkTimeOptions = ref([5, 10, 15, 20, 25, 30])
const attemptsOptions = ref([1, 2, 3, 4, 5, 6, 7, 8])

// 弹窗控制
const showCountdownPicker = ref(false)
const showThinkTimePicker = ref(false)
const showAttemptsPicker = ref(false)

onMounted(async () => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  eventId.value = currentPage.options.id
  
  await loadEvent()
  await loadMySignup()
  generateCalendar()
})

async function loadEvent() {
  try {
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/events/${eventId.value}`,
      method: 'GET'
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      event.value = res.data.data
      countdown.value = event.value.default_countdown
      thinkTime.value = event.value.default_think_time
      attempts.value = event.value.default_attempts
    }
  } catch (err) {
    console.error('加载活动详情失败:', err)
  }
}

async function loadMySignup() {
  try {
    const token = uni.getStorageSync('token')
    if (!token) return
    
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/my-signup/${eventId.value}`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      const data = res.data.data
      isSignedUp.value = data.signed_up
      if (data.signed_up) {
        countdown.value = data.countdown
        thinkTime.value = data.think_time
        attempts.value = data.attempts
      }
    }
  } catch (err) {
    console.error('加载报名信息失败:', err)
  }
}

function generateCalendar() {
  if (!event.value) return
  
  const startDate = new Date(event.value.start_date)
  const endDate = new Date(event.value.end_date)
  const today = new Date()
  
  // 设置当前月份
  currentMonth.value = startDate.getMonth() + 1
  
  // 生成日历天数
  const days = []
  let currentDate = new Date(startDate)
  
  while (currentDate <= endDate) {
    const isToday = currentDate.toDateString() === today.toDateString()
    const isFuture = currentDate > today
    const isChecked = false // TODO: 从后端获取已打卡日期
    
    days.push({
      day: currentDate.getDate(),
      isToday,
      isFuture,
      isChecked
    })
    
    currentDate.setDate(currentDate.getDate() + 1)
  }
  
  calendarDays.value = days
}

function toggleExpand() {
  expanded.value = !expanded.value
}

function selectCountdown(val) {
  countdown.value = val
  showCountdownPicker.value = false
}

function selectThinkTime(val) {
  thinkTime.value = val
  showThinkTimePicker.value = false
}

function selectAttempts(val) {
  attempts.value = val
  showAttemptsPicker.value = false
}

async function handleSignup() {
  try {
    const token = uni.getStorageSync('token')
    if (!token) {
      uni.showToast({ title: '请先登录', icon: 'none' })
      return
    }
    
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/signup`,
      method: 'POST',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: {
        event_id: eventId.value,
        countdown: countdown.value,
        think_time: thinkTime.value,
        attempts: attempts.value
      }
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      isSignedUp.value = true
      uni.showToast({ title: res.data.data.message, icon: 'success' })
      
      // 延迟跳转到打卡页面
      setTimeout(() => {
        uni.navigateTo({
          url: `/pages/jixun/checkin?id=${eventId.value}`
        })
      }, 1500)
    }
  } catch (err) {
    console.error('报名失败:', err)
    uni.showToast({ title: '报名失败，请重试', icon: 'none' })
  }
}

function goBack() {
  uni.navigateBack()
}

function viewDayRecord(day) {
  // TODO: 查看当天打卡记录
  uni.showToast({ title: `查看第${day.day}天打卡`, icon: 'none' })
}
</script>

<style scoped lang="scss">
.jixun-detail-page {
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

.event-header {
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  
  .event-title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
  }
  
  .event-date {
    font-size: 26rpx;
    color: #666;
  }
}

.section {
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  
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
    
    .expand-btn {
      font-size: 24rpx;
      color: #4CAF50;
    }
  }
  
  .section-content {
    .description-text {
      font-size: 28rpx;
      color: #666;
      line-height: 1.6;
    }
    
    .requirement-text {
      font-size: 28rpx;
      color: #333;
    }
    
    .time-text {
      font-size: 28rpx;
      color: #333;
    }
  }
}

.calendar-container {
  .calendar-header {
    text-align: center;
    margin-bottom: 20rpx;
    
    .month-text {
      font-size: 28rpx;
      font-weight: bold;
      color: #333;
    }
  }
  
  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 10rpx;
    
    .calendar-day {
      aspect-ratio: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-radius: 8rpx;
      background: #f5f5f5;
      
      &.today {
        background: #4CAF50;
        color: #fff;
      }
      
      &.checked {
        background: #8BC34A;
        color: #fff;
      }
      
      &.future {
        opacity: 0.5;
      }
      
      .day-number {
        font-size: 24rpx;
      }
      
      .day-status {
        font-size: 20rpx;
        margin-top: 4rpx;
      }
    }
  }
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
  
  &:last-child {
    border-bottom: none;
  }
  
  .config-label {
    font-size: 28rpx;
    color: #333;
  }
  
  .config-value {
    font-size: 28rpx;
    color: #4CAF50;
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  
  .signup-btn {
    width: 100%;
    height: 88rpx;
    background: #4CAF50;
    color: #fff;
    border: none;
    border-radius: 44rpx;
    font-size: 32rpx;
    font-weight: bold;
    
    &.signed-up {
      background: #2196F3;
    }
  }
}

.picker-panel {
  background: #fff;
  border-radius: 20rpx 20rpx 0 0;
  padding: 30rpx;
  
  .picker-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30rpx;
    
    .picker-title {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
    }
    
    .picker-close {
      font-size: 36rpx;
      color: #999;
    }
  }
  
  .picker-list {
    max-height: 400rpx;
    
    .picker-option {
      padding: 20rpx 0;
      font-size: 28rpx;
      color: #666;
      
      &.active {
        color: #4CAF50;
        font-weight: bold;
      }
    }
  }
}

.picker-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  display: flex;
  align-items: flex-end;
  
  .picker-panel {
    width: 100%;
    background: #fff;
    border-radius: 20rpx 20rpx 0 0;
    padding: 30rpx;
    max-height: 70vh;
    overflow-y: auto;
  }
}
</style>
