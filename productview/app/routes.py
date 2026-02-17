from flask import render_template, jsonify, abort
from .models import Product

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/product/<int:product_id>')
    def show_product(product_id):
        product = Product.get_by_id(product_id)
        
        if not product:
            abort(404, description="Product not found")
        
        template_type = product.get('template_type', 'default')
        template_name = f"product_{template_type}.html"
        
        return render_template(template_name, product=product)
    
    @app.route('/api/product/<int:product_id>')
    def api_product(product_id):
        product = Product.get_by_id(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product})
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error=error), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error=error), 500