def handler(request, context):
    if request.get('httpMethod') == 'POST':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"status": "POST received", "message": "Endpoint working"}'
        }
    else:
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"status": "Dating Matcher Agent is running", "agent": "lovefi-matcher", "message": "GET endpoint working"}'
        }
