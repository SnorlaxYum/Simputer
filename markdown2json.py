from functools import cmp_to_key
import os
import markdown
from slugify import slugify
from datetime import datetime
from datetime import timedelta
from json import dump
from copy import deepcopy
import collections
from urllib.parse import urljoin
from feedgen.feed import FeedGenerator
from pytz import timezone

SITENAME = "Simputer"
SITEURL = "https://snorl.ax"
TZ = timezone("Asia/Chongqing")
FEEDAUTHOR = {'name': 'Sim', 'email': 'sim@snorl.ax'}
output_directory = 'static'
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
        cat_json_path = os.path.join(output_directory, cat_slug)
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
                                               'meta',
                                               'footnotes',
                                               'toc',
                                               'codehilite',
                                               'attr_list',
                                               'pymdownx.emoji',
                                               'pymdownx.extra',
                                               'pymdownx.tilde',
                                               'pymdownx.smartsymbols',
                                               'tables',
                                               'nl2br'],
                                   extension_configs={'codehilite':
                                                      {'linenums': True}})
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
                                               tag_slug_format.format(slug=slugify(content_meta['tags'][index]))]
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
                content_meta['slug'] = '{}-{}/'.format(
                    content_meta['slug'].rstrip('/'), rep_index)
            post_slugs.append(content_meta['slug'])
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
    os.makedirs(os.path.join(output_directory, 'tags'), exist_ok=True)
    # init feed for tags
    tags_feed_path = os.path.join(output_directory, 'tags/atom.xml')
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
        # write to json
        tag_json = os.path.join(
            output_directory, '{}.json'.format(tag.strip('/')))
        dump(parsepostdates(tags[tag]), open(tag_json, 'w'))
        print("Wrote to {}".format(tag_json))

    # tags atom generation
    tags_feed.atom_file(tags_feed_path)
    print("Wrote to %s" % tags_feed_path)

    # tags json generation
    tags_json = os.path.join(output_directory, 'tags.json')
    dump({'atom': urljoin(SITEURL, '/'.join(tags_feed_path.split('/')
                                            [1:])), 'tags': tags_list}, open(tags_json, 'w'))
    print("Wrote to {}".format(tags_json))


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
        cat_feeds[cat].atom_file(cat_feed_path)
        print("Wrote to %s" % (cat_feed_path))
        # dump to json
        json_name = os.path.join(output_directory, '{}.json'.format(cat_slug))
        dump(
            parsepostdates(
                {'name': cat, 'atom': urljoin(SITEURL, '/'.join(cat_feed_path.split('/')[1:])),
                 'posts': posts[cat]}),
            open(json_name, 'w'))
        print("Wrote to {}".format(json_name))

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

    # write to cat/post.json
    for single_post in posts_inside:
        json_name = os.path.join(output_directory, slugify(
            single_post['category']), '{}.json'.format(single_post['slug'].split("/")[-2]))
        dump(parsepostdate_single(single_post), open(json_name, 'w'))
        print("Wrote to {}".format(json_name))


all_feed = AtomGen('Recent posts in %s' %
                   SITENAME, 'Recent posts in %s' % SITENAME, SITEURL, 'en')
posts_meta('contents')
tags_files(tags)
posts_files(posts_all, posts_inside)
