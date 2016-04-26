package QUnion;


public class QuickUnion
{

	private int[] ID;
	public QuickUnion(int N)
	{
		ID = new int[N];
		for(int i = 0; i < N; i++)
		{
			ID[i] = i;
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
		ID[p] = q;
	}
}
