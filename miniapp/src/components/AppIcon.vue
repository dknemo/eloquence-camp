<template>
  <text class="app-icon" :class="[iconClass, `ri-size-${size}`, { 'ri-active': active }]" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: String, default: 'md' },
  active: { type: Boolean, default: false }
})

// 旧图标名 → Remix Icon class 映射
const MAP = {
  mic: 'ri-mic-line',
  search: 'ri-search-line',
  star: 'ri-star-line',
  fire: 'ri-fire-line',
  trophy: 'ri-trophy-line',
  profile: 'ri-user-3-line',
  calendar: 'ri-calendar-line',
  bell: 'ri-notification-3-line',
  moon: 'ri-moon-line',
  gift: 'ri-gift-line',
  info: 'ri-information-line',
  list: 'ri-list-check-3',
  robot: 'ri-robot-3-line',
  target: 'ri-crosshair-line',
  bolt: 'ri-flashlight-line',
  video: 'ri-video-line',
  briefcase: 'ri-briefcase-line',
  book: 'ri-book-open-line',
}

const iconClass = computed(() => MAP[props.name] || `ri-${props.name}-line`)
</script>
