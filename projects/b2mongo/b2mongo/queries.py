# Connexion
from pymongo import MongoClient
from collections import Counter


client = MongoClient('mongodb://localhost:27017/')
db     = client['books_toscrape']
books  = db['books']

total = books.count_documents({})
print(f"Total livres: {total}")

# Trouver les livres les mieux notés
top_rated = books.find({'rating': 5}).limit(10)
for book in top_rated:
    print(f"{book['title']} - {book['price_incl_tax']}£")

categories = [book['category'] for book in books.find({}, {'category': 1})]
print(Counter(categories))

# Prix moyen par catégorie
pipeline = [
    {'$group': {
        '_id'       : '$category',
        'avg_price' : {'$avg': '$price_incl_tax'},
        'count'     : {'$sum': 1}
    }},
    {'$sort': {'avg_price': -1}}
]
results = books.aggregate(pipeline)
for result in results:
    print(f"{result['_id']}: {result['avg_price']:.2f}£ ({result['count']} livres)")

# Livres en stock avec bon rating
in_stock = books.find({
    'availability': {'$gt' : 0},
    'rating'      : {'$gte': 4}
}).sort('price_incl_tax', 1)

# Recherche full-text
books.create_index([('title', 'text'), ('description', 'text')])
results = books.find({'$text': {'$search': 'python programming'}})

# Statistiques globales
stats = books.aggregate([
    {'$group': {
        '_id'       : None,
        'total'     : {'$sum': 1},
        'avg_price' : {'$avg': '$price_incl_tax'},
        'max_price' : {'$max': '$price_incl_tax'},
        'min_price' : {'$min': '$price_incl_tax'},
        'avg_rating': {'$avg': '$rating'}
    }}
])
print(list(stats))