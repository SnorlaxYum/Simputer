<script>
export default {
    methods: {
        format_date_from_unix(unix) {
            return new Date(unix)
        },
        date_string_from_date(date) {
            const month_list = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ]
            return month_list[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear()
        }
    }
}
</script>