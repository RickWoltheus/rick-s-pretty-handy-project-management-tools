import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class JiraConfig:
    """Configuration class for Jira API settings"""
    
    def __init__(self):
        self.domain = os.getenv('JIRA_DOMAIN', 'https://your-domain.atlassian.net')
        self.email = os.getenv('JIRA_EMAIL', 'your-email@example.com')
        self.api_token = os.getenv('JIRA_API_TOKEN', 'your-api-token')
        self.project_key = os.getenv('JIRA_PROJECT_KEY', 'PROJ')
        
        # Story Points field ID - you'll need to find this in your Jira instance
        # Common values: customfield_10016, customfield_10002, customfield_10008
        self.story_points_field = os.getenv('JIRA_STORY_POINTS_FIELD', 'customfield_10016')
        
        # Type of Work field ID - used for determining risk profiles
        # Common values: customfield_10273, customfield_10020, customfield_10030
        self.type_of_work_field = os.getenv('JIRA_TYPE_OF_WORK_FIELD', 'customfield_10273')
        
        # Validate required settings
        self.validate()
    
    def validate(self):
        """Validate that all required settings are provided"""
        required_fields = [
            ('JIRA_DOMAIN', self.domain),
            ('JIRA_EMAIL', self.email), 
            ('JIRA_API_TOKEN', self.api_token),
            ('JIRA_PROJECT_KEY', self.project_key)
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value or field_value.startswith('your-'):
                missing_fields.append(field_name)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}. Please update your .env file.")

class SpreadsheetConfig:
    """Configuration class for spreadsheet settings"""
    
    def __init__(self):
        self.file_path = os.getenv('EXCEL_PATH', 'jira_cost_estimation.xlsx')
        self.sheet_name = os.getenv('EXCEL_SHEET_NAME', 'Cost Estimation')
        
        # Column mappings (1-based indexing)
        self.epic_column = int(os.getenv('EPIC_COLUMN', '1'))
        self.story_column = int(os.getenv('STORY_COLUMN', '2'))
        self.story_points_column = int(os.getenv('STORY_POINTS_COLUMN', '3'))
        self.cost_per_point_column = int(os.getenv('COST_PER_POINT_COLUMN', '4'))
        self.total_cost_column = int(os.getenv('TOTAL_COST_COLUMN', '5'))
        
        # Starting row for data (1-based indexing, accounting for headers)
        self.data_start_row = int(os.getenv('DATA_START_ROW', '2'))
        
        # Cost calculation settings
        self.cost_per_story_point = float(os.getenv('COST_PER_STORY_POINT', '100.0')) 