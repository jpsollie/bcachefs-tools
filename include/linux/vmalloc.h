#ifndef __TOOLS_LINUX_VMALLOC_H
#define __TOOLS_LINUX_VMALLOC_H

#include <stdlib.h>
#include <sys/mman.h>

#include "linux/slab.h"
#include "tools-util.h"

#define PAGE_KERNEL		0
#define PAGE_KERNEL_EXEC	1

#define vfree(p)		free(p)

static inline void *__vmalloc(unsigned long size, gfp_t gfp_mask)
{
	void *p;

	run_shrinkers();

	p = aligned_alloc(PAGE_SIZE, size);
	if (!p)
		return NULL;

	if (gfp_mask & __GFP_ZERO)
		memset(p, 0, size);

	return p;
}

static inline void *vmalloc_exec(unsigned long size, gfp_t gfp_mask)
{
	void *p;

	p = __vmalloc(size, gfp_mask);
	if (!p)
		return NULL;

	if (mprotect(p, size, PROT_READ|PROT_WRITE|PROT_EXEC)) {
		vfree(p);
		return NULL;
	}

	return p;
}

static inline void *vmalloc(unsigned long size)
{
	return __vmalloc(size, GFP_KERNEL);
}

static inline void *vzalloc(unsigned long size)
{
	return __vmalloc(size, GFP_KERNEL|__GFP_ZERO);
}

#endif /* __TOOLS_LINUX_VMALLOC_H */
