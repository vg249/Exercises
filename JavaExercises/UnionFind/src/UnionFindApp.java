package UFindPack;

public class UnionFindApp
{

public static void main(String[] args)
{

UnionFind objUFind = new UnionFind(10);

objUFind.Union(0,9);
objUFind.Union(0,2);
objUFind.Union(0,3);
objUFind.Union(0,4);
System.out.println(objUFind.Connected(0,9));
System.out.println(objUFind.Connected(0,2));
System.out.println(objUFind.Connected(2,9));
System.out.println(objUFind.Connected(4,9));
System.out.println(objUFind.Connected(5,9));

}

}

