<script setup>
defineProps({
  text: String,
  note: String
})
</script>

<template>
  <aside class="quote-highlight">
    <p>{{ text }}</p>
    <span v-if="note">{{ note }}</span>
  </aside>
</template>

<style scoped>
.quote-highlight {
  padding: 26px 30px;
  border-radius: 26px;
  background: var(--color-primary-dark);
  color: white;
  box-shadow: 0 18px 44px rgba(8, 63, 73, 0.18);
}
p {
  font-size: 32px;
  line-height: 1.18;
  font-weight: 760;
  margin: 0;
}
span {
  display: block;
  margin-top: 12px;
  font-size: 18px;
  color: rgba(255,255,255,0.78);
}
</style>
