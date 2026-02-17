"""
Database Connection Test
Tests MongoDB connectivity using the production DB connection
"""

from apps.db.mongo import db


def test_mongo_connection():
    print("🔍 Testing MongoDB connection...")

    try:
        # Simple ping via listing collections
        collections = db.list_collection_names()

        print("✅ MongoDB connected successfully")
        print("📦 Collections:", collections)

    except Exception as e:
        print("❌ MongoDB connection failed")
        raise e


if __name__ == "__main__":
    test_mongo_connection()
