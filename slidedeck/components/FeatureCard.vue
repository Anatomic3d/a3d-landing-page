<script setup>
defineProps({
  title: String,
  text: String,
  icon: { type: String, default: "check" },
  compact: { type: Boolean, default: false }
})
</script>

<template>
  <article class="feature-card" :class="{ compact }">
    <div class="icon-wrap"><MaterialIcon :name="icon" size="30" /></div>
    <h3>{{ title }}</h3>
    <p>{{ text }}</p>
  </article>
</template>

<style scoped>
.feature-card {
  min-height: 210px;
  padding: 26px;
  border-radius: 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
}
.feature-card.compact {
  min-height: 164px;
  padding: 22px;
}
.icon-wrap {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: var(--color-soft);
  color: var(--color-primary);
  margin-bottom: 16px;
}
h3 {
  font-size: 25px;
  line-height: 1.12;
  color: var(--color-primary-dark);
  margin: 0 0 10px;
}
p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 19px;
  line-height: 1.32;
}
</style>
