<template lang="pug">
div.comment(:id="'isso-'+id")
  div.avatar
    svg(class="author" viewBox="0 0 64 64" v-if="author === 'Sim'")
      path(d="M 28.119602,63.687325 C 15.444107,62.092566 4.681433,52.836864 1.2957829,40.619334 0.11804536,36.369328 -0.185297,32.047578 0.40669427,27.952396 0.69034349,25.990213 1.3169968,23.254213 1.7992571,21.872396 2.6221506,19.514564 2.6782584,19.005642 2.7112744,13.6 2.7417236,8.6146227 2.8453445,7.4957232 3.4817866,5.28 3.8862189,3.872 4.4899277,2.438339 4.8233613,2.0940868 5.3919661,1.5070331 5.5924787,1.4919128 8.0530368,1.8505427 9.7650208,2.1000669 11.519265,2.6284115 13.102298,3.3712832 l 2.425829,1.1383715 2.810077,-1.3168464 C 23.004118,1.006287 26.530877,0.24542803 32,0.24542803 c 3.972189,0 5.097274,0.11994026 7.817158,0.83335317 1.747437,0.4583443 4.51401,1.4836929 6.147936,2.2785526 l 2.970781,1.4451993 1.852061,-0.9325504 C 53.049917,2.7310315 55.417488,2.017684 57.848464,1.7426501 60.108198,1.4869906 60.493357,1.8249348 61.332982,4.8 c 0.483114,1.7118336 0.59232,3.3261014 0.616973,9.12 0.02765,6.496686 0.09324,7.274798 0.849907,10.082398 4.566663,16.94446 -5.813776,34.536165 -22.942928,38.88133 -3.33783,0.84671 -8.555399,1.20393 -11.737332,0.803597 z M 38.24,60.649782 c 1.408,-0.298499 3.064,-0.757152 3.68,-1.019228 3.241824,-1.379226 5.474157,-2.556234 7.2,-3.796244 3.720666,-2.673273 8.131558,-7.911904 8.822595,-10.478224 C 59.25961,40.465069 59.581949,33.50585 58.691546,29.186509 58.13889,26.505588 56.57383,22.820999 55.169696,20.895086 53.906966,19.16313 49.20567,14.4 48.758928,14.4 c -0.433472,0 -3.415709,1.36704 -11.394115,5.222995 l -5.67519,2.742812 -8.19846,-3.982904 C 18.98201,16.192307 15.090266,14.4 14.842844,14.4 c -0.762398,0 -5.5003909,4.779988 -7.0531384,7.115653 -3.497993,5.261733 -4.369359,11.908078 -2.6606307,20.293963 0.7388339,3.625958 1.2158147,4.784512 2.9931449,7.270147 C 12.730995,55.525238 19.813746,59.823027 28,61.141533 c 2.319095,0.373523 7.283005,0.135142 10.24,-0.491751 z M 18.459705,44.24 c -0.168454,-0.292826 2.369714,-4.56 2.712344,-4.56 0.134257,0 0.830835,0.864 1.547951,1.92 l 1.303847,1.92 h 8.293139 c 9.326966,0 8.195555,0.287078 10.014748,-2.541085 0.389546,-0.605597 0.842423,-1.109597 1.006394,-1.12 0.386915,-0.02454 3.336666,4.066019 3.159248,4.381085 -0.07433,0.132 -6.38215,0.24 -14.017376,0.24 -7.635226,0 -13.944359,-0.108 -14.020295,-0.24 z m 3.933179,-0.96 c -0.0039,-0.132 -0.270644,-0.582707 -0.592735,-1.001574 l -0.58562,-0.761572 -0.527264,0.752775 C 19.934991,43.343648 20.018589,43.52 21.28,43.52 c 0.616,0 1.116798,-0.108 1.112884,-0.24 z M 44.48,43.271203 c 0,-0.136841 -0.23727,-0.587549 -0.527264,-1.001574 L 43.425472,41.516854 42.83985,42.278426 C 42.016218,43.349523 42.087638,43.52 43.36,43.52 c 0.616,0 1.12,-0.111958 1.12,-0.248797 z M 9.4672397,30.764075 C 9.3585162,30.588156 9.4435181,30.336711 9.6561328,30.205308 10.343228,29.78066 28.48745,29.31945 28.88454,29.71654 c 0.828893,0.828893 0.233742,0.892686 -10.85208,1.163202 -5.452805,0.133059 -8.4364002,0.09277 -8.5652203,-0.115667 z M 43.68,30.708397 c -3.52,-0.115004 -6.436,-0.231441 -6.48,-0.258748 -0.044,-0.02731 -0.08,-0.285278 -0.08,-0.573269 0,-0.475389 0.655837,-0.504405 7.12,-0.315006 9.993392,0.292804 12.4,0.493965 12.4,1.036475 0,0.487302 -1.132803,0.496965 -12.96,0.110548 z M 5.5620982,22.22338 C 5.671377,21.938604 5.6177299,21.810157 5.4363347,21.922265 5.2623507,22.029793 5.12,22.253272 5.12,22.418885 c 0,0.460299 0.2293651,0.358868 0.4420982,-0.195505 z M 9.1740301,9.7583581 C 9.2329155,9.5814547 8.850247,9.2460042 8.3236557,9.0129123 7.7970643,8.7798202 6.9773104,8.1770614 6.5019802,7.673448 5.5334675,6.6473069 5.12,6.7027869 5.12,7.8588854 c 0,0.5299799 0.1800445,0.7816256 0.56,0.782704 0.308,8.64e-4 0.992,0.3577972 1.52,0.7931616 0.9618739,0.793117 1.7734582,0.926162 1.9740301,0.3236071 z")
    svg(class="anonymous" viewBox="0 0 200 200" v-else-if="!avatar||(avatar.search('d41d8cd98f00b204e9800998ecf8427e')+1)")
      path(d="m 84.25,199.31067 c 0.9625,-0.25152 2.5375,-0.25152 3.5,0 0.9625,0.25153 0.175,0.45733 -1.75,0.45733 -1.925,0 -2.7125,-0.2058 -1.75,-0.45733 z m 30.75,-0.0209 c 1.375,-0.24399 2.9275,-0.85899 3.45,-1.36667 0.5225,-0.50768 1.90618,-0.92305 3.07485,-0.92305 5.96351,0 25.77723,-8.7565 36.25279,-16.02161 17.09178,-11.85364 32.22929,-33.31876 37.71373,-53.47839 0.89777,-3.3 2.03576,-6.9 2.52887,-8 0.49311,-1.1 1.08652,-2.9 1.3187,-4 0.23218,-1.1 0.27173,-0.17667 0.0879,2.05184 -0.57415,6.95992 -5.38889,20.53443 -10.97701,30.94816 -11.91009,22.19502 -31.76882,38.84853 -56.52108,47.39852 -4.63581,1.60131 -10.90374,3.11922 -13.92874,3.37314 -3.025,0.25392 -4.375,0.26205 -3,0.0181 z M 75.5,198.32319 C 74.4,198.07854 69.42891,196.33123 64.453133,194.44027 48.963938,188.55386 34.181983,178.23648 23.613455,165.93533 13.771053,154.47935 3.3796793,133.25505 2.4064731,122.62023 1.939495,117.51728 1.9444414,117.52362 3.872149,124.5 11.911171,153.59323 29.964555,175.95227 55.96464,189.01634 62.203266,192.15101 76.496655,197 79.498123,197 80.874155,197 82,197.45 82,198 c 0,1.00711 -2.799122,1.14628 -6.5,0.32319 z M 90.454545,159.54545 C 87.424279,156.51519 87.220169,151.77983 90,149 c 2.702734,-2.70273 6.572447,-2.51846 9.545455,0.45455 3.340225,3.34023 3.264075,7.76351 -0.180314,10.47287 -3.460164,2.72177 -5.911964,2.61667 -8.910596,-0.38197 z m -2.807819,-29.65129 c -1.624903,-15.54623 -0.270742,-24.67325 3.898076,-26.27298 0.890325,-0.34165 7.319469,-0.64711 14.286988,-0.67881 22.27118,-0.10131 23.97786,-1.09115 24.41191,-14.158281 0.22857,-6.881164 0.01,-7.963016 -2.02006,-10 C 125.97119,76.523984 125.61417,76.49475 94.223643,76 L 62.5,75.5 61.619294,68.639798 c -0.702214,-5.469847 -0.600879,-7.037434 0.5,-7.734687 1.958125,-1.2402 59.550296,-1.124598 64.062326,0.128589 6.21266,1.725527 12.83139,7.029413 16.21389,12.992923 2.90633,5.124017 3.10325,6.111666 3.085,15.473377 -0.0161,8.242157 -0.4183,10.8725 -2.2882,14.96346 -2.818,6.16522 -4.49839,8.04333 -10.19109,11.39018 C 128.96071,118.22914 127.22059,118.55118 116,119 l -12.5,0.5 -0.5,8 -0.5,8 -7.103274,0.29085 -7.103274,0.29085 z M 199.19495,85.5 c 0.0204,-1.65 0.2445,-2.203936 0.49804,-1.230968 0.25354,0.972967 0.23687,2.322967 -0.0371,3 C 199.38201,87.946064 199.17457,87.15 199.19495,85.5 Z M 2.0851509,78.25 c 0.4325538,-2.6125 1.9403487,-8.091319 3.3506553,-12.175152 2.322811,-6.726179 2.5649049,-8.891306 2.571748,-23 C 8.0185411,20.422466 10.633311,7.8721646 15.932685,5.0360259 18.815174,3.4933648 31.730803,5.3197723 37.871117,8.1383538 48.535106,13.033432 48.905956,13.074432 54.977809,10.029609 65.183076,4.912024 75.913315,1.7799372 82.88225,1.884485 86.419884,1.9375565 89.543592,2.2102585 89.823823,2.4904893 90.104054,2.7707202 88.432602,3 86.109487,3 78.97568,3 66.210658,6.8396621 55.789838,12.120017 50.814775,14.64094 47.401358,14.488301 41.775308,11.493323 35.943422,8.3887709 25.106656,5.7978043 19.630478,6.1987072 16.20962,6.4491433 15.279977,6.992343 14.122952,9.4168107 10.74022,16.505099 9.7907141,22.845135 9.3180619,41.5 8.8754797,58.968049 8.6013629,61.246782 5.9183326,69.761958 4.3132497,74.856034 3,79.918534 3,81.011958 3,82.105381 2.6172051,83 2.1493447,83 1.6814842,83 1.652597,80.8625 2.0851509,78.25 Z M 197,80.038095 c 0,-1.079047 -1.07484,-5.346611 -2.38854,-9.483476 -2.25841,-7.111776 -2.33653,-8.189883 -1.43372,-19.788095 C 194.23276,37.212777 193.63495,25.636418 191.40821,16.5 188.98652,6.5637147 188.58927,6 184.00878,6 c -5.16507,0 -15.97397,3.0014428 -22.94593,6.371684 -6.88479,3.3281 -8.87756,3.295989 -15.328,-0.246989 C 140.94629,9.4945184 130.79247,5.6730312 122,3.1918529 l -3.5,-0.9876772 3.24602,-0.1020878 c 4.12779,-0.1298199 13.57076,3.084865 23.53069,8.0105921 l 7.77672,3.846006 6.22328,-3.015752 c 11.58587,-5.614412 27.08395,-8.0108446 30.3949,-4.6998928 2.00259,2.0025883 5.01847,14.6811318 5.84038,24.5525628 0.35282,4.237418 0.18129,13.217182 -0.38117,19.955031 -0.91308,10.937973 -0.82709,12.819067 0.80252,17.555618 C 198.45599,75.638447 199.4569,82 198.0879,82 197.48955,82 197,81.117143 197,80.038095 Z M 58.666667,21.333333 C 57.101918,19.768584 58.213867,16.940766 60.95034,15.52568 63.779488,14.062671 72,13.366344 72,14.589707 c 0,1.062792 -4.433123,4.488827 -7.717881,5.964583 -3.584845,1.610577 -4.637835,1.75666 -5.615452,0.779043 z")
    img(:src="avatar" v-else)
    div.num 
      svg.up(viewBox="0 0 512 512" @click="vote(id, 'like')")
        path(d="M8 256C8 119 119 8 256 8s248 111 248 248-111 248-248 248S8 393 8 256zm143.6 28.9l72.4-75.5V392c0 13.3 10.7 24 24 24h16c13.3 0 24-10.7 24-24V209.4l72.4 75.5c9.3 9.7 24.8 9.9 34.3.4l10.9-11c9.4-9.4 9.4-24.6 0-33.9L273 107.7c-9.4-9.4-24.6-9.4-33.9 0L106.3 240.4c-9.4 9.4-9.4 24.6 0 33.9l10.9 11c9.6 9.5 25.1 9.3 34.4-.4z")
      span.likes {{likes}}
      svg.down(viewBox="0 0 512 512" @click="vote(id, 'dislike')")
        path(d="M504 256c0 137-111 248-248 248S8 393 8 256 119 8 256 8s248 111 248 248zm-143.6-28.9L288 302.6V120c0-13.3-10.7-24-24-24h-16c-13.3 0-24 10.7-24 24v182.6l-72.4-75.5c-9.3-9.7-24.8-9.9-34.3-.4l-10.9 11c-9.4 9.4-9.4 24.6 0 33.9L239 404.3c9.4 9.4 24.6 9.4 33.9 0l132.7-132.7c9.4-9.4 9.4-24.6 0-33.9l-10.9-11c-9.5-9.5-25-9.3-34.3.4z")          
  div.content
    div.information
      span.author(v-html="author ? (website ? `<a href=${website} target=_blank>${author}</a>` : author) : 'Anonymous'")
      span.timeline(v-html="timeFromNow(created)")
      span.edit(v-if="cookie('isso-'+id)" class="clickable" @click="editCom(id)") Edit
      span.delete(v-if="cookie('isso-'+id)" class="clickable" @click="deleteCom(id)") Delete
      span.reply(@click="reply2Com(id)" class="clickable") Reply
    div.text(v-html="setLinkTarget(text)")
    div.reply-section(v-if="replyshow" :id="'isso-reply-'+id")
      h5 Reply To {{ author ? author : "Anonymous" }}
      isso-input-field(:parent='id' :error="replyError" @submit="submit")
    div.edit-section(v-if="editshow" :id="'isso-edit-'+id")
      h5 Edit The Comment
      isso-input-field(:parent='null' :error="editError" @submit="edit" :oldcontent="text")
    slot
