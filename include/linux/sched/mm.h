#ifndef _LINUX_SCHED_MM_H
#define _LINUX_SCHED_MM_H

#define PF_MEMALLOC		0x00000800	/* Allocating memory */
#define PF_MEMALLOC_NOFS	0x00040000	/* All allocation requests will inherit GFP_NOFS */

static inline unsigned int memalloc_nofs_save(void)
{
	unsigned int flags = current->flags & PF_MEMALLOC_NOFS;
	current->flags |= PF_MEMALLOC_NOFS;
	return flags;
}

static inline void memalloc_nofs_restore(unsigned int flags)
{
	current->flags = (current->flags & ~PF_MEMALLOC_NOFS) | flags;
}

static inline unsigned int memalloc_noreclaim_save(void)
{
	unsigned int flags = current->flags & PF_MEMALLOC;
	current->flags |= PF_MEMALLOC;
	return flags;
}

static inline void memalloc_noreclaim_restore(unsigned int flags)
{
	current->flags = (current->flags & ~PF_MEMALLOC) | flags;
}

#endif /* _LINUX_SCHED_MM_H */
