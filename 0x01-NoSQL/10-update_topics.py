#!/usr/bin/env python3
"""
topic change
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    multi row update
    """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
