# Dagster Snowflake dbt Demo - Serverless Analytics Pipeline

A comprehensive **Proof of Value** project showcasing Dagster 1.11+ capabilities with Snowflake and dbt. This project uses modern Dagster patterns including the `defs` folder structure and `dg` CLI, designed for prospects to quickly evaluate Dagster's value proposition without having to write custom code.

## 🎯 What This Demo Showcases

This project demonstrates enterprise-grade data orchestration with:

- **🔄 dbt Component Integration**: YAML-configured dbt project with staging and mart models
- **📊 Asset-Based Architecture**: Data lineage tracking and dependency management  
- **⚡ Serverless Deployment**: Ready for Dagster Cloud with minimal configuration
- **📅 Scheduling & Orchestration**: Multiple job types with different cadences
- **🔍 Data Quality Monitoring**: Asset checks and automated validation
- **📈 Business Intelligence**: KPI calculations and trend analysis  
- **🚨 Event-Driven Architecture**: Sensors for conditional orchestration
- **⏰ Asset Freshness Policies**: Monitor data staleness with time windows and cron schedules
- **📧 Alert Policies**: Comprehensive monitoring with email/Slack notifications
- **👥 Dagster+ Features**: RBAC, cost monitoring, branch deployments, asset catalog
- **🆕 Modern dg-managed Project**: Uses Dagster 1.11+ `dg` CLI with automatic definition discovery from `defs` folder

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Snowflake account with access to `SNOWFLAKE_SAMPLE_DATA`
- Python 3.9+ 
- Dagster Cloud account (free tier available)

### 1. Clone and Install

**Option A: Command Line**
```bash
git clone https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git
cd snowflake-dbt-serverless-example
pip install -e .
```

**Option B: VS Code**
1. **Open VS Code** and press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. **Type "Git: Clone"** and select it
3. **Paste repository URL**: `https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git`
4. **Choose a folder** and open the cloned project
5. **Open terminal** in VS Code (`View` → `Terminal`) and run:
   ```bash
   pip install -e .
   ```

**Option C: Cursor IDE**
1. **Open Cursor** and click "Clone Repository" on the welcome screen
2. **Paste repository URL**: `https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git`
3. **Choose a folder** and open the cloned project
4. **Open terminal** in Cursor (`Terminal` → `New Terminal`) and run:
   ```bash
   pip install -e .
   ```

> 💡 **IDE Benefits**: VS Code and Cursor provide excellent Python support, Git integration, and terminal access for running Dagster commands.

### 2. Configure Snowflake Connection
Copy the example environment file and fill in your Snowflake credentials:
```bash
cp env.example .env
```

Edit `.env` with your Snowflake details:
```bash
# Your Snowflake connection details
SNOWFLAKE_ACCOUNT=your_account.region.cloud_provider
SNOWFLAKE_USER=your_username  
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH

# Using public sample data (no changes needed)
SNOWFLAKE_DATABASE=SNOWFLAKE_SAMPLE_DATA
SNOWFLAKE_SCHEMA=TPCH_SF1
SNOWFLAKE_ROLE=PUBLIC
```

> 💡 **Modern Environment Variable Management**  
> This project uses Dagster's `dg.EnvVar()` class for enhanced Dagster+ integration:
> - **🔍 Improved observability** - Config values visible in Dagster+ UI
> - **🔒 Secret protection** - Passwords automatically hidden in UI  
> - **🧪 Simplified testing** - Easy to mock for unit tests
> - **☁️ Dagster+ ready** - Seamless integration with cloud environment variables

### 3. Test Locally
```bash
# Install development dependencies
pip install -e ".[dev]"

# Launch Dagster UI with modern dg CLI
dg dev

# Navigate to http://localhost:3000
```

**IDE-Specific Tips:**

**VS Code Users:**
- **Install Python extension** for better code navigation and debugging
- **Use integrated terminal** (`View` → `Terminal`) to run `dg dev`
- **Split terminal** to keep `dg dev` running while exploring code
- **Port forwarding** automatically works for http://localhost:3000

**Cursor Users:**
- **AI assistant** can help explain Dagster concepts as you explore
- **Use terminal** (`Terminal` → `New Terminal`) to run `dg dev`
- **AI can help modify** assets, jobs, and schedules as you customize
- **Excellent for learning** Dagster patterns through code exploration

> 🚀 **Coming Soon**: VS Code extension for even easier Dagster+ deployment directly from your editor!

