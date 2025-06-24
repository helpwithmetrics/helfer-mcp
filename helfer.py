from typing import Any
import httpx
import os
import json
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Initialize FastMCP server
mcp = FastMCP("helfer")
load_dotenv()

# Constants
API_BASE = "https://api.helfer-ai.com"
USER_AGENT = "helfer-app/1.0"

# Cache for the auth token
auth_token = None
token_expiry = None

async def get_auth_token() -> str:
    """Get an authentication token from the API server using env credentials."""
    global auth_token, token_expiry  # Add global declaration here
    
    # Check if we have a valid cached token
    if auth_token and token_expiry and datetime.now() < token_expiry:
        return auth_token
    
    # Get credentials from environment variables
    username = os.environ.get("HELFER_USERNAME")
    password = os.environ.get("HELFER_PASSWORD")
    
    if not username or not password:
        raise ValueError("Missing HELFER_USERNAME or HELFER_PASSWORD environment variables")
    
    # Make token request
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    form_data = {
        "username": username,
        "password": password
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_BASE}/token", 
                headers=headers,
                data=form_data,  # Use form data for token endpoint
                timeout=30.0
            )
            response.raise_for_status()
            token_data = response.json()
            
            auth_token = token_data.get("access_token")
            
            # Parse expiry time - if it's a string, convert to datetime
            if isinstance(token_data.get("expires_at"), str):
                token_expiry = datetime.fromisoformat(token_data["expires_at"].replace("Z", "+00:00"))
            else:
                # If not provided, set a conservative expiry (30 minutes)
                token_expiry = datetime.now() + timedelta(minutes=30)
                
            return auth_token
            
        except Exception as ex:
            print(f"Failed to get auth token: {str(ex)}")
            if hasattr(ex, 'response') and hasattr(ex.response, 'text'):
                print(f"Response: {ex.response.text}")
            raise

async def make_request(url: str, data: dict) -> dict[str, Any] | None:
    """Make an authenticated request to the API with proper error handling."""
    global auth_token, token_expiry  # Add global declaration here too
    
    try:
        # Get authentication token
        token = await get_auth_token()
        
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, timeout=60.0, json=data)
            response.raise_for_status()
            return response.json()
    except Exception as ex:
        if hasattr(ex, 'response') and ex.response:
            status_code = ex.response.status_code
            error_text = ex.response.text
            try:
                error_json = ex.response.json()
                error_detail = error_json.get('detail', 'Unknown error')
            except:
                error_detail = error_text[:200]  # Truncate long error messages
                
            # If unauthorized, clear token and retry once
            if status_code == 401 and auth_token:
                print("Token expired, getting new token...")
                auth_token = None  # Now properly affects the global variable
                token_expiry = None
                # Try the request again with a new token
                return await make_request(url, data)
                
            return {"error": f"API error ({status_code}): {error_detail}"}
        return {"error": f'Error in MCP server: {str(ex)}'}

@mcp.tool()
async def ask(question: str) -> str:
    """I'm helfer, I can answer questions about your data. When the user wants to ask helfer, use this tool.

    Args:
        question: Natural Language Question to get answers from your Database
    """
    url = f"{API_BASE}/ask"
    payload = {
      "question": question,
      "include_visualization": False
    }
    data = await make_request(url, payload)

    if not data:
        return "Unable to fetch data"
    elif data and "error" in data and data['error']:
        return f"Error: {data['error']}"

    if not data.get("answer"):
        return "No answer"

    return data['answer']


@mcp.tool()
async def run_sql(sql: str, additional_context: str = '') -> str:
    """I'm helfer-sql, I can run queries to your database. When the user wants helfer ro run a query, use this tool. Provide context for the sql.

    Args:
        sql: SQL query to run to your database Database
        additional_context: Additional Context for the sql. (Optional)
    """
    url = f"{API_BASE}/ask"

    prompt = f"""{additional_context}
Run this query:
```sql
{sql}
```
"""
    payload = {
      "question": prompt,
      "include_visualization": False
    }
    data = await make_request(url, payload)

    if not data:
        return "Unable to fetch data"
    elif data and "error" in data and data['error']:
        return f"Error: {data['error']}"

    if not data.get("answer"):
        return "No answer"

    return data['answer']


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
