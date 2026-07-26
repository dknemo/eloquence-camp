<template>
<view class="page detail-page">
  <!-- 顶部标题栏 -->
  <view class="top-bar">
    <view class="ri-icon ri-size-lg ri-arrow-left-s-line" @tap="goBack" style="color:#333"></view>
    <text class="page-title">{{ item.title }}</text>
    <view class="top-actions">
      <view class="ri-icon ri-size-md ri-dots-vertical" style="color:#333"></view>
      <view class="ri-icon ri-size-md ri-minimize" style="color:#333"></view>
      <view class="ri-icon ri-size-md ri-circle-dot" style="color:#333"></view>
    </view>
  </view>

  <!-- 详情介绍 -->
  <view class="detail-section">
    <view class="detail-header">
      <text class="detail-tag">[庆祝]</text>
      <text class="detail-header-text">详情介绍</text>
    </view>
    <text class="detail-content">{{ item.description }}</text>
    <view class="expand-link" @tap="toggleExpand">
      <text>{{ isExpanded ? '收起全部' : '展开所有' }}</text>
      <text class="expand-arrow">{{ isExpanded ? '^' : 'v' }}</text>
    </view>
  </view>

  <!-- 报名条件 -->
  <view class="info-card">
    <text class="info-label">报名条件</text>
    <text class="info-value">{{ item.requirement }}</text>
  </view>

  <!-- 集训时间 -->
  <view class="info-card">
    <text class="info-label">集训时间</text>
    <view class="info-row">
      <text class="info-value">{{ item.startTime }} 至 {{ item.endTime }}</text>
      <text class="info-days">共 {{ item.totalDays }} 天</text>
    </view>
  </view>

  <!-- 打卡日历 -->
  <view class="calendar-section" v-if="item.hasCalendar">
    <text class="section-label">打卡日历</text>
    <view class="calendar-nav">
      <view class="ri-icon ri-size-lg ri-arrow-left-s-line" @tap="prevMonth" style="color:#4CAF50"></view>
      <text class="calendar-month">{{ currentYear }} / {{ String(currentMonth).padStart(2,'0') }}</text>
      <view class="ri-icon ri-size-lg ri-arrow-right-s-line" @tap="nextMonth" style="color:#4CAF50"></view>
    </view>
    <view class="today-btn" @tap="goToday">今日</view>
    <view class="calendar-grid">
      <text class="cal-day-name" v-for="d in dayNames" :key="d">{{ d }}</text>
      <view v-for="(day, idx) in calendarDays" :key="idx" class="cal-day" :class="{ today: day.isToday }">
        <text>{{ day.num }}</text>
        <text v-if="day.isToday" class="today-tag">今日</text>
      </view>
    </view>
  </view>

  <!-- 倒计时/构思时间/尝试次数 -->
  <view class="config-section">
    <view class="config-item" @tap="editConfig('countdown')">
      <text class="config-label">倒计时</text>
      <text class="config-value">{{ item.countdown }} ›</text>
    </view>
    <view class="config-item" @tap="editConfig('think')">
      <text class="config-label">构思时间</text>
      <text class="config-value">{{ item.thinkTime }} ›</text>
    </view>
    <view class="config-item" @tap="editConfig('attempts')">
      <text class="config-label">尝试次数</text>
      <text class="config-value">{{ item.attempts }} ›</text>
    </view>
  </view>

  <!-- 底部按钮 -->
  <view class="bottom-action">
    <view class="submit-btn" @tap="handleSignup">
      <text>{{ item.isSignedUp ? '去打卡' : '报名并打卡' }}</text>
    </view>
  </view>
</view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'

const isExpanded = ref(false)
const currentYear = ref(2026)
const currentMonth = ref(7)
const dayNames = ['日', '一', '二', '三', '四', '五', '六']

const item = ref({
  title: '7月7天批判性思维（独立思考）打卡集训',
  description: '[庆祝]7天"独立思考（批判性思维）"集训，开始报名啦\n[太阳]集训时间：7月27日-8月2日\n觉得自己没有独立思考能力怎么办？想要不被他人观点的话忽悠，想要学会独立思考判断，想要知道自己的选择是否靠谱，我们就需要提升独立思考能力，通过"独立思考（批判性思维）"训练，就能帮我们更好的找出别人的观点有什么问题，做出正确判断。\n注意：批判，不是指批判某个人，而是批判某些观点和观点背后的推理过程是否严谨，是否有漏洞。\n训练内容，模拟相关场景，分析该场景中的思考有没有问题。\n[勾引]适合对象：到了条理表达模块的学员，希望进一步提升思考力的同学。\n[礼物]报名方式：多维班在训学员，在约课宝上报名，消耗一次约课机会报名。（周五、周六、周一任选一天即可）',
  requirement: '高级会员可报名',
  startTime: '2026-07-27',
  endTime: '2026-08-03',
  totalDays: 8,
  countdown: '45分钟',
  thinkTime: '30分钟',
  attempts: '8次',
  hasCalendar: true,
  isSignedUp: false,
})

