package dijkstra.model;

import java.util.List;


public class Vertex
{
	private final String id;
	private final String name;

	public Vertex(String id, String name)
	{
		this.id  = id;
		this.name = name;		
	}

	public String getID()
	{
		return this.id;
	}
	
	public String getName()
	{
		return this.name;
	}
	
	@Override
	public boolean equals(Object obj)
	{
		if(this == obj)
			return true;
		else if(obj == null)
			return false;
		
		if(obj.getClass() != this.getClass())
			return false;

		Vertex tempObj = (Vertex)obj;
		
		if(tempObj != null || id != null){
			if(id == tempObj.getID())
				return true;	
		}
		return false;
			
	}

}
