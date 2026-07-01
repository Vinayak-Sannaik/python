# Feed Cache Assignment – Cache Aside Pattern using LRU Cache

## Objective

This project demonstrates how to implement the **Cache-Aside** caching pattern using a custom **LRU (Least Recently Used) Cache** in a FastAPI application.

The application simulates a social media feed where users can view posts from people they follow. Instead of querying the database for every request, the feed is cached to improve response time.

---

# Tech Stack

- Python 3.x
- FastAPI
- Uvicorn
- Custom LRU Cache
- In-memory database

---

# Project Structure

```
.
├── main.py             
├── lru_cache.py       
├── lfu_cache.py
├── test_lru.py        
├── test_lfu.py         
└── README.md
```

---

# API Endpoints

## Get Feed

```
GET /feed/{userId}
```

Returns the feed for a user.

### Cache Miss Flow

```
Client
   |
   |
GET /feed/1
   |
   |
Cache Lookup
   |
Cache Miss
   |
Read Database
   |
Store in Cache
   |
Return Feed
```

### Cache Hit Flow

```
Client
   |
GET /feed/1
   |
Cache Lookup
   |
Cache Hit
   |
Return Cached Feed
```

---

## Create Post

```
POST /post
```

Example Request

```json
{
    "userId": 2,
    "content": "Learning FastAPI Cache"
}
```

Flow

```
Create Post
      |
Store in Database
      |
Find Followers
      |
Invalidate Cached Feeds
      |
Return Success
```

---

# Cache-Aside Pattern

This project uses the **Cache-Aside** strategy.

### Read

```
Client
   |
GET /feed
   |
Check Cache
   |
 +----------+
 | Hit      |
 |          |
Return Data |
 +----------+

 +----------+
 | Miss     |
 |          |
Read DB     |
Store Cache |
Return Data |
 +----------+
```

### Write

```
POST /post
      |
Update Database
      |
Invalidate Followers Cache
```

The cache is **not updated immediately**. It is simply invalidated. The next read repopulates the cache with fresh data.

---

# LRU Cache

The cache is implemented from scratch using

- HashMap (Dictionary)
- Doubly Linked List

Supported Operations

- get(key)
- put(key, value)
- invalidate(key)

Time Complexity

| Operation | Complexity |
|------------|------------|
| get() | O(1) |
| put() | O(1) |
| invalidate() | O(1) |

Space Complexity

```
O(capacity)
```

---

# Running the Project

Install dependencies

```bash
pip install fastapi uvicorn
```

Start server

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

Swagger UI allows testing all endpoints.

---

# Demonstrating Cache

## First Request

```
GET /feed/1
```

Response

```json
{
    "source": "DATABASE",
    "cached": false,
    "latency_ms": 100.42
}
```

The data is fetched from the simulated database and stored in the cache.

---

## Second Request

```
GET /feed/1
```

Response

```json
{
    "source": "CACHE",
    "cached": true,
    "latency_ms": 0.03
}
```

The data is returned directly from the cache.

---

# Cache Invalidation Example

Assume

```
User 1 follows User 2
```

User 2 creates a post

```
POST /post
```

The application

```
Stores New Post
        |
Find Followers
        |
Invalidate Cache of User 1
```

The next request

```
GET /feed/1
```

will fetch fresh data from the database and repopulate the cache.

---

# Before vs After Latency

| Scenario | Average Latency |
|-----------|-----------------|
| Without Cache | ~100 ms |
| First Request (Cache Miss) | ~100 ms |
| Second Request (Cache Hit) | ~0.03 ms |

The exact numbers may vary depending on the machine, but the cache hit should be significantly faster than reading from the database.

---

# Unit Tests

Run

```bash
python test_lru.py
```

The tests verify

- Cache insertion
- Cache retrieval
- Updating existing keys
- Eviction order
- Cache invalidation
- Capacity handling

---

# Example Workflow

### Step 1

```
GET /feed/1
```

Output

```
DATABASE
```

---

### Step 2

```
GET /feed/1
```

Output

```
CACHE
```

---

### Step 3

```
POST /post
```

Creates a new post and invalidates affected users' cached feeds.

---

### Step 4

```
GET /feed/1
```

Output

```
DATABASE
```

The cache was invalidated, so fresh data is loaded from the database and cached again.

---