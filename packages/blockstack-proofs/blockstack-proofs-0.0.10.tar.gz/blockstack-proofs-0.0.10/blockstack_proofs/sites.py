# -*- coding: utf-8 -*-
"""
    proofchecker
    ~~~~~
    :copyright: (c) 2014-2016 by Halfmoon Labs, Inc.
    :copyright: (c) 2016 blockstack.org
    :license: MIT, see LICENSE for more details.
"""

SITES = {
    'twitter': {
        'base_url': 'https://twitter.com/',
        'html_query': {
            'class': 'permalink-inner permalink-tweet-container'
        }
    },
    'facebook': {
        'base_url': 'https://facebook.com/',
        'html_query': {
            'class': '_5pbx userContent'
        }
    },
    'facebook-www': {
        'base_url': 'https://www.facebook.com/',
        'html_query': {
            'class': '_5pbx userContent'
        }
    },
    'github': {
        'base_url': 'https://gist.github.com/',
        'html_query': {
            'class': 'blob-wrapper data type-markdown js-blob-data'
        }
    },
    'hackernews': {
        'base_url': 'https://news.ycombinator.com/user?id=',
        'html_query': {
        }
    },
    'instagram-http': {
        'base_url': 'https://instagram.com/',
        'html_query': {
        },
        'base_url_enough': True,

    },
    'instagram': {
        'base_url': 'https://www.instagram.com/',
        'html_query': {
        },
        'base_url_enough': True,
    },
    'linkedin': {
        'base_url': 'https://www.linkedin.com/feed/update/',
        'html_query': {
        },
        'base_url_enough': True
    },
    'stackoverflow': {
        'base_url': 'http://stackoverflow.com/users/',
        'html_query': {
        }
    },
    'angellist': {
        'base_url': 'https://angel.co/',
        'html_query': {
        }
    },
}

UNSUPPORTED_SITES = {
    'googleplus': {
        'base_url': 'https://plus.google.com/',
        'html_query': {
            'title': True
        }
    },
    'reddit': {
        'base_url': 'http://www.reddit.com/user/',
        'html_query': {
        }
    }
}
