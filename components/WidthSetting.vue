<template>
    <input type="range" min="70" max="100" :value="width" @mouseup="changeWidth" @touchend="changeWidth">
</template>

<script>
const contentWidthImport = () => import("../features/widthSettingValue")
let contentWidthGet, contentWidthSet

export default {
    async beforeMount() {
        if(!contentWidthGet) {
            contentWidthGet = await contentWidthImport().then(({contentWidthGet}) => contentWidthGet)
        }
        
        this.width = contentWidthGet()
    },

    data() {
        return {width: 100}
    },

    computed: {
        async widthNow() {
            return this.width
        }
    },

    methods: {
        async changeWidth(e) {
            if(!contentWidthSet) {
                contentWidthSet = await contentWidthImport().then(({contentWidthSet}) => contentWidthSet)
            }
            this.width = contentWidthSet(e)
            this.$emit("change-width", this.width)
        }
    },
};
</script>