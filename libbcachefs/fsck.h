#ifndef _BCACHEFS_FSCK_H
#define _BCACHEFS_FSCK_H

s64 bch2_count_inode_sectors(struct bch_fs *, u64);
int bch2_fsck(struct bch_fs *, bool);

#endif /* _BCACHEFS_FSCK_H */
