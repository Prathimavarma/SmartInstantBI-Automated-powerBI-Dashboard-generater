# SmartInstantBI-Automated-powerBI-Dashboard-generater
The project builds an AI chatbot that automates business dashboard creation. Users type queries like “Show me sales by region for 2024.” The bot uses NLP to understand the query, converts it into SQL, fetches data from SQL Server, and auto-generates an interactive Power BI dashboard—removing manual SQL and design work.
Synopsis of Your Project:
    The project aims to build an AI-powered conversational system that automates the process of creating business dashboards.
    Users can simply type queries like “Show me total sales by region for 2024”, and the chatbot:
    
    Understands the query using Natural Language Processing (NLP),
    
    Translates it into an SQL query,
    
    Fetches data from the SQL Server, and
    
    Automatically generates an interactive Power BI dashboard showing the results.
    
    This system eliminates manual SQL writing and dashboard design, making business intelligence faster, smarter, and more accessible to everyone in an organization.
    
Execution:

The project is implemented using Streamlit for the web interface.

    Users upload a CSV or Excel dataset.
    
    The backend loads a TinyLlama model (for AI processing) and connects to Ollama (for insights generation).
    
    When a file is uploaded, the system automatically generates a Plotly-based dashboard showing key visualizations.
    
    Users can also chat with the AI assistant to ask specific questions about the data — it processes the question, generates Python code, executes it safely, and shows results instantly.
    
Methodology:

    The methodology follows a step-by-step intelligent pipeline:
    
    Data Input: User uploads a CSV or Excel dataset.
    
    NLP Understanding: The chatbot interprets user queries using AI models.
    
    Query Conversion: Natural language is converted into SQL or Python code dynamically.
    
    Data Processing: Extracted data is analyzed using pandas and NumPy.
    
    Visualization: Dashboards are auto-generated using Plotly (in Streamlit) and integrated with Power BI APIs for advanced visualizations.
    
    Insight Generation: Ollama (Gemma3 model) provides textual insights, trends, and observations.
    
    This hybrid AI + BI workflow ensures automation and interactivity throughout the process.

Demo Flow:
    Upload dataset → Preview → Auto Dashboard → Ollama Insights → Chat with Data

Algorithms Used:
    Several algorithmic approaches and AI models are used:
    
    Natural Language Processing (NLP):
    
    Used to interpret user queries and extract metrics, filters, and operations.
    
    Libraries: spaCy, Transformers
    
    Text-to-SQL Conversion Algorithm:
    
    Converts the NLP output into SQL queries automatically.
    
    Ensures syntactic correctness and prevents SQL injection.
    
    Data Analysis Algorithms:
    
    Uses pandas and NumPy for aggregation, grouping, and descriptive analytics.
    
    Dashboard Generation Logic:
    
    Auto-detects column types and suggests appropriate chart types (bar, line, scatter, histogram, etc.)
    
    Uses Plotly Express for dynamic visualization.
    
    AI Insight Generation (Ollama + TinyLlama):
    
    TinyLlama helps generate the dashboard.
    
    Gemma3 model (via Ollama) analyzes datasets to generate human-readable insights.
