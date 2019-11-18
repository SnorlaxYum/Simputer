<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import Slugify from "~/features/Slugify"
export default Vue.extend({
  mixins: [Slugify],
  methods: {
    async query_comment_numbers() {
      let slugs = []
      for (const data of this.posts) {
        slugs.push(this.link(data[1], data[0]))
      }
      try {
        const counts = await axios.post(
          `${this.$store.state.isso}count`,
          slugs
        )
        let index = 0
        for (let post of this.posts) {
          this.$set(this.posts.get(post[0]), "isso", counts.data[index++])
        }
        this.$forceUpdate()
      } catch (e) {
        console.log(e)
      }
    },
    link(link, slug) {
      let linkdate = new Date(link.attributes.date)
      return [
        "",
        this.slugify_string(link.attributes.category),
        linkdate.getFullYear(),
        this.slugify_num(linkdate.getMonth() + 1),
        this.slugify_num(linkdate.getDate()),
        slug,
        ""
      ].join("/")
    }
  },
  mounted() {
    this.$nextTick(this.query_comment_numbers)
  }
})
</script>