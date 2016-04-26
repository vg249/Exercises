#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(int argc, char* argv[])
{

	FILE *fp;

	char str[1024];
	
//	char ** strArray = malloc(sizeof(str));	

	fp = fopen("example.csv","r");

	if(fp == NULL)
	{
		perror("Error openning file");
		return -1;
	}
	while(fgets(str,60,fp) != NULL)
	{
		char *s = strtok(str,",");
		char * StringTemp;
		printf("%s\n",s);
		while((s = strtok(NULL,",")) != NULL)
		{
			StringTemp = malloc(sizeof(char)*strlen(s));
			strcpy(StringTemp,s);
			int d = strlen(StringTemp);
			printf("%s and the string lenth is %d\n",StringTemp,d);
		}
	}
	fclose(fp);
	return 0;
}


