#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Les Lanternistes'
SITENAME = 'Écovillage La Lanterne'
SITESUBTITLE = 'Un écovillage du Finistère !'

SITEURL = ''

READERS = {'html': None}

STATIC_PATHS = ['images']

# Simpler urls for pages, and don't use {lang} in article names
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
ARTICLE_LANG_URL = 'blog/{slug}.html'
ARTICLE_LANG_SAVE_AS = 'blog/{slug}.html'
DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'
DRAFT_LANG_URL = 'drafts/{slug}.html'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_LANG_URL = '{slug}.html'
PAGE_LANG_SAVE_AS = '{slug}.html'
AUTHOR_SAVE_AS = ''  # no author page

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
LANDING_PAGE_TITLE = "Bienvenue sur le site de l'Écovillage la Lanterne"  # see https://elegant.oncrashreboot.com/write-welcome-message for doc
FEATURED_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/0/0e/Sch%C3%A9ma_du_d%C3%A9veloppement_durable.svg'
PROJECTS_TITLE = 'Accès rapides'  # see https://elegant.oncrashreboot.com/projects-list for doc
PROJECTS = [
    {
        'name': 'Notre plaquette',
        'url': 'https://ecovillage-la-lanterne.net/files/plaquette.pdf',
        'description': 'Pour une présentation formelle du projet',
    },
    {
        'name': 'Notre facebook',
        'url': 'https://ecovillage-la-lanterne.net/files/nope.webp',
        'description': 'lalala',
    },
    {
        'name': 'Notre twitter',
        'url': 'https://ecovillage-la-lanterne.net/files/nope.webp',
        'description': 'lululu',
    },
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (
    # ('Notre plaquette', 'https://ecovillage-la-lanterne.net/files/plaquette.pdf'),
    # ('Notre facebook', 'https://ecovillage-la-lanterne.net/files/nope.webp'),
    # ('Notre twitter', 'https://ecovillage-la-lanterne.net/files/nope.webp'),
# )

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
          # ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
