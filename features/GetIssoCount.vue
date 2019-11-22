<script lang="ts">
import Vue from 'vue'
import Slugify from "~/features/Slugify"
export default Vue.extend({
  mixins: [Slugify],
  methods: {
    async query_comment_numbers() {
      let slugs = []
      for (const data of this.posts) {
        slugs.push(this.get_link(data))
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
    },
    get_link(link) {
      let linkdate = new Date(link.date)
      return [
        "",
        link['category_slug'],
        linkdate.getFullYear(),
        this.slugify_num(linkdate.getMonth() + 1),
        this.slugify_num(linkdate.getDate()),
        link.slug,
        ""
      ].join("/")
    }
  },
  mounted() {
    this.$nextTick(this.query_comment_numbers)
  }
})
</script>