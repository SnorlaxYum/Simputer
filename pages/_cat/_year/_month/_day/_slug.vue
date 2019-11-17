<template lang="pug">
client-only
  div
    div
      transition(name="fade")
        article.post-nav(v-if="nav")
          h1 Table of Contents
          ul
            nuxt-link(v-for="link in links" :to="link.link" :key="link.link")
              li(v-html="link.title")
      post(
        :title="attributes.title"
        :date="attributes.date"
        :modified="attributes.modified"
        :tags="attributes.tags"
        :content="html"
      )
      
    isso(:title="attributes.title" :slug="slug")
</template>

<script>
import url from 'url';
import Post from "~/components/Post";
import Isso from '~/components/Isso';
export default {
  asyncData({ params, error, store }) {
    const target = store.state.blog.category["all"].posts.get(
      params.slug
    );
    if (
      target &&
      target.attributes.published &&
      params.cat === store.getters['blog/slugify'](target.attributes.category)
    ) {
      return target;
    } else {
      return error({ message: "Page not found", statusCode: 404 });
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
    description = this.attributes.summary.replace('<br>', ' '),
    siteUrl = this.$store.state.siteUrl,
    thisUrl = url.resolve(siteUrl, this.$route.fullPath)
    let image_path = this.attributes.ogimage ? this.attributes.ogimage : '/images/og/default.webp'
    image_path = url.resolve(siteUrl, image_path)
    return {
      title: `${this.attributes.title} - ${this.attributes.category}`,
      meta: [
        { hid: 'keywords', name: 'keywords', content: this.attributes.tags.join(",") },
        { hid: 'og:title', property: 'og:title', content: `${this.attributes.title} - ${this.attributes.category} - ${siteTitle}` },
        { hid: 'og:description', property: 'og:description', content: description },
        { hid: 'og:image', property: 'og:image', content: image_path },
        { hid: 'og:url', property: 'og:url', content: thisUrl },
        { hid: 'twitter:card', name: 'twitter:card', content: "summary_large_image" }
      ]
    };
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
      const body = document.body,
      bottom_title = this.links[this.links.length-1],
      bottom_title_current = this.$route.fullPath.search(bottom_title.link),
      isso_current = this.$route.fullPath.search('#isso-thread')
      if (window.pageYOffset + window.innerHeight >= body.offsetHeight && !(bottom_title_current+1) && !(isso_current)) {
        this.$router.push(bottom_title.link)
      } 
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
};
</script>