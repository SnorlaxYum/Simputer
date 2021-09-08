<template lang="pug">
nav
  nuxt-link(to='/' :class="nav ? undefined : 'center-item'")
    .logo
  ul.site-navigation(v-show='nav')
    li(v-for='nav in InNavList')
      nuxt-link(:to="'/' + nav.slug") {{nav.title}}
</template>

<script>
import {InNavList} from "~/data/NavList"

export default {
  data() {
    return {InNavList}
  },
  props: ["nav"]
}
</script>