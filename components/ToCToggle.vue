<template>
    <input type="checkbox" :checked="value" @change="changeValue">
</template>

<script>
const toggleImport = () => import("../features/styleSettings")
let ToCOnGet, ToCOnSet

export default {
    async beforeMount() {
        if(!ToCOnGet) {
            ToCOnGet = await toggleImport().then(({ToCOnGet}) => ToCOnGet)
        }
        this.value = ToCOnGet()
    },

    data() {
        return {value: true}
    },

    methods: {
        async changeValue(e) {
            if(!ToCOnSet) {
                ToCOnSet = await toggleImport().then(({ToCOnSet}) => ToCOnSet)
            }
            this.value = ToCOnSet(e)
        }
    },
};
</script>