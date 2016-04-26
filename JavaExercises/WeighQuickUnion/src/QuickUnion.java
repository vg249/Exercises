package QUnion;


public class QuickUnion
{

	private int[] ID;
	private int[] size;
	public QuickUnion(int N)
	{
		ID = new int[N];
		size = new int[N];
		for(int i = 0; i < N; i++)
		{
			ID[i] = i;
			size[i] = 1;
		}
	}

	public int root(int pos)
	{
		while(ID[pos] != pos) pos = ID[pos];
		return pos;
	}
	
	public boolean Connected(int i, int j)
	{
		return (root(i) == root(j));
	}
	
	public void Union(int i, int j)
	{
		int p = root(i);
		int q = root(j);
		if(p == q) return;
		else{
			if(size[p] < size[q]){ ID[p] = q; size[q] += size[p];}
			else {ID[q] = p; size[p] += size[q];}
		}
	}
}
