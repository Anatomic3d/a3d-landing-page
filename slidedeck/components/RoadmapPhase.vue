<script setup>
defineProps({
  phase: String,
  period: String,
  title: String,
  goals: Array,
  milestone: String,
  future: { type: Boolean, default: false }
})
</script>

<template>
  <article class="roadmap-phase" :class="{ future }">
    <div class="phase-head">
      <span>{{ phase }}</span>
      <strong>{{ period }}</strong>
    </div>
    <h3>{{ title }}</h3>
    <ul>
      <li v-for="goal in goals" :key="goal">{{ goal }}</li>
    </ul>
    <div class="milestone">{{ milestone }}</div>
  </article>
</template>

<style scoped>
.roadmap-phase {
  min-height: 610px;
  padding: 26px;
  border-radius: 26px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
}
.roadmap-phase.future {
  background: #f0f7f8;
  border-style: dashed;
}
.phase-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.phase-head span {
  color: var(--color-primary);
  font-weight: 800;
  font-size: 18px;
}
.phase-head strong {
  font-size: 18px;
  color: var(--color-text-muted);
}
h3 {
  margin: 0 0 18px;
  font-size: 30px;
  color: var(--color-primary-dark);
}
ul {
  padding-left: 22px;
  margin: 0;
  color: var(--color-text-muted);
  font-size: 18px;
  line-height: 1.34;
}
li {
  margin-bottom: 9px;
}
.milestone {
  margin-top: 22px;
  padding: 16px;
  border-radius: 16px;
  background: rgba(69, 183, 168, 0.14);
  color: var(--color-primary-dark);
  font-size: 18px;
  font-weight: 760;
}
</style>
