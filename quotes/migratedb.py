
import os
import django
from datetime import datetime
from dateutil import parser

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from dotenv import load_dotenv
from mongoengine import connect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from quoteapp.models import Author, Quote, Tag
from django.contrib.auth.models import User


load_dotenv()


# Load environment variables
mongo_user = os.getenv("USER")
mongodb_pass = os.getenv("PASS")
db_name = os.getenv("DB_NAME")
domain = os.getenv("DOMAIN")
uri = os.getenv("URI")


# Connect to MongoDB
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

# Access the specific database and collection
db = mongo_client[db_name]

# Get migration user
migration_user = User.objects.get(username="valentynarudenko")


def migrate_authors():
    authors_collection = db.authors
    for mongo_author in authors_collection.find():
        try:
            born_date = parser.parse(
                mongo_author['born_date']).strftime('%Y-%m-%d')
        except (ValueError, KeyError):
            born_date = None
        pg_author, created = Author.objects.get_or_create(
            fullname=mongo_author['fullname'],
            defaults={
                'born_date': born_date,
                'born_location': mongo_author['born_location'],
                'description': mongo_author['description'],
                'user': migration_user
            }
        )


def migrate_tags():
    tag_map = {}
    quotes_collection = db.quotes
    for mongo_quote in quotes_collection.find():
        for tag in mongo_quote['tags']:
            tag_name = tag["name"][:25]
            if tag_name not in tag_map:
                pg_tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'user': migration_user}
                )
                tag_map[tag_name] = pg_tag
    return tag_map


def migrate_quotes(tag_map):
    quotes_collection = db.quotes
    authors_collection = db.authors
    for mongo_quote in quotes_collection.find():
        print(mongo_quote)
        if 'author' in mongo_quote and mongo_quote['author']:
            mongo_author_id = mongo_quote['author']
        # if mongo_author_id:
            mongo_author = authors_collection.find_one(
                {"_id": mongo_author_id})
            if mongo_author:
                pg_author = Author.objects.get(
                    fullname=mongo_author['fullname'])

                pg_quote = Quote.objects.create(
                    author=pg_author,
                    quote=mongo_quote['quote'],
                    user=migration_user
                )

                for tag in mongo_quote['tags']:
                    tag_name = tag["name"][:25]
                    pg_tag = tag_map.get(tag_name)
                    if not pg_tag:
                        pg_tag = Tag.objects.get(name=tag_name)
                        print(pg_tag)
                        tag_map[tag_name] = pg_tag
                    pg_quote.tags.add(pg_tag)

                pg_quote.save()


def main():
    migrate_authors()
    tag_map = migrate_tags()
    migrate_quotes(tag_map)
    print("Migration completed successfully!")


if __name__ == "__main__":
    main()
