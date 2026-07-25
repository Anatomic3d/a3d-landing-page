<script setup>
defineProps({
  index: String,
  title: String,
  text: String,
  icon: { type: String, default: "scan" }
})
</script>

<template>
  <article class="process-step">
    <div class="step-top">
      <span>{{ index }}</span>
      <MaterialIcon :name="icon" size="34" />
    </div>
    <h3>{{ title }}</h3>
    <p>{{ text }}</p>
  </article>
</template>

<style scoped>
.process-step {
  min-height: 250px;
  padding: 24px;
  border-radius: 24px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
}
.step-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-primary);
}
.step-top span {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: var(--color-soft);
  font-size: 18px;
  font-weight: 800;
}
h3 {
  font-size: 25px;
  line-height: 1.12;
  color: var(--color-primary-dark);
  margin: 22px 0 10px;
}
p {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 18px;
  line-height: 1.32;
}
</style>
