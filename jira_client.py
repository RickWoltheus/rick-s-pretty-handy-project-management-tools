import requests
import json
from typing import List, Dict, Optional
from config import JiraConfig

class JiraClient:
    """Client for interacting with Jira API"""
    
    def __init__(self, config: JiraConfig):
        self.config = config
        self.auth = (config.email, config.api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to Jira API with error handling"""
        url = f"{self.config.domain}/rest/api/3/{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, auth=self.auth, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            raise
    
    def get_epics(self) -> List[Dict]:
        """Fetch all epics from the specified project"""
        jql = f'project = {self.config.project_key} AND issuetype = Epic ORDER BY created DESC'
        params = {
            'jql': jql,
            'fields': 'summary,description,status',
            'maxResults': 100
        }
        
        result = self._make_request('search', params)
        return result.get('issues', [])
    
    def get_stories_for_epic(self, epic_key: str) -> List[Dict]:
        """Fetch all stories linked to a specific epic"""
        # Try different JQL queries for epic linking
        jql_queries = [
            f'"Epic Link" = {epic_key}',  # Classic epic link
            f'parent = {epic_key}',        # New hierarchy
            f'"Epic Name" = "{epic_key}"'  # Alternative epic linking
        ]
        
        all_stories = []
        for jql in jql_queries:
            try:
                params = {
                    'jql': f'{jql} AND project = {self.config.project_key}',
                    'fields': f'summary,description,status,labels,priority,{self.config.story_points_field},{self.config.type_of_work_field}',
                    'maxResults': 100
                }
                
                result = self._make_request('search', params)
                stories = result.get('issues', [])
                
                # Add stories that aren't already in our list
                existing_keys = {story['key'] for story in all_stories}
                for story in stories:
                    if story['key'] not in existing_keys:
                        all_stories.append(story)
                        
            except Exception as e:
                print(f"Warning: Could not fetch stories with JQL '{jql}': {e}")
                continue
        
        return all_stories
    
    def get_story_points(self, story: Dict) -> Optional[float]:
        """Extract story points from a story issue"""
        try:
            story_points = story['fields'].get(self.config.story_points_field)
            if story_points is not None:
                return float(story_points)
            return None
        except (ValueError, TypeError):
            return None
    
    def get_custom_field_id(self, field_name: str) -> Optional[str]:
        """Find the custom field ID for a given field name (useful for setup)"""
        try:
            result = self._make_request('field')
            for field in result:
                if field.get('name', '').lower() == field_name.lower():
                    return field.get('id')
            return None
        except Exception as e:
            print(f"Error finding custom field ID: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test if the Jira connection is working"""
        try:
            result = self._make_request('myself')
            print(f"✅ Connected to Jira as: {result.get('displayName', 'Unknown')}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Jira: {e}")
            return False 