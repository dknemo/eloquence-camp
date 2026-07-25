<script setup>
import { onLaunch, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

onLaunch(() => {
  console.log('App Launch')
  // 自动登录：检查本地是否有token，有则直接恢复
  const savedToken = uni.getStorageSync('token')
  if (savedToken) {
    userStore.setToken(savedToken)
  }
  // 无论是否有token，都走一遍微信登录刷新token
  doLogin()
})

onShow(() => {
  console.log('App Show')
})

async function doLogin() {
  try {
    // 1. 调用微信登录获取code（测试号环境可能拿不到，用兜底code）
    let code = ''
    try {
      const loginRes = await uni.login()
      code = loginRes.code || ''
    } catch (e) {
      console.warn('uni.login 异常，使用兜底 code', e)
    }
    if (!code) {
      // 测试号/无 AppID 环境兜底，后端 wechat-login 接受任意 code 走 mock
      code = 'dev_' + Date.now()
      console.warn('使用兜底 code 登录:', code)
    }

    // 2. 发送code到后端换取JWT
    const resp = await uni.request({
      url: getBaseUrl() + '/auth/wechat-login',
      method: 'POST',
      data: { code },
      header: { 'Content-Type': 'application/json' }
    })

    if (resp.statusCode === 200 && resp.data.code === 200) {
      const { token, user, is_new_user } = resp.data.data
      // 3. 存储token
      userStore.setToken(token)
      userStore.setUser(user)
      uni.setStorageSync('token', token)
      console.log('登录成功', user.nickname || '新用户', is_new_user ? '(首次)' : '')
    } else {
      console.error('登录失败', resp.data)
    }
  } catch (e) {
    console.error('登录异常', e)
    // 登录失败不阻塞使用，部分功能降级
  }
}

function getBaseUrl() {
  // #ifdef MP-WEIXIN
  return 'http://192.168.200.214:5000/api'
  // #endif
  // #ifndef MP-WEIXIN
  return 'https://api.your-domain.com/api'
  // #endif
}
</script>

<template>
  <view>
    <!-- 页面路由出口 -->
  </view>
</template>

<style lang="scss">
@import '@/styles/global.scss';
</style>
