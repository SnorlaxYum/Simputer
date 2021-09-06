<template lang="pug">
  div 
    article.cat
      h1 Tag: {{ name }}
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
<script lang="ts">
import Vue from 'vue'
import GetIssoCount from "~/features/GetIssoCount"
import PostNav from '~/components/PostNav'

export default Vue.extend({
  async asyncData({ params, error }) {
    let data = await import(`~/posts/tags/${params.tag}.json`).then(mod => mod.default)
    if (data) {
      return data
    } else {
      return error({ message: "Section not found", statusCode: 404 })
    }
  },
  components: {
      PostNav
  },
  mixins: [GetIssoCount],
  head() {
    return {
      title: this.name+" - Tags"
    }
  }
})
</script>