from Storage import GetStorage
import logging
from azure.cosmosdb.table.common._http import HTTPResponse
import azure.functions as func
# the_connection_string = "DefaultEndpointsProtocol=https;AccountName=shortner;AccountKey=afWLw3WdSmkhVqbLT0gJ4P6oTbq2njGNghi12D4wtF26eayFZqFYF3cy8qW4L9TOmeiPLurV61OBclCwAoGdPg==;TableEndpoint=https://shortner.table.cosmos.azure.com:443/;"
# table_service = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string= the_connection_string)
table_service = GetStorage()
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    vanity = req.route_params.get('vanity')
    
    longurl = table_service.query_entities('Shortner', filter=f"RowKey eq '{vanity}'")
    response = longurl.items[0]['LongURL']
    return func.HttpResponse(
            status_code= 302, headers= {'Location': f'{response}'}
    )
  

