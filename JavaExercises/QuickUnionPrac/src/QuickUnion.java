package QuickUnion


class QuickUnion
{

	private int[] numbers;

	public void QuickUnion(int n)
	{
		numbers = new int[n];
		for(int i = 0; i < n; i++)
		{
			numbers[i] = i;
		}
	}

	public void Union(int pos1, int pos2)
	{
		int j = Findroot[pos1];
		int k = Findroot[pos2];
		numbers[j] = k;
	}

	public int Findroot(int pos)
	{
		while(pos != numbers[pos]) pos = numbers[pos];
		
		return pos;
	}
	
	public boolean Connected(int pos1, int pos2)
	{
		return Findroot[pos1] == Findroot[pos2];
	}
}
