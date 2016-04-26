#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "alloc.h"

/* You must implement these functions according to the specification given in
 * alloc.h. You can add any data structures you like to this file.
 */

/*
alloc_get & alloc_resize:
Followed First fit approach.

alloc_relaese;
When releaseing a memorty chunk previous and next chunks are collasced
if they are also free.
*/

typedef enum { false, true} bool;

/*

Struct mchunk is the header for each memory block requested by the end program.

Size : Holds the total size of the chunk with data, header and allignment overhead.

bkChnksize : Holds the size of immediate previous chunk. 

Both "size" and "bkChnksize" helps to find the previous and next chunks.

//double linked list to navigate from one free chunk to other. 
//Used only when the chunk is free

mchunk* fd : Pointer to next free chunk
mchunk* bk : Pointer to previous free chunk

mchunk header size : 32 bytes
*/
struct mchunk
{  
  unsigned int	size;      
  unsigned int  bkChnksize;
  bool inUse;
  struct mchunk* fd;         
  struct mchunk* bk;

};


/*
Header to total memory area.

mchunktop: pointer to the top memorychunk of the memory area
lastFreeptr : pointer to the latest memory chunk freeed by the alloc.
blocksize : Total memory size of the mem area.

mstateheader size : 24 bytes
*/

struct mstate
{
  struct mchunk* mchunktop;
  struct mchunk* lastFreeptr;
  unsigned int blocksize;
};

/*
initializes the memory area where user program can get, resize and relaese
the memory. 

memAllign - Number of bytes required to make the memory pointers 8 byte aligned.

Checks whther the requested memory area size is bigger than the minimum required
Size, which is sum of memory state header and memory chunk header.

*/
int alloc_init(void * memarea, int size) {	


	unsigned int memAllign = (((uintptr_t)((char*)memarea+sizeof(struct mstate))) % 8);		
	
	if (memAllign > 0)
	{
		memAllign = 8 - memAllign;
	}

	if(size > (sizeof(struct mchunk) + sizeof(struct mstate)))
	{
		struct mstate* mstateptr	 = (struct mstate*)((char*)memarea + memAllign);
		mstateptr->blocksize		 = size;		
		mstateptr->mchunktop		 = (struct mchunk*)((char*)memarea+sizeof(struct mstate)+memAllign);
		mstateptr->mchunktop->size	 = size - sizeof(struct mstate) - memAllign;
		mstateptr->lastFreeptr		 = mstateptr->mchunktop;
		return 1;
	}
	return 0;
}

/*
Gets the memory pointer for the requested size.
Returned pointers are 8 byte memory aligned.

Free memory chunk if possible is created out of the available memory.
"tempptr" is the variable used to accomplish that.
Once done, the memorystate's lastFree pointer is updated with new one.

Once the memory chunk is assigned, the Forward and Backeward pointers are set accordingly.
If new memory pointer is not alligned additional overhead is added as extra space at the end of
requested memory making all the Free memory chunks as memory aligned.

Returns 0 if memory is not available
*/

void * alloc_get(void * memarea, int size) {
	
	unsigned int memAllign = (((uintptr_t)((char*)memarea+sizeof(struct mstate))) % 8);		
	
	if (memAllign > 0)
	{
		memAllign = 8 - memAllign;
	}
	struct mstate* mstateptr = memarea + memAllign;
	struct mchunk* mptr	 = mstateptr->lastFreeptr;
	struct mchunk* tempptr	 = NULL;
	
	
	while(mptr != NULL && mptr->bk != NULL)
	{
		mptr = mptr->bk;
	}
		
	while(mptr != NULL && size >= (mptr->size-sizeof(struct mchunk)))
	{
		mptr = mptr->fd;
	}
	
	if (mptr != NULL)
	{
		mptr->inUse = true;
		
		memAllign = 8 - ((uintptr_t)((char*)mptr + sizeof(struct mchunk) + size))%8;

		if (memAllign > 0)
		{
			memAllign = 8 - memAllign;
		}
		
		tempptr 	= (struct mchunk*)((char*)mptr + sizeof(struct mchunk) + size + memAllign);

		tempptr->size	= mptr->size - sizeof(struct mchunk) - size - memAllign;

		mptr->size	= sizeof(struct mchunk) + size + memAllign;

		tempptr->bkChnksize	= mptr->size;
		
		if (mptr->fd != NULL)
		{
			mptr->fd->bk	= tempptr;
		}

		if (tempptr < mptr->fd)
		{
			tempptr->fd	= mptr->fd;
		}

		mptr->fd	= NULL;

		if(mptr->bk != NULL)
		{
			mptr->bk->fd 	= tempptr;
		}

		if (tempptr > mptr->bk)
		{
			tempptr->bk	= mptr->bk;
		}

		mptr->bk	= NULL;			
		
		mstateptr->lastFreeptr	= tempptr;
		return (void *)((char*)mptr + sizeof(struct mchunk));
	}
	mstateptr->lastFreeptr	= tempptr;
	return 0;
}

