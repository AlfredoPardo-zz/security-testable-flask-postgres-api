from flask_restplus import Api

api = Api(
    title='Security-testable Flask API',
    version='1.0',
    description='This API is able to be automatically tested by providing a swagger.json file to feed Vulnerability Assessment Tools like OWASP ZAP and Burp Suite. Additionally it is documented from the get-go which is important for an organized Software Development Life Cycle.',
    # All API metadatas
)
