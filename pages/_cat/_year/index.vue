<template lang="pug">
div
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
export default Vue.extend({
  async asyncData({ params, error, $axios }) {
    let data = await $axios.get(`/${params.cat}.json`).then(res => res.data)
    if (data) {
      let data_this = {...data}
      data_this.posts = [...data_this.posts]
      // console.log(data_this.posts)
      for (let i = data_this.posts.length - 1; i >= 0; i--) {
        let post = data_this.posts[i], post_date = new Date(post.date)
        if (post_date.getFullYear() !== Number(params.year)) {
          // console.log(post_date.getFullYear(), params.year)
          data_this.posts.splice(i, 1)
        }
      }
      return data_this
    } else {
      return error({ message: "Section not found", statusCode: 404 })
    }
  },
  mixins: [GetIssoCount],
  components: {
    PostNav
  },
  head() {
    return {
      title: this.name
    }
  }
})
</script>