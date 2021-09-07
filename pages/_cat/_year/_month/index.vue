<template lang="pug">
div
  article.cat
    h1 {{ name }} ({{period}})
      feed-link(:link="atom")
  post-nav(v-for='post, title of posts'
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

<script lang="ts">
import Vue from 'vue'
import GetIssoCount from "~/features/GetIssoCount"
import PostNav from "~/components/PostNav"
import FeedLink from "~/components/FeedLink"

export default Vue.extend({
  async asyncData({ params, error }) {
    const {year, month, cat} = params
    let data = await import(`~/posts/${cat}.json`).then(mod => mod.default)
    if (data) {
      data.posts = data.posts.filter(post => {
        const date = new Date(post.date)
        return date.getFullYear() === Number(year) && date.getMonth()+1 === Number(month)
      })
      return {...data, period: new Date(year, month - 1).toLocaleString('en-US', {month: 'long', year: 'numeric'})}
    } else {
      return error({ message: "Section not found", statusCode: 404 })
    }
  },
  mixins: [GetIssoCount],
  components: {
    PostNav,
    FeedLink
  },
  head() {
    return {
      title: this.title,
      link: [{ rel: 'alternate', href: this.atom, type: 'application/atom+xml' }]
    }
  }
})
</script>