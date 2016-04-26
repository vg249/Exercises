#include<stdio.h>
#include<omp.h>

static long num_steps = 100000;
double step;

#define NUM_THREADS 4

int main()
{
int i; double pi,sum[NUM_THREADS];

step = 1.0/(double)num_steps;

int num_threads = 0;
omp_set_num_threads(NUM_THREADS);

#pragma omp parallel
{
int i,id;
double x;

num_threads = omp_get_num_threads();
id = omp_get_thread_num();

for(i = 0,sum[id]=0.0; i < num_steps; i=i+num_threads)
{
x = (i+0.5)*step;
sum[id] = sum[id] + 4.0/(1.0 + x*x);
}
}

for(i=0;i<num_threads;i++)
{
pi += sum[i]*step;
}

printf("The Value of pi is %f\n", pi);

return 0;
}
