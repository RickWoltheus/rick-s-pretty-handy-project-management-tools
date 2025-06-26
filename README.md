# Jira to Spreadsheet Sync Tool

Automatically sync Jira epics and stories to a cost estimation spreadsheet. This tool pulls story points from Jira and calculates estimated costs based on your configured rate per story point.

## Features

### Basic System (`jira_sync.py`)

- ✅ Simple Jira Epics and Stories sync
- ✅ Basic story points to cost calculation
- ✅ Clean Excel output with formatting

### Enhanced System (`enhanced_jira_sync.py`)

- 🚀 **Risk-based pricing** (Proven/Experimental/Dependant)
- 🚀 **Definition of Done impact** (63% quality multiplier)
- 🚀 **MoSCoW prioritization** from Jira priorities/labels
- 🚀 **Syncs to existing spec sheet** structure
- 🚀 **Sophisticated pricing calculations** matching your format
- 🚀 **Multiple pricing models** (Fixed/Range/Hourly)
- ✅ Preserves existing manual entries
- ✅ Configurable via environment variables
- ✅ Error handling and connection testing

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Jira API Access

1. **Get your Jira API Token:**

   - Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
   - Click "Create API token"
   - Copy the generated token

2. **Find your Jira domain and project key:**
   - Domain: `https://your-company.atlassian.net`
   - Project key: Found in your Jira project URL (e.g., `PROJ` in `PROJ-123`)

### 3. Create Configuration File

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your details:
   ```bash
   JIRA_DOMAIN=https://your-company.atlassian.net
   JIRA_EMAIL=your-email@company.com
   JIRA_API_TOKEN=your-api-token-here
   JIRA_PROJECT_KEY=PROJ
   ```

### 4. Discover JIRA Custom Fields

Jira uses custom field IDs for story points and many other fields. Use the interactive field discovery tool:

```bash
python field_discovery.py
```

Or for quick Story Points discovery:

```bash
python field_discovery.py --story-points
```

Or find any specific field:

```bash
python field_discovery.py --find "Epic Link"
```

The tool will automatically offer to update your `.env` file with the discovered field IDs.

**Legacy Support**: The old method still works:

```bash
python jira_sync.py --find-field
```

### 5. Customize Spreadsheet Settings (Optional)

You can customize the spreadsheet layout by editing these variables in `.env`:

```bash
# Spreadsheet file and sheet name
EXCEL_PATH=my_cost_estimation.xlsx
EXCEL_SHEET_NAME=Cost Analysis

# Column positions (1-based)
EPIC_COLUMN=1
STORY_COLUMN=2
STORY_POINTS_COLUMN=3
COST_PER_POINT_COLUMN=4
TOTAL_COST_COLUMN=5

# Cost per story point
COST_PER_STORY_POINT=150.0
```

## Usage

### Quick Start with Menu System 🚀

The easiest way to get started is using the interactive menu system:

```bash
python start.py
```

This will launch an interactive menu that provides access to all available tools:

- **Enhanced Spec Sheet Generator** - Generate sophisticated spec sheets with risk-based pricing
- **Basic JIRA Sync** - Simple sync of JIRA epics and stories to spreadsheet
- **Validate JIRA Setup** - Check JIRA configuration and field mappings
- **Setup & Configuration** - Configure JIRA connection and environment settings
- **Discover JIRA Fields** - Interactive tool to find and configure any JIRA custom field
- **View Configuration** - Display current environment configuration
- **Show Documentation** - Access helpful guides and documentation

The menu system handles all the complexity of running different tools and provides helpful descriptions and error handling.

### Basic Sync (Simple System)

Run the basic sync command:

```bash
python jira_sync.py
```

This creates a new simple spreadsheet with basic story point calculations.

### Enhanced Sync (Sophisticated System) 🚀

For the advanced system that matches your existing spec sheet structure:

```bash
python enhanced_jira_sync.py
```

This will:

