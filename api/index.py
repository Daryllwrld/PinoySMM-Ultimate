from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# THE FACEBOOK MASTER DATA
# Everything here is dedicated to your FB Page
fb_stats = {
    "followers": 1000000,
    "reviews": 5000,
    "shares": 12000,
    "comments": 8000,
    "likes": 150000,
    "reach": 2000000
}

@app.route('/')
def home():
    return render_template('index.html', stats=fb_stats)

# FEATURE: Add Follower
@app.route('/add_follower', methods=['POST'])
def add_follower():
    fb_stats['followers'] += 1
    return jsonify({"new_count": fb_stats['followers']})

# FEATURE: Add Review
@app.route('/add_review', methods=['POST'])
def add_review():
    fb_stats['reviews'] += 1
    return jsonify({"new_count": fb_stats['reviews']})

# FEATURE: Add Share
@app.route('/add_share', methods=['POST'])
def add_share():
    fb_stats['shares'] += 1
    return jsonify({"new_count": fb_stats['shares']})

# FEATURE: Add Comment
@app.route('/add_comment', methods=['POST'])
def add_comment():
    fb_stats['comments'] += 1
    return jsonify({"new_count": fb_stats['comments']})
