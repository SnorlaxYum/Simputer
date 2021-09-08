<template>
<div>
  <div class="post-flex">
    <transition name="fade">
      <post-side-nav :links="links" />
    </transition>
    <post :title="title" :date="date" :modified="modified" :tags="tags">
      <slot></slot>
    </post>
  </div>
  <client-only>
    <isso :title="title" :slug="slug"></isso>
  </client-only>
</div>
</template>

<script>
const Post = () => import("~/components/Post")
const Isso = () => import('~/components/Isso')
const PostSideNav = () => import("~/components/PostSideNav")
export default {
  props: ['title', 'date', 'modified', 'slug', 'tags', 'summary', 'ogimage', 'category', 'links'],
  head() {
    const siteTitle = this.$store.state.siteTitle,
    description = this.summary ? this.summary.replace('<br>', ' ') : '',
    siteUrl = this.$store.state.siteUrl,
    thisUrl = siteUrl + this.$route.fullPath
    let image_path = this.ogimage
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
  components: {
    Post,
    Isso,
    PostSideNav
  }
}
</script>