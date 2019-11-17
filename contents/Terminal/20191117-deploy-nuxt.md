---
title: Just switched to nuxt
date: 2019-11-17 20:49
author: Sim
tags: 
- nuxt
- Vue
- Github Pages
status: published
summary: Just started my first frontend developer job as an intern worker. And to learn vue better, I rewrote my blog using nuxt.
---

The blog is now powered by nuxt.js, I just posted the source code on [Github](https://github.com/SnorlaxYum/Simputer)[^1].  

## Populate Vuex store with posts

Thanks to hmsk's plugin[^4], I could write my posts in markdown and process it really efficiently. However to use the posts across several pages like Tag or Category it's a must to populate Vuex Store with them. The implementation is in my source code. To sort the posts or tags by a certain standard, I have to save them to `Map`, then define the behaviour of its iterator.

## Abandon embed.min.js from isso

I already abandoned it since I can do the same thing with `axios` with my own styles. The implementation is in my source code[^1].  
With `axios` we could also interact with commenting systems like `Discus` with our own styles, which can be a cool solution of serverless commenting.  
In the future I might write my own commenting system along with API to learn more about backend things.

## The paths that need to be taken care of

I don't have to worry about this until I decides to deploy the blog as a static site[^2].  
Normally the nested routes won't be generated if not set in the `generate` block of `nuxt.config.js`.  
Also I should configure `fallback: true` option in the same block for Firebase Hosting to take care of.

## Error: t is undefined

On pages like this post of this blog, I just came across a problem when using `nuxt generate`. The page loads fine if I initially arrives at a page rather than any post. In the console log it just showed:  

```
TypeError: "t is undefined" [nuxt] Error while initializing app
DOMException: "Node cannot be inserted at the specified point in the hierarchy"
```

This error is caused because data differs on server vs client.[^3]  

When I inspected, I found that the error will disappear if the page don't have any components. Eventually, I solved this by adding `<client-only>` out of the post things.  

## Deploy to Github Pages

In `nuxt.config.js`:  

```
...
export default {
  ...
  generate: {... dir: 'docs'},
...
```

Then `yarn generate`, and then push to the repository, toggle settings to open github pages at `/docs`.  

## Why I don't use Firebase Functions or my own server

Firebase Functions are way too slow......

I took some screenshots:  

1. [Firebase Functions](https://static.snorl.ax/nuxt-speed/fb-functions.webp)
2. [My Server](https://static.snorl.ax/nuxt-speed/my-server.webp)
3. [Firebase Hosting](https://static.snorl.ax/nuxt-speed/fb-hosting.webp)

I'd rather use my own server when it comes to SSR. But nothing compares to Fastly CDN.

[^1]: [The source code of the blog](https://github.com/SnorlaxYum/Simputer)
[^2]: [API: The generate Property - NuxtJS](https://nuxtjs.org/api/configuration-generate)
[^3]: [Nuxt.js app doesn't load charts or maps when copying and pasting a link into a new browser tab, otherwise works](https://stackoverflow.com/questions/54010529/nuxt-js-app-doesnt-load-charts-or-maps-when-copying-and-pasting-a-link-into-a-n)
[^4]: [hmsk/frontmatter-markdown-loader: 📝 Webpack Loader for: FrontMatter (.md) -> HTML + Attributes (+ React/Vue Component)](https://github.com/hmsk/frontmatter-markdown-loader)