#include<stdio.h>

int main(int argc, char* argv[])
{

int numbers[2] = {10,20,30,40,50,60};
char name[] = "Zed";
char full_name[] = {'Z','e','d',' ','S','h','a','h'};

printf("Size of int %ld\n",sizeof(int));
printf("Size of numbers %ld\n",sizeof(numbers));
printf("Size of numbers in array %ld\n",sizeof(numbers)/sizeof(int));
printf("Size of char %ld\n",sizeof(char));
printf("Size of name %ld\n",sizeof(name));
printf("Size of chars in name array %ld\n",sizeof(name)/sizeof(char));
printf("Size of full name %ld\n",sizeof(full_name));
printf("Size of chars in name array %ld\n",sizeof(full_name)/sizeof(char));

return 0;
}
