#ifndef __LINUX_BIT_SPINLOCK_H
#define __LINUX_BIT_SPINLOCK_H

#include <linux/kernel.h>
#include <linux/preempt.h>
#include <linux/futex.h>

static inline void bit_spin_lock(int nr, unsigned long *_addr)
{
	u32 mask, *addr = ((u32 *) _addr) + (nr / 32), v;

	nr &= 31;
	mask = 1U << nr;

	while (1) {
		v = __atomic_fetch_or(addr, mask, __ATOMIC_ACQUIRE);
		if (!(v & mask))
			break;

		futex(addr, FUTEX_WAIT|FUTEX_PRIVATE_FLAG, v, NULL, NULL, 0);
	}
}

static inline void bit_spin_wake(int nr, unsigned long *_addr)
{
	u32 *addr = ((u32 *) _addr) + (nr / 32);

	futex(addr, FUTEX_WAKE|FUTEX_PRIVATE_FLAG, INT_MAX, NULL, NULL, 0);
}

static inline void bit_spin_unlock(int nr, unsigned long *_addr)
{
	u32 mask, *addr = ((u32 *) _addr) + (nr / 32);

	nr &= 31;
	mask = 1U << nr;

	__atomic_and_fetch(addr, ~mask, __ATOMIC_RELEASE);
	futex(addr, FUTEX_WAKE|FUTEX_PRIVATE_FLAG, INT_MAX, NULL, NULL, 0);
}

#endif /* __LINUX_BIT_SPINLOCK_H */

