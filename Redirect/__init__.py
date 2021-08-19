import logging
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import azure.functions as func
the_connection_string = "DefaultEndpointsProtocol=https;AccountName=shortner;AccountKey=h74uGbZ4Ud37C0Wo5wAvM5ZIhsSGCcAVKXtMoGkOp6fjJ3emGAm5Wzn1PRJ79g2uK09Es9bAXPib7G1kWqxzFA==;TableEndpoint=https://shortner.table.cosmos.azure.com:443/;"
table_service = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string= the_connection_string)
#table_service = TableService(account_name='shortner', account_key='WnJudA0n088k8u8wyHtvBV8rrgs4CHwp9avKEVnWFERIruu7gumgj4Dfqa0ICvLWv7WA2S3Fb7NWqUzRTKsogw==')
if table_service.exists(table_name='Shortner'):
            print('Table exists')
else:
    table_service.create_table('Shortner')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    vanity = req.route_params.get('vanity')

    longurl = table_service.query_entities('Shortner', filter=f"RowKey eq '{vanity}'")
    response = {'location': longurl.items[0]['LongURL']}
    return func.HttpResponse(
            status_code=302, headers=response
    )
  

