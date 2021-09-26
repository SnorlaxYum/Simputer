<template lang="pug">
    div.site-container(ref="container")
        slot
</template>

<script>
const contentWidthImport = () => import("../features/styleSettings")
let contentWidthGet

export default {
    async beforeMount() {
        if(!contentWidthGet) {
            contentWidthGet = await contentWidthImport().then(({contentWidthGet}) => contentWidthGet)
        }
        
        this.changeWidth(contentWidthGet())
    },
    methods: {
        changeWidth(e) {
            if(e == 100) {
                this.$refs.container.style.width = ``
            } else {
                this.$refs.container.style.width = `${e}%`
            }
        }
    },
};
</script>