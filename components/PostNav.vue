<template lang="pug">
  article.main
    header
      nuxt-link(:to='link') {{title}}
    content(v-if='summary')
      p(v-html='summary')
      p.t-right
        nuxt-link(:to='link') Continue Reading
    content(v-else='' v-html='content')
    footer
      span
        time.published(:datetime="'Unix time:' + date") {{date_string_from_date(pub_date)}}
      span(v-if='modified')
        time.modified(:datetime="'Unix time:' + modified") {{date_string_from_date(mod_date)}}
      span
        nuxt-link(:to="link+'#isso-thread'" v-html="comment_count(isso)")
</template>
<script>
import FormatDate from "~/features/FormatDate";
import Slugify from "~/features/Slugify";
import DateParseVue from '../features/DateParse.vue';
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
  mixins: [FormatDate, Slugify, DateParseVue],
  computed: {
    link() {
      return [
        "",
        this.slugify_string(this.category),
        this.year,
        this.slugify_num(this.month + 1),
        this.slugify_num(this.day),
        this.slug,
        ""
      ].join("/");
    }
  },
  methods: {
    comment_count(newv) {
      if (newv) {
        return `${newv} comments`
      } else {
        return "Leave A Comment"
      }
    }
  }
};
</script>