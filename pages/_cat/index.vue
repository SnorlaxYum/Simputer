<template lang="pug">
div
  article.cat
    h1 {{ name }}
      feed-link(:link="atom")
  post-nav(v-for='post of posts'
            :key='post.slug'
            :category='post.category'
            :title='post.title'
            :date='post.date'
            :modified='post.modified'
            :slug='post.slug'
            :content='post.summary ? false : post.html'
            :summary='post.summary ? post.summary : false'
            :isso='post.isso')
</template>
<script>
import GetIssoCount from "~/features/GetIssoCount"
import PostNav from "~/components/PostNav"
import FeedLink from "~/components/FeedLink"

export default {
  async asyncData({ params, error }) {
    let data = await import(`~/posts/${params.cat}.json`).then(mod => mod.default)
    return data || error({ message: "Section not found", statusCode: 404 })
  },
  mixins: [GetIssoCount],
  components: {
    PostNav,
    FeedLink
  },
  head() {
    return {
      title: this.name,
      link: [{ rel: 'alternate', href: this.atom, type: 'application/atom+xml' }]
    }
  }
}
</script>