const markdownIt = require('markdown-it');
const markdownItFootnote = require('markdown-it-footnote');
const markdownItEmoji = require('markdown-it-emoji');
const markdownAnchor = require('markdown-it-anchor');
const markdownhljs = require('markdown-it-highlightjs');

const gen = ['/browser',
  '/terminal',
  '/tags/isso',
  '/tags/cloudflare',
  '/tags/nginx',
  '/tags/debian',
  '/tags/dovecot',
  '/tags/learning-notes',
  '/tags/cdn',
  '/tags/speed',
  '/tags/firebase',
  '/tags/fall-out-boy',
  '/tags/m-a-n-i-a',
  '/tags/email',
  '/tags/postfix',
  '/tags/spamassassin',
  '/tags/git',
  '/tags/js',
  '/tags/you-dont-know-js',
  '/tags/panic-at-the-disco',
  '/tags/gevent',
  '/tags/uwsgi',
  '/tags/keycdn',
  '/tags/gitlab',
  '/tags/github',
  '/tags/netlify',
  '/tags/tour',
  '/tags/shanghai',
  '/tags/pray-for-the-wicked',
  '/tags/winter',
  '/tags/snow',
  '/tags/hangzhou',
  '/tags/saslauthd',
  '/tags/imap',
  '/tags/smtp',
  '/tags/sendgrid',
  '/tags/amazon-ses',
  '/tags/dkim',
  '/tags/spf',
  '/tags/dmarc',
  '/tags/mailutils',
  '/tags/conflicts',
  '/tags/pokemon',
  '/tags/movie',
  '/tags/mdn',
  '/tags/javascript',
  '/tags/brotli',
  '/tags/file',
  '/tags/ssh',
  '/tags/load-balancing',
  '/tags/perfops',
  '/tags/config',
  '/tags/sqlite',
  '/tags/buster',
  '/tags/openssl',
  '/tags/cloudiplc',
  '/tags/vps',
  '/tags/nat',
  '/tags/chinese',
  '/tags/bbr',
  '/tags/proxy',
  '/tags/bandwagonhost',
  '/tags/nuxt',
  '/tags/vue',
  '/tags/github-pages',
  '/tags/python',
  '/terminal/2019',
  '/terminal/2019/11',
  '/terminal/2019/11/17',
  '/terminal/2019/11/17/just-switched-to-nuxt',
  '/terminal/2019',
  '/terminal/2019/08',
  '/terminal/2019/08/08',
  '/terminal/2019/08/08/ifup-cannot-bring-up-eth1-after-upgrading',
  '/terminal/2019',
  '/terminal/2019/07',
  '/terminal/2019/07/11',
  '/terminal/2019/07/11/permission-issues-with-dovecot-stats-writer',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/22',
  '/terminal/2019/06/22/purchased-a-nat-vps-from-cloudiplc',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/17',
  '/terminal/2019/06/17/updated-to-debian-buster',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/10',
  '/terminal/2019/06/10/performance-test-on-a-page-cloudflare-vs-bare-nginx',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/10',
  '/terminal/2019/06/10/my-isso-configuration',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/10',
  '/terminal/2019/06/10/inside-the-isso-database',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/08',
  '/terminal/2019/06/08/doing-site-mirroring-with-nginx-on-the-same-domain',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/07',
  '/terminal/2019/06/07/git-an-excellent-file-transferer',
  '/terminal/2019',
  '/terminal/2019/06',
  '/terminal/2019/06/07',
  '/terminal/2019/06/07/add-brotli-to-nginx-on-debian-stretch',
  '/terminal/2019',
  '/terminal/2019/05',
  '/terminal/2019/05/23',
  '/terminal/2019/05/23/notes-on-mdn-web-docs-javascript-guide',
  '/terminal/2019',
  '/terminal/2019/05',
  '/terminal/2019/05/17',
  '/terminal/2019/05/17/notes-on-async-performance-ydjs',
  '/browser/2019',
  '/browser/2019/05',
  '/browser/2019/05/10',
  '/browser/2019/05/10/refresh-the-browser',
  '/terminal/2019',
  '/terminal/2019/05',
  '/terminal/2019/05/07',
  '/terminal/2019/05/07/notes-on-types-grammer-ydjs',
  '/terminal/2019',
  '/terminal/2019/04',
  '/terminal/2019/04/16',
  '/terminal/2019/04/16/resolving-conflicts-in-git',
  '/terminal/2018',
  '/terminal/2018/12',
  '/terminal/2018/12/27',
  '/terminal/2018/12/27/running-email-service-on-my-own-server',
  '/browser/2018',
  '/browser/2018/12',
  '/browser/2018/12/08',
  '/browser/2018/12/08/cold-winter-in-2018',
  '/browser/2018',
  '/browser/2018/05',
  '/browser/2018/05/04',
  '/browser/2018/05/04/waiting-for-pray-for-the-wicked',
  '/browser/2018',
  '/browser/2018/05',
  '/browser/2018/05/02',
  '/browser/2018/05/02/mania-in-shanghai',
  '/browser/2018',
  '/browser/2018/01',
  '/browser/2018/01/23',
  '/browser/2018/01/23/a-mania-you-cant-miss',
  '/terminal/2016',
  '/terminal/2016/12',
  '/terminal/2016/12/08',
  '/terminal/2016/12/08/site-migration-history',
  '/terminal/2016',
  '/terminal/2016/07',
  '/terminal/2016/07/12',
  '/terminal/2016/07/12/start-to-use-isso'
]

