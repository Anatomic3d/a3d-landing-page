<script setup>
defineProps({
  label: String,
  value: String,
  percent: Number,
  color: { type: String, default: "var(--color-primary)" }
})
</script>

<template>
  <div class="budget-bar">
    <div class="budget-row">
      <strong>{{ label }}</strong>
      <span>{{ value }} - {{ percent.toFixed(2).replace(".", ",") }}%</span>
    </div>
    <div class="track">
      <div class="fill" :style="{ width: percent + '%', background: color }"></div>
    </div>
  </div>
</template>

<style scoped>
.budget-bar {
  margin-bottom: 18px;
}
.budget-row {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: baseline;
  margin-bottom: 8px;
  font-size: 18px;
}
.budget-row strong {
  color: var(--color-primary-dark);
}
.budget-row span {
  color: var(--color-text-muted);
  font-weight: 650;
}
.track {
  height: 18px;
  border-radius: 999px;
  background: #e6eef0;
  overflow: hidden;
}
.fill {
  height: 100%;
  border-radius: inherit;
}
</style>
