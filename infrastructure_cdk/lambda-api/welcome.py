import json

def handler(event, context):
    print(f'request: {json.dumps(event)}')
    return {
        'statusCode': 200,
        'header': {
            'Context-Type': 'text/plain'
        },
        'body': f'Hello {event['queryStringParameter']['name']}. You got here!'
    }
