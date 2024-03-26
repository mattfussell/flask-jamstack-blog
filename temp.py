@app.route('/')
def index():
  all_pages = (p for p in pages)  # Get all pages
  content_pages = [p for p in all_pages if p.meta.get('type') == 'content']
  blog_pages = [p for p in all_pages if p.meta.get('type') == 'blog']
  sorted_content = sorted(content_pages, key=lambda p: p.meta.get('content', ''), reverse=True)
  sorted_blogs = sorted(blog_pages, key=lambda p: p.meta.get('content', ''), reverse=True)
  return render_template('index.html', content=sorted_content, blogs=sorted_blogs)

# something to try later