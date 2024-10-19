import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import gzip
import json

from scraper import get_total_pages, scrape_wallpapers

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/', methods=['GET'])
def api_documentation():
    """Provide basic API documentation"""
    return jsonify({
        "endpoints": {
            "/api/search": {
                "method": "GET",
                "parameters": {
                    "q": "Search term (required)",
                    "page": "Page number (optional, default: 1)",
                    "limit": "Number of wallpapers to return (optional, default: all on page)"
                },
                "description": "Search for wallpapers"
            },
            "/api/total_pages": {
                "method": "GET",
                "parameters": {
                    "q": "Search term (required)"
                },
                "description": "Get total number of pages for a search term"
            }
        }
    })

@app.route('/api/search', methods=['GET'])
def search_wallpapers():
    search_term = request.args.get('q', '').strip()
    page = request.args.get('page', '1')
    limit = request.args.get('limit')

    if not search_term:
        return jsonify({"error": "Search term is required"}), 400

    try:
        page = int(page)
        if page < 1:
            return jsonify({"error": "Page number must be a positive integer"}), 400
    except ValueError:
        return jsonify({"error": "Invalid page number"}), 400

    if limit:
        try:
            limit = int(limit)
            if limit < 1:
                return jsonify({"error": "Limit must be a positive integer"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit"}), 400

    total_pages = get_total_pages(search_term)
    
    if page > total_pages:
        return jsonify({"error": f"Page number exceeds total pages. Max page: {total_pages}"}), 404

    wallpapers = scrape_wallpapers(search_term, page=page, limit=limit)

    response_data = {
        "page": page,
        "total_pages": total_pages,
        "results_on_page": len(wallpapers),
        "wallpapers": wallpapers,
    }

    json_data = json.dumps(response_data)
    gzip_data = gzip.compress(json_data.encode('utf-8'))

    response = Response(gzip_data)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/total_pages', methods=['GET'])
def get_total_pages_api():
    search_term = request.args.get('q', '').strip()
    if not search_term:
        return jsonify({"error": "Search term is required"}), 400

    total_pages = get_total_pages(search_term)
    return jsonify({"total_pages": total_pages})

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
            host=os.getenv('FLASK_HOST', '127.0.0.1'),
            port=int(os.getenv('FLASK_PORT', 5000)))
