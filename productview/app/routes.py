from flask import render_template, jsonify, abort
from .models import Item, CodesTypes

import logging
logger = logging.getLogger(__name__)

def register_routes(app):

    @app.route('/index')
    def index():
        return render_template('index.html')
    
    @app.route('/<item_id>')
    def show_product(item_id):
        item = Item.get_by_id(item_id)
        
        if not item:
            abort(404, description="Item not found")
        
        template_type = item.get('template_type', 'default')
        template_name = f"items_{template_type}.html"
        
        return render_template(template_name, item=item)
    
    @app.route('/api/<item_id>')
    def api_item(item_id):
        item = Item.get_by_id(item_id)
        
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        return jsonify({'Item': item})
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error=error), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error=error), 500