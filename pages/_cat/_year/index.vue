<template lang="pug">
div
  post-nav(v-for='data of posts'
           :key='data[0]'
           :category='data[1].attributes.category'
           :title='data[1].attributes.title'
           :date='data[1].attributes.date'
           :modified='data[1].attributes.modified'
           :slug='data[0]'
           :content='data[1].attributes.summary ? false : data[1].html'
           :summary='data[1].attributes.summary ? data[1].attributes.summary : false'
           :isso='data[1].isso')
</template>
<script lang="ts">
import Vue from 'vue'
import GetIssoCount from "~/features/GetIssoCount"
import PostNav from "~/components/PostNav"
export default Vue.extend({
  asyncData({ params, error, store }) {
    let data = store.state.blog.category[params.cat], data_this
    if (data) {
      data_this = {...data}
      data_this.posts = new Map(data_this.posts)
      for (let post of data_this.posts) {
        let post_date = new Date(post[1].attributes.date)
        if (post_date.getFullYear() !== Number(params.year)) {
          // console.log(post_date.getFullYear(), params.year)
          data_this.posts.delete(post[0])
        }
      }
      // console.log(data_this.posts)
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
      title: this.title
    }
  }
})
</script>