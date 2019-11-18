<template lang="pug">
  article.main
    header(v-html='title')
    content(v-html='content')
    footer
      span
        time.published(:datetime="'Unix time:' + date") {{date_string_from_date(pub_date)}}
      span(v-if='modified')
        time.modified(:datetime="'Unix time:' + modified") {{date_string_from_date(mod_date)}}
      span.tag-list
        span(:class="tags.indexOf(tag) == 0 ? 'tag' : 'tag seq-tag'" v-for='tag in tags' :key='tag')
          nuxt-link(:to="['', 'tags', slugify_string(tag), ''].join('/')") {{ tag }}
</template>

<script lang="ts">
import Vue from 'vue'
import FormatDate from "~/features/FormatDate"
import Slugify from "~/features/Slugify"
import DateParseVue from '../features/DateParse.vue'
export default Vue.extend({
  props: [
    "title",
    "date",
    "modified",
    "content",
    "tags"
  ],
  mixins: [FormatDate, Slugify, DateParseVue],
  watch: {'content': 'contentUpdated'},
  methods: {
    navigate(event) {
      let target = event.target
      let i = 0

      // go through 5 parents max to find a tag
      while (i < 5 && !(target instanceof HTMLAnchorElement) && target.parentNode) {
        target = target.parentNode
        i++
      }

      // ignore if no link found
      if (!(target instanceof HTMLAnchorElement)) { return }

      const href = target.getAttribute('href')

      // use router to push it if it's on this site
      if (href && !(href.indexOf("png")+1) && !(href.indexOf("webp")+1) && href[0] === '/' || href[0] === '#') {
        event.preventDefault()
        this.$router.push(href)
      } else {
        event.preventDefault()
        window.open(href, '_blank')
      }
    },
    addListeners() {
      this._links = this.$el.getElementsByTagName('a')
      for (let link of this._links) {
        link.addEventListener('click', this.navigate)
      }
    },
    removeListeners() {
      for (let link of this._links) {
        link.removeEventListener('click', this.navigate)
      }
    },
    contentUpdated() {
      this.removeListeners()
      this.$nextTick(()=>{
        this.addListeners()
      })
    }
  },
  mounted() {
    this.addListeners()
  },
  beforeDestroy() {
    this.removeListeners()
  }
})
</script>