#include<stdio.h>
#include<stdlib.h>

int main(int argc, char* argv[])
{

int * p1 = malloc(4*sizeof(int));
int * p2 = malloc(sizeof(int[4]));
int * p3 = malloc(sizeof *p3);
int*p4 = p1;
int i = 0;

	if(p1)
	{
		for(i = 1;i<=4;i++)
		{
			*p1 = i*i;
			p1++;
	//		p1[i] = i*i;
		}
		for(i = 0;i < 4;i++)
			printf("%d \n",p4[i]);
	}
return 0;
}