/*
Releases the memory of requested pointer.

Checks for free memory chunk above it or below it.
If found, collasce all of them to form a big memory chunk and 
add itself to the Free memory chunk list by setting the fd and bk pointers 
in header.
Helps reducing the fragmentation.

if no neighboring memory chunks are found, jus inserts itself to the
existing Free memory chunk list.
*/

void alloc_release(void * memarea, void * mem) {
	
	if(mem == 0)
	{
		return;
	}
	
	unsigned int memAllign = (((uintptr_t)((char*)memarea+sizeof(struct mstate))) % 8);		
	
	if (memAllign > 0)
	{
		memAllign = 8 - memAllign;
	}

	struct mstate* mstateptr = (struct mstate*)((char*)memarea + memAllign);
	struct mchunk* mptr	 = (struct mchunk*)((char*)mem - sizeof(struct mchunk));
	struct mchunk* mptrNxt	 = NULL;
	struct mchunk* mptrPrv	 = NULL;
	
	if(mptr->inUse == false)
	{
		return;
	}
	mptr->inUse	= false;

	if(((char*)mptr + mptr->size) < ((char*)memarea + mstateptr->blocksize - sizeof(struct mchunk) - 1))
	{
		mptrNxt	 = (struct mchunk*)((char*)mptr + mptr->size);
	}

	if(((char*)mptr - mptr->bkChnksize) >= (char*)mstateptr->mchunktop && mptr != mstateptr->mchunktop)
	{
		mptrPrv	 = (struct mchunk*)((char*)mptr - mptr->bkChnksize);
	}
	
	if((mptrNxt != NULL && mptrNxt->inUse == false) || (mptrPrv != NULL && mptrPrv->inUse == false))
	{	
		if(mptrNxt != NULL && mptrNxt->inUse == false)
		{
			mptr->fd 	= mptrNxt->fd;
	
			mptr->bk	= mptrNxt->bk;
	
			if (mptr->fd != NULL)
			{
				mptr->fd->bk = mptr;
			}
	
			if(mptr->bk != NULL)
			{
				mptr->bk->fd = mptr;
			}
			mptr->size	= mptr->size + mptrNxt->size;
	
			struct mchunk* fdfd = (struct mchunk*)((char*)mptrNxt + mptrNxt->size);
			if (fdfd != NULL && (char*)fdfd < ((char*)memarea + mstateptr->blocksize - sizeof(struct mchunk) - 1) && fdfd->inUse == true)
			{
				fdfd->bkChnksize = mptr->size;
			}
			mstateptr->lastFreeptr	= mptr;
		}
		
		if(mptrPrv != NULL && mptrPrv->inUse == false)
		{
			mptrPrv->size = mptrPrv->size + mptr->size;
			if(((char*)mptr + mptr->size) < ((char*)memarea + mstateptr->blocksize - sizeof(struct mchunk) - 1))
			{
				struct mchunk* fdfd = (struct mchunk*)((char*)mptr + mptr->size);
				if (fdfd != NULL)
				{
					fdfd->bkChnksize = mptrPrv->size;
				}
			}
			mstateptr->lastFreeptr	= mptrPrv;
		}
		
	}
	else 
	{
		struct mchunk* immTemp	= NULL;
		
		if(mstateptr->lastFreeptr != NULL && mstateptr->lastFreeptr > mptr)
		{
			struct mchunk* immPrev	= mstateptr->lastFreeptr;
			immTemp	= NULL;
			while(immPrev != NULL && immPrev > mptr)
			{
				immTemp = immPrev;
				immPrev = immPrev->bk;	
			}

			if(immPrev == NULL && immTemp > mptr)
			{
				mptr->fd = immTemp;
				mptr->bk = NULL;
				immTemp->bk = mptr;
				mstateptr->lastFreeptr = mptr;
			}
			else if (immPrev != NULL && immPrev < mptr)
			{
				mptr->bk = immPrev;
				mptr->fd = immPrev->fd;
				mptr->bk->fd = mptr;
				mptr->fd->bk = mptr;
				mstateptr->lastFreeptr = mptr;
			}
		}
		else if (mstateptr->lastFreeptr != NULL && mstateptr->lastFreeptr < mptr)
		{
			struct mchunk* immNext	= mstateptr->lastFreeptr;
			immTemp	= NULL;
			while(immNext != NULL && immNext < mptr)
			{
				immTemp = immNext;
				immNext = immNext->fd;	
			}

			if(immNext == NULL && immTemp < mptr)
			{
				mptr->bk = immTemp;
				mptr->fd = NULL;
				immTemp->fd = mptr;
				mstateptr->lastFreeptr = mptr;
			}
			else if (immNext != NULL && immNext > mptr)
			{
				mptr->fd = immNext;
				mptr->bk = immNext->bk;
				mptr->bk->fd = mptr;
				mptr->fd->bk = mptr;
				mstateptr->lastFreeptr = mptr;
			}
			
		}
			
	}		
}

