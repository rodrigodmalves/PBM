import time
import json
import logging
import traceback
import PyPDF2
import os
import scraperwiki
import pickle5 as pickle
from ..locales import pt_br as msgs
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@csrf_exempt
def execute(request):
    try:
        if request.method == 'POST':  
            #nome = "Brigada"
            #pegar o arquivo dinamicamente (informando numa pagina web)
            # print(os.getcwd()) pra saber em que pasta tá
            file = open('DOE20200217.pdf', 'rb')
            response = pickle.load(file)
            xml = scraperwiki.pdftoxml(response)
            pdfToSoup = BeautifulSoup(xml)
            soupToArray = pdfToSoup.findAll('brigada')
            for line in soupToArray:
                print(line)
            return JsonResponse({'mensagem':'Integração Finalizada'}, safe=False, status=201)
        else:
            method = request.method
            formatted_response = msgs.LOG_METHOD_NOT_ALLOWED.format(method)
            logger.warn(formatted_response,
                        extra={'method': method})
            return JsonResponse({'msg': formatted_response}, status=405)

    except Exception as e:

        logger.error(msgs.LOG_INTERNAL_ERROR)
        logger.exception(e)

        print(traceback.format_exc())

        return JsonResponse({'msg': msgs.RESPONSE_INTERNAL_ERROR}, status=500)

