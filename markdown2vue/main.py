from functools import cmp_to_key
import os
import markdown
from slugify import slugify
from datetime import datetime
from datetime import timedelta
from json import dump, dumps
from copy import deepcopy
import collections
from urllib.parse import urljoin
from feedgen.feed import FeedGenerator
from pytz import timezone

SITENAME = "Simputer"
SITEURL = "https://snorl.ax"
TZ = timezone("Asia/Chongqing")
FEEDAUTHOR = {'name': 'Sim', 'email': 'sim@snorl.ax'}
post_output_directory = 'posts'
static_dir = 'static'
posts = {}
posts_all = []
post_slugs = []
post_slug_format = "/{cat}/{year}/{month}/{day}/{slug}/"
tag_slug_format = "/tags/{slug}/"
posts_inside = []
tags = {}
generate_list = []
cat_feed_path_format = 'static/%s/atom.xml'
cat_feeds = {}


def getTemp(path):
    temp_file = open(path, 'r')
    temp = temp_file.read()
    temp_file.close()
    return temp


def writeToVue(pathNow, content):
    os.makedirs(os.path.dirname(pathNow), exist_ok=True)
    infoWr = open(pathNow, 'w')
    infoWr.write(content)
    infoWr.close()


class AtomGen(FeedGenerator):
    def __init__(self, title, description, link, language):
        super().__init__()
        self.title(title)
        self.description(description)
        self.author(FEEDAUTHOR)
        self.id(link)
        self.link(href=SITEURL, rel='alternate')
        self.link(href=link, rel='self')
        self.language(language)

    def entry_add(self,
                  titl,
                  link,
                  published,
                  updated='',
                  content='',
                  order='append'):
        entry = super().add_entry(order=order)
        # print(entry)
        entry.title(titl)
        entry.link(href=link)
        if content:
            entry.content(content)
        entry.id(link)
        # print("published: "+published)
        # print("updated: "+updated)
        entry.published(TZ.localize(
            datetime.strptime(published, '%Y-%m-%d %H:%M')))
        entry.updated(TZ.localize(
            datetime.strptime(published, '%Y-%m-%d %H:%M')))
        if updated:
            entry.updated(TZ.localize(
                datetime.strptime(updated, '%Y-%m-%d %H:%M')))
        return entry


def posts_meta(directory):
    """Deal with the posts"""
    # list markdown directory
    cats = os.listdir(directory)
    for cat in cats:
        cat_slug = slugify(cat)
        cat_path = os.path.join(directory, cat)
        cat_json_path = os.path.join(post_output_directory, cat_slug)
        if cat not in posts.keys():
            posts[cat] = []
        os.makedirs(cat_json_path, exist_ok=True)
        cat_posts = os.listdir(cat_path)
        generate_list.append('/{}'.format(cat_slug))
        # initiate feed for the category
        cat_id = urljoin(SITEURL, cat_slug)
        cat_feeds[cat] = AtomGen(
            "%s - %s" % (cat, SITENAME),
            "%s in %s" % (cat, SITENAME), cat_id, 'en')
        for post in cat_posts:
            md = markdown.Markdown(extensions=['pymdownx.superfences',
                                               'pymdownx.tabbed',
                                               'meta',
                                               'footnotes',
                                               'toc',
                                               #    'codehilite',
                                               'pymdownx.highlight',
                                               'attr_list',
                                               'pymdownx.emoji',
                                               'pymdownx.extra',
                                               'pymdownx.tilde',
                                               'pymdownx.smartsymbols',
                                               'tables',
                                               'nl2br'],
                                   extension_configs={
                #    'codehilite':
                #                   {'linenums': True},
                'pymdownx.highlight': {
                    'linenums': True,
                    'linenums_style': 'pymdownx-inline',
                    'guess_lang': True
                },
                'pymdownx.superfences':
                {'disable_indented_code_blocks': True}})
            content = open(os.path.join(cat_path, post),
                           encoding='utf-8-sig').read()
            content_html = md.convert(content)
            rep_index = 0
            content_meta = md.Meta
            content_meta['title'] = "".join(content_meta['title'])
            content_meta['date'] = "".join(content_meta['date'])
            post_date = datetime.strptime(
                content_meta['date'], '%Y-%m-%d %H:%M')
            post_year = post_date.year
            post_month = '%02d' % post_date.month
            post_day = '%02d' % post_date.day
            if not '/{}/{}'.format(cat_slug, post_year) in generate_list:
                generate_list.append('/{}/{}'.format(cat_slug, post_year))
            if not '/{}/{}/{}'.format(cat_slug,
                                      post_year,
                                      post_month) in generate_list:
                generate_list.append(
                    '/{}/{}/{}'.format(cat_slug, post_year, post_month))
            if not '/{}/{}/{}/{}'.format(cat_slug, post_year, post_month, post_day) in generate_list:
                generate_list.append(
                    '/{}/{}/{}/{}'.format(cat_slug, post_year, post_month, post_day))
            if (len(content_meta["tags"]) == 1):
                content_meta['tags'] = content_meta['tags'][0].split(', ')
            for index in range(len(content_meta['tags'])):
                content_meta['tags'][index] = [content_meta['tags'][index],
                                               tag_slug_format.format(slug=slugify(content_meta['tags'][index])).rstrip('/')]
            if 'modified' in content_meta:
                content_meta['modified'] = "".join(content_meta['modified'])
            if 'author' in content_meta:
                content_meta['author'] = "".join(content_meta['author'])
            content_meta['summary'] = "".join(content_meta['summary'])
            if 'slug' in content_meta:
                content_meta['slug'] = "".join(content_meta['slug'])
            else:
                content_meta['slug'] = slugify(content_meta['title'])
            content_meta['slug'] = post_slug_format.format(
                cat=cat_slug, year=post_year, month=post_month, day=post_day, slug=content_meta['slug'])
            while content_meta['slug'] in post_slugs:
                rep_index += 1
                content_meta['slug'] = '{}-{}'.format(
                    content_meta['slug'].rstrip('/'), rep_index)
            post_slugs.append(content_meta['slug'].rstrip('/'))
            if not content_meta['slug'] in generate_list:
                generate_list.append(content_meta['slug'])
            # do the extra for the inside of the post
            content_inside = content_meta.copy()
            content_inside['html'] = content_html
            content_inside['category'] = cat
            posts[cat].append(content_meta)
            posts_all.append(content_meta)
            for tag in content_meta['tags']:
                if not tag[1] in tags:
                    tags[tag[1]] = {'name': tag[0], 'posts': []}
                if not tag[1] in generate_list:
                    generate_list.append(tag[1])
                tags[tag[1]]['posts'].append(content_meta)
            posts_inside.append(content_inside)


