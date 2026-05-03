import redis
import time

# Redis connection
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
# Default config
RATE_LIMIT = 5   # max requests
WINDOW = 60      # seconds

def check_rate_limit(key: str, limit: int = RATE_LIMIT, window: int = WINDOW):
    """
    Sliding window rate limiter using Redis sorted set.

    Args:
        key (str): unique identifier (e.g., user:1)
        limit (int): max requests allowed
        window (int): time window in seconds

    Returns:
        (bool, int): (allowed, retry_after_seconds)
    """
    current_time = int(time.time())
    window_start = current_time - window
    redis_key = f"rate:{key}"

    try:
        # Remove old requests
        r.zremrangebyscore(redis_key, 0, window_start)

        # Count requests
        request_count = r.zcard(redis_key)

        # Limit exceeded
        if request_count >= limit:
            oldest_request = r.zrange(redis_key, 0, 0, withscores=True)
            if oldest_request:
                oldest_time = int(oldest_request[0][1])
                retry_after = window - (current_time - oldest_time)
            else:
                retry_after = window
            return False, retry_after

        # Add request
        unique_member = f"{current_time}-{time.time_ns()}"
        r.zadd(redis_key, {unique_member: current_time})
        # Expiry
        r.expire(redis_key, window)
        return True, 0

    except Exception as e:
        print("Rate limiter error:", str(e))
        return True, 0