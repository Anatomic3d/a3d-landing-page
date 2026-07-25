<script setup>
defineProps({ text: { type: String, required: true } })
</script>

<template>
  <div class="section-label">{{ text }}</div>
</template>

<style scoped>
.section-label {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  min-height: 34px;
  padding: 7px 14px;
  border-radius: 999px;
  background: rgba(30, 136, 168, 0.11);
  color: var(--color-primary-dark);
  border: 1px solid rgba(30, 136, 168, 0.18);
  font-size: 15px;
  font-weight: 760;
  letter-spacing: 0;
}
</style>
