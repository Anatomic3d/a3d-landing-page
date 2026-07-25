<script setup>
const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 28 },
  label: { type: String, default: "" }
})

const paths = {
  scan: "M4 8V4h4M20 8V4h-4M4 16v4h4M20 16v4h-4M7 12h10M12 7v10",
  brain: "M9 4a4 4 0 0 0-4 4v1a4 4 0 0 0 0 6v1a4 4 0 0 0 7 2.65A4 4 0 0 0 19 16v-1a4 4 0 0 0 0-6V8a4 4 0 0 0-7-2.65A4 4 0 0 0 9 4Z",
  cube: "M12 3 4.5 7.2v9.1L12 21l7.5-4.7V7.2L12 3ZM12 3v8.8m7.5-4.6L12 11.8 4.5 7.2",
  check: "m5 12 4 4L19 6",
  hospital: "M4 21V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v15M8 21v-6h8v6M9 8h6M12 5v6",
  blood: "M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11Z",
  cloud: "M7 18a5 5 0 0 1 1.2-9.85A6 6 0 0 1 19.7 10.3 4 4 0 0 1 19 18H7Z",
  print: "M7 8V3h10v5M7 17H5a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2M7 14h10v7H7z",
  ai: "M12 3v3m0 12v3M3 12h3m12 0h3M7.8 7.8 5.7 5.7m12.6 12.6-2.1-2.1M16.2 7.8l2.1-2.1M5.7 18.3l2.1-2.1M9 9h6v6H9z",
  revenue: "M4 18h16M7 16V9m5 7V5m5 11v-4",
  team: "M16 11a4 4 0 1 0-8 0M4 21a8 8 0 0 1 16 0",
  map: "M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z",
  rocket: "M12 15 9 12m3 3 3-3M8 16l-2 4 4-2M14 6c2-2 4-3 7-3 0 3-1 5-3 7l-6 6-4-4 6-6Z"
}
</script>

<template>
  <svg
    class="material-icon"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
    stroke-linecap="round"
    stroke-linejoin="round"
    role="img"
    :aria-label="label || name"
  >
    <path :d="paths[name] || paths.check" />
  </svg>
</template>

<style scoped>
.material-icon {
  display: inline-block;
  flex: 0 0 auto;
}
</style>
