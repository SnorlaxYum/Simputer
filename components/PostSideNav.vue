<template>
    <article class="post-side-nav" style="display:none">
        <h1>Table of Contents</h1>
        <ul>
          <nuxt-link v-for="link in links" :to="link.link" :key="link.link" :class="active && active.link == link.link ? 'nuxt-nav-active' : ''">
            <li>{{link.title}}</li>
          </nuxt-link>
        </ul>
      </article>
</template>

<script>
export default {
    data() {
        return {
            nav: false,
            links: [],
            active: null
        }
    },
  watch: {
    'html': 'contentUpdated',
    'nav': 'navUpdated'
  },
    mounted() {
        this.$nextTick(this.addListeners)
    },
    methods: {
    addListeners() {
      this.processTitles()
    },
    processTitles() {
      const titles = this.$el.parentElement.getElementsByTagName("h2")
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
    },
    navUpdated(newVal) {
        if(newVal) {
            console.log(newVal)
            this.$el.style.display = 'block'
            if(getComputedStyle(this.$el).position === 'sticky') {
                const navHeight = parseInt(getComputedStyle(this.$el.parentElement.parentElement.parentElement.previousElementSibling).height)
                this.$el.style.maxHeight = `${window.innerHeight-navHeight}px`
                this.$el.style.top = `${navHeight}px`
            } else {
                this.$el.style.top = '0'
            }
        } else {
            this.$el.style.display = 'none'
        }
    }
    },
  beforeDestroy() {
    this.destroyListeners()
  }
};
</script>