<template lang="pug">
  article.main
    header {{title}}
    content
      div
        slot
    footer
      span
        time.published {{date}}
      span(v-if='modified')
        time.modified {{modified}}
      span.tag-list
        span(:class="tags.indexOf(tag) == 0 ? 'tag' : 'tag seq-tag'" v-for='tag in tags' :key='tag[1]')
          nuxt-link(:to="tag[1]") {{ tag[0] }}
</template>

<script lang="ts">
export default {
  props: {  
    title: {
      type: String
    },
    date: {
      type: String
    },
    modified: {
      type: [String, Boolean],
      required: false,
      default: ''
    },
    content: {
      type: String
    },
    tags: {
      type: Array
    }
  },
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
}
</script>