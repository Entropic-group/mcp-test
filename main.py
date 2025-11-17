import os
import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from dotenv import load_dotenv

from utils.auth import create_auth0_verifier
from models import init_db, get_session_maker, seed_sample_data
from service import DependencyService
from stats import get_dependency_health_overview, get_stale_dependencies

# Load environment variables from .env file
load_dotenv()

# Initialize database
init_db()

# Populate with sample data on first run
seed_sample_data()

# Initialize service layer
dependency_service = DependencyService()
session_maker = get_session_maker()

# Get Auth0 configuration from environment
auth0_domain = os.getenv("AUTH0_DOMAIN")
resource_server_url = os.getenv("RESOURCE_SERVER_URL")

if not auth0_domain:
    raise ValueError("AUTH0_DOMAIN environment variable is required")
if not resource_server_url:
    raise ValueError("RESOURCE_SERVER_URL environment variable is required")

# Load server instructions
with open("prompts/server_instructions.md", "r") as file:
    server_instructions = file.read()

# Initialize Auth0 token verifier
token_verifier = create_auth0_verifier()

port = int(os.getenv("PORT", 8000))

# Create an MCP server with OAuth authentication
mcp = FastMCP(
    "yt-mcp",
    instructions=server_instructions,
    host="0.0.0.0",
    port=port,
    # OAuth Configuration
    token_verifier=token_verifier,
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(f"https://{auth0_domain}/"),
        resource_server_url=AnyHttpUrl(resource_server_url),
        required_scopes=["openid", "profile", "email", "address", "phone"],
    ),
)

@mcp.tool()
def get_all_dependencies() -> str:
    """
    Retrieve all dependencies in the system.
    
    Returns:
        str: JSON string containing list of all dependencies
    """
    try:
        dependencies = dependency_service.get_all_dependencies()
        return json.dumps(dependencies, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_dependency_by_id(dependency_id: str) -> str:
    """
    Retrieve a dependency by its UUID.
    
    Args:
        dependency_id: The UUID of the dependency to retrieve
    
    Returns:
        str: JSON string containing the dependency data or error message
    """
    try:
        dependency = dependency_service.get_dependency_by_id(dependency_id)
        if dependency:
            return json.dumps(dependency, indent=2)
        else:
            return json.dumps({"error": f"Dependency with id '{dependency_id}' not found"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_dependency_by_name(name: str) -> str:
    """
    Retrieve a dependency by its name.
    
    Args:
        name: The exact name of the dependency to retrieve
    
    Returns:
        str: JSON string containing the dependency data or error message
    """
    try:
        dependency = dependency_service.get_dependency_by_name(name)
        if dependency:
            return json.dumps(dependency, indent=2)
        else:
            return json.dumps({"error": f"Dependency with name '{name}' not found"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def search_dependencies(query: str) -> str:
    """
    Search dependencies by name (case-insensitive partial match).
    
    Args:
        query: The search query to match against dependency names
    
    Returns:
        str: JSON string containing list of matching dependencies
    """
    try:
        dependencies = dependency_service.search_dependencies(query)
        return json.dumps(dependencies, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def check_dependency_existence(name: str) -> str:
    """
    Check if a dependency with the given name exists.
    
    Args:
        name: The dependency name to check
    
    Returns:
        str: JSON string indicating whether the dependency exists
    """
    try:
        exists = dependency_service.dependency_exists(name)
        return json.dumps({"name": name, "exists": exists}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def find_updated_dependencies(start_date: str, end_date: str) -> str:
    """
    Find dependencies that were updated within a date range.
    
    Args:
        start_date: Start date in ISO format (e.g., '2024-01-01T00:00:00')
        end_date: End date in ISO format (e.g., '2024-12-31T23:59:59')
    
    Returns:
        str: JSON string containing list of dependencies updated in the date range
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        dependencies = dependency_service.find_updated_between(start, end)
        return json.dumps(dependencies, indent=2)
    except ValueError as e:
        return json.dumps({"error": f"Invalid date format: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def find_dependencies_with_planned_updates(start_date: str, end_date: str) -> str:
    """
    Find dependencies with planned updates in a date range.
    
    Args:
        start_date: Start date in ISO format (e.g., '2024-01-01T00:00:00')
        end_date: End date in ISO format (e.g., '2024-12-31T23:59:59')
    
    Returns:
        str: JSON string containing list of dependencies with planned updates in the date range
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        dependencies = dependency_service.find_next_update_between(start, end)
        return json.dumps(dependencies, indent=2)
    except ValueError as e:
        return json.dumps({"error": f"Invalid date format: {str(e)}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def get_health_overview() -> str:
    """
    Get comprehensive health overview of all dependencies.
    
    Includes metrics for:
    - Total count
    - Version drift (test vs prod differences)
    - Overdue updates
    - Test-only dependencies
    - Recently updated dependencies
    
    Returns:
        str: JSON string containing health overview metrics
    """
    session = session_maker()
    try:
        overview = get_dependency_health_overview(session)
        return json.dumps(overview, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    finally:
        session.close()


@mcp.tool()
def get_stale_dependencies_tool(days_threshold: int = 180) -> str:
    """
    Find dependencies that haven't been updated in the specified number of days.
    
    Args:
        days_threshold: Number of days to consider a dependency stale (default: 180)
    
    Returns:
        str: JSON string containing stale dependency information
    """
    session = session_maker()
    try:
        stale_info = get_stale_dependencies(session, days_threshold)
        return json.dumps(stale_info, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)
    finally:
        session.close()


@mcp.tool()
def create_sample_dependency(name: str, test_version: str, prod_version: str = None) -> str:
    """
    Create a sample dependency for demonstration purposes.
    
    Args:
        name: Unique name for the dependency
        test_version: Version in test environment
        prod_version: Optional version in production environment
    
    Returns:
        str: JSON string containing the created dependency data
    """
    try:
        # check if dependency already exists
        if dependency_service.dependency_exists(name):
            return json.dumps({"error": f"Dependency with name '{name}' already exists"}, indent=2)
        
        # create the dependency
        dependency = dependency_service.create_dependency(
            name=name,
            test_version=test_version,
            prod_version=prod_version
        )
        return json.dumps(dependency, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
def fetch_video_transcript(url: str) -> str:
    """
    Returns sample data for testing

    Args:
        url (str): Any URL (not used, just for compatibility)

    Returns:
        str: Sample formatted data
    """
    sample_data = """[00:00] Welcome to this sample video transcript
[00:15] This is just test data for the MCP server
[00:30] You can use this for quick testing without API calls
[00:45] The data is returned instantly
[01:00] No external dependencies required
[01:15] Perfect for development and testing
[01:30] Thank you for watching"""
    
    return sample_data

@mcp.tool()
def fetch_instructions(prompt_name: str) -> str:
    """
    Fetch instructions for a given prompt name from the prompts/ directory

    Args:
        prompt_name (str): Name of the prompt to fetch instructions for
        Available prompts: 
            - write_blog_post
            - write_social_post
            - write_video_chapters

    Returns:
        str: Instructions for the given prompt
    """
    script_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(script_dir, "prompts", f"{prompt_name}.md")
    with open(prompt_path, "r") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(transport='streamable-http')