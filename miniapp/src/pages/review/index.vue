<template>
<view class="page review-page">
  <!-- 顶部标题 -->
  <view class="page-header">
    <text class="page-title">训练复盘</text>
    <text class="page-sub">回顾每一次进步</text>
  </view>

  <!-- 数据统计卡片 -->
  <view class="stats-row">
    <view class="stat-card">
      <text class="stat-num">{{ stats.total }}</text>
      <text class="stat-lab">总训练</text>
    </view>
    <view class="stat-card">
      <text class="stat-num highlight">{{ stats.avgScore }}</text>
      <text class="stat-lab">平均分</text>
    </view>
    <view class="stat-card">
      <text class="stat-num success">{{ stats.successRate }}%</text>
      <text class="stat-lab">成功率</text>
    </view>
    <view class="stat-card">
      <text class="stat-num">{{ stats.streak }}</text>
      <text class="stat-lab">连续天</text>
    </view>
  </view>

  <!-- 筛选标签 -->
  <view class="filter-row">
    <text class="ftab" :class="{active:filter==='all'}" @tap="setFilter('all')">全部</text>
    <text class="ftab" :class="{active:filter==='success'}" @tap="setFilter('success')">✓ 成功</text>
    <text class="ftab" :class="{active:filter==='fail'}" @tap="setFilter('fail')">✗ 未过</text>
  </view>

  <!-- 训练列表 -->
  <scroll-view scroll-y class="review-list" :show-scrollbar="false">
    <view v-if="list.length===0" class="empty">
      <view class="ri-icon ri-size-xl ri-file-list-3-line" style="color:#ccc;font-size:80rpx;margin-bottom:16rpx"></view>
      <text>暂无训练记录</text>
      <text class="empty-sub">完成一次练习后这里会出现复盘数据</text>
    </view>

    <view
      v-for="(r,i) in list"
      :key="r.id"
      class="review-card"
      @tap="goDetail(r)"
    >
      <view class="rc-left">
        <view class="rc-score" :class="scoreClass(r.ai_score)">
          <text class="rc-score-num">{{ r.ai_score || '-' }}</text>
          <text class="rc-score-lab">分</text>
        </view>
      </view>
      <view class="rc-body">
        <view class="rc-row">
          <text class="rc-title ellipsis">{{ r.title || '口才练习' }}</text>
          <view class="rc-badge" :class="r.success ? 'pass' : 'fail'">
            {{ r.success ? '通过' : '未过' }}
          </view>
        </view>
        <view class="rc-meta">
          <text class="rc-cat">{{ catLabel(r.category) || '综合训练' }}</text>
          <text class="rc-dot">·</text>
          <text class="rc-time">{{ fmtDate(r.created_at) }}</text>
        </view>
      </view>
      <view class="rc-arrow">
        <view class="ri-icon ri-size-sm ri-arrow-right-s-line"></view>
      </view>
    </view>

    <view class="list-bottom"></view>
  </scroll-view>
</view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import api from '@/api/request'
import { catLabel } from '@/utils/category'

const filter = ref('all')
const list = ref([])
const stats = ref({ total: 0, avgScore: '-', successRate: 0, streak: 0 })

const scoreClass = (s) => {
  if (!s && s !== 0) return ''
  if (s >= 80) return 'great'
  if (s >= 60) return 'good'
  return 'poor'
}

function fmtDate(d) {
  if (!d) return ''
  const t = new Date(d)
  const m = t.getMonth() + 1
  const day = t.getDate()
  return `${m}月${day}日`
}

function setFilter(v) { filter.value = v; load() }

async function load() {
  try {
    const params = { page_size: 100 }
    if (filter.value !== 'all') params.success = filter.value === 'success'
    const d = await api.get('/training/reviews', params)
    const items = d.items || []
    list.value = items
    
    // Calc stats
    const total = items.length
    const scores = items.filter(i => i.ai_score != null).map(i => i.ai_score)
    const avg = scores.length ? Math.round(scores.reduce((a,b) => a+b, 0) / scores.length) : '-'
    const succ = items.filter(i => i.success).length
    const rate = total ? Math.round(succ / total * 100) : 0
    stats.value = { total, avgScore: avg, successRate: rate, streak: d.continuous_days || 0 }
  } catch (e) {
    list.value = []
    stats.value = { total: 0, avgScore: '-', successRate: 0, streak: 0 }
  }
}

