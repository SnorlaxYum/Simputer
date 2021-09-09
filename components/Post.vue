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
  }
}
</script>