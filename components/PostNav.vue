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
        time.published {{date}}
      span(v-if='modified')
        time.modified {{modified}}
      span
        nuxt-link(:to="slug+'#isso-thread'") {{comment_count(isso)}}
</template>

<script>
export default {
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
    },
    displaySet() {
      let this_offset = this.$el.getBoundingClientRect().top, window_height = window.innerHeight, classlist = this.$el.classlist
      if (this_offset <= window_height) {
        this.$el.style.height = "auto"
        this.$el.style.opacity = "1"
      } else {
        this.$el.style.opacity = "0"
        this.$el.style.height = "0"
      }
    },
    checkDisplay(event) {
      this.displaySet()
    },
    addEventListener() {
      document.addEventListener('scroll', this.checkDisplay)
    },
    removeEventListener() {
      document.removeEventListener('scroll', this.checkDisplay)
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.displaySet()
      this.addEventListener()
    })
  },
  beforeDestroy() {
    this.removeEventListener()
  }
}
</script>