# Dagster Cloud Serverless Deployment Guide

This guide walks you through deploying the Snowflake dbt demo to Dagster Cloud Serverless.

## Quick Start Options

**🚀 Choose your deployment method:**

### Option A: Fork & Use Dagster+ Onboarding (Recommended)
**To use the Dagster+ onboarding flow:**
1. **Fork this repository** to your GitHub account first: 
   - Go to https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example
   - Click "Fork" in the top right
2. **Start Dagster+ trial** and select "Import a Dagster project"
3. **Choose GitHub** and authorize Dagster+ to access your repositories
4. **Select your forked repository**: `your-username/snowflake-dbt-serverless-example`
5. **Complete setup** - Dagster+ will automatically deploy the project
6. **Set environment variables** in Dagster+ UI (see [Environment Variables](#3-set-environment-variables))
7. **Ready to test and customize!** ✅

> 📝 **Why fork first?** Dagster+ onboarding requires you to own the repository - you can't import public repositories you don't control.

### Option B: Skip Onboarding - Direct CLI Upload
**For immediate testing without Git setup:**

1. **Clone this repository** locally:

   **Command Line:**
   ```bash
   git clone https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git
   cd snowflake-dbt-serverless-example
   pip install -e .
   ```

   **VS Code:**
   - Open VS Code → `Cmd+Shift+P` → "Git: Clone"
   - Enter: `https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git`
   - Open project and run `pip install -e .` in terminal

   **Cursor IDE:**
   - Open Cursor → "Clone Repository"
   - Enter: `https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git`
   - Open project and run `pip install -e .` in terminal

2. **Setup Dagster+ CLI authentication** (see [CLI Authentication](#setting-up-cli-authentication) below)
3. **Deploy with CLI**: `dagster-cloud serverless deploy --location-name snowflake-demo`
4. **Set Snowflake environment variables** in Dagster+ UI (see [Environment Variables](#3-set-environment-variables))
5. **Good for quick POV**, but you'll need to fork later for customization

> ⚠️ **Prerequisites**: You need a Dagster+ account, API token, and organization name before deploying. See the detailed steps below.

## Manual Deployment

### Prerequisites

- Dagster Cloud account ([sign up for free](https://dagster.cloud))
- Snowflake account with access to `SNOWFLAKE_SAMPLE_DATA`
- Git repository with this code

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your repository contains all the necessary files:
- `dagster_cloud.yaml` (deployment configuration)
- `Dockerfile` (container configuration)  
- `pyproject.toml` (dependencies)
- Your Python code in `dagster_snowflake_dbt_demo/`

### 2. Connect Repository to Dagster Cloud

1. **Login to Dagster Cloud**
   - Go to your Dagster Cloud instance
   - Navigate to "Deployment" → "Settings"

2. **Add Git Integration**
   - Click "Add code location"
   - Select "GitHub" or "GitLab"
   - Authorize Dagster Cloud to access your repositories
   - Select your forked repository (or this repository if you have access)

3. **Configure Branch Deployment**
   - Set branch to `main` (or your primary branch)
   - Set location name to `snowflake-dbt-demo`

> 💡 **For Your Own Repository**: If you forked this repo, you'll connect to your fork (e.g., `your-username/snowflake-dbt-serverless-example`). This gives you full control to customize and iterate.

### 3. Set Environment Variables

In Dagster Cloud UI, go to "Deployment" → "Environment Variables":

```bash
# Required - Your Snowflake connection details
SNOWFLAKE_ACCOUNT=your_account.region.cloud_provider
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password

# Optional - Override defaults if needed
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=SNOWFLAKE_SAMPLE_DATA  
SNOWFLAKE_SCHEMA=TPCH_SF1
SNOWFLAKE_ROLE=PUBLIC
```

> **Security Note**: Dagster Cloud encrypts all environment variables. For production, consider using Snowflake key-pair authentication instead of passwords.

### 4. Deploy

1. **Trigger Deployment**
   - Push to your main branch, or
   - Click "Redeploy" in Dagster Cloud UI

2. **Monitor Deployment**
   - Watch the deployment logs in real-time
   - Deployment typically takes 2-5 minutes

3. **Verify Success**
   - Check that all assets are visible
   - Run a test job to validate Snowflake connectivity

### 5. Test Your Deployment

#### Manual Testing
1. Navigate to "Assets" in Dagster Cloud
2. Select a few assets and click "Materialize selected"
3. Monitor the run progress

#### Test Jobs
1. Go to "Jobs" tab
2. Launch `daily_analytics_job`
3. Verify successful completion

#### Verify Data Quality
1. Check "Asset Checks" tab
2. Run data quality validations
3. Review any failures or warnings

## Production Configuration

### Monitoring Setup

1. **Configure Alerts**
   - Go to "Settings" → "Alerts"
   - Set up job failure notifications
   - Configure asset SLA monitoring

2. **Slack Integration**
   - Install Dagster Slack app
   - Configure channels for different alert types

3. **Asset Health Monitoring**
   - Enable asset freshness policies
   - Set up custom asset checks

### Security Best Practices

1. **Use Key-Pair Authentication**
   ```bash
   # Instead of password, use:
   SNOWFLAKE_PRIVATE_KEY=your_private_key
   SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=your_passphrase
   ```

2. **Rotate Credentials Regularly**
   - Update Snowflake passwords quarterly
   - Use Snowflake's credential rotation features

3. **Principle of Least Privilege**
   - Create dedicated Snowflake role for Dagster
   - Grant minimal required permissions

## Troubleshooting

### Common Issues

#### Deployment Fails
```bash
# Check deployment logs for:
- Missing dependencies in pyproject.toml
- Docker build errors  
- Repository access issues
```

#### Snowflake Connection Errors
```bash
# Verify:
- Environment variables are set correctly
- Snowflake account URL format
- User has access to SNOWFLAKE_SAMPLE_DATA
- Warehouse is running
```

#### Asset Materialization Failures
```bash
# Check:
- dbt models compile correctly
- SQL syntax is valid for Snowflake
- Required tables exist in source schema
```

### Getting Help

1. **Check Deployment Logs**
   - Real-time logs available in Dagster Cloud
   - Download full logs for detailed debugging

2. **Test Locally First**
   ```bash
   dagster dev
   # Ensure everything works locally before deploying
   ```

3. **Contact Support**
   - Dagster Cloud support chat
   - [Dagster Slack Community](https://dagster.io/slack)
   - Email: support@dagsterlabs.com

## Advanced Deployment Options

### Multi-Environment Setup

Create separate deployments for dev/staging/prod:

```yaml
# dagster_cloud.yaml
locations:
  - location_name: snowflake-dbt-demo-dev
    # ... dev configuration
  - location_name: snowflake-dbt-demo-prod  
    # ... prod configuration
```

### Blue/Green Deployments

Use branch deployments for zero-downtime updates:
1. Deploy to feature branch
2. Test thoroughly
3. Merge to main for production deployment

### Custom Docker Images

For advanced customization:
```dockerfile
# Use custom base image
FROM your-registry/python:3.11-custom

# Add custom tools
RUN apt-get update && apt-get install -y your-tools

# Continue with standard setup
COPY pyproject.toml .
RUN pip install -e .
```

## Customization Workflow

**After you've forked or deployed this project**, here's how to customize it:

### 1. Get the Source Code

If you **forked the repository**:

**Command Line:**
```bash
# Clone YOUR fork to your local machine
git clone https://github.com/YOUR-USERNAME/snowflake-dbt-serverless-example.git
cd snowflake-dbt-serverless-example

# Install dependencies for local development
pip install -e ".[dev]"
```

**VS Code:**
1. **Open VS Code** → `Cmd+Shift+P` → "Git: Clone"
2. **Enter your fork URL**: `https://github.com/YOUR-USERNAME/snowflake-dbt-serverless-example.git`
3. **Open the project** and run in terminal:
   ```bash
   pip install -e ".[dev]"
   ```

**Cursor IDE:**
1. **Open Cursor** → "Clone Repository"
2. **Enter your fork URL**: `https://github.com/YOUR-USERNAME/snowflake-dbt-serverless-example.git`
3. **Open the project** and run in terminal:
   ```bash
   pip install -e ".[dev]"
   ```

If you **used CLI deployment** and want to customize:
```bash
# Clone the original repository (you'll need to create your own repo later)
git clone https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git
cd snowflake-dbt-serverless-example

# Install dependencies for local development
pip install -e ".[dev]"
```

### 2. Make Your Changes

```bash
# Test locally first
dg dev

# Make your customizations:
# - Add new assets in dagster_snowflake_dbt_demo/defs/assets/
# - Modify dbt models in dbt_project/models/
# - Update schedules, sensors, jobs as needed
# - Add new integrations or data sources
```

### 3. Deploy Your Changes

If you **forked the repository**:
```bash
# Push changes to YOUR fork
git add .
git commit -m "Customize analytics pipeline for my use case"
git push origin main

# Dagster+ will automatically deploy your changes via Git integration
```

If you **used CLI deployment** and want to switch to Git:
1. **Create a new repository** in your GitHub or GitLab
2. **Push your customized code** to that repository:
   ```bash
   git remote add origin https://github.com/your-org/your-dagster-project.git
   git push -u origin main
   ```
3. **Update Dagster+** to use your new repository (see [Step 2](#2-connect-repository-to-dagster-cloud))
4. **Remove the old CLI location** (optional, for cleanup)

### 5. Continuous Development

```bash
# For ongoing development:
git add .
git commit -m "Add custom analytics assets"
git push origin main

# Dagster+ will automatically deploy your changes
```

### Development Best Practices

- **Test locally first** with `dg dev`
- **Use branch deployments** for testing major changes
- **Update dbt manifest** after model changes: `cd dbt_project && dbt parse`
- **Monitor deployment logs** in Dagster+ during updates
- **Use asset checks** to validate data quality after changes

---

This deployment guide should get you up and running with Dagster Cloud Serverless in under 30 minutes. For more advanced configurations, consult the [Dagster Cloud documentation](https://docs.dagster.cloud).
