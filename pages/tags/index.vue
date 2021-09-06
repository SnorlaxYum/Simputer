<template lang="pug">
  article.tags
    header Tags
      feed-link(:link="atom")
    content
      ul
        li(v-for='tag_info, tag of tags')
          nuxt-link(:to="tag_info.slug") {{tag}}
          |           ({{tag_info.length}})
</template>

<script lang="ts">
import Vue from 'vue'
import FeedLink from "~/components/FeedLink"

export default Vue.extend({
  async asyncData({ params, error }) {
    let tags = await import("~/posts/tags.json").then(mod => mod.default)
    if (tags) {
      return tags
    } else {
      return error({ message: "Section not found", statusCode: 404 })
    }
  },
  components: {
    FeedLink
  },
  head() {
    return {
      title: "Tags",
      link: [{ rel: 'alternate', href: this.atom, type: 'application/atom+xml' }]
    }
  }
})
</script>