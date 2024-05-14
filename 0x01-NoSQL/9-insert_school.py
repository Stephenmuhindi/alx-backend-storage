#!/usr/bin/env python3
"""
utility function to insert documents
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    school insert
    """
    return mongo_collection.insert_one(kwargs).inserted_id
