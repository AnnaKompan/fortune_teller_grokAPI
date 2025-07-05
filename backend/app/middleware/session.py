from starlette.middleware.base import BaseHTTPMiddleware
from itsdangerous import URLSafeSerializer
import os

serializer = URLSafeSerializer(os.getenv("SESSION_SECRET"))

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        cookie = request.cookies.get("session")
        try:
            data = serializer.loads(cookie) if cookie else {}
            request.state.user_id = data.get("user_id")
        except:
            request.state.user_id = None
        return await call_next(request)
