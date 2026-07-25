<script setup>
defineProps({
  photo: String,
  photoLabel: String,
  name: String,
  formation: String,
  role: String,
  skills: Array,
  responsibility: String
})
</script>

<template>
  <article class="team-card">
    <div class="team-top">
      <PhotoPlaceholder :src="photo" :label="photoLabel" />
      <div>
        <h3>{{ name }}</h3>
        <p class="formation">{{ formation }}</p>
        <p class="role">{{ role }}</p>
      </div>
    </div>
    <div class="chips">
      <span v-for="skill in skills" :key="skill" class="chip">{{ skill }}</span>
    </div>
    <p class="responsibility"><strong>Responsabilidade:</strong> {{ responsibility }}</p>
  </article>
</template>

<style scoped>
.team-card {
  min-height: 560px;
  padding: 26px;
  border-radius: 28px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
}
.team-top {
  display: flex;
  gap: 22px;
  align-items: center;
  margin-bottom: 20px;
}
h3 {
  font-size: 30px;
  line-height: 1.08;
  color: var(--color-primary-dark);
  margin: 0 0 10px;
}
.formation,
.role {
  margin: 0 0 8px;
  color: var(--color-text-muted);
  font-size: 18px;
  line-height: 1.28;
}
.responsibility {
  margin: 20px 0 0;
  color: var(--color-text-muted);
  font-size: 19px;
  line-height: 1.34;
}
.responsibility strong {
  color: var(--color-primary-dark);
}
</style>