def write_to_generate_list():
    dump(generate_list, open('gen_list.json', 'w'))
    print('Wrote to gen_list.json')


def sortmethod(a, b):
    """sort posts in a descending order according to the date"""
    a_time = datetime.strptime(a['date'], '%Y-%m-%d %H:%M')
    b_time = datetime.strptime(b['date'], '%Y-%m-%d %H:%M')
    com_value = a_time - b_time
    if (com_value > timedelta(0)):
        return -1
    elif (com_value == timedelta(0)):
        return 0
    else:
        return 1


def parsepostdate_single(ob):
    """write the parsed date string to the post"""
    post = deepcopy(ob)
    published = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
    parsed_published = "{dt:%B} {dt.day}, {dt.year}".format(dt=published)
    post['date'] = parsed_published
    if ('modified' in post):
        modified = datetime.strptime(post['modified'], '%Y-%m-%d %H:%M')
        parsed_modified = "{dt:%B} {dt.day}, {dt.year}".format(dt=modified)
        post['modified'] = parsed_modified
    return post


def parsepostdates(ob):
    """write the parsed date string to each post"""
    parsed_ob = deepcopy(ob)
    parsed_posts = deepcopy(ob['posts'])
    for post in parsed_posts:
        published = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
        parsed_published = "{dt:%B} {dt.day}, {dt.year}".format(dt=published)
        post['date'] = parsed_published
        if ('modified' in post):
            modified = datetime.strptime(post['modified'], '%Y-%m-%d %H:%M')
            parsed_modified = "{dt:%B} {dt.day}, {dt.year}".format(dt=modified)
            post['modified'] = parsed_modified
    parsed_ob['posts'] = parsed_posts
    return parsed_ob


def addEntryToFeed(post, feed):
    """add a post to posts feed"""
    post_entry_url = urljoin(SITEURL, post['slug'])
    if 'modified' in post:
        up_date = post['modified']
    else:
        up_date = ''
    post_entry = feed.entry_add(
        post['title'], post_entry_url, post['date'], up_date, post['summary'])
    return post_entry


