import boto3
import json

from decimal import Decimal


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ACCJJR')

    # Obtener el contador actual
    response = table.get_item(Key={'id': 'contador'})
    visitas = int(response['Item']['visitas']) + 1  # Convertimos Decimal a int

    # Actualizar el contador en la tabla
    table.update_item(
        Key={'id': 'contador'},
        UpdateExpression='SET visitas = :val',
        ExpressionAttributeValues={':val': Decimal(visitas)}  # Convertimos de vuelta a Decimal para DynamoDB
    )

    # Respuesta
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'visitas': visitas})  # JSON serializable
    }