**🔧 Dependency Management:**

This project uses pinned dependency versions in `pyproject.toml` to ensure compatibility:
- `dbt-core==1.8.4` and `dbt-snowflake==1.8.4` for stable dbt integration
- `protobuf>=4.0.0,<5.0` to avoid gRPC conflicts
- `click>=8.0,<8.2` for Dagster CLI compatibility

If you encounter dependency conflicts, the pinned versions ensure a working environment.

**🔧 dbt Manifest Management:**

This project includes a pre-generated `dbt_project/target/manifest.json` for immediate testing. If you modify dbt models, regenerate the manifest:

```bash
# Navigate to dbt project directory
cd dbt_project

# Generate fresh manifest (requires valid Snowflake connection)
dbt parse

# Or generate with sample profiles
dbt parse --profiles-dir .
```

**🎯 What You'll See in the UI:**
- 📊 **2 Python analytics assets** (business_intelligence group) with dual kinds (python + snowflake)
- 🔄 **6 dbt models** (tpch_analytics group) from staging to marts
- 🌐 **3 external sources** (default group) representing TPC-H sample data
- 📅 **3 schedules** for different cadences (daily, hourly, weekly)
- 🔍 **1 demo sensor** showing conditional orchestration patterns
- ⚡ **4 orchestration jobs** demonstrating different pipeline patterns
- 📋 **4 asset checks** for comprehensive data quality validation
- ⏰ **Freshness policies** monitoring data staleness with time windows and cron schedules

### 4. Deploy to Dagster+

Choose your deployment method:

#### Option A: Fork & Use Dagster+ Onboarding (Recommended)
**For the guided onboarding experience:**
```bash
# 1. Fork this repository to your GitHub account:
#    https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example
# 2. Sign up for Dagster+ trial at https://dagster.cloud
# 3. Select "Import a Dagster project" in onboarding
# 4. Choose GitHub and select your forked repository
# 5. Set environment variables in Dagster+ UI (see below)
# 6. ✅ Ready to test and customize!
```

> **Why fork?** Dagster+ onboarding requires repository ownership - you can't import public repos you don't control.

#### Option B: Quick Upload (Manual Testing)
```bash
# 1. Clone the repository first (see "Clone and Install" section above)

# 2. Install Dagster CLI if not already installed
pip install dagster-cloud

# 3. Configure authentication (get token from Dagster+ UI)
export DAGSTER_CLOUD_API_TOKEN="your_token_here"
export DAGSTER_CLOUD_ORGANIZATION="your_org_name"

# 4. Set deployment target (or use --deployment flag)
export DAGSTER_CLOUD_DEPLOYMENT="prod"  # or your deployment name

# 5. Upload directly to Dagster+ (no Git setup needed)
dagster-cloud serverless deploy \
  --location-name snowflake-demo \
  --package-name dagster_snowflake_dbt_demo

# 6. Set Snowflake environment variables in Dagster+ UI:
#    - SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, etc.
# ✅ Ready to test!
```

**Required Setup:**
- Dagster+ account and organization
- API token from Dagster+ UI (Settings → Tokens)
- Deployment name (usually "prod" for main deployment)

#### Option C: Manual Git Integration (Skip Onboarding)
1. **Fork this repository** to your GitHub account
2. **Skip the onboarding** and go directly to Dagster+ UI
3. **Add code location manually** in Deployment → Settings
4. **Connect to your forked repository**
5. **Set environment variables** in Dagster+ UI

> 💡 **Recommendation**: Use **Option A** for the best experience - fork first, then use Dagster+ onboarding for guided setup.

> 🚀 **Coming Soon**: VS Code extension for even easier Dagster+ deployment directly from your editor!

## ⏰ Asset Freshness Policies

Monitor data staleness with built-in Dagster freshness policies:

- **🕒 Time Window Policies**: Critical assets like `business_kpis` warn after 2 hours, fail after 4 hours
- **📅 Cron Policies**: Raw data assets expected to refresh daily at 6 AM UTC  
- **🌍 Default Policies**: All assets get 24-hour warning, 48-hour failure unless overridden
- **🔧 Auto-enabled**: Preview feature enabled via `dagster.yaml`

This modern approach replaces custom "data staleness" sensors with native UI monitoring.

## 🔧 Orchestration Jobs Explained

The project includes 4 different job patterns demonstrating real-world orchestration strategies:

