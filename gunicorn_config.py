workers = 4
bind = "0.0.0.0:8000" 

# Use gevent worker type for better concurrency (optional, install gevent first)
worker_class = "gevent"

# Set the maximum requests per worker to avoid potential memory leaks
max_requests = 1000
max_requests_jitter = 100

