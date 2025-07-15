# Supabase MCP Server

A powerful Model Context Protocol (MCP) server that provides seamless integration with Supabase databases. This server enables AI assistants like Claude to interact with your Supabase database through a standardized interface, supporting all CRUD operations with advanced querying capabilities.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete records with full support
- **Advanced Querying**: Filter, sort, paginate, and select specific columns
- **Type Safety**: Built with Pydantic for robust data validation
- **Error Handling**: Comprehensive error handling with detailed error messages
- **FastMCP Integration**: Uses the latest FastMCP framework for optimal performance
- **Secure Authentication**: Supports Supabase service role keys for secure access
- **Modern Architecture**: Clean, maintainable code with decorator-based tool registration

## 📋 Prerequisites

- Python 3.8+
- Supabase account and project
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/iamRajamurugan/Supabase_MCP_Server.git
cd Supabase_MCP_Server
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
```

Edit the `.env` file with your Supabase credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 🔧 Configuration

### Environment Variables

- `SUPABASE_URL`: Your Supabase project URL (format: `https://your-project.supabase.co`)
- `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role key (found in Project Settings > API)

### Claude Desktop Integration

Add this configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "python",
      "args": [
        "C:\\path\\to\\your\\project\\supabase-mcp\\server.py"
      ],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
```

## 🚀 Usage

### Starting the Server

```bash
python supabase-mcp/server.py
```

### Available Tools

#### 1. **read_records**
Fetch records from any table with advanced filtering and sorting.

**Parameters:**
- `table` (required): Table name
- `columns` (optional): Comma-separated column names or "*" for all
- `filters` (optional): Key-value pairs for filtering
- `limit` (optional): Maximum number of records
- `offset` (optional): Number of records to skip
- `order_by` (optional): Sorting options

**Example:**
```json
{
  "table": "users",
  "columns": "name,email,age",
  "filters": {"age": {"gte": 18}},
  "limit": 10,
  "order_by": {"created_at": "desc"}
}
```

#### 2. **create_records**
Create one or multiple records in a table.

**Parameters:**
- `table` (required): Table name
- `records` (required): Single record object or array of records

**Example:**
```json
{
  "table": "users",
  "records": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
```

#### 3. **update_records**
Update existing records based on filter conditions.

**Parameters:**
- `table` (required): Table name
- `updates` (required): Fields to update
- `filters` (required): Conditions to identify records

**Example:**
```json
{
  "table": "users",
  "updates": {"age": 31},
  "filters": {"id": 1}
}
```

#### 4. **delete_records**
Delete records based on filter conditions.

**Parameters:**
- `table` (required): Table name
- `filters` (required): Conditions to identify records

**Example:**
```json
{
  "table": "users",
  "filters": {"id": 1}
}
```

## 📊 Database Schema Example

Here's a sample schema to test the server:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    author_id INTEGER REFERENCES users(id),
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sample data
INSERT INTO users (name, email, age) VALUES
('John Doe', 'john@example.com', 25),
('Jane Smith', 'jane@example.com', 30),
('Bob Johnson', 'bob@example.com', 35);

INSERT INTO posts (title, content, author_id, published) VALUES
('First Post', 'This is the content of the first post', 1, true),
('Second Post', 'This is the content of the second post', 2, false);
```

## 🧪 Testing

### Manual Testing

1. **Start the server:**
```bash
python supabase-mcp/server.py
```

2. **Initialize the MCP connection:**
```json
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
```

3. **Send initialized notification:**
```json
{"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
```

4. **List available tools:**
```json
{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
```

5. **Test a tool:**
```json
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "read_records", "arguments": {"table": "users"}}}
```

### Natural Language Testing

Use these prompts with Claude Desktop:

- "Show me all users in the database"
- "Create a new user named Sarah with email sarah@example.com and age 28"
- "Update the user with ID 1 to have age 26"
- "Delete the user with ID 3"

## 🏗️ Architecture

### Project Structure
```
supabase-mcp/
├── server.py              # Main MCP server with tool definitions
├── supabase_client.py     # Supabase client wrapper
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your environment variables (not in repo)
└── README.md            # This file
```

### Key Components

- **FastMCP Framework**: Modern MCP server implementation
- **Pydantic Models**: Type-safe data validation
- **Supabase Client**: Official Supabase Python client
- **Error Handling**: Comprehensive error catching and reporting

## 🔒 Security

- Use service role keys for server-to-server communication
- Environment variables for sensitive data
- Input validation through Pydantic models
- Proper error handling to prevent information leakage

## 🐛 Troubleshooting

### Common Issues

1. **Connection Refused**: Check your `SUPABASE_URL` format
2. **Authentication Errors**: Verify your service role key
3. **Permission Denied**: Ensure RLS policies allow service role access
4. **Import Errors**: Make sure all dependencies are installed

### Debug Mode

Enable debug logging by modifying the server:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [FastMCP](https://gofastmcp.com/) for the excellent MCP framework
- [Supabase](https://supabase.com/) for the amazing database platform
- [Model Context Protocol](https://github.com/modelcontextprotocol) for the standardized interface


**Built with ❤️ by [Raja Murugan](https://github.com/iamRajamurugan)**
