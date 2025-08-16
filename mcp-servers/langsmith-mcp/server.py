#!/usr/bin/env python3
"""
MCP Server for LangSmith Integration
Enables Claude to interact directly with LangSmith for SAPience project
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from langsmith import Client
from langsmith.evaluation import evaluate
from langsmith.schemas import Run, Example

# Initialize LangSmith client
langsmith_client = Client()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("langsmith-mcp")

server = Server("langsmith-mcp")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available LangSmith tools for Claude."""
    return [
        types.Tool(
            name="trace_sapience_workflow",
            description="Trace a SAPience ML workflow execution",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_name": {
                        "type": "string",
                        "description": "Name of the workflow (monthly_forecast, anomaly_detection, etc.)"
                    },
                    "session_id": {
                        "type": "string", 
                        "description": "Session ID for grouping related traces"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Additional metadata (company_code, period, etc.)"
                    }
                },
                "required": ["workflow_name"]
            }
        ),
        types.Tool(
            name="evaluate_ml_predictions",
            description="Evaluate ML model performance using LangSmith",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "ML model name (pup_predictor, anomaly_detector, etc.)"
                    },
                    "dataset_name": {
                        "type": "string",
                        "description": "Evaluation dataset name"
                    },
                    "metrics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Metrics to evaluate (mape, rmse, f1_score, etc.)"
                    }
                },
                "required": ["model_name", "dataset_name"]
            }
        ),
        types.Tool(
            name="optimize_claude_prompts",
            description="Optimize Claude prompts for SAP analysis using LangSmith",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt_template": {
                        "type": "string",
                        "description": "Current prompt template to optimize"
                    },
                    "use_case": {
                        "type": "string",
                        "description": "Use case (anomaly_explanation, forecast_summary, etc.)"
                    },
                    "test_examples": {
                        "type": "array",
                        "description": "Test examples for evaluation"
                    }
                },
                "required": ["prompt_template", "use_case"]
            }
        ),
        types.Tool(
            name="create_sap_dataset",
            description="Create LangSmith dataset from SAP data for ML evaluation",
            inputSchema={
                "type": "object",
                "properties": {
                    "dataset_name": {
                        "type": "string",
                        "description": "Name for the new dataset"
                    },
                    "sap_data_source": {
                        "type": "string",
                        "description": "SAP data source (ACDOCA, MBEW, CKML, etc.)"
                    },
                    "company_codes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Company codes to include"
                    },
                    "period_range": {
                        "type": "object",
                        "description": "Date range for data extraction"
                    }
                },
                "required": ["dataset_name", "sap_data_source"]
            }
        ),
        types.Tool(
            name="monitor_sapience_performance",
            description="Monitor real-time performance of SAPience ML pipelines",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_range": {
                        "type": "string",
                        "description": "Time range for monitoring (1h, 24h, 7d, 30d)"
                    },
                    "components": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Components to monitor (ml_models, claude_copilot, n8n_workflows)"
                    }
                },
                "required": ["time_range"]
            }
        ),
        types.Tool(
            name="generate_langsmith_report",
            description="Generate comprehensive LangSmith analytics report for SAPience",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_type": {
                        "type": "string",
                        "enum": ["performance", "quality", "usage", "comprehensive"],
                        "description": "Type of report to generate"
                    },
                    "period": {
                        "type": "string",
                        "description": "Reporting period (weekly, monthly, quarterly)"
                    },
                    "include_recommendations": {
                        "type": "boolean",
                        "description": "Include AI-powered recommendations"
                    }
                },
                "required": ["report_type"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> List[types.TextContent]:
    """Handle tool calls from Claude."""
    
    try:
        if name == "trace_sapience_workflow":
            return await trace_sapience_workflow(arguments)
        elif name == "evaluate_ml_predictions":
            return await evaluate_ml_predictions(arguments)
        elif name == "optimize_claude_prompts":
            return await optimize_claude_prompts(arguments)
        elif name == "create_sap_dataset":
            return await create_sap_dataset(arguments)
        elif name == "monitor_sapience_performance":
            return await monitor_sapience_performance(arguments)
        elif name == "generate_langsmith_report":
            return await generate_langsmith_report(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]

async def trace_sapience_workflow(args: Dict[str, Any]) -> List[types.TextContent]:
    """Trace SAPience workflow execution."""
    workflow_name = args["workflow_name"]
    session_id = args.get("session_id", f"session_{datetime.now().isoformat()}")
    metadata = args.get("metadata", {})
    
    # Create trace session
    trace_url = f"https://smith.langchain.com/projects/sapience/sessions/{session_id}"
    
    # Start tracing workflow
    with langsmith_client.trace(
        name=workflow_name,
        session_id=session_id,
        metadata=metadata
    ) as trace:
        trace.log_metadata({
            "platform": "sapience",
            "component": workflow_name,
            "timestamp": datetime.now().isoformat(),
            **metadata
        })
    
    return [types.TextContent(
        type="text",
        text=f"""✅ Workflow tracing started for '{workflow_name}'
        
📊 **Trace Details:**
- Session ID: {session_id}
- Workflow: {workflow_name}
- Metadata: {json.dumps(metadata, indent=2)}
- Trace URL: {trace_url}

🔍 **Next Steps:**
- Execute your workflow normally
- All ML predictions, Claude interactions, and n8n triggers will be automatically traced
- View real-time performance at: {trace_url}
"""
    )]

async def evaluate_ml_predictions(args: Dict[str, Any]) -> List[types.TextContent]:
    """Evaluate ML model performance."""
    model_name = args["model_name"]
    dataset_name = args["dataset_name"]
    metrics = args.get("metrics", ["mape", "rmse"])
    
    # Run evaluation
    try:
        evaluation_results = await run_model_evaluation(model_name, dataset_name, metrics)
        
        return [types.TextContent(
            type="text",
            text=f"""📈 **ML Model Evaluation Results**

🎯 **Model:** {model_name}
📊 **Dataset:** {dataset_name}

**Performance Metrics:**
{format_evaluation_results(evaluation_results)}

**Recommendations:**
{generate_model_recommendations(evaluation_results)}

🔗 **View detailed results:** https://smith.langchain.com/projects/sapience/evaluations
"""
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Evaluation failed: {str(e)}"
        )]

async def optimize_claude_prompts(args: Dict[str, Any]) -> List[types.TextContent]:
    """Optimize Claude prompts using LangSmith."""
    prompt_template = args["prompt_template"]
    use_case = args["use_case"]
    test_examples = args.get("test_examples", [])
    
    # Run prompt optimization
    optimization_results = await run_prompt_optimization(
        prompt_template, use_case, test_examples
    )
    
    return [types.TextContent(
        type="text",
        text=f"""🚀 **Prompt Optimization Results**

📝 **Use Case:** {use_case}

**Original Prompt Performance:**
- Accuracy: {optimization_results['original_score']:.2%}
- Latency: {optimization_results['original_latency']:.2f}s

**Optimized Prompt Performance:**
- Accuracy: {optimization_results['optimized_score']:.2%} (+{optimization_results['improvement']:.1%})
- Latency: {optimization_results['optimized_latency']:.2f}s

**🎯 Recommended Prompt:**
```
{optimization_results['optimized_prompt']}
```

**Key Improvements:**
{format_prompt_improvements(optimization_results['improvements'])}
"""
    )]

async def create_sap_dataset(args: Dict[str, Any]) -> List[types.TextContent]:
    """Create LangSmith dataset from SAP data."""
    dataset_name = args["dataset_name"]
    sap_data_source = args["sap_data_source"]
    company_codes = args.get("company_codes", [])
    
    # Create dataset
    dataset_info = await create_dataset_from_sap(
        dataset_name, sap_data_source, company_codes
    )
    
    return [types.TextContent(
        type="text",
        text=f"""📊 **SAP Dataset Created Successfully**

**Dataset:** {dataset_name}
**Source:** {sap_data_source}
**Records:** {dataset_info['record_count']:,}
**Company Codes:** {', '.join(company_codes) if company_codes else 'All'}

**Schema:**
{format_dataset_schema(dataset_info['schema'])}

**Usage:**
- Use this dataset for ML model evaluation
- Available in LangSmith for prompt testing
- Suitable for {sap_data_source} analysis workflows

🔗 **Dataset URL:** https://smith.langchain.com/projects/sapience/datasets/{dataset_name}
"""
    )]

async def monitor_sapience_performance(args: Dict[str, Any]) -> List[types.TextContent]:
    """Monitor SAPience performance in real-time."""
    time_range = args["time_range"]
    components = args.get("components", ["ml_models", "claude_copilot", "n8n_workflows"])
    
    monitoring_data = await get_performance_metrics(time_range, components)
    
    return [types.TextContent(
        type="text",
        text=f"""📊 **SAPience Performance Monitor** ({time_range})

{format_performance_dashboard(monitoring_data)}

**🚨 Alerts:**
{format_performance_alerts(monitoring_data['alerts'])}

**📈 Trends:**
{format_performance_trends(monitoring_data['trends'])}

**🎯 Recommendations:**
{format_performance_recommendations(monitoring_data)}
"""
    )]

async def generate_langsmith_report(args: Dict[str, Any]) -> List[types.TextContent]:
    """Generate comprehensive LangSmith report."""
    report_type = args["report_type"]
    period = args.get("period", "monthly")
    include_recommendations = args.get("include_recommendations", True)
    
    report_data = await generate_analytics_report(report_type, period)
    
    return [types.TextContent(
        type="text",
        text=f"""📋 **SAPience Analytics Report** ({report_type.title()} - {period.title()})

{format_analytics_report(report_data, include_recommendations)}

📊 **Executive Summary:**
{report_data['executive_summary']}

🔗 **Full Report:** https://smith.langchain.com/projects/sapience/reports/{report_data['report_id']}
"""
    )]

# Helper functions (implementation would be more detailed)
async def run_model_evaluation(model_name: str, dataset_name: str, metrics: List[str]) -> Dict:
    # Implementation for ML evaluation
    pass

async def run_prompt_optimization(prompt: str, use_case: str, examples: List) -> Dict:
    # Implementation for prompt optimization
    pass

async def create_dataset_from_sap(name: str, source: str, company_codes: List[str]) -> Dict:
    # Implementation for SAP dataset creation
    pass

async def get_performance_metrics(time_range: str, components: List[str]) -> Dict:
    # Implementation for performance monitoring
    pass

async def generate_analytics_report(report_type: str, period: str) -> Dict:
    # Implementation for report generation
    pass

def format_evaluation_results(results: Dict) -> str:
    # Format evaluation results
    pass

def format_performance_dashboard(data: Dict) -> str:
    # Format performance dashboard
    pass

def format_analytics_report(data: Dict, include_recommendations: bool) -> str:
    # Format analytics report
    pass

async def main():
    """Main entry point for the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="langsmith-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())