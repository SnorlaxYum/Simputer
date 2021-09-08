<template lang="pug">
div.nav-box-list
  content(v-if='InSite')
    nuxt-link(v-for='nav in NavList' :key='nav.slug' :to="'/' + nav.slug")
      div(:class="'nav-box ' + nav.slug")
        div(:class='nav.textcontainer' @mouseenter='showInfo(nav)' @mouseleave='showName(nav)')
          span(:id='nav.slug') {{ nav.title }}
  content(v-else)
    a(v-for='nav in NavList' :key='nav.id' :href='nav.link' target='_blank')
      div(:class="'nav-box '+ nav.id")
        div(:class='nav.textcontainer' @mouseenter='showInfo(nav)' @mouseleave='showName(nav)')
          span(:id='nav.id ? nav.id : nav.slug') {{ nav.title }}
</template>

<script>
export default {
  props: ["InSite", "NavList"],
  methods: {
    showInfo(page) {
      let elem = ""
      if (page.id) {
        elem = document.getElementById(page.id)
      } else {
        elem = document.getElementById(page.slug)
      }
      elem.innerHTML = page.description
    },
    showName(page) {
      if (page.id) {
        document.getElementById(page.id).innerHTML = page.title
      } else {
        document.getElementById(page.slug).innerHTML = page.title
      }
    }
  }
}
</script>