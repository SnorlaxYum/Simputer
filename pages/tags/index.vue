<template lang="pug">
  article.tags
    header Tags
      feed-link(:link="atom")
    content
      ul
        li(v-for='tag_info, tag of tags')
          nuxt-link(:to="tag_info.slug") {{tag}}
          |           ({{tag_info.length}})
</template>

<script lang="ts">
const FeedLink = () => import("~/components/FeedLink")

export default {
  components: {
    FeedLink
  },
  data() {
    return {"atom": "https://snorl.ax/tags/atom.xml", "tags": {"isso": {"length": 4, "slug": "/tags/isso"}, "git": {"length": 4, "slug": "/tags/git"}, "Debian": {"length": 4, "slug": "/tags/debian"}, "nginx": {"length": 4, "slug": "/tags/nginx"}, "cloudflare": {"length": 4, "slug": "/tags/cloudflare"}, "dovecot": {"length": 3, "slug": "/tags/dovecot"}, "Firebase": {"length": 2, "slug": "/tags/firebase"}, "Fall Out Boy": {"length": 2, "slug": "/tags/fall-out-boy"}, "M A N I A": {"length": 2, "slug": "/tags/m-a-n-i-a"}, "speed": {"length": 2, "slug": "/tags/speed"}, "CDN": {"length": 2, "slug": "/tags/cdn"}, "email": {"length": 2, "slug": "/tags/email"}, "postfix": {"length": 2, "slug": "/tags/postfix"}, "spamassassin": {"length": 2, "slug": "/tags/spamassassin"}, "Pokemon": {"length": 1, "slug": "/tags/pokemon"}, "movie": {"length": 1, "slug": "/tags/movie"}, "Winter": {"length": 1, "slug": "/tags/winter"}, "snow": {"length": 1, "slug": "/tags/snow"}, "Hangzhou": {"length": 1, "slug": "/tags/hangzhou"}, "Panic! At The Disco": {"length": 1, "slug": "/tags/panic-at-the-disco"}, "Pray For The Wicked": {"length": 1, "slug": "/tags/pray-for-the-wicked"}, "Tour": {"length": 1, "slug": "/tags/tour"}, "Shanghai": {"length": 1, "slug": "/tags/shanghai"}, "Netease": {"length": 1, "slug": "/tags/netease"}, "employment": {"length": 1, "slug": "/tags/employment"}, "sqlite": {"length": 1, "slug": "/tags/sqlite"}, "Conflicts": {"length": 1, "slug": "/tags/conflicts"}, "WebRTC": {"length": 1, "slug": "/tags/webrtc"}, "p2p": {"length": 1, "slug": "/tags/p2p"}, "study": {"length": 1, "slug": "/tags/study"}, "frontend": {"length": 1, "slug": "/tags/frontend"}, "RTCPeerConnection": {"length": 1, "slug": "/tags/rtcpeerconnection"}, "config": {"length": 1, "slug": "/tags/config"}, "Buster": {"length": 1, "slug": "/tags/buster"}, "openssl": {"length": 1, "slug": "/tags/openssl"}, "nuxt": {"length": 1, "slug": "/tags/nuxt"}, "markdown": {"length": 1, "slug": "/tags/markdown"}, "Gridsome": {"length": 1, "slug": "/tags/gridsome"}, "Vue": {"length": 1, "slug": "/tags/vue"}, "Github Pages": {"length": 1, "slug": "/tags/github-pages"}, "Python": {"length": 1, "slug": "/tags/python"}, "json": {"length": 1, "slug": "/tags/json"}, "Bandwagonhost": {"length": 1, "slug": "/tags/bandwagonhost"}, "KeyCDN": {"length": 1, "slug": "/tags/keycdn"}, "Gitlab": {"length": 1, "slug": "/tags/gitlab"}, "Github": {"length": 1, "slug": "/tags/github"}, "Netlify": {"length": 1, "slug": "/tags/netlify"}, "detached HEAD": {"length": 1, "slug": "/tags/detached-head"}, "submodule": {"length": 1, "slug": "/tags/submodule"}, "load balancing": {"length": 1, "slug": "/tags/load-balancing"}, "PerfOps": {"length": 1, "slug": "/tags/perfops"}, "brotli": {"length": 1, "slug": "/tags/brotli"}, "file": {"length": 1, "slug": "/tags/file"}, "ssh": {"length": 1, "slug": "/tags/ssh"}, "gevent": {"length": 1, "slug": "/tags/gevent"}, "uwsgi": {"length": 1, "slug": "/tags/uwsgi"}, "saslauthd": {"length": 1, "slug": "/tags/saslauthd"}, "imap": {"length": 1, "slug": "/tags/imap"}, "smtp": {"length": 1, "slug": "/tags/smtp"}, "SendGrid": {"length": 1, "slug": "/tags/sendgrid"}, "Amazon SES": {"length": 1, "slug": "/tags/amazon-ses"}, "dkim": {"length": 1, "slug": "/tags/dkim"}, "spf": {"length": 1, "slug": "/tags/spf"}, "dmarc": {"length": 1, "slug": "/tags/dmarc"}, "mailutils": {"length": 1, "slug": "/tags/mailutils"}, "golang": {"length": 1, "slug": "/tags/golang"}, "angular": {"length": 1, "slug": "/tags/angular"}, "Ant Design": {"length": 1, "slug": "/tags/ant-design"}, "React.js": {"length": 1, "slug": "/tags/react-js"}, "Javascript": {"length": 1, "slug": "/tags/javascript"}, "wrappedComponentRef": {"length": 1, "slug": "/tags/wrappedcomponentref"}, "Promise": {"length": 1, "slug": "/tags/promise"}, "Form": {"length": 1, "slug": "/tags/form"}, "CloudIPLC": {"length": 1, "slug": "/tags/cloudiplc"}, "VPS": {"length": 1, "slug": "/tags/vps"}, "NAT": {"length": 1, "slug": "/tags/nat"}, "Chinese": {"length": 1, "slug": "/tags/chinese"}, "BBR": {"length": 1, "slug": "/tags/bbr"}, "Proxy": {"length": 1, "slug": "/tags/proxy"}}}
  },
  head() {
    return {
      title: "Tags",
      link: [{ rel: 'alternate', href: this.atom, type: 'application/atom+xml' }]
    }
  }
}
</script>