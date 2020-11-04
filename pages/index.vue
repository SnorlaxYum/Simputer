<template lang="pug">
div
  article.main
    header Site Navigation
    nav-boxes(:in-site="true" :nav-list="InNavList")
  article.main
    header Social
    nav-boxes(:in-site="false" :nav-list="OutNavList")
</template>

<script lang="ts">
import Vue from 'vue'
import NavBoxes from '~/components/NavBoxes'
import NavList from '~/data/NavList'
export default Vue.extend({
  head() {
    return {title: 'Homepage',
      link: [{ rel: 'alternate', href: `${this.$store.state.siteUrl}/atom.xml`, type: 'application/atom+xml' }]}
  },
  components: {
    NavBoxes
  },
  mixins: [NavList]
})
</script>