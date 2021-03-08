import os
import time

from flask import Flask, Blueprint, request, Response, render_template, make_response

from funcs.blog import *

CONFIG = {
	'expire_date':  60*60*24*365*2,
	'cache': time.time(),
}

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.before_request
def before_request():
	CONFIG['url'] = "https://khabin.co" + request.path
	app.jinja_env.cache = {}

@app.after_request
def after_request(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

"""
Home
"""
@app.route('/')
def index():
	CONFIG['posts'] = all_posts()[:2]
	response = make_response(render_template('index.html',
		SEO = {
			"title" : "Simple & Powerful Technology Products",
			"description": "Khabin LLC is a bootstrapped company making simple yet powerful technology products.",
			"type": "website"
		},
		CONFIG=CONFIG,
		HOME=True
	))
	return response

"""
Privacy
"""
@app.route('/privacy')
def privacy():
	response = make_response(render_template('privacy.html',
		SEO = {
			"title" : "Privacy Policy",
			"description": "This policy applies to all information collected or submitted on Khabin’s website and our apps for iPhone and any other devices and platforms.",
			"type": "website"
		},
		CONFIG=CONFIG
	))
	return response

"""
Support
"""
@app.route('/support')
def support():
	response = make_response(render_template('support.html',
		SEO = {
			"title" : "Support",
			"description": "Khabin LLC Support",
			"type": "website"
		},
		CONFIG=CONFIG
	))
	return response

"""
Terms
"""
@app.route('/terms')
def terms():
	response = make_response(render_template('terms.html',
		SEO = {
			"title" : "Terms of Use",
			"description": "Khabin LLC Terms of Use",
			"type": "website"
		},
		CONFIG=CONFIG,
	))
	return response

"""
Blog
"""
@app.route('/blog')
def blog():
	response = Response(render_template('blog.html',
		SEO = {
			"title" : "Company Blog",
			"description": "The offical company blog of Khabin LLC",
			"type": "website"
		},
		CONFIG=CONFIG,
		posts=all_posts(),
	), mimetype='text/html')
	return response

"""
Blog Post
"""
@app.route('/blog/<date>/<slug>')
def blog_post(date, slug):
	lookup = find_single(date, slug)
	if lookup:
		CONFIG['image'] = lookup['image']
		response = Response(render_template('blog-single.html', CONFIG=CONFIG, post=lookup, SEO={
			"title" : lookup['title'],
			"description": lookup['summary'],
			"type": "article"
		}), mimetype='text/html')
		response.set_cookie('ref', 'blog', CONFIG['expire_date'])
		return response
	else:
		return abort(404)

"""
Sitemap
"""
@app.route('/sitemap.txt', methods=['GET'])
def sitemap():
	resp = Response(render_template('sitemap.txt'), mimetype='text/plain')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

"""
Robots
"""
@app.route('/robots.txt', methods=['GET'])
def robots():
	resp = Response(render_template('robots.txt'), mimetype='text/plain')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

"""
Blog Sitemap
"""
@app.route('/sitemap/blog.txt')
def blog_sitemap():
	map = ""
	for post in all_posts():
		map += "https://khabin.co/blog/" + post['slug'] + '\n'

	resp = Response(map, mimetype='text/plain')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80, debug=True)