def tags_files(tags):
    # tags json and atom generation
    # sort the tags by post count in a descending order
    tags = collections.OrderedDict(
        sorted(tags.items(), key=lambda kv: -len(kv[1]['posts'])))
    tags_list = {}
    os.makedirs(os.path.join(static_dir, 'tags'), exist_ok=True)
    os.makedirs(os.path.join(post_output_directory, 'tags'), exist_ok=True)
    # init feed for tags
    tags_feed_path = os.path.join(static_dir, 'tags/atom.xml')
    tags_id = urljoin(SITEURL, 'tags')
    tags_feed = AtomGen("Tags - %s" %
                        SITENAME, "The tags in %s" % SITENAME, tags_id, 'en')

    for tag, tag_things in tags.items():
        # dump to tags_list
        tags_list[tag_things['name']] = {
            'length': len(tag_things['posts']), 'slug': tag}
        # sort the posts
        tags[tag]['posts'] = sorted(
            tags[tag]['posts'], key=cmp_to_key(sortmethod))
        # Add the tag to the total tags feed
        tag_entry_url = urljoin(SITEURL, tag)
        # print(tags[tag]['posts'], "Pub: "+tags[tag]['posts'][-1]['date'])
        tag_entry = tags_feed.entry_add(
            tag_things['name'], tag_entry_url, tags[tag]['posts'][-1]['date'], tags[tag]['posts'][0]['date'])

        # parsepostdates(tags[tag])
        # {
        #     "name": string,
        #     "posts": [
        #         {
        #         "title": string,
        #         "date": string,
        #         "author": string,
        #         "tags": [
        #             ["golang", "/tags/golang"],
        #             ["angular", "/tags/angular"]
        #         ],
        #         "summary": string,
        #         "slug": string
        #         }
        #     ]
        # }
        tagPath = os.path.join(post_output_directory, "{}.vue".format(tag.strip('/')))
        tagData = parsepostdates(tags[tag])
        tagContent = getTemp('template/tags/_tag.vue').replace('{data}', dumps(tagData))
        writeToVue(tagPath, tagContent)
        print("Wrote to {}".format(tagPath))

    # tags atom generation
    tags_feed.atom_file(tags_feed_path)
    print("Wrote to %s" % tags_feed_path)

    # tags
    # {"atom": "https://snorl.ax/tags/atom.xml", "tags": {"isso": {"length": 4, "slug": "/tags/isso"},}}

    tagsPathNow = os.path.join(post_output_directory, 'tags', 'index.vue')
    tagsContent = getTemp('template/tags/index.vue').replace('{data}', dumps(
        {'atom': urljoin(SITEURL, '/'.join(tags_feed_path.split('/')[1:])), 'tags': tags_list}))

    writeToVue(tagsPathNow, tagsContent)

    print("Wrote to {}".format(tagsPathNow))


