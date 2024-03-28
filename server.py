import sys, os
from flask import Flask, render_template, render_template_string
from flask_flatpages import FlatPages
from flask_flatpages.utils import pygmented_markdown, pygments_style_defs
from flask_frozen import Freezer
from flask_htmx import HTMX

# config: flat pages
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {
        'linenums': 'True',
        'guess_lang': 'True',
        #'pygments_style': 'friendly',
        #'noclasses': 'False'
    }
}

def my_renderer(text):
    prerendered_body = render_template_string(text)
    return pygmented_markdown(prerendered_body)


# config: freezer
FREEZER_RELATIVE_URLS = True

# config: app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['FLATPAGES_HTML_RENDERER'] = my_renderer
pages = FlatPages(app)
freezer = Freezer(app)
htmx = HTMX(app)


# routing: home page
@app.route('/')
def index():
    content = (p for p in pages if 'content' in p.meta)
    blogs = (p for p in pages if 'blog' in p.meta)
    sorted_blogs = sorted(blogs, key=lambda p: p.meta['date'], reverse=True)
    return render_template('index.html', content=content, pages=sorted_blogs)


# routing: flat pages
@app.route('/blog/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    title = f"FJB | {page.meta.get('title')}" if not page.meta.get('content') else 'FJB'
    return render_template('page.html', pages=pages, page=page, title=title)


# https://flask-flatpages.readthedocs.io/en/latest/
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}


# main: remap server port
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(port=8000, debug=True)