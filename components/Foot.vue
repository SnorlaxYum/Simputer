<template lang="pug">
  footer.footer This site is proudly served by Python and Nuxt.js. Simputer &copy; 2016 - {{ thisYear }}
</template>

<script lang="ts">
export default {
  computed: {
    thisYear() {
      return new Date().getFullYear();
    }
  }
};
</script>