def posts_files(posts_all, posts_inside):
    # write to category.json
    for cat, cat_posts in posts.items():
        cat_slug = slugify(cat)
        posts[cat] = sorted(posts[cat], key=cmp_to_key(sortmethod))
        # Add the recent 5 posts to the total cat feed
        recent_po = posts[cat][:5]
        for post in recent_po:
            post_entry = addEntryToFeed(post, cat_feeds[cat])
        # cat rss generation
        cat_feed_path = cat_feed_path_format % cat_slug
        os.makedirs(os.path.dirname(cat_feed_path), exist_ok=True)
        cat_feeds[cat].atom_file(cat_feed_path)
        print("Wrote to %s" % (cat_feed_path))
        # cat
        # {
        #     "name": "Browser",
        #     "atom": "https://snorl.ax/browser/atom.xml",
        #     "posts": [
        #         {
        #         "title": "NetEase went under fire for treatment of ill employee",
        #         "date": "November 25, 2019",
        #         "author": "Sim",
        #         "tags": [
        #             ["Netease", "/tags/netease"],
        #             ["employment", "/tags/employment"]
        #         ],
        #         "summary": "Recently NetEase went under fire for treatment of ill employee",
        #         "slug": "/browser/2019/11/25/netease-went-under-fire-for-treatment-of-ill-employee/"
        #         },
        #     ]
        # }
        catPath = os.path.join(post_output_directory, '{}/index.vue'.format(cat_slug))
        catData = parsepostdates({'name': cat, 'atom': urljoin(
            SITEURL, '/'.join(cat_feed_path.split('/')[1:])), 'posts': posts[cat]})
        catContent = getTemp('template/_cat/index.vue').replace('{data}', dumps(catData))
        writeToVue(catPath, catContent)

        print("Wrote to {}".format(catPath))

    # sort all posts
    posts_all = sorted(posts_all, key=cmp_to_key(sortmethod))
    # Add the recent 5 posts to the total cat feed
    all_recent = posts_all[:5]
    for post in all_recent:
        post_entry = addEntryToFeed(post, all_feed)
    # rss generation for recent posts
    all_feed.atom_file('static/atom.xml')
    print("Wrote to %s" % 'static/atom.xml')

    # sort the inside posts
    posts_inside = sorted(posts_inside, key=cmp_to_key(sortmethod))

    post_temp = getTemp('template/_cat/_year/_month/_day/_slug.vue')

    # write to cat/post.json
    for single_post in posts_inside:
        # {
        # "title": "A mania you can't miss",
        # "date": "January 23, 2018",
        # "tags": [
        #     ["Fall Out Boy", "/tags/fall-out-boy"],
        #     ["M A N I A", "/tags/m-a-n-i-a"]
        # ],
        # "author": "Sim",
        # "summary": "Ready for a mania?",
        # "ogimage": ["/images/og/fobmania-twitter.png"],
        # "slug": "/browser/2018/01/23/a-mania-you-can-t-miss/",
        # "html": "<p><img alt=\"mania\" src=\"https://static.snorl.ax/posts/fobmania.jpg\" title=\"Album Cover\"><br><strong>On January 18,</strong><br>Mania, Fall Out Boy's new studio album, was released on Google Play Music one day ahead of the release date of the Audio CD form.<br>The music video of a album track, \"Church\", was released on Youtube.<br><iframe class=\"youtube\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" src=\"https://www.youtube.com/embed/l3vbvF8bQfI\" frameborder=\"0\"></iframe><br>Previously released music video from the album:<br><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/VtVFTuIZFYU\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/JJJpRl2cTJc\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/7YAAyUFL1GQ\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/jG1JY0rt2Os\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/wH-by1ydBTM\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe></p>\n<p><strong>On January 19,</strong><br>The audio CD form was released. And they did a LIVE on Good Morning America.<br><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/Fjr1420IndY\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe><iframe class=\"youtube\" src=\"https://www.youtube.com/embed/PRLa_q13PgE\" allow=\"autoplay; encrypted-media\" allowfullscreen=\"\" frameborder=\"0\"></iframe></p>\n<p><strong>On January 22,</strong><br>Fall Out Boy released the video where Patrick did the magic nerd stuff about \"Church\" on Twitter.<br></p>\n<blockquote class=\"twitter-video\" data-lang=\"en\"><p lang=\"en\" dir=\"ltr\">The voice of an \ud83d\udc7c watch back when Patrick was in the studio recording vocal takes for Church <a href=\"https://twitter.com/hashtag/blessed?src=hash&amp;ref_src=twsrc%5Etfw\">#blessed</a> <a href=\"https://twitter.com/hashtag/nerdstuff?src=hash&amp;ref_src=twsrc%5Etfw\">#nerdstuff</a> <a href=\"https://twitter.com/hashtag/FOBMANIA?src=hash&amp;ref_src=twsrc%5Etfw\">#FOBMANIA</a> <a href=\"https://t.co/GpbaogM9Zv\">pic.twitter.com/GpbaogM9Zv</a></p>&mdash; Fall Out Boy (@falloutboy) <a href=\"https://twitter.com/falloutboy/status/955612181751574528?ref_src=twsrc%5Etfw\">January 23, 2018</a></blockquote>\n<script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>\n<p>Pete Wentz did a LIVE with the album music played while bathing and doing some Q&amp;A.<br></p>\n<blockquote class=\"twitter-tweet\" data-lang=\"en\"><p lang=\"und\" dir=\"ltr\"><a href=\"https://t.co/U9jm3hqX4i\">https://t.co/U9jm3hqX4i</a></p>&mdash; pw (@petewentz) <a href=\"https://twitter.com/petewentz/status/955563045715144706?ref_src=twsrc%5Etfw\">January 22, 2018</a></blockquote>\n<script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>\n<p>Buy a copy if u haven't done that! You can't miss the mania!<br>I have been listenin' to the whole album like hundreds of times since buying one on Google Play Music!</p>",
        # "category": "Browser"
        # }
        infoNow = parsepostdate_single(single_post)
        pathNow = os.path.join(post_output_directory, '.'+infoNow['slug'], 'index.vue')
        if 'modified' in infoNow:
            modi = infoNow['modified']
        else:
            modi = ''
        if 'ogimage' in infoNow:
            ogimage = infoNow['ogimage']
        else:
            ogimage = '/images/og/default.webp'

        content = post_temp.replace(
            '{title}', dumps(infoNow['title'])).replace(
            '{date}', dumps(infoNow['date'])).replace(
            '{modified}', dumps(modi)).replace(
            '{tags}', dumps(infoNow['tags'])).replace(
            '{html}', infoNow['html']).replace(
            '{slug}', dumps(infoNow['slug'])).replace(
            '{category}', dumps(infoNow['category'])).replace(
            '{ogimage}', dumps(ogimage))

        writeToVue(pathNow, content)

        print("Wrote to {}".format(pathNow))


all_feed = AtomGen('Recent posts in %s' %
                   SITENAME, 'Recent posts in %s' % SITENAME, SITEURL, 'en')
posts_meta('../contents')
tags_files(tags)
posts_files(posts_all, posts_inside)
