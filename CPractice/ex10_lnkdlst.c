#include<stdio.h>
#include<stdlib.h>


typedef struct node{

struct node* next;
int data;

} node_t;

void linkdlstRev(node_t* head);

node_t* previous = NULL;

int main(int argc, char* argv[])
{

int i =0; int input = 0;

node_t* firstvalue = malloc(sizeof(node_t));
node_t* travalue;

travalue = firstvalue;

printf("Please enter 10 integers \n");
scanf("%d",&input);
travalue->data = input;
for(i = 1; i < 10;i++)
{
	travalue->next = malloc(sizeof(node_t));
	scanf("%d",&input);
	travalue->next->data = input;
	travalue = travalue->next;
}
travalue = firstvalue;

printf("Linked List Traversal \n");
int length = 0;
while(travalue != NULL)
{
	printf("%d\n",travalue->data);
	travalue = travalue->next;
        length++;
}

travalue = firstvalue;
node_t * prev = NULL;
node_t* next;
while(travalue != NULL)
{

next = travalue->next;
travalue->next = prev;
prev = travalue;
travalue = next;

}

travalue = prev;

printf("Linked List Reversal \n");
while(travalue != NULL)
{
	printf("%d\n",travalue->data);
	travalue = travalue->next;
}

travalue = prev;
linkdlstRev(travalue);

travalue = previous;

printf("Linked List Reversal Recursive\n");

while(travalue != NULL)
{
	printf("%d\n",travalue->data);
	travalue = travalue->next;
}

return 0;
}



void linkdlstRev(node_t* head)
{
if(head != NULL)
{
	node_t* next = head->next;
	head->next = previous;
	previous = head;
	linkdlstRev(next);
}
}

