<template lang="pug">
  div
    div.post-flex
      transition(name="fade")
        article.post-nav(v-if="nav")
          h1 Table of Contents
          ul
            nuxt-link(v-for="link in links" :to="link.link" :key="link.link" :class="active && active.link == link.link ? 'nuxt-nav-active' : ''")
              li(v-html="link.title")
      post(
        :title="title"
        :date="date"
        :modified="modified"
        :tags="tags"
        :content="html"
      )
    client-only
      isso(:title="title" :slug="slug")
</template>

<script lang="ts">
import Vue from 'vue'
import Post from "~/components/Post"
import Isso from '~/components/Isso'
export default Vue.extend({
  async asyncData({ params, error, route, $axios }) {
    let target = await $axios.get(`/${params.cat}/${params.slug}.json`).then(res => res.data)
    if (
      target &&
      target.slug === route.path
    ) {
      target['modified'] = target['modified'] ? target['modified'] : false
      return target
    } else {
      return error({ message: "Page not found", statusCode: 404 })
    }
  },
  data() {
    return {
      nav: false,
      links: [],
      active: null,
      slug: this.$route.fullPath
    }
  },
  head() {
    const siteTitle = this.$store.state.siteTitle,
    description = this.summary ? this.summary.replace('<br>', ' ') : '',
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
        let height = 50
        if (getComputedStyle(document.getElementsByTagName('nav')[0]).position === "sticky") {
          let navHeight = document.getElementsByTagName('nav')[0].clientHeight
          if (Math.abs(dis - navHeight) <= height) {
            this.active = link
          }
        } else if (Math.abs(dis) <= height) {
          this.active = link
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
    if (this.$route.hash.search('#isso-')+1) {
      setTimeout(() => {
        scrollTo({top: document.getElementById(this.$route.hash.replace('#', '')).offsetTop, behavior: 'smooth'})
      }, 1)
    }
  },
  beforeDestroy() {
    this.destroyListeners()
  }
})
</script>