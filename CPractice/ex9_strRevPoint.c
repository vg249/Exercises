#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void strRev(char* input);


int main(int argc, char* argv[])
{

char* input = "Vishnu";
char* output = malloc(sizeof(char)* strlen(input));
strcpy(output,input);
strRev(output);
printf("The output is %s\n",output);
return 0;
}

void strRev(char* input)
{

int length = 0, i = 0, j = 0;
length = strlen(input);
i = length - 1;
j = 0;
char temp;

while(j < i)
{
      temp = input[i];
      input[i] = input[j];
      input[j] = temp;
      i--;
      j++;
}

}