export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  generate: {routes: gen, fallback: true},
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
    // Load a Node.js module directly (here it's a Sass file)
    // 'bulma',
    // CSS file in the project
    // '@/assets/css/main.css',
    // SCSS file in the project
    '@/assets/css/main.sass'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    'cookie-universal-nuxt',
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
  },
  hooks: {
    build: {
      generate: {
        done(nuxt, errors) {
        console.log(errors)
      }
    }
    }
  },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
   extractCSS: true,
    extend (config, ctx) {
      
      config.module.rules.push({
        test: /\.md$/,
        loader: 'frontmatter-markdown-loader',
        options: {
          markdownIt: markdownIt({
            html: true,
            linkify: false,
            breaks: true,
            typographer: true
          }).use(markdownItFootnote).use(markdownItEmoji).use(markdownAnchor, {
            slugify(title) {
              // Credit: https://blog.vjeux.com/2010/javascript/javascript-slug.html
              function keys(o) { var a = []; for (var k in o) a.push(k); return a; }
              //  var accents = "àáäâèéëêìíïîòóöôùúüûñç";
              let accents = "\u00e0\u00e1\u00e4\u00e2\u00e8"
                  + "\u00e9\u00eb\u00ea\u00ec\u00ed\u00ef"
                  + "\u00ee\u00f2\u00f3\u00f6\u00f4\u00f9"
                  + "\u00fa\u00fc\u00fb\u00f1\u00e7"
              let without = "aaaaeeeeiiiioooouuuunc"
              let map = {'@': ' at ', '\u20ac': ' euro ', 
                  '$': ' dollar ', '\u00a5': ' yen ',
                  '\u0026': ' and ', '\u00e6': 'ae', '\u0153': 'oe'}
              return title
                  // Handle uppercase characters
                  .toLowerCase()
              
                  // Handle accentuated characters
                  .replace(
                  new RegExp('[' + accents + ']', 'g'),
                  function (c) { return without.charAt(accents.indexOf(c)); })
              
                  // Handle special characters
                  .replace(
                  new RegExp('[' + keys(map).join('') + ']', 'g'),
                  function (c) { return map[c]; })
              
                  // Dash special characters
                  .replace(/[^a-z0-9]/g, '-')
              
                  // Compress multiple dash
                  .replace(/-+/g, '-')
              
                  // Trim dashes
                  .replace(/^-|-$/g, '')
          }
        }).use(markdownhljs)
        }
      })
    }
  }
}
