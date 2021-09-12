<template lang="pug">
nuxt-link(:to="link" class="icon")
  img(src="/images/tags.svg")
</template>
<script>
export default {
  props: ["link"],
};
</script>