<template lang="pug">
  div
    div
      transition(name="fade")
        article.post-nav(v-if="nav")
          h1 Table of Contents
          ul
            nuxt-link(v-for="link in links" :to="link.link" :key="link.link")
              li(v-html="link.title")
      post(
        :title="title"
        :date="date"
        :modified="modified"
        :tags="tags"
        :content="html"
      )
    client-only
      isso(:title="title" :slug="link")
</template>

<script lang="ts">
import Vue from 'vue'
import Post from "~/components/Post"
import Isso from '~/components/Isso'
import SlugifyVue from '../../../../../features/Slugify.vue'
import DateParseVue from '../../../../../features/DateParse.vue'
import FormatDateVue from '../../../../../features/FormatDate.vue'
import ThisSlugVue from '../../../../../features/ThisSlug.vue'
export default Vue.extend({
  async asyncData({ params, error, $axios }) {
    let target = await $axios.get(`/${params.cat}/${params.slug}.json`).then(res => res.data)
    if (
      target &&
      params.cat === target["category_slug"]
    ) {
      target['modified'] = false
      return target
    } else {
      return error({ message: "Page not found", statusCode: 404 })
    }
  },
  data() {
    return {
      nav: false,
      links: [],
      slug: this.$route.fullPath
    }
  },
  head() {
    const siteTitle = this.$store.state.siteTitle,
    description = this.summary.replace('<br>', ' '),
    siteUrl = this.$store.state.siteUrl,
    thisUrl = siteUrl + this.$route.fullPath
    let image_path = this.ogimage ? this.ogimage : '/images/og/default.webp'
    image_path = siteUrl + image_path
    return {
      title: `${this.title} - ${this.category}`,
      meta: [
        { hid: 'keywords', name: 'keywords', content: this.tags.join(",") },
        { hid: 'og:title', property: 'og:title', content: `${this.title} - ${this.category} - ${siteTitle}` },
        { hid: 'og:description', property: 'og:description', content: description },
        { hid: 'og:image', property: 'og:image', content: image_path },
        { hid: 'og:url', property: 'og:url', content: thisUrl },
        { hid: 'twitter:card', name: 'twitter:card', content: "summary_large_image" }
      ]
    }
  },
  mixins: [FormatDateVue,DateParseVue,SlugifyVue,ThisSlugVue],
  watch: {
    'html': 'contentUpdated'
  },
  components: {
    Post,
    Isso
  },
  methods: {
    addListeners() {
      this.processTitles()
    },
    processTitles() {
      // console.log(this.$el)
      const titles = this.$el.getElementsByTagName("h2")
      if (titles.length > 0) {
        for (const title of titles) {
          this.links.push({link: `#${title.id}`, title: `${title.innerHTML}`})
        }
        this.nav = true
        // add a listenner to this.$router.push on the position when it's there
        document.addEventListener('scroll', this.addActive)
      }
    },
    addActive(event) {
      for (const link of this.links) {
        const dis = document.getElementById(link.link.replace('#','')).getBoundingClientRect().top
        let already = this.$route.hash === link.link, height = 50
        if (getComputedStyle(document.getElementsByTagName('nav')[0]).position === "sticky") {
          height = document.getElementsByTagName('nav')[0].clientHeight * 0.8
        }
        if (Math.abs(dis) <= height && !already) {
          this.$router.push(link.link)
        }
      }
      // const body = document.body,
      // bottom_title = this.links[this.links.length-1],
      // bottom_title_current = this.$route.fullPath.search(bottom_title.link),
      // isso_current = this.$route.fullPath.search('#isso-thread')
      // if (window.pageYOffset + window.innerHeight >= body.offsetHeight && !(bottom_title_current+1) && !(isso_current)) {
      //   this.$router.push(bottom_title.link)
      // } 
    },
    destroyListeners() {
      if (this.links.length) {
        this.nav = false
        // destroy the listener
        document.removeEventListener('scroll', this.addActive)
      }  
    },
    contentUpdated() {
      this.destroyListeners()
      this.$nextTick(() => {
        this.addListeners()
      })
    }
  },
  mounted() {
    this.$nextTick(this.addListeners)
  },
  beforeDestroy() {
    this.destroyListeners()
  }
})
</script>