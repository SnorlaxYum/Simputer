<template lang="pug">
  article
    header Tags
    content
      ul
        li(v-for='tag_info, tag of tags')
          nuxt-link(:to="tag_info.slug") {{tag}}
          |           ({{tag_info.length}})
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  async asyncData({ params, error, $axios }) {
    let tags = await $axios.get("/tags.json").then(res => res.data)
    if (tags) {
      return { tags }
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