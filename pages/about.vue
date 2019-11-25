<template lang="pug">
article.page
  header About Me
  content
    client-only
      table
        tr
          td Name
          td Sim
        tr
          td Languages
          td Html, CSS, Javascript, Python, Shell Script
        tr
          td Tools
          td Visual Studio Code, Gimp, Vim
        tr
          td System
          td
            | On my laptop, Arch Linux is my day-to-day system, Windows 10 is there in case that I need it (which is rare). Debian is my server system.
        tr
          td Status
          td
            | Recently I&apos;m learning the interesting framework, Nuxt.js, which is basically the SSR version of Vue.js. Well, it&apos;s made for web development.
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  head() {
    return {
      title: "About Me"
    }
  }
})
</script>