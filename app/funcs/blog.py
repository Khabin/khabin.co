import os
import json
import contentful
import markdown

client = contentful.Client(
  os.environ.get('SPACE_ID'),
  os.environ.get('ACCESS_TOKEN')
)

"""
All blog post and podcasts
"""
def all_posts():

	# Blog Posts
	blog_posts = []
	for post in client.entries({'content_type': 'blog'}):
		fields = post.fields()
		date = fields['published']
		fields['id'] = post.id
		fields['date_raw'] = date.strftime("%Y-%m-%d 12:00:00")
		fields['date_published'] = date.strftime("%a, %-d %b %Y")
		fields['date_short'] = date.strftime("%Y-%m-%d")
		fields['date_sort'] = date.strftime("%Y%m%d")
		fields['html'] = markdown.markdown(fields['content'], extensions=['md_in_html'])
		fields['image'] = client.asset(fields['photo'].id).url()
		fields['url'] = "/blog/%s/%s" % (fields['date_short'], fields['slug'])
		# fields['type'] = 'Article'
		blog_posts.append(fields)

		print(fields['photo'])

	# Sort
	blog_posts = list(reversed(sorted(blog_posts, key = lambda i: i['date_sort'])))
	return blog_posts

"""
Find a single blog post
"""
def find_single(date, slug):
	response = False
	for post in all_posts():
		if post['date_short'] == date and post['slug'] == slug:
			response = post
	return response

def find_by_tag(name):
	all = all_posts()
	by_tag = []
	for post in all:
		print(post['tags'])
		if name in post['tags']:
			by_tag.append(post)

	print(by_tag)

	return by_tag
