import sys
import functools
from typing import Any, Callable

class MemoizedConst:
    """High-performance lookup table for expensive runtime constants."""
    def __init__(self, func: Callable):
        self.func = func
        self.cache: dict[tuple, Any] = {}

    def __call__(self, *args: Any) -> Any:
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@MemoizedConst
def get_system_affinity_mask(core_id: int) -> int:
    """Generates binary mask for process pinning."""
    return 1 << (core_id % 64)

class SystemConstants:
    __slots__ = ('_mem_map',)
    
    def __init__(self):
        self._mem_map = {i: get_system_affinity_mask(i) for i in range(8)}

    def __getitem__(self, key: int) -> int:
        return self._mem_map.get(key, 0)

    def __repr__(self) -> str:
        return f"ConstantsPool(size={len(self._mem_map)})"

# Singleton pattern for global access without re-init overhead
GLOBAL_CONSTS = SystemConstants()

def get_optimized_constant(key: int) -> int:
    """Fast-path accessor for frequently requested system values."""
    return GLOBAL_CONSTS[key] if key < 8 else 0

if __name__ == '__main__':
    # Validate performance shortcut
    assert get_optimized_constant(2) == 4