### 1. **`dbt_models_job`** - Pure Data Transformation
- **Purpose**: Runs only dbt models (staging + marts)
- **Selection**: `tpch_analytics` group
- **Use Case**: Data engineering-focused runs, useful for testing dbt changes
- **Schedule**: Manual/on-demand

### 2. **`daily_analytics_job`** - Full Pipeline
- **Purpose**: Complete daily analytics refresh
- **Selection**: `tpch_analytics` + `business_intelligence` groups
- **Use Case**: Primary production job for daily reporting
- **Schedule**: Daily at 6:00 AM UTC

### 3. **`hourly_metrics_job`** - Lightweight Updates  
- **Purpose**: Quick refresh of business metrics for dashboards
- **Selection**: Only `business_kpis` and `monthly_trends` assets
- **Use Case**: Real-time dashboard updates without heavy dbt processing
- **Schedule**: Hourly

### 4. **`data_quality_job`** - Pure Quality Validation
- **Purpose**: Runs asset checks only (no data materialization)
- **Selection**: Asset checks for critical mart models
- **Use Case**: Data quality monitoring, can run independently of data processing
- **Schedule**: Weekly on Mondays at 8:00 AM UTC

**Business Value**: This job variety demonstrates how teams can optimize for different needs - specialized vs. comprehensive runs, fast updates, quality-first validation, etc. 

**Note**: For complete rebuilds or recovery scenarios, simply run `daily_analytics_job` manually - it covers the full pipeline.

## 🔧 Modern dg-managed Architecture

This project showcases the latest Dagster patterns:

### **Complete Auto-Discovery**
- **No manual imports**: Definitions automatically discovered from `defs/` folder
- **Zero boilerplate**: `load_from_defs_folder()` handles everything
- **Clean separation**: Resources defined separately and merged automatically

### **dg CLI Integration**
```bash
dg dev          # Modern development server
dg check        # Validate project structure  
dg scaffold     # Generate new assets/jobs
dg docs         # Generate documentation
```

### **dbt Component Configuration**
- **YAML-driven**: dbt project configured via `defs/dbt_analytics/defs.yaml`
- **Zero Python code**: No custom dbt_assets functions needed
- **Component structure**: Follows proper Dagster component directory pattern
- **Auto-discovery**: dbt models automatically become Dagster assets

### **Project Structure Benefits**
- **Intuitive organization**: Everything in logical `defs/` subfolders
- **Scalable**: Add new definitions without touching `definitions.py`
- **Standard compliance**: Follows Dagster 1.11+ best practices

## 📊 Data Architecture

### Source Data (TPC-H Sample Dataset)
- **Customer**: Customer information and account details
- **Orders**: Order transactions and metadata  
- **LineItem**: Individual line items within orders

### dbt Models

#### Staging Layer (`models/staging/`)
- `stg_customers`: Cleaned customer dimension
- `stg_orders`: Normalized order facts
- `stg_lineitems`: Line item details with calculations

#### Mart Layer (`models/marts/`)
- `customer_metrics`: Customer-level analytics and segmentation
- `order_analytics`: Order-level insights with line item rollups
- `daily_sales_summary`: Daily aggregated metrics for dashboards

### Dagster Assets

#### Raw Data Assets
- `raw_customer_data`: Direct Snowflake connectivity demonstration

#### Analytics Assets  
- `business_kpis`: Key performance indicators calculation
- `monthly_trends`: Time-series analysis with growth metrics
- `data_quality_checks`: Comprehensive quality monitoring

## 🔧 Orchestration Features

### Jobs
- **Daily Analytics Job**: Complete pipeline refresh (6 AM UTC)
- **Hourly Metrics Job**: Dashboard metrics update (every hour)
- **Data Quality Job**: Validation and monitoring (weekly)
- **Full Refresh Job**: Complete asset refresh (on-demand)

### Schedules
- **Daily Schedule**: Morning pipeline execution
- **Hourly Schedule**: Real-time metrics updates
- **Weekly Data Quality**: Comprehensive validation

### Sensors
- **Data Freshness Sensor**: Triggers quality checks when data becomes stale
- **Business Hours Sensor**: Conditional execution during business hours

### Asset Checks
- **Customer Metrics Quality**: Validates completeness and business logic
- **Order Analytics Quality**: Ensures order total consistency
- **Daily Sales Completeness**: Monitors data freshness and gaps
- **Business KPIs Validation**: Validates metric calculations

