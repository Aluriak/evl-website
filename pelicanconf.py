#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Les Lanternistes'
SITENAME = 'Écovillage La Lanterne'
SITESUBTITLE = 'Un écovillage du Finistère !'

SITEURL = ''

READERS = {'html': None}

STATIC_PATHS = ['images']

# don't use {lang} in article names
ARTICLE_LANG_URL = '{slug}.html'
ARTICLE_LANG_SAVE_AS = '{slug}.html'
DRAFT_LANG_URL = 'drafts/{slug}.html'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}.html'
PAGE_LANG_URL = 'pages/{slug}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}.html'

# Menu configuration
# DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (
)

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'

# Theme
THEME = 'theme/elegant'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Notre plaquette', 'https://ecovillage-la-lanterne.net/files/plaquette.pdf'),
    ('Notre facebook', 'https://ecovillage-la-lanterne.net/files/nope.webp'),
    ('Notre twitter', 'https://ecovillage-la-lanterne.net/files/nope.webp'),
)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
          # ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
