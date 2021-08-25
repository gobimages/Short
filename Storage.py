from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
def GetStorage():
    table_service = TableService(account_name='g70us9siterecoveasrcache', account_key='fN2FX2GITMo/iL4xkRK5XrOWsy15s6iags9u9lRGReYa1iB0vJJXeiLTDeZC+FwmC2sY57+DZiw2sMpNAH1IIw==')
    if table_service.exists(table_name='Shortner'):
        print('Table exists')
    else:
        table_service.create_table('Shortner')
    return table_service