## 🏢 Customizing for Your Organization

### Option 1: Connect to Your Own Snowflake Data

1. **Update Environment Variables**:
   ```bash
   # Replace with your database and schema
   SNOWFLAKE_DATABASE=your_production_db
   SNOWFLAKE_SCHEMA=your_schema
   ```

2. **Modify dbt Models**:
   - Update `models/staging/sources.yml` with your table names
   - Adjust column names in staging models
   - Customize business logic in mart models

3. **Update Asset Dependencies**:
   - Modify asset selectors in `jobs.py`
   - Adjust asset checks for your data quality requirements

### Option 2: Extend with Additional Features

#### Add New Data Sources
```python
# In assets/your_new_assets.py
@asset(description="Your custom data source")
def your_custom_asset(context, snowflake: SnowflakeResource):
    # Your logic here
    pass
```

#### Create Custom Sensors
```python
# In sensors.py
@sensor(job=your_job)
def your_custom_sensor(context):
    # Your trigger logic
    pass
```

#### Add Machine Learning Models
- Create ML training assets
- Set up model validation checks
- Schedule retraining jobs

## 📁 Project Structure

```
dagster-snowflake-dbt-demo/          # dg-managed project
├── dg.toml                          # dg project configuration
├── dagster_snowflake_dbt_demo/      # Main Python package 
│   ├── defs/                       # Definitions folder (auto-discovered)
│   │   ├── assets/                 # Asset definitions  
│   │   │   └── snowflake_assets.py# Direct Snowflake assets
│   │   ├── dbt_analytics/          # dbt component directory
│   │   │   └── defs.yaml          # dbt project component (YAML-driven)
│   │   ├── jobs.py                # Job definitions
│   │   ├── schedules.py           # Schedule definitions  
│   │   ├── sensors.py             # Sensor definitions
│   │   └── asset_checks.py        # Data quality checks
│   └── definitions.py             # Auto-discovery loader with inline resources
├── dbt_project/                     # dbt project
│   ├── models/                      # dbt models
│   │   ├── staging/                 # Staging layer
│   │   └── marts/                   # Business logic layer
│   ├── dbt_project.yml             # dbt configuration
│   └── profiles.yml                 # Connection profiles
├── dagster_cloud.yaml              # Serverless deployment config
├── Dockerfile                      # Container configuration
├── pyproject.toml                  # Python dependencies
└── README.md                       # This file
```

## 🔍 Key Value Propositions Demonstrated

### 1. **Unified Orchestration**
- Single platform for all data workflows
- Native dbt integration with lineage tracking
- Cross-tool dependency management

### 2. **Developer Experience**
- Code-first approach with Python
- Rich UI for monitoring and debugging
- Local development with cloud deployment

### 3. **Operational Excellence**
- Built-in data quality monitoring
- Flexible scheduling and event-driven triggers
- Comprehensive observability and alerting

### 4. **Scalability & Performance**
- Serverless execution with auto-scaling
- Optimized resource utilization
- Enterprise-grade reliability

### 5. **Data Governance**
- Asset lineage and impact analysis
- Quality checks and validation
- Audit trails and compliance

## 🚀 Deployment Options

### Quick Testing vs Production Setup

**For immediate POV testing:**
- Use `dagster-cloud serverless deploy` for instant uploads
- Requires: Dagster+ account, API token, organization name
- No Git repository setup required
- Perfect for demos and quick validation
- Environment variables set directly in Dagster+ UI

**For production workflows:**
- Git integration with automatic deployments
- Proper version control and collaboration
- Branch deployments for testing changes
- CI/CD integration with your development workflow

### Setting Up CLI Authentication

Before using `dagster-cloud` CLI, you need:

