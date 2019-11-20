<template lang="pug">
article
  header Tags
  content
    ul
      li(v-for='tag of tags')
        nuxt-link(:to="['','tags',tag[0],''].join('/')") {{tag[1].title}}
        |           ({{tag[1].posts.size}})
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  asyncData({ params, error, store }) {
    let data = store.state.blog.tags
    if (data) {
      return { tags: data }
    } else {
      return error({ message: "Section not found", statusCode: 404 })
    }
  },
  head() {
    return {
      title: "Tags"
    }
  }
})
</script>