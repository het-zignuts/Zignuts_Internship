from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        print(f"\nRequest Logs: \n Method: {request.method} \n Request URL: {request.url} \n Request Headers: {request.headers} \n Request Body: {await request.body()}\n Query Params: {dict(request.query_params)} \n Client: {request.client} \n Path Params: {request.path_params}")
        
        start_time = time.time()       
        response = await call_next(request)
        process_time = time.time() - start_time

        print(f"\nResponse Logs: \n Response Status: {response.status_code} \n Response Headers: {response.headers} \n Response Media Type: {response.media_type} \n")
        
        print(f"Processing Time: {process_time:.5f} seconds")

        return response