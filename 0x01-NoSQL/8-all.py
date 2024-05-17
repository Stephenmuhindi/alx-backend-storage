#!/usr/bin/env python3
"""
utility function
"""
import pymongo


def list_all(mongo_collection):
    """
    list all function
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
