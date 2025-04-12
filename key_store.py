from typing import TypedDict
import redis


class StaticKeys(TypedDict):
    test_reason: str


s = redis.Redis(host='localhost', port=6379, db=0)
static_keys: StaticKeys = {
    'test_reason': 'test_reason'
}
