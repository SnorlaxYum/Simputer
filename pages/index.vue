<template lang="pug">
div
  article.main
    header Site Navigation
    nav-boxes(:in-site="true" :nav-list="InNavList")
  article.main
    header Social
    nav-boxes(:in-site="false" :nav-list="OutNavList")
</template>

<script>
const NavBoxes = () => import('~/components/NavBoxes')
import {InNavList, OutNavList} from '~/data/NavList'
export default {
  data() {
    return {InNavList, OutNavList}
  },
  head() {
    return {title: 'Homepage',
      link: [{ rel: 'alternate', href: `${this.$store.state.siteUrl}/atom.xml`, type: 'application/atom+xml' }]}
  },
  components: {
    NavBoxes
  }
}
</script>