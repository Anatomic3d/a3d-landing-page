<script setup>
defineProps({
  src: String,
  label: String
})
</script>

<template>
  <div class="photo-placeholder">
    <img v-if="src" :src="src" :alt="label" />
    <div v-else class="empty">
      <MaterialIcon name="team" size="44" />
      <span>{{ label }}</span>
    </div>
  </div>
</template>

<style scoped>
.photo-placeholder {
  width: 178px;
  height: 178px;
  border-radius: 26px;
  overflow: hidden;
  background: linear-gradient(145deg, #e8f3f5, #ffffff);
  border: 1px dashed #b9cbd0;
  flex: 0 0 auto;
}
img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.empty {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  text-align: center;
  color: var(--color-primary);
  padding: 20px;
}
.empty span {
  font-size: 15px;
  line-height: 1.2;
  color: var(--color-text-muted);
}
</style>
