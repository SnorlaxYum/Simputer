<template lang="pug">
nav
  nuxt-link(to='/' :class="nav ? undefined : 'center-item'")
    .logo
  ul.site-navigation(v-if='nav')
    li(v-for='nav in InNavList')
      a(:href="'/' + nav.slug") {{nav.title}}
</template>
<script>
import NavList from "~/data/NavList";

export default {
  props: ["nav"],
  mixins: [NavList]
};
</script>