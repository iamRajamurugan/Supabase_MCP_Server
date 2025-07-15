"""
Supabase MCP Server

A FastMCP server that provides tools for interacting with a Supabase database.
Uses the Model Context Protocol (MCP) with Stdio transport.
"""

from typing import Any, Dict, List, Optional, Union
import json
import sys

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from supabase_client import SupabaseClient

# Initialize FastMCP server
mcp = FastMCP(name="supabase-mcp")

# Initialize Supabase client
supabase = SupabaseClient()


@mcp.tool
def read_records(
    table: str = Field(..., description="Name of the table to read from"),
    columns: str = Field("*", description="Columns to select (comma-separated or * for all)"),
    filters: Optional[Dict[str, Any]] = Field(
        None, 
        description="Filtering conditions as key-value pairs (e.g., {\"column\": \"value\"} for column = value)"
    ),
    limit: Optional[int] = Field(None, description="Maximum number of records to return"),
    offset: Optional[int] = Field(None, description="Number of records to skip for pagination"),
    order_by: Optional[Dict[str, str]] = Field(
        None, 
        description="Sorting options as column:direction pairs (e.g., {\"created_at\": \"desc\"})"
    )
) -> Dict[str, Any]:
    """
    Reads records from a Supabase database table with flexible querying options.
    Use this tool to fetch data from your database with options for filtering,
    sorting, and pagination.
    
    Common use cases:
    - Retrieve all records from a table
    - Fetch specific records based on conditions
    - Get paginated results for large datasets
    - Retrieve only specific columns from records
    
    The returned data is always an array of record objects, even if only one record is found.
    If no records match the criteria, an empty array is returned.
    """
    try:
        records = supabase.read_records(
            table=table,
            columns=columns,
            filters=filters,
            limit=limit,
            offset=offset,
            order_by=order_by
        )
        return {"records": records}
    except Exception as e:
        return {"error": str(e), "records": []}


@mcp.tool
def create_records(
    table: str = Field(..., description="Name of the table to create records in"),
    records: Union[Dict[str, Any], List[Dict[str, Any]]] = Field(
        ..., 
        description="A single record object or array of record objects to create"
    )
) -> Dict[str, Any]:
    """
    Creates one or more records in a Supabase database table.
    Use this tool to insert new data into your database.
    
    Common use cases:
    - Add a single new record to a table
    - Bulk insert multiple records at once
    - Create related records
    
    You can provide either a single record object or an array of record objects.
    The tool returns the created records with their assigned IDs and timestamps (if applicable).
    Make sure the data structure matches the table schema to avoid validation errors.
    """
    try:
        created = supabase.create_records(
            table=table,
            records=records
        )
        return {"records": created}
    except Exception as e:
        return {"error": str(e), "records": []}


@mcp.tool
def update_records(
    table: str = Field(..., description="Name of the table to update records in"),
    updates: Dict[str, Any] = Field(..., description="Fields to update as key-value pairs"),
    filters: Dict[str, Any] = Field(
        ..., 
        description="Filtering conditions to identify records to update (e.g., {\"id\": 123})"
    )
) -> Dict[str, Any]:
    """
    Updates existing records in a Supabase database table based on filter conditions.
    Use this tool to modify existing data that matches specific criteria.
    
    Common use cases:
    - Update a specific record by ID
    - Batch update multiple records matching a condition
    - Modify specific fields while keeping others unchanged
    
    The 'updates' parameter specifies which fields to update and their new values.
    The 'filters' parameter determines which records will be updated.
    Be careful with filter conditions - if they match many records, all of them will be updated.
    The tool returns the updated records after modification.
    """
    try:
        updated = supabase.update_records(
            table=table,
            updates=updates,
            filters=filters
        )
        return {"records": updated}
    except Exception as e:
        return {"error": str(e), "records": []}


@mcp.tool
def delete_records(
    table: str = Field(..., description="Name of the table to delete records from"),
    filters: Dict[str, Any] = Field(
        ..., 
        description="Filtering conditions to identify records to delete (e.g., {\"id\": 123})"
    )
) -> Dict[str, Any]:
    """
    Deletes records from a Supabase database table based on filter conditions.
    Use this tool to remove data that matches specific criteria.
    
    Common use cases:
    - Delete a specific record by ID
    - Remove multiple records matching a condition
    - Clean up old or unnecessary data
    
    ⚠️ IMPORTANT: Deletions are permanent and cannot be undone. Always confirm the filter
    conditions carefully before deleting records.
    For safety, always use specific filter conditions to avoid accidentally deleting too many records.
    The tool returns the deleted records as they were before deletion.
    """
    try:
        deleted = supabase.delete_records(
            table=table,
            filters=filters
        )
        return {"records": deleted}
    except Exception as e:
        return {"error": str(e), "records": []}


if __name__ == "__main__":
    mcp.run(transport="stdio")