1. Connect to your Jira instance
2. Load your existing `spec-sheet.xlsx` structure
3. Fetch all epics and stories from your project
4. Apply risk-based pricing calculations (Proven/Experimental/Dependant)
5. Add items to your existing spec sheet with proper formatting
6. Preserve all your existing manual entries

**Recommended**: Use the enhanced system if you have an existing sophisticated pricing structure.

See `JIRA_MAPPING_GUIDE.md` for detailed configuration instructions.

### Spreadsheet Structure

The generated spreadsheet will have this structure:

```
| Epic/Story | Task Description | Story Points | Cost per Point | Total Cost |
|------------|------------------|--------------|----------------|------------|
| [EPIC] User Authentication (AUTH-1) |          |              |            |            |
|   └─ Login functionality (AUTH-2)   |    5     |    $100      |   $500     |
|   └─ Password reset (AUTH-3)        |    3     |    $100      |   $300     |
|   EPIC TOTAL:                       |    8     |    $100      |   $800     |
```

## Configuration Options

### Jira Settings

| Variable                  | Description            | Example                         |
| ------------------------- | ---------------------- | ------------------------------- |
| `JIRA_DOMAIN`             | Your Jira instance URL | `https://company.atlassian.net` |
| `JIRA_EMAIL`              | Your Jira email        | `user@company.com`              |
| `JIRA_API_TOKEN`          | Your Jira API token    | `ATATT3xFfGF0...`               |
| `JIRA_PROJECT_KEY`        | Project key            | `PROJ`                          |
| `JIRA_STORY_POINTS_FIELD` | Story points field ID  | `customfield_10016`             |

### Spreadsheet Settings

| Variable               | Description          | Default                     |
| ---------------------- | -------------------- | --------------------------- |
| `EXCEL_PATH`           | Output file path     | `jira_cost_estimation.xlsx` |
| `EXCEL_SHEET_NAME`     | Sheet name           | `Cost Estimation`           |
| `COST_PER_STORY_POINT` | Cost per story point | `100.0`                     |

## Troubleshooting

### Common Issues

1. **"Authentication failed"**

   - Verify your email and API token
   - Make sure your API token has the right permissions

2. **"No epics found"**

   - Check your project key
   - Ensure you have epics in your Jira project
   - Verify your Jira user has access to the project

3. **"Story points field not found"**

   - Run `python jira_sync.py --find-field` to find the correct field ID
   - Update your `.env` file with the correct field ID

4. **"Permission denied" on spreadsheet**
   - Make sure the Excel file isn't open in another program
   - Check file permissions in the directory

### Testing Your Setup

Run a connection test:

```bash
python -c "
from config import JiraConfig
from jira_client import JiraClient
config = JiraConfig()
client = JiraClient(config)
client.test_connection()
"
```

## Automation

### Schedule Regular Syncs

You can set up automatic syncing using cron (macOS/Linux) or Task Scheduler (Windows):

**Cron example (run every day at 9 AM):**

```bash
crontab -e
# Add this line:
0 9 * * * cd /path/to/jira-spec-sheet-sync && python jira_sync.py
```

**Windows Task Scheduler:**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Set action to run: `python C:\path\to\jira-spec-sheet-sync\jira_sync.py`

## Advanced Usage

### Custom Epic-Story Linking

The tool tries multiple methods to link stories to epics:

- Classic "Epic Link" field
- New Jira hierarchy (parent-child)
- Epic Name matching

If your Jira instance uses a different linking method, you can modify the `get_stories_for_epic` method in `jira_client.py`.

### Custom Calculations

You can modify the cost calculation logic in `spreadsheet_manager.py` to add:

- Different rates for different story types
- Complexity multipliers
- Risk factors
- Time-based calculations

## Support

If you encounter issues:

1. Check the error messages in the console
2. Verify your configuration in `.env`
3. Test your Jira connection with `--find-field`
4. Check the generated Excel file for any data issues

## License

This project is open source. Feel free to modify and adapt it to your needs.
