from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["app_name", "method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["app_name", "endpoint"],
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5)
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        route = request.scope.get("route")
        endpoint = route.path if route else "unknown"

        # Skip metrics endpoint itself
        if endpoint != "/metrics":
            REQUEST_COUNT.labels(
                app_name="redirect_service",
                method=request.method,
                endpoint=endpoint,
                http_status=str(response.status_code)
            ).inc()

            duration = time.perf_counter() - start_time
            REQUEST_LATENCY.labels(
                app_name="redirect_service",
                endpoint=endpoint
            ).observe(duration)

        return response
