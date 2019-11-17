<template lang="pug">
  site-container
    top-nav-error(:nav='topnav')
    contents
      nuxt
    foot
</template>

<script>
import TopNavError from '~/components/TopNavError'
import SiteContainer from '~/components/SiteContainer'
import Contents from '~/components/Contents'
import Foot from '~/components/Foot'
import SiteInfo from '~/data/SiteInfo'

export default {
  components: {
    TopNavError,
    SiteContainer,
    Contents,
    Foot
  },
  data() {
    return {
      topnav: true
    }
  },
  mixins: [SiteInfo]
}
</script>