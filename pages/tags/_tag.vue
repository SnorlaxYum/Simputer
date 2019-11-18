<template lang="pug">
  div 
    post-nav(v-for='data of posts'
             :key='data[0]'
             :category='data[1].attributes.category'
             :title='data[1].attributes.title'
             :month='data[1].attributes.month'
             :day='data[1].attributes.day'
             :year='data[1].attributes.year'
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
import PostNav from '~/components/PostNav'
export default Vue.extend({
  asyncData({ params, error, store }) {
    let data = store.state.blog.tags.get(params.tag)
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
      title: this.title+" - Tags"
    }
  }
})
</script>