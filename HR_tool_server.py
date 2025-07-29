from langchain_core.tools import tool
import random
from mcp.server.fastmcp import FastMCP

#creating mcp instance
mcp = FastMCP("Employee_Info_tool_server",
              instructions="You are an assistant designed to provide employee-related information like employee supervisor, location and skill set using the available tools.",
              port=8002)

@mcp.tool()
def get_employee_supervisor(employee_ID: str):
    """
    Returns the supervisor for a given employee ID.

    Args:
        employee_ID (str): The unique identifier of an employee.

    Returns:
        str: Supervisor's name associated with the given employee ID.
    """
    if employee_ID:
        list_of_supervisors = ['Michael', 'Jessica', 'David', 'Ashley', 'Christopher']
        supervisor = random.choice(list_of_supervisors)
    return f"The supervisor for the given employee is {supervisor}"

@mcp.tool()
def get_employee_location(employee_name: str):
    """
    Returns the location of a given employee.

    Args:
        employee_name (str): The name of the employee.

    Returns:
        str: Location where the employee is based.
    """
    if employee_name:
        list_of_locations = ["Hyderbad", "Bangalore", "Chennai", "Mumbai"]
        location = random.choice(list_of_locations)
    return f"The location for {employee_name} is {location}"

@mcp.tool()
def get_employee_ID(employee_name: str):
    """
    Returns the employee ID for a given employee name.

    Args:
        employee_name (str): The name of the employee.

    Returns:
        str: Unique ID assigned to the employee.
    """
    if employee_name: 
        list_of_ids = ['abd104', '3ni3n', '93jnj', 'ikh2k']
        employee_ID = random.choice(list_of_ids)
    return employee_ID

@mcp.tool()
def get_employee_skill_set(employee_ID: str):
    """
    Returns the skill set of a given employee ID.

    Args:
        employee_ID (str): The unique identifier of the employee.

    Returns:
        str: Primary skill associated with the employee.
    """
    if employee_ID:
        skill = random.choice(["Machine Learning", "Generative AI", "ML Ops", "Image Analysis"])
    return skill

##

if __name__=="__main__":
    mcp.run(transport="sse")