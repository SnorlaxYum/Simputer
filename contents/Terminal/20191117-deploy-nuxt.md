title: Just switched to nuxt
date: 2019-11-17 20:49
modified: 2019-11-22 17:56
author: Sim
tags: nuxt, markdown, Gridsome, Vue, Github Pages, git, Python, json
summary: Just started my first frontend developer job as an intern worker. And to learn vue better, I rewrote my blog using nuxt.

The blog is now powered by nuxt.js, I just posted the source code on [Github](https://github.com/SnorlaxYum/Simputer)[^1].  

## Deal with the markdown posts

~~Thanks to hmsk's plugin[^4], I could write my posts in markdown and process it really efficiently. However to use the posts across several pages like Tag or Category it's a must to populate Vuex Store with them. The implementation is in my source code. To sort the posts or tags by a certain standard, I have to save them to `Map`, then define the behaviour of its iterator.~~  

Populating the store with the markdown files converted by that plugin[^4] could place my generated site in an oversized situation:  

1. [The Large Markdown Buudle Pages](https://static.snorl.ax/nuxt-speed/md-html.webp)
2. [The Large Markdown Bundle Javascript File](https://static.snorl.ax/nuxt-speed/md-js-bundle.webp)

I don't have many posts on this blog, but the output of `nuxt generate` comes with 60MB+, which is incredibly large. The reason is the generated page just bundles every pages into one html and js files. The js files are large also due to my reliance on plugins like `uslug`, `hljs`, etc.  
So could I just make each markdown pages load their own content and thus make the size much small? Yes, and I searched about markdown on nuxt, many people just recommend Gridsome, saying it's a perfect solution about a markdown blog on nuxt. So I just took a look on their website and switched to another page, and I saw their [new GET requests](https://static.snorl.ax/nuxt-speed/gridsome-solution.webp) on switching to a new page are mainly JSON-based. And that's possible in a nuxt.js app, all I need is **loading the needed json on a specific page**.  

Then here's my solution, **generate the jsons before-hand and load them on the specific post page**. In doing this, I don't need that many packages imported in my nuxt project and all these things could be done with python much more easily and quickly, after spending some time writing and testing the code in that python file for my JSON generating process, now my [page size](https://static.snorl.ax/nuxt-speed/page-size-now.webp) and [js bundle size](https://static.snorl.ax/nuxt-speed/my-js-bundle-now.webp) are back to normal. At least they won't be increasing together with my markdown files. Here's the magic of json! Especially for a static nuxt website, I'd better preprocess the data and save them to files, thus making the html files and js bundle files generated as small as possible. Just let a backend language do all the dirty work for me, which serves as an API server in this case. Frontend languages are there for bringing data to the browser. Python is ideal for the job 'cause it has tons of tools such as `slugify`, `markdown` to do that well and it's easy to write code in the language, basically the codes are really self-explanatory and easy to debug (Python Shell just comes in handy).  

Auto deployment on Github is a bit tricky, since it also needs call the API when running `nuxt generate`, an API server listening at a port that serves the json files is also needed.  

![](https://static.snorl.ax/graphs/nuxt-20191122.svg)
{: .text-center .graph}

## Abandon embed.min.js from isso

I already abandoned it since I can do the same thing with `axios` with my own styles. The implementation is in my source code[^1].  
With `axios` we could also interact with commenting systems like `Discus` with our own styles, which can be a cool solution of serverless commenting.  
In the future I might write my own commenting system along with API to learn more about backend things.

## Preview locally

A static generated nuxt app could be different than the one we preview using `yarn dev`. So it's necessary to preview the generated site locally.  

I changed some lines in `packages.json` to implement this:  

    {
      ...
      "scripts": {
        ...
        "serve": "python -m http.server --directory dist"
      },
      ...
    }

Then I could do `yarn generate && yarn serve` every time I generate the pages to see the result.  

## The paths that need to be taken care of

I don't have to worry about this until I decides to deploy the blog as a static site[^2].  
Normally the nested routes won't be generated if not set in the `generate` block of `nuxt.config.js`.  
Also I should configure `fallback: true` option in the same block for Github Pages to take care of.

## Error: t is undefined

On pages like this post of this blog, I just came across a problem when using `nuxt generate`. The page loads fine if I initially arrives at a page rather than any post. In the console log it just showed:  

  TypeError: "t is undefined" [nuxt] Error while initializing app
  DOMException: "Node cannot be inserted at the specified point in the hierarchy"

This error is caused because data differs on server vs client.[^3]  

When I inspected, I found that the error will disappear if the page don't have any components. Eventually, I solved this by adding `<client-only>` out of the post things.  

## Deploy to Github Pages

One easy way is to change the generate dir from `dist` to `docs` and then `nuxt generate` and push to the repository. However, that's kinda silly and unneccessary since we've got Github Actions. I use [this](https://github.com/peaceiris/actions-gh-pages) for my deployment[^5], which will be triggered automatically once I send a new commit to the `master` branch.  

Be sure to put a CNAME file with the custom domain to `static` folder.  

## Why I don't use Firebase Functions or my own server

Firebase Functions are way too slow......

I took some screenshots:  

1. [Firebase Functions](https://static.snorl.ax/nuxt-speed/fb-functions.webp)
2. [My Server](https://static.snorl.ax/nuxt-speed/my-server.webp)
3. [Firebase Hosting](https://static.snorl.ax/nuxt-speed/fb-hosting.webp)
4. [Github Pages](https://static.snorl.ax/nuxt-speed/github-pages.webp)

I'd rather use my own server when it comes to SSR. But nothing compares to Fastly CDN.

[^1]: [The source code of the blog](https://github.com/SnorlaxYum/Simputer)
[^2]: [API: The generate Property - NuxtJS](https://nuxtjs.org/api/configuration-generate)
[^3]: [Nuxt.js app doesn't load charts or maps when copying and pasting a link into a new browser tab, otherwise works](https://stackoverflow.com/questions/54010529/nuxt-js-app-doesnt-load-charts-or-maps-when-copying-and-pasting-a-link-into-a-n)
[^4]: [hmsk/frontmatter-markdown-loader: 📝 Webpack Loader for: FrontMatter (.md) -> HTML + Attributes (+ React/Vue Component)](https://github.com/hmsk/frontmatter-markdown-loader)
[^5]: [peaceiris/actions-gh-pages: GitHub Actions for GitHub Pages 🚀 Deploy static files and publish your site easily. Static-Site-Generators-friendly.](https://github.com/peaceiris/actions-gh-pages)