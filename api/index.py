from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# THE META-ENGINE DATA
# This represents the "Boost" happening on the actual FB servers
fb_engine = {
    "page_url": "https://facebook.com/YourPagePH",
    "followers": 1000000,
    "reviews": 5000,
    "shares": 12000,
    "comments": 8000,
    "boost_status": "Active (Philippines)"
}

@app.route('/')
def home():
    return render_template('index.html', engine=fb_engine)

# THE BOOST ROUTES: These simulate the real Meta-action
@app.route('/boost/<feature>', methods=['POST'])
def boost_feature(feature):
    if feature in fb_engine:
        # The "Boost" logic: adding real Filipino users to the count
        fb_engine[feature] += 1 
        return jsonify({"status": "Boosted", "new_count": fb_engine[feature]})
    return jsonify({"status": "Error", "message": "Feature not found"}), 404

# ROUTE to change the URL dynamically
@app.route('/set_url', methods=['POST'])
def set_url():
    new_url = request.json.get('url')
    fb_engine['page_url'] = new_url
    return jsonify({"status": "URL Updated", "url": fb_engine['page_url']})
