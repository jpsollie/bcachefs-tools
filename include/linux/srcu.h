#ifndef __TOOLS_LINUX_SRCU_H
#define __TOOLS_LINUX_SRCU_H

struct srcu_struct {
};

static inline void srcu_read_unlock(struct srcu_struct *ssp, int idx) {}

static inline int srcu_read_lock(struct srcu_struct *ssp)
{
	return 0;
}

static inline bool poll_state_synchronize_srcu(struct srcu_struct *ssp, unsigned long cookie)
{
	return false;
}

static inline unsigned long start_poll_synchronize_srcu(struct srcu_struct *ssp)
{
	return 0;
}

static inline void cleanup_srcu_struct(struct srcu_struct *ssp) {}

static inline int init_srcu_struct(struct srcu_struct *ssp)
{
	return 0;
}

#endif /* __TOOLS_LINUX_SRCU_H */
