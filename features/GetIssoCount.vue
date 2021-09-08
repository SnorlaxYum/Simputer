<script>
export default {
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
}
</script>