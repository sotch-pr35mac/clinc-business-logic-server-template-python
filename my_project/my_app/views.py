"""
Create your views here.
"""
import json
from hotels import find_express_deal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # pylint: disable=unused-import


class BusinessLogic(APIView):
    """
    This is an example of adding/modifying slots using business logic, using
    the `hotel_booking` competency.
    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.
        """
        # print out the Business Logic payload from Clinc
        print json.dumps(request.data, indent=2)

        # Assign hotel_booking variables
        if '_TRANSACTION_TYPE_' in request.data['slots']:
            transaction_type = request.data['slots']['_TRANSACTION_TYPE_']['candidates'][0]['tokens']
        else:
            transaction_type = None

        if '_LOCATION_' in request.data['slots']:
            location = request.data['slots']['_LOCATION_']['candidates'][0]['tokens']
        else:
            location = None

        if '_PRICE_' in request.data['slots']:
            price = request.data['slots']['_PRICE_']['candidates'][0]['tokens']
        else:
            price = None

        # this loop sets all of the _SLOTS_ to have a `"resovled": 1` so they will be kept
        # through each turn of the conversation.  Currently, each turn the slots are sent
        # with a `"resolved": -1`, so they need to be reset each time, however, they are
        # changing to be persistent based on their resolved status in an update coming soon
        for (slot, slot_data) in request.data['slots'].iteritems():
            if 'candidates' in request.data['slots'][slot]:
                for candidate in range(len(slot_data['candidates'])):
                    request.data['slots'][slot]['candidates'][candidate]['resolved'] = 1
                    if slot <> '_DATE_':
                        request.data['slots'][slot]['candidates'][candidate]['value'] = \
                            request.data['slots'][slot]['candidates'][candidate]['tokens']
            else:
                request.data['slots'][slot]['resolved'] = 1

        if transaction_type == 'express deal':
            if location and price:
                # This is our magical API call to find express deals
                hotel = find_express_deal(location, price)
                if hotel:
                    # This is how to add new _SLOTS_ to the business logic json
                    _HOTEL_RATING_ = {
                        "candidates": [
                            {
                                "resolved": 1,
                                "value": hotel['hotel_rating']
                            }
                        ],
                        "required_matches": "EQ 1",
                        "type": "string"
                    }
                    request.data['slots']['_HOTEL_RATING_'] = _HOTEL_RATING_
                    _HOTEL_TYPE_ = {
                        "candidates": [
                            {
                                "resolved": 1,
                                "value": hotel['hotel_type']
                            }
                        ],
                        "required_matches": "EQ 1",
                        "type": "string"
                    }
                    request.data['slots']['_HOTEL_TYPE_'] = _HOTEL_TYPE_

        # print out the modified business logic payload
        print "Running through the webhook"
        print json.dumps(request.data, indent=2)

        # return the modified business logic payload
        return Response(request.data)

