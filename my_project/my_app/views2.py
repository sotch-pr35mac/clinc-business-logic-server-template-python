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
    This is an exmaple of how Business Logic Transitions work.
    Please note: You NEED to have set up the business logic transition in Spotlight
    for the transition to work.
    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.
        """
        #print out the Business Logic payload from Clinc
        print json.dumps(request.data, indent=2)

        #overwrite state for state transition example
        if request.data['state'] == "clean_hello":
            request.data['state'] = "clean_goodbye"

        #print out modified business logic payload

        print "Running through the webhook"
        print json.dumps(request.data, indent=2)

        return Response(request.data)

