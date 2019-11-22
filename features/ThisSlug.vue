<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  computed: {
    link() {
      this.catslug =
        typeof this.catslug == "string" ? this.catslug : this.category_slug;
      return [
        "",
        this.catslug,
        this.year,
        this.slugify_num(this.month + 1),
        this.slugify_num(this.day),
        this.slug,
        ""
      ].join("/");
    }
  }
});
</script>