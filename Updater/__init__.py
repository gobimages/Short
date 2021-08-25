import logging
from datetime import datetime
import json
import azure.functions as func
from Storage import GetStorage
# the_connection_string = "DefaultEndpointsProtocol=https;AccountName=shortner;AccountKey=afWLw3WdSmkhVqbLT0gJ4P6oTbq2njGNghi12D4wtF26eayFZqFYF3cy8qW4L9TOmeiPLurV61OBclCwAoGdPg==;TableEndpoint=https://shortner.table.cosmos.azure.com:443/;"
# table_service = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string= the_connection_string)
table_service = GetStorage()
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    #table_service = TableService(account_name='shortner', account_key='WnJudA0n088k8u8wyHtvBV8rrgs4CHwp9avKEVnWFERIruu7gumgj4Dfqa0ICvLWv7WA2S3Fb7NWqUzRTKsogw==')
    delete = req.params.get('delete')
    update = req.params.get('update')
    upn = req.params.get('upn')
    Today = (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
    if not delete:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            delete = req_body.get('delete')
    #accessTokenPayLoad = req.headers.get("Authorization").replace("Bearer ","").split(".")[1]
    #data = base64.b64decode(accessTokenPayLoad + '==')
    #jsonObj = json.loads(data)
    #upn = jsonObj['upn']
    if delete and req.method == 'POST':
       
        username = table_service.query_entities('Shortner', filter=f"ShortURL eq '{delete}'")
        if username.items[0]['Username'] == upn:
            remove = Entity()
            remove.PartitionKey = username.items[0]['PartitionKey']
            remove.RowKey = username.items[0]['RowKey']
            remove.LongURL = username.items[0]['LongURL']
            remove.Username = username.items[0]['Username']
            remove.ShortURL = username.items[0]['ShortURL']
            remove.CreatedDate = username.items[0]['CreatedDate']
            table_service.insert_entity('tasktable', remove)
            table_service.delete_entity('Shortner', username.items[0]['PartitionKey'], username.items[0]['RowKey'])
            return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a delete in the query string or in the request body for a personalized response.",
             status_code=200)
        else:
            logging.info("Cannot Find ShortURL")
    
    
    if update and req.method == 'POST':
        updater = table_service.query_entities('Shortner', filter=f"LongURL eq '{update}'")

        task = {'PartitionKey': f"'{updater.items[0]['PartitionKey']}'", 'RowKey': f"'{updater.items[0]['RowKey']}'",
        'LongURL': f"'{updater.items[0]['LongURL']}'", 'ShortURL': f"'{updater.items[0]['ShortURL']}'", 'CreatedDate': f"'{updater.items[0]['CreatedDate']}'"}
        table_service.update_entity('tasktable', task)

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a delete in the query string or in the request body for a personalized response.",
             status_code=200
        )
