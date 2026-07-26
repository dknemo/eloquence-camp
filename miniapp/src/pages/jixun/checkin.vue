<template>
  <view class="page checkin-page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="back-btn" @click="goBack">
        <text class="icon">←</text>
      </view>
      <text class="nav-title">集训打卡</text>
      <view class="menu-btn">⋯</view>
    </view>

    <!-- 倒计时和构思时间 -->
    <view class="timer-bar">
      <view class="timer-item">
        <text class="timer-label">倒计时</text>
        <text class="timer-value">{{ formatTime(countdownTimer) }}</text>
      </view>
      <view class="timer-item">
        <text class="timer-label">构思时间</text>
        <text class="timer-value">{{ formatTime(thinkTimer) }}</text>
      </view>
    </view>

    <!-- 本次打卡题目 -->
    <view class="topic-section">
      <view class="section-header">
        <text class="section-title">本次打卡题目</text>
      </view>
      <view class="topic-content">
        <text class="topic-text">{{ currentTopic }}</text>
      </view>
    </view>

    <!-- 开始打卡按钮 -->
    <view class="action-section">
      <button class="start-btn" @click="startCheckin">
        开始打卡
      </button>
      
      <!-- AI功能按钮 -->
      <view class="ai-buttons">
        <button class="ai-btn ai-feedback" @click="getAIFeedback">
          AI评述
        </button>
        <button class="ai-btn ai-hints" @click="getAIHints">
          AI启发
        </button>
      </view>
    </view>

    <!-- 打卡内容输入区 -->
    <view class="input-section" v-if="showInput">
      <view class="input-header">
        <text class="input-label">打卡内容</text>
        <text class="char-count">{{ contentText.length }}/10000</text>
      </view>
      <textarea 
        class="input-area"
        v-model="contentText"
        placeholder="请输入你的打卡内容..."
        maxlength="10000"
      />
      
      <!-- 语音和图片按钮 -->
      <view class="media-buttons">
        <button class="media-btn" @click="toggleRecording">
          {{ isRecording ? '⏹ 停止录音' : '🎤 开始录音' }}
        </button>
        <button class="media-btn" @click="uploadImage">
          📷 图片
        </button>
      </view>
      
      <!-- 录音状态显示 -->
      <view class="recording-status" v-if="isRecording">
        <text class="recording-text">正在录音... {{ recordingDuration }}s</text>
      </view>
      <view class="audio-playback" v-else-if="audioUrl" @click="playAudio">
        <view class="play-btn">
          <text class="play-icon">{{ isPlaying ? '⏸' : '▶️' }}</text>
        </view>
        <text class="audio-duration">{{ formatAudioDuration(audioDuration) }}</text>
      </view>
    </view>

    <!-- 已提交录音展示（作业列表里的） -->
    <view class="submitted-audio" v-if="submittedAudioUrl">
      <view class="audio-card">
        <view class="play-btn-large" @click="playSubmittedAudio">
          <text class="play-icon-large">{{ submittedIsPlaying ? '⏸' : '▶️' }}</text>
        </view>
        <text class="audio-label">{{ submittedAudioDuration }}</text>
      </view>
    </view>

    <!-- 权限设置 -->
    <view class="permission-section" v-if="showInput">
      <view class="permission-row">
        <text class="permission-label">权限</text>
        <text class="permission-value">所有人可见 ›</text>
      </view>
    </view>

    <!-- 底部操作按钮 -->
    <view class="bottom-actions" v-if="showInput">
      <button class="cancel-btn" @click="cancelCheckin">取消</button>
      <button class="submit-btn" @click="submitCheckin">提交打卡</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getBaseUrl } from '@/api/request.js'

const eventId = ref(null)
const event = ref(null)
const countdownTimer = ref(0)
const thinkTimer = ref(0)
const currentTopic = ref('')
const showInput = ref(false)
const contentText = ref('')
const audioUrl = ref('')
const imageUrls = ref([])

// 录音相关状态
const isRecording = ref(false)
const isPlaying = ref(false)
const recordingDuration = ref(0)
const audioDuration = ref(0)
let recorderManager = null
let recordingInterval = null
let innerAudioContext = null

// 已提交录音状态
const submittedAudioUrl = ref('')
const submittedIsPlaying = ref(false)
const submittedAudioDuration = ref('00:00')
let submittedAudioContext = null

onMounted(async () => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  eventId.value = currentPage.options.id
  
  await loadEvent()
  startTimers()
  initRecorder()
})

function initRecorder() {
  recorderManager = uni.getRecorderManager()
  
  recorderManager.onStart(() => {
    console.log('录音开始')
    isRecording.value = true
    recordingDuration.value = 0
    recordingInterval = setInterval(() => {
      recordingDuration.value++
      // 最长录音10分钟
      if (recordingDuration.value >= 600) {
        stopRecording()
      }
    }, 1000)
  })
  
  recorderManager.onStop((res) => {
    console.log('录音停止', res.tempFilePath)
    isRecording.value = false
    clearInterval(recordingInterval)
    audioUrl.value = res.tempFilePath
    // 微信 onStop 回调中时长字段为 durationTime（字符串，单位ms）
    const durationMs = res.durationTime ? parseInt(res.durationTime) : (res.duration || 0)
    audioDuration.value = durationMs / 1000 || 0
  })
  
  recorderManager.onError((err) => {
    console.error('录音错误', err)
    isRecording.value = false
    clearInterval(recordingInterval)
    uni.showToast({ title: '录音失败，请重试', icon: 'none' })
  })
}

