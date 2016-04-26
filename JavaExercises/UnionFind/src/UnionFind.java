package UFindPack;
public class UnionFind
{
private int[] ID;

public UnionFind(int N)
{
ID = new int[N];
for(int i=0;i<N;i++)
   ID[i] = i;
} 

public boolean Connected(int p, int q)
{ return ID[p] == ID[q];}

public void Union(int p, int q)
{
int pval = ID[p];
int qval = ID[q];
for(int i =0;i<ID.length;i++)
     if(ID[i] == pval) ID[i] = qval;
}
}


