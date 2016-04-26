#include<stdio.h>
#include<stdlib.h>

int main(int argc, char* argv[])
{

char* input = "Vishnu";

int i = 0,length = 0;

while(input[i] != '\0')
{

i++;
}
length = i;
char* output = malloc(sizeof(char)*i);
i =0;
while(i < length)
{

output[i] = input[length-i-1];
i++;
}

output[length] = '\0';

printf("The input length  is %d\n",i);
printf("The output is %s\n",output);


return 0;
}
