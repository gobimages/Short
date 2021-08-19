
#Cleanup this 
import logging
from datetime import datetime
import short_url
import uuid
import json
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import azure.functions as func
import requests
domain = 'http://localhost:7071/api/Redirect/'
the_connection_string = "DefaultEndpointsProtocol=https;AccountName=shortner;AccountKey=afWLw3WdSmkhVqbLT0gJ4P6oTbq2njGNghi12D4wtF26eayFZqFYF3cy8qW4L9TOmeiPLurV61OBclCwAoGdPg==;TableEndpoint=https://shortner.table.cosmos.azure.com:443/;"
table_service = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string= the_connection_string)
#table_service = TableService(account_name='shortner', account_key='WnJudA0n088k8u8wyHtvBV8rrgs4CHwp9avKEVnWFERIruu7gumgj4Dfqa0ICvLWv7WA2S3Fb7NWqUzRTKsogw==')
#three_months = parser.isoparse((datetime.now() + relativedelta(months=-1))) 

if table_service.exists(table_name='Shortner'):
            print('Table exists')
else:
    table_service.create_table('Shortner')

def main(req: func.HttpRequest) -> func.HttpResponse:
    #accessTokenPayLoad = req.headers.get("Authorization").replace("Bearer ","").split(".")[1]
    #data = base64.b64decode(accessTokenPayLoad + '==')
    #jsonObj = json.loads(data)
    #upn = jsonObj['upn']
    logging.info('Python HTTP trigger function processed a request.')
    Today = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    name = req.params.get('name')
    vanity = req.params.get('vanity')
    upn = req.params.get('upn')
    
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    
    if req.method == 'GET':
        Getmyitems = table_service.query_entities('Shortner', filter=f"Username eq '{upn}'", select=f"{'LongURL'}, {'ShortURL'}")
        return func.HttpResponse(json.dumps(Getmyitems.items), status_code=200)
        
    if name and req.method == 'POST' and not vanity:
        Checkurl = req.params.get('name')
        api = "a635b902d307181320ed0d4b604f365c2de73b40279b5e64a74c5341fe6b576a"
        response = requests.post('https://www.virustotal.com/api/v3/urls', headers={'x-apikey': f'{api}'}, data={'url': f'{Checkurl}'})
        gobi = response.json()
        id = gobi['data']['id']
        output = requests.get(f'https://www.virustotal.com/api/v3/analyses/{id}', headers={'x-apikey': f'{api}'})
        result = output.json()['data']['attributes']['stats']['harmless']
        if int(result) < int(90):
            #upn = jsonObj['upn']
            task = Entity()
            task.PartitionKey = 'ODSCode'
            url= short_url.encode_url(int(uuid.uuid4()))[:6]
            task.RowKey = str(url)
            task.CreatedDate = Today
            task.LongURL = req.params.get('name')
            task.Username = upn
            task.ShortURL = domain+url
            table_service.insert_entity('Shortner', task)
            return func.HttpResponse(f"{domain+url}")
        else:
            return func.HttpResponse("URL was found to be Malicious")
    if name and vanity and req.method == 'POST':
        try:
            vanvalue = table_service.query_entities('Shortner', filter=f"RowKey eq '{vanity}'")
            if vanity == str(vanvalue.items[0]['RowKey']):
                return func.HttpResponse(f"{vanity} Already exists")
        except IndexError:
            #upn = jsonObj['upn']
            task = Entity()
            task.PartitionKey = 'ODSCode'
            task.Username = upn
            task.CreatedDate = Today
            task.RowKey = str(vanity)
            task.LongURL = req.params.get('name')
            task.ShortURL = domain+vanity
            table_service.insert_entity('Shortner', task)
            return func.HttpResponse(f"{domain+vanity}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
