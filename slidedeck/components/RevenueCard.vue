<script setup>
defineProps({
  title: String,
  text: String,
  icon: { type: String, default: "revenue" }
})
</script>

<template>
  <article class="revenue-card">
    <MaterialIcon :name="icon" size="28" />
    <h3>{{ title }}</h3>
    <p>{{ text }}</p>
  </article>
</template>

<style scoped>
.revenue-card {
  min-height: 150px;
  padding: 20px;
  border-radius: 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  color: var(--color-primary);
}
h3 {
  font-size: 21px;
  color: var(--color-primary-dark);
  margin: 12px 0 8px;
}
p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 16px;
  line-height: 1.28;
}
</style>
