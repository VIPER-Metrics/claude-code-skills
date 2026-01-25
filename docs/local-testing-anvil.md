# Local Testing Options for Anvil Apps

This document covers options for testing Anvil applications locally, particularly useful when working with Claude Code as your primary development tool.

---

## Why Local Testing Matters for Claude Code

When using Claude Code, the ability to test locally enables:
- **Direct endpoint testing** via curl/HTTP without user round-trips
- **Database inspection** to verify data state
- **Automated pytest execution** with immediate feedback
- **Faster iteration cycles** - change → test → fix without context switching

Without local testing, the workflow requires the user to:
1. Deploy changes to Anvil
2. Manually test in browser
3. Copy/paste errors back to Claude Code
4. Repeat

---

## Option 1: Anvil App Server (Open Source Runtime)

### What It Is
The [Anvil Runtime](https://github.com/anvil-works/anvil-runtime) is the open-source engine that powers Anvil apps. It includes a standalone App Server that runs Anvil apps from the local filesystem.

### Installation

```bash
# Prerequisites
# Linux: sudo apt-get install openjdk-8-jdk libpq-dev
# macOS: brew install openjdk pgcli

# Create virtual environment
python -m venv anvil-env
source anvil-env/bin/activate

# Install
pip install anvil-app-server
```

### Running an App

```bash
# Start the server
anvil-app-server --app /path/to/viper-metrics-v2-0

# App runs at http://localhost:3030
# Live reload - just refresh browser to see code changes
```

### Database Access

The App Server uses its own local Postgres database (stored in `.anvil-data/` by default).

```bash
# Access the database shell
psql-anvil-app-server

# Or connect directly (find port/password in .anvil-data/)
psql -h localhost -p <port> -U postgres
```

### Connecting to External Database

```bash
anvil-app-server --app /path/to/app \
  --database "jdbc:postgresql://localhost/my_database?username=user&password=pass"
```

### What Claude Code Can Do With This

```bash
# Test HTTP endpoints directly
curl -X POST http://localhost:3030/_/api/sync-inspections \
  -H "Content-Type: application/json" \
  -d '{"inspection_id": "test-123"}'

# Query database state
psql-anvil-app-server -c "SELECT * FROM app_tables.inspections LIMIT 5;"

# Run the app in background
anvil-app-server --app /path/to/app &
```

### Limitations

- **Separate database** - Not connected to production Anvil Data Tables
- **Needs test data** - Must seed data locally
- **Single app** - Each App Server instance runs one app

### Best For

- Full local development of a single app
- Testing server functions in isolation
- Rapid iteration without deployment

---

## Option 2: Anvil Uplink

### What It Is
The [Anvil Uplink](https://anvil.works/docs/uplink) connects external Python code to your **live Anvil app**, with full access to Data Tables and server functions.

### Installation

```bash
pip install anvil-uplink
```

### Setup in Anvil IDE

1. Go to your app in Anvil IDE
2. Click the `+` button in the Sidebar
3. Select "Uplink"
4. Copy the Server Uplink key

### Basic Usage

```python
import anvil.server
from anvil.tables import app_tables

# Connect to your Anvil app
anvil.server.connect("your-server-uplink-key")

# Now you have full access to Data Tables
assets = app_tables.assets.search()

# Call existing server functions
result = anvil.server.call('get_company_assets')

# Define callable functions
@anvil.server.callable
def my_test_function():
    return list(app_tables.users.search())
```

### Running pytest with Uplink

```python
# tests/test_server_functions.py
import pytest
import anvil.server
from anvil.tables import app_tables

@pytest.fixture(scope="session", autouse=True)
def connect_anvil():
    anvil.server.connect("your-uplink-key")
    yield
    anvil.server.disconnect()

def test_get_assets():
    result = anvil.server.call('get_company_assets')
    assert isinstance(result, list)

def test_sync_endpoint():
    # Test the sync logic directly
    from server_code.InspectionsOTS.Sync_Endpoints import process_inspection
    result = process_inspection({"test": "data"})
    assert result['status'] == 'success'
```

### What Claude Code Can Do With This

```bash
# Run tests against live/staging app
cd /path/to/viper-metrics-v2-0
python -m pytest tests/ -v

# Quick interactive testing
python -c "
import anvil.server
anvil.server.connect('uplink-key')
print(anvil.server.call('get_some_data'))
"
```

### Two Types of Uplink Keys

| Type | Access Level | Use Case |
|------|--------------|----------|
| **Server Uplink** | Full server privileges, Data Tables access | Testing, automation |
| **Client Uplink** | Same as client-side code, limited access | External integrations |

### Limitations

- **Affects real data** - Connected to live database (use staging!)
- **Requires network** - Must be online
- **Key management** - Need to secure uplink keys

### Best For

- Testing server functions against real database
- Verifying sync endpoints work correctly
- Integration testing across apps

---

## Option 3: anvil_works_design_test

### What It Is
A [community tool](https://github.com/benlawraus/anvil_works_design_test) that mocks Anvil's environment so you can run pytest locally with a local SQLite database.

### Installation

```bash
pip install anvil-works-design-test
```

### Project Structure

```
your-anvil-app/
├── client_code/
├── server_code/
├── tests/                    # pytest tests go here
│   ├── conftest.py
│   └── test_server_functions.py
└── anvil.yaml
```

### Basic Usage

```python
# tests/conftest.py
import pytest
from anvil_works_design_test import setup_anvil

@pytest.fixture(scope="session", autouse=True)
def anvil_env():
    setup_anvil()
    yield

# tests/test_example.py
from anvil.tables import app_tables

def test_create_asset():
    # Uses local SQLite, not production
    row = app_tables.assets.add_row(asset_id="TEST-001", name="Test Asset")
    assert row['asset_id'] == "TEST-001"
```

### Running Tests

```bash
python -m pytest tests/ -v
```

### What Claude Code Can Do With This

```bash
# Run unit tests safely
cd /path/to/viper-metrics-v2-0
python -m pytest tests/test_server_functions.py -v

# Test specific function
python -m pytest tests/test_sync.py::test_process_inspection -v
```

### Limitations

- **Mock data required** - Need to set up test fixtures
- **Not real integration** - Doesn't test actual Anvil infrastructure
- **May need updates** - Community maintained

### Best For

- Unit testing business logic
- Safe testing without affecting production
- CI/CD pipeline integration

---

## Recommended Setup for VIPER

Given that VIPER has three apps sharing one database, here's the recommended approach:

### 1. Create a Staging Environment

In Anvil IDE:
- Clone viper-metrics-v2-0 to create "VIPER Metrics Staging"
- Use a separate database for staging
- Get an Uplink key for staging

### 2. Local Testing Structure

```
viper-metrics-v2-0/
├── tests/
│   ├── conftest.py           # Uplink connection setup
│   ├── test_sync_endpoints.py
│   ├── test_server_functions.py
│   └── fixtures/
│       └── test_data.py      # Test data generators
├── scripts/
│   ├── start-local-server.sh
│   ├── seed-test-data.py
│   └── run-tests.sh
└── .env.test                  # Uplink keys (git-ignored)
```

### 3. Test Configuration

```python
# tests/conftest.py
import os
import pytest
import anvil.server

@pytest.fixture(scope="session", autouse=True)
def connect_staging():
    """Connect to staging Anvil app via Uplink."""
    uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
    if uplink_key:
        anvil.server.connect(uplink_key)
        yield
        anvil.server.disconnect()
    else:
        pytest.skip("No ANVIL_UPLINK_KEY set")
```

### 4. Claude Code Workflow

```bash
# Set uplink key (staging only!)
export ANVIL_UPLINK_KEY="your-staging-uplink-key"

# Run tests
cd /path/to/viper-metrics-v2-0
python -m pytest tests/ -v

# Test specific sync endpoint
python -m pytest tests/test_sync_endpoints.py::test_sync_inspections -v
```

---

## Testing Sync Endpoints

Since VIPER Operator and VIPER Inspect both hit endpoints on VIPER Metrics, testing these is critical.

### Direct HTTP Testing (with App Server)

```bash
# Start local server
anvil-app-server --app /path/to/viper-metrics-v2-0 &

# Test sync endpoint
curl -X POST http://localhost:3030/_/api/new/sync-inspections \
  -H "Content-Type: application/json" \
  -d '{
    "inspection_uuid": "test-123",
    "asset_id": "ASSET-001",
    "sections": []
  }'
```

### Via Uplink (against staging)

```python
# tests/test_sync_endpoints.py
import anvil.server

def test_sync_inspections():
    """Test inspection sync endpoint logic."""
    test_payload = {
        "inspection_uuid": "test-123",
        "asset_id": "ASSET-001",
        "sections": [{"section_id": "s1", "complete": True}]
    }

    # Call the underlying function directly
    result = anvil.server.call('process_sync_inspection', test_payload)

    assert result['status'] == 'success'
    assert 'inspection_id' in result
```

---

## Environment Variables

Store these in `.env.test` (add to `.gitignore`):

```bash
# Staging Uplink key - NEVER use production!
ANVIL_UPLINK_KEY=your-staging-server-uplink-key

# Local App Server config
ANVIL_APP_PORT=3030
ANVIL_DATA_DIR=.anvil-data
```

---

## Quick Reference for Claude Code

### Start Local Server
```bash
anvil-app-server --app /path/to/app &
```

### Test Endpoint
```bash
curl -X POST http://localhost:3030/_/api/endpoint-name -d '{"key": "value"}'
```

### Run Tests
```bash
python -m pytest tests/ -v
```

### Query Local Database
```bash
psql-anvil-app-server -c "SELECT * FROM app_tables.table_name LIMIT 10;"
```

### Connect via Uplink
```python
import anvil.server
anvil.server.connect("uplink-key")
result = anvil.server.call('function_name', arg1, arg2)
```

---

## Resources

- [Anvil Runtime GitHub](https://github.com/anvil-works/anvil-runtime)
- [Anvil App Server on PyPI](https://pypi.org/project/anvil-app-server/)
- [Anvil Uplink Documentation](https://anvil.works/docs/uplink)
- [anvil_works_design_test](https://github.com/benlawraus/anvil_works_design_test)
- [Anvil Forum: Local pytest testing](https://anvil.works/forum/t/running-unit-tests-locally-with-pytest/8074)
- [Anvil Open Source Platform](https://anvil.works/open-source)

---

*Last updated: January 2025*
