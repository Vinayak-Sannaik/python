from fastapi import FastAPI
from pydantic import BaseModel
from lru_cache import LRUCache
import time

app = FastAPI()

# LRU Cache with capacity of 3 users' feeds
cache = LRUCache(capacity=3)


class Post(BaseModel):
    userId: int
    content: str


# -----------------------------
# Fake Database
# -----------------------------
posts = [
    {"id": 1, "userId": 1, "content": "Hello"},
    {"id": 2, "userId": 2, "content": "FastAPI"},
    {"id": 3, "userId": 1, "content": "Learning Cache"},
    {"id": 4, "userId": 3, "content": "Python is awesome"},
    {"id": 5, "userId": 2, "content": "Building APIs"},
]

# Users each user follows
following = {
    1: [2, 3],
    2: [1],
    3: [1, 2]
}

# Followers of each user
followers = {
    1: [2, 3],
    2: [1, 3],
    3: [1]
}


@app.get("/")
async def home():
    return {"message": "Feed Cache Assignment"}


@app.get("/feed/{userId}")
async def get_feed(userId: int):
    start = time.perf_counter()

    # -----------------------------
    # Cache Lookup
    # -----------------------------
    cached_feed = cache.get(userId)

    if cached_feed is not None:
        end = time.perf_counter()

        return {
            "source": "CACHE",
            "cached": True,
            "latency_ms": round((end - start) * 1000, 2),
            "feed": cached_feed
        }

    # -----------------------------
    # Simulate Slow Database
    # -----------------------------
    time.sleep(0.1)

    following_users = following.get(userId, [])

    feed = []

    for post in posts:
        if post["userId"] in following_users:
            feed.append(post)

    # Store in cache
    cache.put(userId, feed)

    end = time.perf_counter()

    return {
        "source": "DATABASE",
        "cached": False,
        "latency_ms": round((end - start) * 1000, 2),
        "feed": feed
    }


@app.post("/post")
async def create_post(post: Post):
    new_post = {
        "id": len(posts) + 1,
        "userId": post.userId,
        "content": post.content
    }

    posts.append(new_post)

    # -----------------------------
    # Invalidate followers' caches
    # -----------------------------
    affected_followers = followers.get(post.userId, [])

    for follower in affected_followers:
        cache.invalidate(follower)

    return {
        "message": "Post created successfully.",
        "new_post": new_post,
        "invalidated_cache_for_users": affected_followers
    }


@app.get("/posts")
async def all_posts():
    return posts