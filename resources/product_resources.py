from flask_restful import Resource, reqparse
from models.product import Product
from db import db
from flask import jsonify, request
from io import StringIO
import csv

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if product:
            return {'message': 'Product details', 'product': {'name' : product.name, 'price' : product.price}}
        return {'message': 'Product not found'}
    
    def put(self, product_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name of the product')
        parser.add_argument('price', type=float, help='Price of the product')
        
        args = parser.parse_args()
        product = Product.query.get(product_id)
        if product:
            # Update product fields
            product.name = args['name']
            product.price = args['price']

            db.session.commit()
            return {'message': 'Product updated successfully'}
        return {'message': 'Product not found'}

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted successfully'}
        return {'message': 'Product not found'}


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name of the product', required=True)
        parser.add_argument('price', type=float, help='Price of the product', required=True)

        args = parser.parse_args()

        # Create a new product instance
        new_product = Product(name=args['name'], price=args['price'])

        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()
        return {'message': 'Product added successfully', 'product_id': new_product.id}

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        # Convert products to a list of dictionaries or use a serializer
        return {'message': 'Product list', 'products': [{'name' : p.name, 'price' : p.price} for p in products]}


    def post(self):
        # Handle bulk upload using CSV file
        try:
            csv_file = request.files['file']
            if csv_file and csv_file.filename.endswith('.csv'):
                self.process_csv(csv_file)
                return {'message': 'Bulk upload successful'}
            else:
                return {'error': 'Invalid file format. Please upload a CSV file.'}, 400
        except Exception as e:
            return {'error': f'Error processing CSV file: {str(e)}'}, 500

    def process_csv(self, csv_file):
        csv_data = csv.reader(StringIO(csv_file.read().decode('utf-8')))
        header = next(csv_data)

        for row in csv_data:
            # Assuming CSV format: name,price
            print(row)
            name, price = row
            new_product = Product(name=name, price=float(price))
            db.session.add(new_product)

        db.session.commit()
