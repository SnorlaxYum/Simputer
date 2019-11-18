const slugify = require('uslug')
export const state = () => ({
    category: {
        all: {title: "Homepage"}
    },
})
export const getters = ({
    slugify: (state) => (title) => {
        return slugify(title)
    }
})
export const mutations = {
    set_posts(state) {
        state.tags = new Map()
        const path = require('path')
        const posts = require.context('~/contents/', true, /\.md$/)
        let post_list = {}
        post_list["all"] = new Map()
        let pre_posts = posts.keys()
        // sort the posts by date before processing them
        function compare_date(a, b) {
            const date_a = Date.parse(posts(a).attributes.date)
            const date_b = Date.parse(posts(b).attributes.date)
            return date_a - date_b
        }
        pre_posts.sort(compare_date)
        pre_posts.forEach(post => {
            // the converted html
            const data = posts(post)
            // the path
            const path_this = path.join('~/contents/', post)
            data.path = path_this
            const path_array = path_this.split('/')
            // the category
            let cat = ""
            if (path_array[path_array.length - 2] !== 'contents') {
                cat = path_array[path_array.length - 2]
            }
            if (!cat && data.attributes.category) {
                cat = data.attributes.category
            }
            // get the slug depending on whether the attribute exists
            let slug = data.attributes.slug ? data.attributes.slug : slugify(data.attributes.title) 
            // deal with the slug duplicate situation in the same category
            let seq = 0
            while (post_list["all"].get(slug)) {
                if (post_list["all"].get(slug + '-' + seq)) {
                    seq = seq + 1
                } else {
                    slug = slug + '-' + seq
                }
            }
            // the tags
            let tags = []
            if (data.attributes.tags && typeof(data.attributes.tags) === "string") {
                tags = data.attributes.tags.split(",")
                for (let i in tags) {
                    tags[i] = tags[i].replace(/^\s\s*/, '').replace(/\s\s*$/, '')
                    const tag_slug = slugify(tags[i])
                    // maek sure if the tag exists
                    if (!state.tags.get(tag_slug)) {
                        state.tags.set(tag_slug, {title: tags[i]})
                        state.tags.get(tag_slug).posts = new Map()
                    }
                    // push the data to the tag list
                    state.tags.get(tag_slug).posts.set(slug, data)
                }
            }
            else if (data.attributes.tags && typeof(data.attributes.tags) === "object") {
                tags = data.attributes.tags
                // console.log(tags)
                for (let i in tags) {
                    const tag_slug = slugify(tags[i])
                    // maek sure if the tag exists
                    if (!state.tags.get(tag_slug)) {
                        state.tags.set(tag_slug, {title: tags[i]})
                        state.tags.get(tag_slug).posts = new Map()
                    }
                    // push the data to the tag list
                    state.tags.get(tag_slug).posts.set(slug, data)
                }
            }
            // create a key pairs for the category, using the Map Object in order to order it afterwards
            if (!post_list[cat]) {
                post_list[cat] = new Map()
            }
            // set properties on the post
            if (!data.attributes.category) {
                data.attributes.category = cat
            }
            if (data.attributes.published === undefined) {
                data.attributes.published = true
            }
            data.attributes.tags = tags
            // push the data to the cat list
            if (cat) {
                post_list[cat].set(slug, data)
            }
            post_list["all"].set(slug, data)
        })
        // create a reference in the coresponding category object to the post list
        for (var key in post_list) {
            // sort the Map before saving it to the state, comment it you want to show older posts on the top
            post_list[key][Symbol.iterator] = function * () {
                yield * [...this.entries()].sort((a, b) => new Date(b[1].attributes.date) - new Date(a[1].attributes.date))
            }
            const key_slug = key.toLowerCase()
            if (!state.category[key_slug]) {
               state.category[key_slug] = {title: key, slug: key_slug, description: ''}
            }
            // saving it to state
            state.category[key_slug].posts = post_list[key]
        }
        // sort the tags
        state.tags[Symbol.iterator] = function * () {
            yield * [...this.entries()].sort((a, b) => b[1].posts.size - a[1].posts.size)
        }
        for (let pairs of state.tags) {
            pairs[1].posts[Symbol.iterator] = function * () {
                yield * [...this.entries()].sort((a, b) => new Date(b[1].attributes.date) - new Date(a[1].attributes.date))
            }
            // state.tags.get(key).posts = [...state.tags.get(key).posts]
        }

        // remove the unpublished posts from tags and categories
        // If not added the unpublished from the start, then once it goes from unpublished to published, the slug of the posts with the same slug can change.......
        for (let post of state.category['all'].posts) {
            const cat = slugify(post[1].attributes.category)
            let tags = post[1].attributes.tags.slice()
            for (let tag_index in tags) {
                tags[tag_index] = slugify(tags[tag_index])
            }
            if (!post[1].attributes.published) {
            // remove from category
            state.category['all'].posts.delete(post[0])
            state.category[cat].posts.delete(post[0])
            // remove from tags
            for (let tag of tags) {
                state.tags.get(tag).posts.delete(post[0])
            }
        }
        }
        // remove the empty tags
        for (let tag of state.tags) {
            if (tag[1].posts.size === 0) {
                state.tags.delete(tag[0])
            }
        }
        // iteration for generation value in nuxt.config.js
        // let slugs = [], date = {}
        // for (let cat of Object.keys(state.category)) {
        //     if (cat !== "all") {
        //         slugs.push(`/${cat}`)
        //     }
        // }
        // for (let tag of state.tags) {
        //     slugs.push(`/tags/${tag[0]}`)
        // }
        // for (let post of state.category['all'].posts) {
        //     let cat = slugify(post[1].attributes.category),
        //     date = new Date(post[1].attributes.date),
        //     year = date.getFullYear(), 
        //     month = (date.getMonth()+1) > 9 ? date.getMonth()+1 : '0'+(date.getMonth()+1),
        //     day = date.getDate() > 9 ? date.getDate() : '0'+date.getDate(),
        //     slug = post[0]
        //     if (!date[year]) {
        //         date[year] = {}
        //         slugs.push(`/${cat}/${year}`)
        //     }
        //     if (!date[year][month]) {
        //         date[year][month] = {}
        //         slugs.push(`/${cat}/${year}/${month}`)
        //     }
        //     if (!date[year][month][day]) {
        //         date[year][month][day] = true
        //         slugs.push(`/${cat}/${year}/${month}/${day}`)
        //     }
        //     slugs.push(`/${cat}/${year}/${month}/${day}/${slug}`)
        // }
        // console.dir(slugs, {'maxArrayLength': null})
    }
}