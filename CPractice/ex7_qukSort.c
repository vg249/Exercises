#include<stdio.h>
#include<stdlib.h>

void quicksort(int* srcArray,int startPos, int lastPos);
int partition(int* srcarray,int startpos, int lastpos);

int j = 0;

int main(int argc, char* argv[])
{

argc--;

if(argc < 1){
	perror("Please enter the number of elements to sort");
	exit(0);
}

int numOfElements = atoi(argv[1]);

printf("Print %d numbers to sort\n",numOfElements);

int i = 0;

int* srcArray = (int*)malloc(sizeof(int)*numOfElements);

for(i = 0; i < numOfElements; i++)
{
	scanf("%d",&srcArray[i]);
}

printf("The Number of Times it runs\n");
quicksort(srcArray,0,numOfElements-1);


printf("The Sorted Elements are \n");
for(i = 0; i < numOfElements; i++)
{
	printf("%d\n",srcArray[i]);
}


return 0;
}

void quicksort(int* srcArray,int startPos, int lastPos)
{


if(startPos < lastPos)
{
    int pivot;
    pivot = partition(srcArray,startPos,lastPos);
    quicksort(srcArray, startPos,pivot-1);
    quicksort(srcArray, pivot+1,lastPos);
}   
}
int partition(int* srcArray,int startPos, int lastPos)
{
int i = 0, pivot = startPos;
int temp = 0;
for(i = startPos; i < lastPos; i++)
{
        printf("%d\n",j++);
	if(srcArray[i] <= srcArray[lastPos])
	{
		temp = srcArray[pivot];
		srcArray[pivot] = srcArray[i];
		srcArray[i] = temp;
		pivot++; 	
	}
}
temp = srcArray[lastPos];
srcArray[lastPos] = srcArray[pivot];
srcArray[pivot] = temp;
return pivot;
}