function goBack() { uni.navigateBack() }
function toggleExpand() { isExpanded.value = !isExpanded.value }
function prevMonth() { if (currentMonth.value > 1) currentMonth.value-- }
function nextMonth() { if (currentMonth.value < 12) currentMonth.value++ }
function goToday() { currentMonth.value = 7; currentYear.value = 2026 }
function editConfig(type) {
  uni.showToast({ title: `编辑${type}`, icon: 'none' })
}
function handleSignup() {
  item.value.isSignedUp = true
  uni.showToast({ title: '报名成功！', icon: 'success' })
}

// Generate calendar days for current month
const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value - 1, 1).getDay()
  const daysInMonth = new Date(currentYear.value, currentMonth.value, 0).getDate()
  // Padding days
  for (let i = 0; i < firstDay; i++) {
    days.push({ num: '', isToday: false })
  }
  for (let i = 1; i <= daysInMonth; i++) {
    days.push({ num: String(i), isToday: i === 26 && currentMonth.value === 7 })
  }
  return days
})

onShow(() => {})
</script>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 30%, #F8F9FC 100%);
}

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
  max-width: 500rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.top-actions {
  display: flex;
  gap: 16rpx;
  align-items: center;
}

.detail-section {
  background: #fff;
  margin: 16rpx;
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.detail-header {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 16rpx;
}
.detail-tag {
  font-size: 28rpx;
}
.detail-header-text {
  font-size: 28rpx;
  font-weight: 600;
  color: #333;
}
.detail-content {
  font-size: 26rpx;
  color: #555;
  line-height: 1.6;
  white-space: pre-line;
}
.expand-link {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8rpx;
  margin-top: 16rpx;
  color: #4CAF50;
  font-size: 24rpx;
}
.expand-arrow {
  font-size: 20rpx;
}

.info-card {
  background: #fff;
  margin: 0 16rpx 16rpx;
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.info-label {
  font-size: 26rpx;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 12rpx;
}
.info-value {
  font-size: 24rpx;
  color: #555;
}
.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.info-days {
  font-size: 24rpx;
  color: #4CAF50;
}

.calendar-section {
  background: #fff;
  margin: 0 16rpx 16rpx;
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.section-label {
  font-size: 26rpx;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 12rpx;
}
.calendar-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24rpx;
  margin-bottom: 12rpx;
}
.calendar-month {
  font-size: 26rpx;
  font-weight: 600;
  color: #333;
}
.today-btn {
  background: #4CAF50;
  color: #fff;
  font-size: 22rpx;
  padding: 8rpx 24rpx;
  border-radius: 20rpx;
  text-align: center;
  margin-bottom: 16rpx;
}
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8rpx;
  text-align: center;
}
.cal-day-name {
  font-size: 22rpx;
  color: #999;
  padding: 8rpx 0;
}
.cal-day {
  font-size: 24rpx;
  color: #333;
  padding: 12rpx 0;
  position: relative;
}
.cal-day.today {
  background: #4CAF50;
  color: #fff;
  border-radius: 50%;
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}
.today-tag {
  font-size: 18rpx;
  color: #4CAF50;
  position: absolute;
  top: -4rpx;
  right: -4rpx;
}

.config-section {
  background: #fff;
  margin: 0 16rpx 16rpx;
  border-radius: 20rpx;
  padding: 0 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.config-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}
.config-item:last-child {
  border-bottom: none;
}
.config-label {
  font-size: 26rpx;
  color: #333;
  font-weight: 500;
}
.config-value {
  font-size: 24rpx;
  color: #666;
}

.bottom-action {
  margin: 24rpx 16rpx;
}
.submit-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 48rpx;
  padding: 24rpx 0;
  text-align: center;
  box-shadow: 0 8rpx 24rpx rgba(76,175,80,.3);
}
.submit-btn text {
  font-size: 30rpx;
  font-weight: 700;
  color: #fff;
}
</style>
