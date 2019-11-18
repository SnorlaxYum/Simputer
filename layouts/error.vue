<template lang="pug">
  article
    header Error {{error.statusCode}} 
    content {{error.message}}
      br
      p
        a(href="/") Click to go back home
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: ["error"],
  head() {
    return {
      title: `Error ${this.error.statusCode}`
    }
  },
  layout: 'errortemp'
})
</script>