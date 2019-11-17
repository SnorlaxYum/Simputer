<template lang="pug">
    footer.footer This site is proudly served by Nuxt.js. Simputer &copy; 2009 - {{ thisYear }}
</template>

<script>
export default {
    computed: {
      thisYear() {
        return new Date().getFullYear()
      }
    }
}
</script>