from functools import cmp_to_key
import os
import markdown
import re
from slugify import slugify
from datetime import datetime
from datetime import timedelta
from json import dump
from copy import deepcopy
import collections

output_directory = 'static'
posts = {
    # I don't need this because I don't need to list all the posts
    # 'all': []
}
post_slugs = []
post_slug_format = "/{cat}/{year}/{month}/{day}/{slug}/"
tag_slug_format = "/tags/{slug}/"
posts_inside = []
tags = {}
generate_list = []

# list 'contents' directory

cats = os.listdir('contents')
for cat in cats:
    cat_slug = cat.lower()
    cat_path = os.path.join('contents', cat)
    cat_json_path = os.path.join(output_directory, cat_slug)
    if not cat in posts.keys():
        posts[cat] = []
    os.makedirs(cat_json_path, exist_ok=True)
    cat_posts = os.listdir(cat_path)
    generate_list.append('/{}'.format(cat_slug))
    for post in cat_posts:
        md = markdown.Markdown(extensions=['pymdownx.superfences', 'meta', 'footnotes', 'toc', 'codehilite', 'attr_list', 'pymdownx.emoji', 'pymdownx.extra',
                                           'pymdownx.tilde', 'pymdownx.smartsymbols', 'tables', 'nl2br'], extension_configs={'codehilite': {'linenums': True}})
        # print(post)
        content = open(os.path.join(cat_path, post),
                       encoding='utf-8-sig').read()
        content_html = md.convert(content)
        rep_index = 0
        content_meta = md.Meta
        # print(content_meta)
        content_meta['title'] = "".join(content_meta['title'])
        content_meta['date'] = "".join(content_meta['date'])
        post_date = datetime.strptime(content_meta['date'], '%Y-%m-%d %H:%M')
        post_year = post_date.year
        post_month = '%02d' % post_date.month
        post_day = '%02d' % post_date.day
        if not '/{}/{}'.format(cat_slug, post_year) in generate_list:
            generate_list.append('/{}/{}'.format(cat_slug, post_year))
        if not '/{}/{}/{}'.format(cat_slug, post_year, post_month) in generate_list:
            generate_list.append(
                '/{}/{}/{}'.format(cat_slug, post_year, post_month))
        if not '/{}/{}/{}/{}'.format(cat_slug, post_year, post_month, post_day) in generate_list:
            generate_list.append(
                '/{}/{}/{}/{}'.format(cat_slug, post_year, post_month, post_day))
        if (len(content_meta["tags"]) == 1):
            content_meta['tags'] = content_meta['tags'][0].split(', ')
        for index in range(len(content_meta['tags'])):
            content_meta['tags'][index] = [content_meta['tags']
                                           [index], tag_slug_format.format(slug=slugify(content_meta['tags'][index]))]
        if 'modified' in content_meta:
            content_meta['modified'] = "".join(content_meta['modified'])
        if 'author' in content_meta:
            content_meta['author'] = "".join(content_meta['author'])
        content_meta['summary'] = "".join(content_meta['summary'])
        if 'slug' in content_meta:
            content_meta['slug'] = "".join(content_meta['slug'])
        else:
            content_meta['slug'] = slugify(content_meta['title'])
        content_meta['slug'] = post_slug_format.format(cat=cat_slug, year=post_year, month=post_month, day=post_day, slug=content_meta['slug'])
        while content_meta['slug'] in post_slugs:
            rep_index += 1
            content_meta['slug'] = '{}-{}/'.format(
                content_meta['slug'].strip('/'), rep_index)
        post_slugs.append(content_meta['slug'])
        if not content_meta['slug'] in generate_list:
            generate_list.append(content_meta['slug'])
        # do the extra for the inside of the post
        content_inside = content_meta.copy()
        content_inside['html'] = content_html
        content_inside['category'] = cat
        posts[cat].append(content_meta)
        for tag in content_meta['tags']:
            if not tag[1] in tags:
                tags[tag[1]] = {'name': tag[0], 'posts': []}
            if not tag[1] in generate_list:
                generate_list.append(tag[1])
            tags[tag[1]]['posts'].append(content_meta)
        posts_inside.append(content_inside)

dump(generate_list, open('gen_list.json', 'w'))
print('Wrote to gen_list.json')

# sort posts in a descending order according to the date

def sortmethod(a, b):
    a_time = datetime.strptime(a['date'], '%Y-%m-%d %H:%M')
    b_time = datetime.strptime(b['date'], '%Y-%m-%d %H:%M')
    com_value = a_time - b_time
    if (com_value > timedelta(0)):
        return -1
    elif (com_value == timedelta(0)):
        return 0
    else:
        return 1

# write the parsed date string to the post

def parsepostdate_single(ob):
    post = deepcopy(ob)
    published = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
    parsed_published = "{dt:%B} {dt.day}, {dt.year}".format(dt = published)
    post['date'] = parsed_published
    if ('modified' in post):
        modified = datetime.strptime(post['modified'], '%Y-%m-%d %H:%M')
        parsed_modified = "{dt:%B} {dt.day}, {dt.year}".format(dt = modified)
        post['modified'] = parsed_modified
    return post

# write the parsed date string to each post

def parsepostdates(ob):
    parsed_ob = deepcopy(ob)
    parsed_posts = deepcopy(ob['posts'])
    for post in parsed_posts:
        published = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
        parsed_published = "{dt:%B} {dt.day}, {dt.year}".format(dt = published)
        post['date'] = parsed_published
        if ('modified' in post):
            modified = datetime.strptime(post['modified'], '%Y-%m-%d %H:%M')
            parsed_modified = "{dt:%B} {dt.day}, {dt.year}".format(dt = modified)
            post['modified'] = parsed_modified
    parsed_ob['posts'] = parsed_posts
    return parsed_ob

# tags

tags = collections.OrderedDict(
    sorted(tags.items(), key=lambda kv: -len(kv[1]['posts'])))
tags_list = {}
os.makedirs(os.path.join(output_directory, 'tags'), exist_ok=True)
for tag, tag_things in tags.items():
    # dump to tags_list
    tags_list[tag_things['name']] = {
        'length': len(tag_things['posts']), 'slug': tag}
    # sort the posts
    tags[tag]['posts'] = sorted(tags[tag]['posts'], key=cmp_to_key(sortmethod))
    # write to json
    tag_json = os.path.join(output_directory, '{}.json'.format(tag.strip('/')))
    dump(parsepostdates(tags[tag]), open(tag_json, 'w'))
    print("Wrote to {}".format(tag_json))

tags_json = os.path.join(output_directory, 'tags.json')
dump(tags_list, open(tags_json, 'w'))
print("Wrote to {}".format(tags_json))

# write to category.json
for cat, cat_posts in posts.items():
    posts[cat] = sorted(posts[cat], key=cmp_to_key(sortmethod))
    json_name = os.path.join(output_directory, '{}.json'.format(slugify(cat)))
    dump(parsepostdates({'name': cat, 'posts': posts[cat]}), open(json_name, 'w'))
    print("Wrote to {}".format(json_name))

posts_inside = sorted(posts_inside, key=cmp_to_key(sortmethod))
# write to cat/post.json
for single_post in posts_inside:
    json_name = os.path.join(output_directory, single_post['category'].lower(
    ), '{}.json'.format(single_post['slug'].split("/")[-2]))
    dump(parsepostdate_single(single_post), open(json_name, 'w'))
    print("Wrote to {}".format(json_name))
