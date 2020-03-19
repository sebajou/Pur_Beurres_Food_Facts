# -*- coding: utf-8 -*-

# import
import requests
import json
import mysql.connector


class CloserWord:
    """Compare word from category name and product_name_fr in tables Food_list
    and delivery an indice of closest """

    # Pick product_name_fr from Food_list table for a given category
    def food_list_extract(self, category):

        prod_cat = (product_name_fr, category)
        return prod_cat

    # Extract words in a list from product_name_fr in tables Food_list
    def extract_word(self, prod_cat):
        # Collect info from prod_cat
        product_name_fr, category = prod_cat

        # List with all the words from product_name_fr in table Food list
        product_name_list = []

        # Extract word from sentence product_name_fr
        product_name_list = product_name_fr.split()

        # Return word and associated category
        prod_name_list_cat = (product_name_list, category)
        return prod_name_list_cat

    # Compare the similarity of extracted word
    # and give an indice of similiraty (1 closest, 5 farer)
    def similar(self, prod_name_list_cat):
        pass


"""Close = CloserWord()
product_name_fr = Close.food_list_extract()
Close.extract_word(product_name_fr)
Close.similar()"""
