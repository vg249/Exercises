package dijkstra.model;

public class Edge
{
	private final int id;
	private final Vertex source;
	private final Vertex destination;
	private final int weight;

	public Edge(int id, Vertex source, Vertex destination, int weight)
	{
		this.id = id;
		this.source = source;
		this.destination = destination;
		this.weight = weight;
	}


	public int getID()
	{
		return this.id;
	}

	public Vertex getSource()
	{
		return this.source;
	}

	public Vertex getDestination()
	{
		return this.destination;
	}

	public int getWeight()
	{
		return this.weight;
	} 

	@Override
	public String toString()
	{
		return this.source + "" + this.destination;
	}
}