function toggleRecording() {
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

function startRecording() {
  // 使用新版权限请求方式（不依赖 scope.record）
  recorderManager.start({
    format: 'mp3',
    sampleRate: 44100,
    numberOfChannels: 1,
    encodeBitRate: 192000
  })
}

function stopRecording() {
  recorderManager.stop()
}

function playAudio() {
  if (!innerAudioContext) {
    innerAudioContext = uni.createInnerAudioContext()
    innerAudioContext.src = audioUrl.value
    innerAudioContext.obeyMuteSwitch = false
    
    innerAudioContext.onPlay(() => {
      isPlaying.value = true
    })
    
    innerAudioContext.onPause(() => {
      isPlaying.value = false
    })
    
    innerAudioContext.onStop(() => {
      isPlaying.value = false
    })
    
    innerAudioContext.onEnded(() => {
      isPlaying.value = false
    })
    
    innerAudioContext.onError((err) => {
      console.error('播放音频失败', err)
      isPlaying.value = false
      uni.showToast({ title: '播放失败', icon: 'none' })
    })
  }
  
  if (isPlaying.value) {
    innerAudioContext.pause()
  } else {
    innerAudioContext.play()
  }
}

function formatAudioDuration(seconds) {
  if (!seconds) return '00:00'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

async function loadEvent() {
  try {
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/events/${eventId.value}`,
      method: 'GET'
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      event.value = res.data.data
      // 从description中提取当前天的题目
      const topics = event.value.description.split('\n').filter(line => line.startsWith('第'))
      if (topics.length > 0) {
        currentTopic.value = topics[0] // 默认显示第一题
      }
    }
  } catch (err) {
    console.error('加载活动详情失败:', err)
  }
}

function startTimers() {
  // 模拟倒计时和构思时间
  countdownTimer.value = 45 * 60 // 45分钟
  thinkTimer.value = 30 * 60 // 30分钟
  
  // 每秒更新
  setInterval(() => {
    if (countdownTimer.value > 0) countdownTimer.value--
    if (thinkTimer.value > 0) thinkTimer.value--
  }, 1000)
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function startCheckin() {
  showInput.value = true
}

function getAIFeedback() {
  // TODO: 调用AI评述接口
  uni.showToast({ title: 'AI评述功能开发中', icon: 'none' })
}

function getAIHints() {
  // TODO: 调用AI启发接口
  uni.showToast({ title: 'AI启发功能开发中', icon: 'none' })
}

function uploadImage() {
  // TODO: 上传图片功能
  uni.chooseImage({
    count: 9,
    success: (res) => {
      imageUrls.value = res.tempFilePaths
    }
  })
}

function cancelCheckin() {
  showInput.value = false
  contentText.value = ''
  audioUrl.value = ''
  imageUrls.value = []
}

async function submitCheckin() {
  // 验证不能空内容提交
  if (!contentText.value.trim() && !audioUrl.value) {
    uni.showToast({ title: '请输入文字或录音', icon: 'none' })
    return
  }
  
  try {
    const token = uni.getStorageSync('token')
    if (!token) {
      uni.showToast({ title: '请先登录', icon: 'none' })
      return
    }
    
    const baseUrl = getBaseUrl()
    const res = await uni.request({
      url: `${baseUrl}/jixun/checkin`,
      method: 'POST',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: {
        event_id: eventId.value,
        day_number: 1, // TODO: 根据当前日期计算第几天
        content_text: contentText.value,
        audio_url: audioUrl.value,
        image_urls: imageUrls.value
      }
    })
    
    if (res.statusCode === 200 && res.data.code === 200) {
      uni.showToast({ title: '打卡成功', icon: 'success' })
      
      // 提交成功后显示已提交的录音
      submittedAudioUrl.value = audioUrl.value
      submittedAudioDuration.value = formatAudioDuration(audioDuration.value)
      
      setTimeout(() => {
        uni.navigateTo({
          url: `/pages/jixun/result?id=${eventId.value}`
        })
      }, 1500)
    }
  } catch (err) {
    console.error('提交打卡失败:', err)
    uni.showToast({ title: '提交失败，请重试', icon: 'none' })
  }
}

function playSubmittedAudio() {
  if (!submittedAudioContext) {
    submittedAudioContext = uni.createInnerAudioContext()
    submittedAudioContext.obeyMuteSwitch = false
    
    submittedAudioContext.onPlay(() => {
      submittedIsPlaying.value = true
    })
    
    submittedAudioContext.onPause(() => {
      submittedIsPlaying.value = false
    })
    
    submittedAudioContext.onStop(() => {
      submittedIsPlaying.value = false
    })
    
    submittedAudioContext.onEnded(() => {
      submittedIsPlaying.value = false
    })
    
    submittedAudioContext.onError((err) => {
      console.error('播放提交录音失败', err)
      submittedIsPlaying.value = false
    })
  }
  
  if (submittedIsPlaying.value) {
    submittedAudioContext.pause()
  } else {
    submittedAudioContext.src = submittedAudioUrl.value
    submittedAudioContext.play()
  }
}

function goBack() {
  uni.navigateBack()
}
</script>

<style scoped lang="scss">
.checkin-page {
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

.timer-bar {
  display: flex;
  justify-content: space-around;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  
  .timer-item {
    text-align: center;
    
    .timer-label {
      font-size: 24rpx;
      color: #666;
      display: block;
      margin-bottom: 10rpx;
    }
    
    .timer-value {
      font-size: 36rpx;
      font-weight: bold;
      color: #4CAF50;
      font-family: monospace;
    }
  }
}

.topic-section {
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  
  .section-header {
    margin-bottom: 20rpx;
    
    .section-title {
      font-size: 30rpx;
      font-weight: bold;
      color: #333;
    }
  }
  
  .topic-content {
    .topic-text {
      font-size: 28rpx;
      color: #333;
      line-height: 1.6;
    }
  }
}

.action-section {
  padding: 30rpx;
  
  .start-btn {
    width: 100%;
    height: 88rpx;
    background: #4CAF50;
    color: #fff;
    border: none;
    border-radius: 44rpx;
    font-size: 32rpx;
    font-weight: bold;
    margin-bottom: 20rpx;
  }
  
  .ai-buttons {
    display: flex;
    gap: 20rpx;
    
    .ai-btn {
      flex: 1;
      height: 72rpx;
      border: 2rpx solid #4CAF50;
      color: #4CAF50;
      border-radius: 36rpx;
      font-size: 28rpx;
      background: transparent;
      
      &.ai-feedback {
        border-color: #FF9800;
        color: #FF9800;
      }
      
      &.ai-hints {
        border-color: #9C27B0;
        color: #9C27B0;
      }
    }
  }
}

.input-section {
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  
  .input-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
    
    .input-label {
      font-size: 28rpx;
      font-weight: bold;
      color: #333;
    }
    
    .char-count {
      font-size: 24rpx;
      color: #999;
    }
  }
  
  .input-area {
    width: 100%;
    height: 300rpx;
    background: #f5f5f5;
    border-radius: 12rpx;
    padding: 20rpx;
    font-size: 28rpx;
    color: #333;
    box-sizing: border-box;
  }
  
  .media-buttons {
    display: flex;
    gap: 20rpx;
    margin-top: 20rpx;
    
    .media-btn {
      flex: 1;
      height: 72rpx;
      background: #f5f5f5;
      color: #666;
      border: none;
      border-radius: 36rpx;
      font-size: 28rpx;
    }
  }
  
  .recording-status {
    margin-top: 20rpx;
    text-align: center;
    
    .recording-text {
      font-size: 28rpx;
      color: #F44336;
      font-weight: bold;
    }
  }
  
  .audio-playback {
    display: flex;
    align-items: center;
    gap: 16rpx;
    margin-top: 20rpx;
    padding: 20rpx;
    background: #f5f5f5;
    border-radius: 12rpx;
    
    .play-btn {
      width: 60rpx;
      height: 60rpx;
      background: #4CAF50;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      
      .play-icon {
        font-size: 24rpx;
        color: #fff;
      }
    }
    
    .audio-duration {
      font-size: 26rpx;
      color: #666;
    }
  }
  
  .submitted-audio {
    margin-top: 30rpx;
    
    .audio-card {
      display: flex;
      align-items: center;
      gap: 16rpx;
      padding: 20rpx;
      background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
      border-radius: 12rpx;
      border: 2rpx solid #4CAF50;
      
      .play-btn-large {
        width: 80rpx;
        height: 80rpx;
        background: #4CAF50;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4rpx 12rpx rgba(76, 175, 80, 0.3);
        
        .play-icon-large {
          font-size: 32rpx;
          color: #fff;
        }
      }
      
      .audio-label {
        font-size: 28rpx;
        color: #2E7D32;
        font-weight: bold;
      }
      
      .audio-time {
        font-size: 26rpx;
        color: #4CAF50;
        margin-left: auto;
      }
    }
  }
}

.permission-section {
  background: rgba(255, 255, 255, 0.9);
  margin: 20rpx 30rpx;
  border-radius: 16rpx;
  padding: 30rpx;
  
  .permission-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .permission-label {
      font-size: 28rpx;
      color: #333;
    }
    
    .permission-value {
      font-size: 28rpx;
      color: #4CAF50;
    }
  }
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  gap: 20rpx;
  
  .cancel-btn {
    flex: 1;
    height: 88rpx;
    background: #f5f5f5;
    color: #666;
    border: none;
    border-radius: 44rpx;
    font-size: 32rpx;
  }
  
  .submit-btn {
    flex: 2;
    height: 88rpx;
    background: #4CAF50;
    color: #fff;
    border: none;
    border-radius: 44rpx;
    font-size: 32rpx;
    font-weight: bold;
  }
}
</style>
