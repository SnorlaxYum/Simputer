<template lang="pug">
div
  article.cat
    h1 {{isTag ? `Tag: ${name}` : name}}
      div.f-right
        tags-link(:link="tags")
        feed-link(:link="atom" v-if="!isTag")
  post-nav(v-for='post of posts'
            :key='post.slug'
            :category='post.category'
            :title='post.title'
            :date='post.date'
            :modified='post.modified'
            :slug='post.slug'
            :content='post.summary ? false : post.html'
            :summary='post.summary || false'
            :isso='post.isso')
</template>
<script>
const PostNav = () => import("~/components/PostNav");
const FeedLink = () => import("~/components/FeedLink");
const TagsLink = () => import("~/components/TagsLink")

export default {
  props: ["name", "atom", "posts", "isTag", "tags"],
  components: {
    PostNav,
    FeedLink,
    TagsLink
  },
  head() {
    if(this.isTag) {
      return {title: this.name+" - Tags"}
    }
    return {
      title: this.name,
      link: [
        { rel: "alternate", href: this.atom, type: "application/atom+xml" }
      ]
    }
  },
  methods: {
    async query_comment_numbers() {
      let slugs = []
      for (const data of this.posts) {
        slugs.push(data.slug)
      }
      // console.log(slugs)
      try {
        const counts = await this.$axios.post(
          `${this.$store.state.isso}count`,
          slugs
        )
        for (let post_index in this.posts) {
          this.$set(this.posts[post_index], "isso", counts.data[post_index])
        }
        // this.$forceUpdate()
      } catch (e) {
        console.log(e)
      }
    }
  },
  mounted() {
    this.$nextTick(this.query_comment_numbers)
  }
};
</script>