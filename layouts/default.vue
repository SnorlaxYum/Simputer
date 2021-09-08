<template lang="pug">
  site-container
    top-nav(:nav='topnav')
    contents
      transition(name="fade")
        nuxt
    foot
</template>

<script>
const TopNav = () => import('~/components/TopNav')
const SiteContainer = () => import('~/components/SiteContainer')
const Contents = () => import('~/components/Contents')
const Foot = () => import('~/components/Foot')

export default {
  components: {
    TopNav,
    SiteContainer,
    Contents,
    Foot
  },
  data() {
    return {
      siteTitle: this.$store.state.siteTitle,
      topnav: false
    }
  },
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
  },
  head() {
    return {
        titleTemplate: '%s - ' + this.$store.state.siteTitle,
        link: [
            {
                rel: 'preconnect',
                href: 'https://isso.snorl.ax'
            }
        ]
    }
  }
}
</script>