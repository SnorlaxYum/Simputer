export const state = () => ({
    siteTitle: 'Simputer',
    siteUrl: 'https://snorl.ax',
    isso: 'https://isso.snorl.ax/'
})

export const actions = {
    nuxtServerInit({commit}) {
        commit('blog/set_posts')
    }
}