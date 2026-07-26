<template>
<view class="page">
  <view class="section-title">探索更多</view>

  <view class="grid-2">
    <view v-for="tool in tools" :key="tool.label" class="grid-item card-glass tool-card" @tap="goTool(tool)">
      <view class="ri-icon ri-size-lg" :class="tool.icon" :style="{color:tool.color||'var(--brand-primary)'}"></view>
      <text class="tool-label">{{tool.label}}</text>
      <text class="tool-desc">{{tool.desc}}</text>
    </view>
  </view>

  <view class="section-title" style="margin-top:24rpx">更多功能</view>
  <view class="grid-2">
    <view v-for="tool in moreTools" :key="tool.label" class="grid-item card-glass tool-card" @tap="goTool(tool)">
      <view class="ri-icon ri-size-lg" :class="tool.icon" :style="{color:tool.color||'var(--brand-primary)'}"></view>
      <text class="tool-label">{{tool.label}}</text>
      <text class="tool-desc">{{tool.desc}}</text>
    </view>
  </view>

  <view class="btn-ghost" style="text-align:center;margin-top:24rpx" @tap="goManage">管理首页快捷功能</view>
</view>
</template>

<script setup>
const tools=[
  {label:'AI问答',desc:'智能对话助手',icon:'ri-robot-3-line',color:'#4F46E5',action:'ai'},
  {label:'认知管理',desc:'梳理思维模型',icon:'ri-crosshair-line',color:'#7C3AED',action:'ai'},
  {label:'打榜',desc:'训练排行榜',icon:'ri-trophy-line',color:'#F59E0B',url:'/pages/training/leaderboard'},
  {label:'高效能复盘',desc:'深度分析训练',icon:'ri-list-check-3',color:'#10B981',url:'/pages/review/index'},
  {label:'圈子',desc:'口才学习社区',icon:'ri-heart-line',color:'#EF4444',action:'ai'},
  {label:'解决问题',desc:'实战场景模拟',icon:'ri-flashlight-line',color:'#F97316',action:'ai'},
  {label:'AI私教',desc:'一对一辅导',icon:'ri-user-3-line',color:'#6366F1',action:'ai'},
  {label:'普通话纠音',desc:'发音精准训练',icon:'ri-mic-line',color:'#06B6D4',action:'ai'},
]
const moreTools=[
  {label:'锤炼思考力',desc:'逻辑思维训练',icon:'ri-fire-line',color:'#8B5CF6',action:'ai'},
  {label:'高效读书',desc:'读书笔记分享',icon:'ri-book-open-line',color:'#3B82F6',action:'ai'},
]

function goTool(t){
  if(t.url) uni.navigateTo({url:t.url})
  else uni.navigateTo({url:'/pages/ai-tools/index'})
}
function goManage(){uni.showToast({title:'功能开发中',icon:'none'})}
</script>

<style scoped>
.tool-card{display:flex;flex-direction:column;align-items:center;padding:28rpx 16rpx;gap:8rpx;text-align:center}
.tool-label{font-size:26rpx;font-weight:600;color:var(--text-primary)}
.tool-desc{font-size:20rpx;color:var(--text-hint)}
</style>