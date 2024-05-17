#!/usr/bin/env python3
"""
topic search
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    topic to find
    """
    return mongo_collection.find({"topics": topic})
