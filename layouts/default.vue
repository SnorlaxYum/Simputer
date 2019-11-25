<template lang="pug">
  site-container
    top-nav(:nav='topnav')
    contents
      transition(name="fade")
        nuxt
    foot
</template>

<script lang="ts">
import Vue from 'vue'
import TopNav from '~/components/TopNav'
import SiteContainer from '~/components/SiteContainer'
import Contents from '~/components/Contents'
import Foot from '~/components/Foot'
import SiteInfo from '~/data/SiteInfo'
export default Vue.extend({
  components: {
    TopNav,
    SiteContainer,
    Contents,
    Foot
  },
  data() {
    return {
      topnav: false
    }
  },
  mixins: [SiteInfo],
  watch: {
    $route(to, from) {
      switch (to.path) {
        case '/':
          this.topnav = false
          break
        default:
          this.topnav = true
          break
      }
      if (!to.hash) {
        window.scrollTo({top:0, behavior: 'smooth'})
      } else if (to.path === from.path && to.hash !== from.hash && getComputedStyle(document.getElementsByTagName('nav')[0]).position === "sticky") {
        let height = document.getElementsByTagName('nav')[0].clientHeight
        setTimeout(() => {window.scrollBy(0, -height)}, 10)
      }
    }
  },
  mounted() {
    switch (this.$route.path) {
      case '/':
        this.topnav = false
        break
      default:
        this.topnav = true
        break
    }
  }
})
</script>