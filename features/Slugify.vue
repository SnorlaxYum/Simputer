<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  methods: {
    slugify_num(num) {
      return Number(num) > 9 ? Number(num) : "0" + num;
    }
  }
});
</script>