#include <stdio.h>
#include <stdlib.h>
#include "alloc.h"

#define NUM_INTS 5000

int main() {
    int i;
    int* ptrs[NUM_INTS];

	
	void* memarea1 = malloc(sizeof(int) * NUM_INTS * (NUM_INTS+1));

	void* memarea = malloc(sizeof(int) * NUM_INTS * (NUM_INTS+1));

	alloc_init(memarea+3, sizeof(int) * NUM_INTS * (NUM_INTS+1));

    for (i = 0; i < NUM_INTS; i++) {
        ptrs[i] = (int*) alloc_get(memarea+3, sizeof(int) * (i + 1));
        ptrs[i][i] = i;
    }
    
    for (i = 0; i < 5000; i++) {
        alloc_release(memarea+3, ptrs[i]);
    }

    int* ptr2[5000];

    for (i = 0; i < 5000; i++) {
        ptr2[i] = (int*) alloc_get(memarea+3, sizeof(int) * (i + 1));
        ptr2[i][i] = i;
    }

    for (i = 100; i < 500; i++) {
        alloc_release(memarea+3, ptr2[i]);
    }

    for (i = 0; i < 5000; i++) {
        ptr2[i] = (int*) alloc_get(memarea+3, sizeof(int) * (i + 1));
        ptr2[i][i] = i;
    }

    for (i = 0; i < 100; i++) {
        ptr2[i] = (int*) alloc_resize(memarea+3, ptr2[i],sizeof(int) * (i + 1));
        ptr2[i][i] = i;
    }

    for (i = 0; i < 5000; i++) {
        alloc_release(memarea+3, ptr2[i]);
    }

	free(memarea);
	free(memarea1);
    return 0;
}
