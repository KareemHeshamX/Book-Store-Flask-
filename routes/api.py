from flask import Blueprint, request, jsonify
from models import Book

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/books')
def books():
    """JSON endpoint for live search."""
    category = request.args.getlist('category')
    book_format = request.args.getlist('format')
    search = request.args.get('search', '')

    query = Book.query
    if category:
        query = query.filter(Book.category.in_(category))
    if book_format:
        query = query.filter(Book.book_format.in_(book_format))
    if search:
        query = query.filter(
            (Book.title.ilike(f'%{search}%')) | (Book.author.ilike(f'%{search}%'))
        )

    books = query.all()
    return jsonify([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'price': b.price,
        'category': b.category,
        'book_format': b.book_format,
        'image_url': b.image_url
    } for b in books])