1. **Create Dagster+ Account**: Sign up at [dagster.cloud](https://dagster.cloud)
2. **Get API Token**: 
   - Go to Settings → Tokens in Dagster+ UI
   - Create a new token with appropriate permissions
3. **Find Organization Name**: Visible in your Dagster+ URL (`https://your-org.dagster.cloud`)

```bash
# Option 1: Environment variables (recommended)
export DAGSTER_CLOUD_API_TOKEN="dgp_your_token_here"
export DAGSTER_CLOUD_ORGANIZATION="your-org-name"

# Option 2: Pass as CLI flags
dagster-cloud serverless deploy \
  --api-token "dgp_your_token_here" \
  --organization "your-org-name" \
  --deployment "prod" \
  --location-name snowflake-demo \
  --package-name dagster_snowflake_dbt_demo
```

### Branch Deployments

Dagster+ supports branch deployments for testing:
```bash
# Deploy to a branch deployment
dagster-cloud serverless deploy \
  --location-name snowflake-demo-dev \
  --deployment my-branch-name
```

This creates an isolated environment for testing changes before promoting to production.

## 🚨 Dagster+ Features to Explore

After deploying, explore these Dagster+ features for a complete POV:

### Alert Policies (Monitoring & Notifications)

Deploy the included alert policies to monitor your pipeline:

```bash
# Deploy alert policies for comprehensive monitoring
dagster-cloud deployment alert-policies sync -a alert_policies.yaml
```

**What you'll get:**
- 📧 Email alerts for asset failures, data quality issues, freshness violations
- 🔔 Schedule/sensor failure notifications  
- 📊 Run failure alerts

> ⚠️ **Before deploying**: Edit `alert_policies.yaml` to update email addresses to your own!

Based on the [Dagster+ alerts documentation](https://docs.dagster.io/guides/observe/alerts/creating-alerts#using-the-cli), these policies demonstrate real-world monitoring patterns.

### Asset Catalog & Health Status

Explore the Asset Catalog in Dagster+ UI:
- 📈 **Asset Health Dashboard** - Real-time status of all data assets
- 🔍 **Lineage Visualization** - Understand data dependencies  
- ⏰ **Freshness Monitoring** - See which assets are stale
- 📋 **Asset Checks Results** - Data quality validation status

### Role-Based Access Control (RBAC)

Configure team access in Settings → Users & Teams:
- 👥 **Team Management** - Organize users into teams
- 🔐 **Permission Levels** - Viewer, Editor, Admin roles
- 🎯 **Resource Scoping** - Limit access to specific deployments
- 🔑 **API Tokens** - Service account management

### Insights & Cost Monitoring  

Monitor compute costs and performance:
- 💰 **Credit Usage** - Track Dagster+ compute costs
- ⚡ **Performance Metrics** - Asset materialization times
- 📊 **Usage Analytics** - Team activity and trends
- 🎯 **Budget Alerts** - Get notified when costs exceed thresholds

### Branch Deployments

Test changes safely:
```bash
# Create a branch deployment for testing
dagster-cloud serverless deploy \
  --deployment feature-branch \
  --location-name snowflake-demo-test
```

### Additional Integrations

Set up additional integrations:
- 📱 **Slack/Teams** - Chat notifications (requires app setup)
- 📞 **PagerDuty** - Incident management
- 📧 **Email Services** - Custom SMTP configuration
- 🔗 **Webhooks** - Custom alert endpoints

## 🛠️ Advanced Configuration

### Custom Environment Variables
Add organization-specific configuration:
```yaml
environment_variables:
  YOUR_API_KEY:
    type: env_var
    name: YOUR_API_KEY
  CUSTOM_CONFIG:
    type: value
    value: "your_value"
```

### Monitoring & Alerting
- Set up Slack/email notifications in Dagster Cloud
- Configure asset SLA monitoring
- Create custom dashboards

## 📞 Support & Next Steps

### Getting Help
- 📖 [Dagster Documentation](https://docs.dagster.io)
- 💬 [Dagster Slack Community](https://dagster.io/slack)
- 🎓 [Dagster University](https://dagster.io/university)

### Production Readiness Checklist
- [ ] Set up monitoring and alerting
- [ ] Configure backup and disaster recovery
- [ ] Implement proper secrets management
- [ ] Set up CI/CD pipelines
- [ ] Configure role-based access control
- [ ] Plan capacity and scaling requirements

### Expanding Your POV
1. **Add Your Data Sources**: Connect to your databases and APIs
2. **Implement ML Workflows**: Add model training and deployment
3. **Create Custom Dashboards**: Build business-specific visualizations
4. **Set Up Data Governance**: Implement cataloging and lineage tracking
5. **Configure Advanced Monitoring**: Set up custom alerts and SLAs

---

**Ready to see Dagster in action?** This demo provides a solid foundation for evaluating Dagster's capabilities. Start with the Quick Start guide above, then customize for your specific use case!

For sales inquiries or technical questions, contact your Dagster representative or visit [dagster.io](https://dagster.io).
