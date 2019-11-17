<script>
export default {
    methods: {
        slugify_num(num) {
            return Number(num) > 9 ? Number(num) : '0' + num
        },
        slugify_string(str) {
            return this.$store.getters['blog/slugify'](str)
        }
    }
}
</script>