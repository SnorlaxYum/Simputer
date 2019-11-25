<template lang="pug">
article.page
    header {{title}}
    content
        #series
            p
                | This post is the index of &quot;
                b My Isso Style
                | &quot; Series.
            ol.parts
                li
                    nuxt-link(to='/terminal/2016/07/12/start-to-use-isso/') Installation
                li
                    nuxt-link(to='/terminal/2019/06/10/my-isso-configuration/') Configuration
                li
                    nuxt-link(to='/terminal/2019/06/10/inside-the-isso-database/') Inside the Database
        br
        | Welcome to My Isso Style!
        br
        | Hope the way I tango with Isso helps u!
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    data() {
        return {title: "My isso Style"}
    },
    head() {
        return {title: this.title}
    }
})
</script>