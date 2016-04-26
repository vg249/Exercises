package dijkstra.model;

import java.util.List;

public class Graph
{
	private final List<Vertex> vertexes;
	private final List<Edge> edges;

	public Graph(List<Vertex> vertexes,List<Edge> edges)
	{
		this.vertexes = vertexes;
		this.edges = edges;
	}
	public List<Vertex> getVertexList()
	{
		return this.vertexes;
	}
	public List<Edge> getEdgeList()
	{
		return this.edges;
	}
}