/*
if the same memory can be able to accomodate the new size,
then the memory chunk is partitioned to form a free chunk if possible.

if requested size is big, loops through the available free chunks, to find
the first free chunk that can accomodate the size.

moves only the data from existing chunk to the new chunk.
memmove is used to accomplish that task.

once moved the current memory chunk is freed and 
new memory pointer is returned.
*/

void * alloc_resize(void * memarea, void * mem, int size) {

	unsigned int memAllign = (((uintptr_t)((char*)memarea+sizeof(struct mstate))) % 8);		
	
	if (memAllign > 0)
	{
		memAllign = 8 - memAllign;
	}

	struct mstate* mstateptr = (struct mstate*)((char*)memarea + memAllign);
	struct mchunk* mptr = (struct mchunk*)((char*)mem - sizeof(struct mchunk));	
	struct mchunk* suitableChunk	 = NULL;	
	struct mchunk* suitableChunkfst	 = NULL;	

	if ((mptr->size - sizeof(struct mchunk))  >= size)
	{
		if((int)size <((int)mptr->size - (int)(2*sizeof(struct mchunk)) -1))
		{
			struct mchunk* tempptr	 = NULL;
			memAllign = 8 - ((uintptr_t)((char*)mptr + sizeof(struct mchunk) + size))%8;
	
			if (memAllign > 0)
			{
				memAllign = 8 - memAllign;
			}
			
			tempptr 	= (struct mchunk*)((char*)mptr + sizeof(struct mchunk) + size + memAllign);
	
			tempptr->size	= mptr->size - sizeof(struct mchunk) - size - memAllign;
	
			mptr->size	= sizeof(struct mchunk) + size + memAllign;
	
			tempptr->bkChnksize	= mptr->size;
			
			if (mptr->fd != NULL)
			{
				mptr->fd->bk	= tempptr;
			}
	
			if (tempptr < mptr->fd)
			{
				tempptr->fd	= mptr->fd;
			}
	
			mptr->fd	= NULL;
	
			if(mptr->bk != NULL)
			{
				mptr->bk->fd 	= tempptr;
			}
	
			if (tempptr > mptr->bk)
			{
				tempptr->bk	= mptr->bk;
			}
	
			mptr->bk	= NULL;			
			mstateptr->lastFreeptr	= tempptr;			
		}		

		return (void*)((char*)mptr + sizeof(struct mchunk));
	}
	else
	{
		suitableChunkfst = mstateptr->lastFreeptr;

		while(suitableChunkfst != NULL && suitableChunkfst >= mstateptr->mchunktop)
		{
			suitableChunk 	 = suitableChunkfst;
			suitableChunkfst = suitableChunkfst->bk;
		}
		
		if(suitableChunkfst != NULL)
		{
			suitableChunk = suitableChunkfst;
		}


		while(suitableChunkfst != NULL && (suitableChunk->size-sizeof(struct mchunk)) < size)
		{
			suitableChunk = suitableChunk;
			suitableChunk = suitableChunk->fd;	
		}
		

		if (suitableChunk == NULL)
		{
			return NULL;
		}	
		
		
		memmove((char*)mptr+sizeof(struct mchunk),(char*)suitableChunk+sizeof(struct mchunk),mptr->size-sizeof(struct mchunk));
		suitableChunk->inUse = true;
		if(suitableChunk->fd != NULL)
		{
			if (suitableChunk->bk != NULL)
			{
				suitableChunk->fd->bk = suitableChunk->bk;
			}
			else
			{
				suitableChunk->fd->bk  = NULL; 
			}
		}
		if(suitableChunk->bk != NULL)
		{
			if (suitableChunk->fd != NULL)
			{
				suitableChunk->bk->fd = suitableChunk->fd;
			}
			else
			{
				suitableChunk->bk->fd  = NULL; 
			}
		}
		suitableChunk->fd = NULL;
		suitableChunk->bk = NULL;
		alloc_release(memarea, (void*)((char*)mptr+sizeof(struct mchunk)));	
		return (void *)((char*)suitableChunk + sizeof(struct mchunk));	
					
	}					
	return NULL;
}