</template>
<script>
const IssoInputField = () => import('~/components/IssoInputField')
export default {
  props: {
    id: {
      type: Number
    },
    avatar: {
      type: String
    },
    likes: {
      type: Number
    },
    author: {
      type: String
    },
    website: {
      type: String
    },
    created: {
      type: Number
    },
    text: {
      type: String
    },
    slug: {
      type: String
    }
  },
  data() {
    return {
      replyshow: false,
      editshow: false, 
      editError: null,
      replyError: null,
      now: new Date()
    }
  },
  methods: {
    currentTime() {
      this.now = new Date()
    },
    vote(id, opinion) {
      this.$emit("vote", id, opinion)
    },
    setLinkTarget(text) {
      let comment = new DOMParser().parseFromString(text, "text/html"),
      links = comment.getElementsByTagName('a')
      for (let link of links) {
          link.setAttribute('target', '_blank')
      }
      const comment_html = new XMLSerializer().serializeToString(comment)
      return comment_html
    },
    timeFromNow(time) {
      let published = new Date(new Date(0).setUTCSeconds(time)),
      theRes = (this.now - published) / 1000
      return theRes < 60 ? `${Math.floor(theRes)} seconds ago` : 
             theRes < 60 * 60 ? `${Math.floor(theRes/60)} minutes ago` :
             theRes < 60 * 60 * 2 ? `1 hour ago` :
             theRes < 60 * 60 * 24 ? `${Math.floor(theRes/60/60)} hours ago` :
             theRes < 60 * 60 * 24 * 30 ? `${Math.floor(theRes/60/60/24)} days ago` :
             theRes < 60 * 60 * 24 * 365 ? `${Math.floor(theRes/60/60/24/30)} months ago` : `${Math.floor(theRes/60/60/24/365)} years ago`
    },
    cookie(name) {
      return this.$cookies.get(name)
    },
    deleteCom(id) {
      this.$emit("deletecom", id)
    },
    editCom(id) {
      this.editshow = !this.editshow
      let text = this.$el.getElementsByClassName('edit')[0].innerHTML
      switch (text) {
        case 'Edit':
          this.$el.getElementsByClassName('edit')[0].innerHTML = 'Close'
          break
        case 'Close': 
          this.$el.getElementsByClassName('edit')[0].innerHTML = 'Edit'
          break
      }
      
    },
    reply2Com(id) {
      this.replyshow = !this.replyshow
      let text = this.$el.getElementsByClassName('reply')[0].innerHTML
      switch (text) {
        case 'Reply':
          this.$el.getElementsByClassName('reply')[0].innerHTML = 'Close'
          break
        case 'Close': 
          this.$el.getElementsByClassName('reply')[0].innerHTML = 'Reply'
          break
      }
      
    },
    submit(content, name, email, website, parent, notification) {
      let data = { title: this.title }
      this.replyError = []
      if (name) {
        data.author = name
      }
      if (email) {
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          this.replyError.push("The email is not a valid email address. ")
        } else {
          data.email = email
          if (notification) {
            data.notification = 1
          }
        }
      }
      if (website) {
        try {
          new URL(website)
          data.website = website
        } catch (_) {
          this.replyError.push("The website address is not valid. ")
        }
      }
      if (parent) {
        data.parent = parent
      }
      if (!content || content.length < 3) {
        this.replyError.push("The comment should be at least 3 chars long. ")
      } else {
        data.text = content
      }
      this.error = this.replyError = this.replyError.join("")
      if (!this.replyError) {
        this.$axios
          .post(`${this.$store.state.isso}new?uri=${this.slug}`, data, {
            withCredentials: true
          })
          .then(res => {
            this.$emit('newcom', res)

            let headers = res.headers["x-set-cookie"].split(" "),
              cookie = headers[0].split("=")
            this.$cookies.set(cookie[0], cookie[1], {
              maxAge: 60 * 20,
              path: "/"
            })
            if (name) {
              this.$cookies.set("isso-name", name)
            }
            if (email) {
              this.$cookies.set("isso-email", email)
            }
            if (website) {
              this.$cookies.set("isso-website", website)
            }
            if (notification) {
              this.$cookies.set("isso-notification", notification)
            }
          })
          this.reply2Com(this.id)
      }
    },
    async edit(content, name, email, website, parent, notification) {
      let data = { }
      this.editError = []
      if (name) {
        data.author = name
      } else {
        data.author = null
      }
      if (email) {
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          this.editError.push("The email is not a valid email address. ")
        } else {
          data.email = email
          if (this.notification !== notification) {
            data.notification = 1
          }
        }
      } else {
        data.email = null
      }
      if (website) {
        try {
          new URL(website)
          data.website = website
        } catch (_) {
          this.editError.push("The website address is not valid. ")
        }
      } else {
        data.website = null
      }
      if (!content || content.length < 3) {
        this.editError.push("The comment should be at least 3 chars long. ")
      } else {
        data.text = content
      }
      this.editError = this.editError.join("")
      if (!this.editError) {
        try {
          let edit_res = await this.$axios.put(`${this.$store.state.isso}id/${this.id}`, data, {
              withCredentials: true
          })
          let headers = edit_res.headers["x-set-cookie"].split("; "),
            cookie = headers[0].split("=")
          this.$cookies.remove(cookie[0], { path: "/" })
          this.$cookies.set(cookie[0], cookie[1], {
            maxAge: 60 * 20,
            path: "/"
          })
          this.$emit('edit', edit_res.data, this.id)
          // console.log(this.id)
          this.editCom(this.id)
          this.$router.push("")
          this.$router.push(`#isso-${edit_res.data.id}`)
        } catch (err) {
          this.editError = err
        }
      } 
    }
  },
  mounted() {
    setInterval(this.currentTime, 1000)
  },
  components: {
    IssoInputField
  }
}
</script>