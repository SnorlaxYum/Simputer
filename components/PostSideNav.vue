<template>
    <article class="post-side-nav" style="display:none">
        <h1>Table of Contents</h1>
        <ul>
          <nuxt-link v-for="link in links" :level="link.level" :to="link.link" :key="link.link" :class="active && active.link == link.link ? 'nuxt-nav-active' : ''">
            <li>{{link.title}}</li>
          </nuxt-link>
        </ul>
      </article>
</template>

<script>
export default {
    props: ["links"],
    data() {
        return {
            nav: false,
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
      if (this.links.length > 0) {
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