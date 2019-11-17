<script>
export default {
    head() {
        return {
        titleTemplate: '%s - ' + this.siteTitle
        }
    },
    data() {
        return {
            siteTitle: this.$store.state.siteTitle
        }
    }
}
</script>