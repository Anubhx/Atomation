import time
import logging
from typing import List, Optional, Dict, Any
from src.config import get_gemini_keys, MAX_RETRIES

logger = logging.getLogger("key_pool")

class KeySlot:
    def __init__(self, slot_id: int, key_str: str):
        self.slot_id = slot_id
        self.key_str = key_str
        self.is_enabled = True
        self.consecutive_rate_limits = 0
        self.consecutive_failures = 0
        self.cooldown_until = 0.0
        self.total_calls = 0
        self.successful_calls = 0
        self.rate_limit_hits = 0
        self.last_used_time = 0.0

    @property
    def is_available(self) -> bool:
        if not self.is_enabled:
            return False
        return time.time() >= self.cooldown_until

    def get_masked_name(self) -> str:
        return f"Key Slot #{self.slot_id + 1}"

class KeyPool:
    def __init__(self, keys: Optional[List[str]] = None, max_retries: int = MAX_RETRIES):
        if keys is None:
            keys = get_gemini_keys()
        
        self.slots: List[KeySlot] = [KeySlot(i, k) for i, k in enumerate(keys)]
        self.max_retries = max_retries
        self._current_index = 0

    @property
    def has_keys(self) -> bool:
        return len(self.slots) > 0

    def get_available_key(self) -> Optional[KeySlot]:
        """
        Returns an available KeySlot using round-robin rotation,
        skipping slots currently in cooldown or disabled.
        Returns None if no keys are available.
        """
        if not self.slots:
            return None

        n = len(self.slots)
        now = time.time()

        for _ in range(n):
            slot = self.slots[self._current_index]
            self._current_index = (self._current_index + 1) % n
            
            if slot.is_available:
                slot.last_used_time = now
                slot.total_calls += 1
                return slot

        return None

    def mark_healthy(self, slot_id: int) -> None:
        if 0 <= slot_id < len(self.slots):
            slot = self.slots[slot_id]
            slot.consecutive_rate_limits = 0
            slot.consecutive_failures = 0
            slot.cooldown_until = 0.0
            slot.successful_calls += 1

    def mark_rate_limited(self, slot_id: int, backoff_seconds: float = 10.0) -> None:
        if 0 <= slot_id < len(self.slots):
            slot = self.slots[slot_id]
            slot.consecutive_rate_limits += 1
            slot.rate_limit_hits += 1
            # Exponential backoff: 10s, 20s, 40s...
            multiplier = 2 ** (slot.consecutive_rate_limits - 1)
            cooldown = min(backoff_seconds * multiplier, 300.0)
            slot.cooldown_until = time.time() + cooldown
            logger.warning(f"{slot.get_masked_name()} rate limited. Cooldown for {cooldown:.1f}s.")

    def mark_failed(self, slot_id: int) -> None:
        if 0 <= slot_id < len(self.slots):
            slot = self.slots[slot_id]
            slot.consecutive_failures += 1
            if slot.consecutive_failures >= 5:
                # Temporarily put slot on a 60s cooldown if repeated failures occur
                slot.cooldown_until = time.time() + 60.0
                logger.error(f"{slot.get_masked_name()} encountered {slot.consecutive_failures} failures. Cooling down for 60s.")

    def disable_slot(self, slot_id: int) -> None:
        if 0 <= slot_id < len(self.slots):
            self.slots[slot_id].is_enabled = False

    def enable_slot(self, slot_id: int) -> None:
        if 0 <= slot_id < len(self.slots):
            self.slots[slot_id].is_enabled = True
            self.slots[slot_id].cooldown_until = 0.0

    def get_status_summary(self) -> List[Dict[str, Any]]:
        """Safe status summary for UI / metrics dashboard. Never exposes raw key string."""
        now = time.time()
        summary = []
        for slot in self.slots:
            remaining_cooldown = max(0.0, slot.cooldown_until - now)
            summary.append({
                "slot_name": slot.get_masked_name(),
                "enabled": slot.is_enabled,
                "available": slot.is_available,
                "cooldown_seconds": round(remaining_cooldown, 1),
                "total_calls": slot.total_calls,
                "successful_calls": slot.successful_calls,
                "rate_limit_hits": slot.rate_limit_hits,
                "consecutive_failures": slot.consecutive_failures
            })
        return summary
