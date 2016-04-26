#include <stdio.h>
#include "alloc.h"

char memarea[100];

int main() {

	alloc_init(memarea, 100 * sizeof(char));
	char* ptr = (char *) alloc_get(memarea, 13 * sizeof(char));

    ptr[0] = 'h';
    ptr[1] = 'e';
    ptr[2] = 'l';
    ptr[3] = 'l';
    ptr[4] = 'o';
    ptr[5] = ' ';
    ptr[6] = 'w';
    ptr[7] = 'o';
    ptr[8] = 'r';
    ptr[9] = 'l';
    ptr[10] = 'd';
    ptr[11] = '!';
    ptr[12] = '\0';

    printf("%s\n", ptr);

    return 0;
}