function goDetail(r) {
  if (r.training_item_id) {
    uni.navigateTo({ url: '/pages/training/detail?id=' + r.training_item_id })
  }
}

onShow(() => { load() })
</script>

<style scoped>
.review-page {
  min-height: 100vh;
  background: #F8F9FC;
}

.page-header {
  padding: 32rpx 32rpx 8rpx;
}
.page-title {
  font-size: 40rpx;
  font-weight: 800;
  color: #1A1A2E;
  display: block;
}
.page-sub {
  font-size: 24rpx;
  color: #888;
  margin-top: 4rpx;
}

/* 统计卡片 */
.stats-row {
  display: flex;
  gap: 12rpx;
  padding: 16rpx 24rpx;
}
.stat-card {
  flex: 1;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx 12rpx;
  text-align: center;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.stat-num {
  font-size: 36rpx;
  font-weight: 800;
  color: #1A1A2E;
  display: block;
}
.stat-num.highlight { color: #4F46E5; }
.stat-num.success { color: #10B981; }
.stat-lab {
  font-size: 20rpx;
  color: #999;
  margin-top: 4rpx;
  display: block;
}

/* 筛选 */
.filter-row {
  display: flex;
  gap: 16rpx;
  padding: 8rpx 24rpx 16rpx;
}
.ftab {
  font-size: 24rpx;
  padding: 10rpx 28rpx;
  border-radius: 24rpx;
  background: #fff;
  color: #666;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,.04);
}
.ftab.active {
  background: #4F46E5;
  color: #fff;
  box-shadow: 0 4rpx 12rpx rgba(79,70,229,.3);
}

/* 列表 */
.review-list {
  padding: 0 24rpx;
  height: calc(100vh - 400rpx);
}
.review-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx;
  margin-bottom: 12rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,.04);
}
.review-card:active { background: #f9f9f9; }

.rc-left {
  flex-shrink: 0;
  margin-right: 16rpx;
}
.rc-score {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
}
.rc-score.great { background: #EEF2FF; }
.rc-score.good { background: #FEF3C7; }
.rc-score.poor { background: #FEF2F2; }
.rc-score-num {
  font-size: 28rpx;
  font-weight: 800;
  color: #1A1A2E;
  line-height: 1.2;
}
.rc-score.great .rc-score-num { color: #4F46E5; }
.rc-score.good .rc-score-num { color: #F59E0B; }
.rc-score.poor .rc-score-num { color: #EF4444; }
.rc-score-lab {
  font-size: 18rpx;
  color: #999;
}

.rc-body {
  flex: 1;
  min-width: 0;
}
.rc-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
}
.rc-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #1A1A2E;
  flex: 1;
  min-width: 0;
}
.rc-badge {
  font-size: 20rpx;
  padding: 2rpx 12rpx;
  border-radius: 6rpx;
  flex-shrink: 0;
}
.rc-badge.pass { background: #ECFDF5; color: #10B981; }
.rc-badge.fail { background: #FEF2F2; color: #EF4444; }

.rc-meta {
  display: flex;
  align-items: center;
  gap: 6rpx;
  margin-top: 8rpx;
}
.rc-cat, .rc-time { font-size: 22rpx; color: #999; }
.rc-dot { color: #ddd; }

.rc-arrow {
  color: #ccc;
  flex-shrink: 0;
  margin-left: 8rpx;
}

.empty {
  text-align: center;
  padding: 120rpx 0;
  color: #999;
  font-size: 28rpx;
}
.empty-sub {
  display: block;
  font-size: 24rpx;
  color: #bbb;
  margin-top: 8rpx;
}
.list-bottom { height: 40rpx; }
</style>
