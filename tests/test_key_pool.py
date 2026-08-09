import pytest
import time
from src.key_pool import KeyPool, KeySlot

def test_key_pool_rotation():
    pool = KeyPool(keys=["KEY_1", "KEY_2", "KEY_3"])
    assert len(pool.slots) == 3

    s1 = pool.get_available_key()
    s2 = pool.get_available_key()
    s3 = pool.get_available_key()

    assert s1.slot_id == 0
    assert s2.slot_id == 1
    assert s3.slot_id == 2

def test_key_pool_rate_limiting():
    pool = KeyPool(keys=["KEY_1", "KEY_2"])
    
    # Mark slot 0 rate limited
    pool.mark_rate_limited(0, backoff_seconds=5.0)

    # Next call should skip slot 0 and give slot 1
    slot = pool.get_available_key()
    assert slot.slot_id == 1

def test_key_pool_masked_names():
    pool = KeyPool(keys=["SECRET_API_KEY_12345"])
    summary = pool.get_status_summary()
    assert summary[0]["slot_name"] == "Key Slot #1"
    # Ensure secret key is NEVER exposed in status summary
    assert "SECRET_API_KEY_12345" not in str(summary)
