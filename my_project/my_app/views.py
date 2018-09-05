"""
Create your views here.
"""
import json
import os
import sys
from ingredients import (
    get_ingredients,
    get_calories
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # pylint: disable=unused-import


class BusinessLogic(APIView):
    """
    This is an example of adding/modifying slots using business logic, using
    the QSR AI Version.
    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.
        """

        # ingredients_list logic
        if (request.data['state'] == 'ingredients_list'):

            ingredients_list = []

            if '_FOOD_MENU_' in request.data['slots']:
                for food_item in request.data['slots']['_FOOD_MENU_']['values']:
                    food_item['resolved'] = 1
                    food_item['value'] = food_item['tokens']

                    # magical API call
                    food_item['ingredients'] = get_ingredients(food_item['tokens'])

        # food_order logic
        if (request.data['state'] == 'food_order'):

            calorie_count = 0

            if '_FOOD_MENU_' in request.data['slots']:
                for food_item in request.data['slots']['_FOOD_MENU_']['values']:
                    if 'resolved' in food_item and food_item['resolved'] == -1:
                        food_item['resolved'] = 1
                        food_item['value'] = food_item['tokens']

                    # magical API call
                    calorie_count = calorie_count + get_calories(food_item['tokens'])

            request.data['slots']['_CALORIE_TOTAL_'] = {
                'type': "string",
                'values': [
                    {
                        "value": calorie_count,
                        "tokens": calorie_count,
                        "resolved": 1,
                    }
                ]
             }

        # return the business logic payload
        return Response(request.data)

