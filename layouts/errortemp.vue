<template lang="pug">
  site-container
    top-nav-error(:nav='topnav')
    contents
      nuxt
    foot
</template>

<script>
import TopNavError from '~/components/TopNavError'
const SiteContainer = () => import('~/components/SiteContainer')
const Contents = () => import('~/components/Contents')
const Foot = () => import('~/components/Foot')

export default {
  components: {
    TopNavError,
    SiteContainer,
    Contents,
    Foot
  },
  data() {
    return {
      siteTitle: this.$store.state.siteTitle,
      topnav: true
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