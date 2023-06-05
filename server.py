import sys, os
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask_htmx import HTMX

# config: flat pages
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']

# config: freezer
FREEZER_RELATIVE_URLS = True

# config: app
app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)
htmx = HTMX(app)

# routing: home page
@app.route('/')
def index():
    return render_template('index.html', pages=pages)


# routing: flat pages
@app.route('/blog/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    title = f"FJB | {page.meta.get('title')}" if not page.meta.get('content') else 'FJB'
    return render_template('page.html', pages=pages, page=page, title=title)


# main: remap server port
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(port=8000, debug=True)