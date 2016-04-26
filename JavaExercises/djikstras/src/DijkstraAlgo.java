package dijkstra.algo;


import dijkstra.model.Graph;

public class DijkstraAlgo
{
	private final List<Vertex> nodes;
	private final List<Edges> edges;
	private final Set<Vertex> unsettledNodes;
	private final Set<Vertex> settledNodes;
	private final Map<Vertex, Vertex> predecessors;
	private final Map<Vertex, Integer> distance;
	

	public DijstraAlgo(Graph G)
	{
		this.nodes = new ArrayList(G.getVertexList());	
		this.edges = new ArrayList(G.getEdgeList());
	}

	public void execute(Vertex source)
	{
		unsettledNodes	= new HashSet<Vertex>();
		settledNodes 	= new HashSet<Vertex>();
		predecessors	= new HashMap<Vertex, Vertex>();
		distance	= new HashMap<Vertex, Integer>();

		distance.put(source,0);
		unsettledNodes.add(source);

		while(unsettledNodes.size() > 0)
		{
			Vertex node = getMinimum(unsettledNodes);
			settledNodes.add(node);
			unsettledNodes.remove(node);	
			FindMinimumDistance(node);
		}
	} 
	
	public void FindMinimumDistance(Vertex node)
	{
		List<Vertex> adjNodes = getNeighbors(Vertex node);
		int intSDistanceSrc = 0, intTargetDistance = 0, intSDistanceTar = 0;
		for(Vertex target : adjNodes)
		{
			intShortDistance = getShortDistance(node);
			intTargetDistance
			if(getShortDistance(target) > (getShortDistance(node) + getDistance(node, target)))
			{
				distance.put(getShortDistance(node) + getDistance());
			}
		}
		
	}

	public int getDistance(Vertex Source, Vertex Destination)
	{
		for(Edge edge : edges)
		{
			if(edge.getSource().equals(Source) && edge.getDestination().equals(Destination))
			{
				return edge.getWeight();
			}
		}
		throw new RuntimeException("Class:DjikstraAlgo, Method:getDistance");
	}	

	public Vertex getMinimum(Set<Vertex> unsettledNodes)
	{
		Vertex minimum = null;
		for(Vertex vertex : unsettledNodes)
		{
			if(minimum == null)
			{
				minimum = vertex;
			}
			else if(getShortDistance(vertex) < getShortDistance(minimum))
			{
				minimum = vertex;
			}
		}	
	}
	
	public int getShortDisance(Vertex node)
	{
		int d = distance.get(node);
		if(d == null)
		{
			return Innteger.MAX_VALUE;
		}
		else
		{
			return d;
		}
	}

	public List<Vertex> getNeighbors(Vertex node)
	{
		List<Vertex> neighbors = new ArrayList<Vertex>;
		for(Edge edge : edges)
		{
			if(edge.getSource() == node && !isSettled(edge.getDestination()))
			{
				neighbors.add(edge.getDestination());
			}
		}
		return neighbors;
	}

	public boolean isSettled(Vertex node)
	{
		return settledNodes.contains(node);
	}
		
}
