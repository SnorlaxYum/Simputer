<template lang="pug">
article.page
  header About Me
  content
    client-only
      table
        tr
          td Name
          td Sim
        tr
          td Languages
          td Html, CSS, Javascript, Golang, Python, Shell Script, etc
        tr
          td(rowspan="2") Site Style Setting
          td Width: 
            WidthSettingButton(@change-width="changeWidth")
        tr
          td Table of Content Shown: 
            toc-toggle
</template>

<script>
import WidthSettingButton from '../components/WidthSetting.vue'
import TocToggle from '../components/ToCToggle.vue'

export default {
  head() {
    return {
      title: "About Me"
    }
  },
  components: {
    WidthSettingButton,
    TocToggle
  },
  methods: {
    changeWidth(e) {
      this.$parent.$parent.$emit('change-width', e);
    }
  }
}
</script>