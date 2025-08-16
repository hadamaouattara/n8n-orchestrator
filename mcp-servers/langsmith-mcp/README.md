# LangSmith MCP Server for SAPience

This MCP server enables Claude to interact directly with LangSmith for observability, evaluation, and optimization of the SAPience ML platform.

## 🚀 Features

### **Workflow Tracing**
- Trace n8n workflows (Monthly Forecast, Anomaly Detection, etc.)
- Monitor Claude copilot interactions
- Track ML pipeline performance
- Real-time debugging and optimization

### **Model Evaluation**
- Evaluate PUP prediction accuracy (MAPE, RMSE)
- Compare ML model performance (LightGBM vs XGBoost)
- Monitor model drift and degradation
- Automated quality assessments

### **Prompt Optimization** 
- A/B test Claude prompts for SAP analysis
- Optimize anomaly explanations and forecasting summaries
- Improve copilot conversation quality
- Measure prompt performance metrics

### **SAP Dataset Management**
- Create LangSmith datasets from SAP CDS data
- Manage ACDOCA, MBEW, CKML datasets
- Version control for ML training data
- Multi-company code support

### **Performance Monitoring**
- Real-time dashboards for SAPience components
- Alerting for performance degradation
- Trend analysis and capacity planning
- Executive reporting

## 🛠️ Installation

```bash
# Install dependencies
pip install langsmith mcp asyncio pydantic httpx

# Set environment variables
export LANGSMITH_API_KEY="your_langsmith_key"
export LANGSMITH_PROJECT="sapience"
```

## 📋 Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "langsmith": {
      "command": "python",
      "args": ["/path/to/n8n-orchestrator/mcp-servers/langsmith-mcp/server.py"],
      "env": {
        "LANGSMITH_API_KEY": "your_api_key",
        "LANGSMITH_PROJECT": "sapience"
      }
    }
  }
}
```

## 🎯 Usage Examples

### **Trace a Workflow**
```
Claude, trace the monthly_forecast workflow for Company Code 1000
```

### **Evaluate ML Models** 
```
Claude, evaluate the pup_predictor model performance using the latest SAP dataset
```

### **Optimize Prompts**
```
Claude, optimize the anomaly explanation prompt for better accuracy
```

### **Monitor Performance**
```
Claude, show me the SAPience platform performance over the last 24 hours
```

### **Create SAP Dataset**
```
Claude, create a LangSmith dataset from ACDOCA data for Company Codes 1000, 2000
```

## 🔧 Tools Available

| Tool | Description | Use Case |
|------|-------------|----------|
| `trace_sapience_workflow` | Trace ML workflow execution | Debug n8n workflows, monitor Claude interactions |
| `evaluate_ml_predictions` | Evaluate ML model performance | Compare models, monitor MAPE/RMSE |
| `optimize_claude_prompts` | Optimize Claude prompts | Improve copilot responses, A/B test prompts |
| `create_sap_dataset` | Create datasets from SAP data | ML training, evaluation, versioning |
| `monitor_sapience_performance` | Real-time performance monitoring | Alerts, dashboards, capacity planning |
| `generate_langsmith_report` | Generate analytics reports | Executive summaries, trend analysis |

## 📊 Integration with SAPience

### **n8n Workflows**
- Monthly Close Forecast tracing
- Anomaly Detection monitoring
- What-if Analysis optimization
- PUP Prediction evaluation

### **Claude Copilot**
- Conversation quality metrics
- Response accuracy tracking
- Prompt effectiveness measurement
- User satisfaction analysis

### **ML Pipelines**
- Model performance tracking
- Feature importance analysis
- Prediction confidence monitoring
- Data drift detection

### **SAP Integration**
- CDS extraction monitoring
- OAuth token performance
- BTP connection health
- Data quality validation

## 🎭 Advanced Features

### **Automated Evaluations**
```python
# Continuous model evaluation
@traceable(name="pup_prediction")
def predict_pup(sap_data):
    prediction = model.predict(sap_data)
    
    # Automatic LangSmith logging
    langsmith_client.log_metrics({
        "mape": calculate_mape(prediction, actual),
        "confidence": prediction.confidence,
        "company_code": sap_data.company_code
    })
    
    return prediction
```

### **Custom Metrics**
```python
# SAP-specific evaluation metrics
def evaluate_sap_forecast(predictions, actuals):
    return {
        "mape": mean_absolute_percentage_error(predictions, actuals),
        "rmse": root_mean_squared_error(predictions, actuals),
        "sap_variance": calculate_sap_variance(predictions, actuals),
        "business_impact": calculate_business_impact(predictions, actuals)
    }
```

### **Real-time Dashboards**
- Executive KPI monitoring
- Technical performance metrics
- User engagement analytics
- Cost optimization insights

## 🔒 Security & Compliance

- **RGPD Compliant**: All data processing in EU-West-3
- **SOX Audit Trail**: Complete traceability of all operations
- **Role-based Access**: Secure access to sensitive SAP data
- **Encryption**: End-to-end encryption for all communications

## 🚀 Deployment

This MCP server is automatically deployed with the SAPience platform:

1. **Northflank Template**: Included in infrastructure template
2. **Environment Variables**: Configured via secret groups
3. **Health Monitoring**: Integrated with platform monitoring
4. **Auto-scaling**: Scales with SAPience workload

## 📈 Benefits

- **🔍 Full Observability**: Complete visibility into ML workflows
- **📊 Data-Driven Optimization**: Evidence-based prompt and model improvements
- **⚡ Real-time Monitoring**: Instant alerts for performance issues
- **🎯 Quality Assurance**: Continuous evaluation and improvement
- **📋 Executive Reporting**: Business-ready analytics and insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request

## 📞 Support

- **Documentation**: [docs.sapience.ai/langsmith-mcp](https://docs.sapience.ai/langsmith-mcp)
- **Issues**: [GitHub Issues](https://github.com/hadamaouattara/n8n-orchestrator/issues)
- **Slack**: #langsmith-mcp in SAPience Slack

---

**Transform your SAP ML workflows with Claude + LangSmith observability! 🚀**