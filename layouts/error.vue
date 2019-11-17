<template lang="pug">
  article
    header Error {{error.statusCode}} 
    content {{error.message}}
      br
      p
        a(href="/") Click to go back home
</template>


<script>
export default {
  props: ["error"],
  head() {
    return {
      title: `Error ${this.error.statusCode}`
    }
  },
  layout: 'errortemp'
};
</script>