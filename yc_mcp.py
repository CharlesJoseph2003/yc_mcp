from mcp.server.fastmcp import FastMCP
import requests
import traceback
import sys
import re

# Create the server
mcp = FastMCP("YC Directory Server")

@mcp.tool()
def list_top_companies(limit: int = 10) -> dict:
    """
    List the top YC companies.
    
    Args:
        limit: Maximum number of companies to return
        
    Returns:
        Dictionary with list of top companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/top.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data[:limit]}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_companies_by_batch(batch: str) -> dict:
    """
    Query companies from a specific YC batch.
    
    Args:
        batch: The YC batch identifier (e.g., "W21")
        
    Returns:
        Dictionary with companies from the specified batch
    """
    try:
        url = f"https://yc-oss.github.io/api/batches/{batch.lower()}.json"
        response = requests.get(url)
        response.raise_for_status()
        return {"batch": batch, "companies": response.json()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_companies(keyword: str) -> dict:
    """
    Search for companies with a keyword in name/description.
    
    Args:
        keyword: The search term to look for in company names and descriptions
        
    Returns:
        Dictionary of matching companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/all.json"
        response = requests.get(url)
        response.raise_for_status()
        all_companies = response.json()
        matches = [c for c in all_companies if keyword.lower() in c['name'].lower() or keyword.lower() in c.get('one_liner', '').lower()]
        return {"matches": matches}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_all_batches() -> dict:
    """
    List all available YC batches with their company counts.
    
    Returns:
        Dictionary with all YC batches and their details
    """
    try:
        # This is a static list of all known YC batches with their URLs
        batches = [
            {"name": "Winter 2012", "count": 66, "url": "https://yc-oss.github.io/api/batches/winter-2012.json"},
            {"name": "Summer 2011", "count": 60, "url": "https://yc-oss.github.io/api/batches/summer-2011.json"},
            {"name": "Winter 2011", "count": 45, "url": "https://yc-oss.github.io/api/batches/winter-2011.json"},
            {"name": "Summer 2010", "count": 36, "url": "https://yc-oss.github.io/api/batches/summer-2010.json"},
            {"name": "Winter 2010", "count": 27, "url": "https://yc-oss.github.io/api/batches/winter-2010.json"},
            {"name": "Summer 2009", "count": 26, "url": "https://yc-oss.github.io/api/batches/summer-2009.json"},
            {"name": "Winter 2009", "count": 16, "url": "https://yc-oss.github.io/api/batches/winter-2009.json"},
            {"name": "Summer 2008", "count": 22, "url": "https://yc-oss.github.io/api/batches/summer-2008.json"},
            {"name": "Winter 2008", "count": 21, "url": "https://yc-oss.github.io/api/batches/winter-2008.json"},
            {"name": "Summer 2007", "count": 19, "url": "https://yc-oss.github.io/api/batches/summer-2007.json"},
            {"name": "Winter 2007", "count": 13, "url": "https://yc-oss.github.io/api/batches/winter-2007.json"},
            {"name": "Summer 2006", "count": 11, "url": "https://yc-oss.github.io/api/batches/summer-2006.json"},
            {"name": "Winter 2006", "count": 7, "url": "https://yc-oss.github.io/api/batches/winter-2006.json"},
            {"name": "Summer 2005", "count": 8, "url": "https://yc-oss.github.io/api/batches/summer-2005.json"},
            {"name": "Summer 2012", "count": 83, "url": "https://yc-oss.github.io/api/batches/summer-2012.json"},
            {"name": "Winter 2013", "count": 46, "url": "https://yc-oss.github.io/api/batches/winter-2013.json"},
            {"name": "Summer 2013", "count": 52, "url": "https://yc-oss.github.io/api/batches/summer-2013.json"},
            {"name": "Winter 2014", "count": 74, "url": "https://yc-oss.github.io/api/batches/winter-2014.json"},
            {"name": "Summer 2014", "count": 80, "url": "https://yc-oss.github.io/api/batches/summer-2014.json"},
            {"name": "Winter 2015", "count": 111, "url": "https://yc-oss.github.io/api/batches/winter-2015.json"},
            {"name": "Summer 2015", "count": 105, "url": "https://yc-oss.github.io/api/batches/summer-2015.json"},
            {"name": "Winter 2016", "count": 122, "url": "https://yc-oss.github.io/api/batches/winter-2016.json"},
            {"name": "Summer 2017", "count": 125, "url": "https://yc-oss.github.io/api/batches/summer-2017.json"},
            {"name": "Summer 2016", "count": 102, "url": "https://yc-oss.github.io/api/batches/summer-2016.json"},
            {"name": "Winter 2017", "count": 116, "url": "https://yc-oss.github.io/api/batches/winter-2017.json"},
            {"name": "Winter 2018", "count": 147, "url": "https://yc-oss.github.io/api/batches/winter-2018.json"},
            {"name": "Summer 2018", "count": 131, "url": "https://yc-oss.github.io/api/batches/summer-2018.json"},
            {"name": "Summer 2019", "count": 175, "url": "https://yc-oss.github.io/api/batches/summer-2019.json"},
            {"name": "Winter 2019", "count": 195, "url": "https://yc-oss.github.io/api/batches/winter-2019.json"},
            {"name": "Winter 2020", "count": 228, "url": "https://yc-oss.github.io/api/batches/winter-2020.json"},
            {"name": "Summer 2020", "count": 208, "url": "https://yc-oss.github.io/api/batches/summer-2020.json"},
            {"name": "Winter 2021", "count": 336, "url": "https://yc-oss.github.io/api/batches/winter-2021.json"},
            {"name": "Summer 2021", "count": 391, "url": "https://yc-oss.github.io/api/batches/summer-2021.json"},
            {"name": "Winter 2022", "count": 399, "url": "https://yc-oss.github.io/api/batches/winter-2022.json"},
            {"name": "Summer 2022", "count": 234, "url": "https://yc-oss.github.io/api/batches/summer-2022.json"},
            {"name": "Winter 2023", "count": 275, "url": "https://yc-oss.github.io/api/batches/winter-2023.json"},
            {"name": "Summer 2023", "count": 219, "url": "https://yc-oss.github.io/api/batches/summer-2023.json"},
            {"name": "Winter 2024", "count": 253, "url": "https://yc-oss.github.io/api/batches/winter-2024.json"},
            {"name": "Winter 2025", "count": 163, "url": "https://yc-oss.github.io/api/batches/winter-2025.json"},
            {"name": "Summer 2024", "count": 252, "url": "https://yc-oss.github.io/api/batches/summer-2024.json"},
            {"name": "Fall 2024", "count": 95, "url": "https://yc-oss.github.io/api/batches/fall-2024.json"},
            {"name": "Spring 2025", "count": 100, "url": "https://yc-oss.github.io/api/batches/spring-2025.json"},
            {"name": "Unspecified", "count": 1, "url": "https://yc-oss.github.io/api/batches/unspecified.json"}
        ]
        
        # Sort batches by year and season
        def batch_sort_key(batch):
            name = batch["name"]
            # Extract year
            year_match = re.search(r'\d{4}', name)
            year = int(year_match.group(0)) if year_match else 0
            
            # Determine season order (Winter=0, Spring=1, Summer=2, Fall=3)
            season_order = 4  # Default for "Unspecified"
            if "Winter" in name:
                season_order = 0
            elif "Spring" in name:
                season_order = 1
            elif "Summer" in name:
                season_order = 2
            elif "Fall" in name:
                season_order = 3
                
            return (year, season_order)
            
        sorted_batches = sorted(batches, key=batch_sort_key)
        return {"batches": sorted_batches}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_batches(query: str) -> dict:
    """
    Search for YC batches by name or year.
    
    Args:
        query: Search term to find matching batches (e.g., "2021", "Winter", etc.)
        
    Returns:
        Dictionary with matching batches
    """
    try:
        # First get all batches
        all_batches_result = list_all_batches()
        
        if "error" in all_batches_result:
            return all_batches_result
            
        all_batches = all_batches_result["batches"]
        
        # Filter batches by the query
        query = query.lower()
        matches = [b for b in all_batches if query in b["name"].lower()]
        
        return {"matches": matches}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    try:
        mcp.run()
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)