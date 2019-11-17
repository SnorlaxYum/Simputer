<script>
export default {
    computed: {
        pub_date() {
            return this.format_date_from_unix(this.date)
        },
        mod_date() {
            return this.format_date_from_unix(this.modified)
        },
        month() {
            return this.pub_date.getMonth()
        },
        day() {
            return this.pub_date.getDate()
        },
        year() {
            return this.pub_date.getFullYear()
        },
    }
}
</script>