#ifndef ALLOC_H
#define ALLOC_H

/* Sets up a new "memory allocation area".  'memarea' points to a chunk of memory
 * of 'size' bytes.  Returns 0 on success, nonzero if setup failed.
 */
int alloc_init(void * memarea, int size);


/* Allocates a block of memory of the given size from the memory area. Returns 
 * a pointer to the block of memory on success; returns 0 if the allocator cannot
 * satisfy the request.
 */
void * alloc_get(void * memarea, int size);


/* Releases the block of previously allocated memory pointed to by mem.
 * No-op if mem == 0.
 */
void alloc_release(void * memarea, void * mem);


/* Changes the size of the memory block pointed to by mem, returning a pointer to the new
 * block, or 0 if the request cannot be satisfied. The contents of the block should be
 * preserved (even if the location of the block changes).
 * If mem == 0, function should behave like alloc_get().
 */
void * alloc_resize(void * memarea, void * mem, int size);

#endif /*ALLOC_H*/
