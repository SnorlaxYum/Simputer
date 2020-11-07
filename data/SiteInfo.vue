<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    head() {
        return {
            titleTemplate: '%s - ' + this.siteTitle,
        }
    },
    data() {
        return {
            siteTitle: this.$store.state.siteTitle
        }
    }
})
</script>