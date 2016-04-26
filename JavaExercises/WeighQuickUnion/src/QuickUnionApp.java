package QUnion;

public class QuickUnionApp
{
	public static void main(String[] str)
	{
		QuickUnion objQuickUnion = new QuickUnion(10);

		objQuickUnion.Union(4,5);
		objQuickUnion.Union(4,6);
		objQuickUnion.Union(2,6);
		objQuickUnion.Union(1,3);
	 	System.out.println(objQuickUnion.Connected(4,5));	
	 	System.out.println(objQuickUnion.Connected(5,6));	
	 	System.out.println(objQuickUnion.Connected(1,6));	
	 	System.out.println(objQuickUnion.Connected(2,8));	
	}
}
