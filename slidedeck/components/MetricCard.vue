<script setup>
defineProps({
  label: String,
  value: String,
  detail: String,
  icon: { type: String, default: "check" }
})
</script>

<template>
  <article class="metric-card">
    <MaterialIcon :name="icon" size="32" />
    <div class="metric-value">{{ value }}</div>
    <h3>{{ label }}</h3>
    <p>{{ detail }}</p>
  </article>
</template>

<style scoped>
.metric-card {
  min-height: 220px;
  padding: 24px;
  border-radius: 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  color: var(--color-primary);
}
.metric-value {
  font-size: 44px;
  line-height: 1;
  font-weight: 800;
  margin: 18px 0 10px;
}
h3 {
  color: var(--color-text);
  font-size: 24px;
  margin: 0 0 10px;
}
p {
  color: var(--color-text-muted);
  font-size: 18px;
  line-height: 1.32;
  margin: 0;
}
</style>
