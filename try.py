from flask import request
print(request.headers.get('X-Forwarded-For', request.remote_addr))