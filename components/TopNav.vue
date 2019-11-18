<template lang="pug">
nav
  nuxt-link(to='/' :class="nav ? undefined : 'center-item'")
    .logo
  ul.site-navigation(v-if='nav')
    li(v-for='nav in InNavList')
      nuxt-link(:to="'/' + nav.slug") {{nav.title}}
</template>

<script lang="ts">
import Vue from 'vue'
import NavList from "~/data/NavList";

export default Vue.extend({
  props: ["nav"],
  mixins: [NavList]
})
</script>