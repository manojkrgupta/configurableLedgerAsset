import sys, os
import traceback
import json
from django.shortcuts import render
from django.http import HttpResponse
sys.path.insert(1, os.path.join(sys.path[0], '/app/corda5/lib/'))
from corda5Interface import  Corda5

# Create your views here.
def homePageView(request):
    data = request.GET.get('data', request.POST.get('data'))
    try:
      data_obj = json.loads(data)
      h = Corda5()

      result = h.verifier(data_obj)
    except Exception as e:
      print("Error while parsing json {}. {}. {}".format(data, e, traceback.format_exc()))
      return HttpResponse("Error parsing input. {} {}".format(e, data))

    if result:
      return HttpResponse("Success. Matched minimum quantity of data.")
    return HttpResponse("Failed to find enough quantity of instrument with the owner")


