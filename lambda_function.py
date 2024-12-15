import boto3
from botocore.exceptions import ClientError

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')

# Nombre de la tabla DynamoDB
TABLE_NAME = "ACCJJR"

def lambda_handler(event, context):
    # Inicializar la tabla
    table = dynamodb.Table(TABLE_NAME)
    
    # Podemos tener muchos contadores dependiendo del ID que enviemos
    key = {"id": event["id"]}  
    
    try:
        # Incrementar el valor en 1
        response = table.update_item(
            Key=key,
            UpdateExpression="SET visit_count = if_not_exists(visit_count, :start) + :increment",
            ExpressionAttributeValues={
                ":start": 0,         # Valor inicial si no existe
                ":increment": 1      # Incremento
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            "statusCode": 200,
            "body": response["Attributes"]
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            "statusCode": 500,
            "body": "Error actualizando DynamoDB"
        }
