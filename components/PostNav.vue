<template lang="pug">
  article.main
    header
      nuxt-link(:to='slug') {{title}}
    content(v-if='summary')
      p(v-html='summary')
      p.t-right
        nuxt-link(:to='slug') Continue Reading
    content(v-else v-html='content')
    footer
      span
        time.published(v-html="date")
      span(v-if='modified')
        time.modified(v-html="modified")
      span
        nuxt-link(:to="slug+'#isso-thread'" v-html="comment_count(isso)")
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: [
    "title",
    "date",
    "modified",
    "content",
    "category",
    "slug",
    "summary",
    "isso"
  ],
  methods: {
    comment_count(newv) {
      if (newv) {
        return `${newv} comments`
      } else {
        return "Leave A Comment"
      }
    }
  }
})
</script>