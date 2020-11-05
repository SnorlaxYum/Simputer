<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    head() {
        return {
            titleTemplate: '%s - ' + this.siteTitle,
            link: [
                {
                    rel: 'preconnect',
                    href: 'https://isso.snorl.ax'
                }
            ]
        }
    },
    data() {
        return {
            siteTitle: this.$store.state.siteTitle
        }
    }
})
</script>