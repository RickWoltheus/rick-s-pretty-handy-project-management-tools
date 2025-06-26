"""
Unit tests for JIRA Client functionality
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.test_data import MOCK_EPICS, MOCK_STORIES, MOCK_VERSIONS, MOCK_FIELDS, TEST_CONFIG


class TestJiraClient:
    """Test JiraClient functionality"""
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_jira_client_initialization(self):
        """Test JIRA client initialization with configuration"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        assert client.config == config
        assert client.auth == (config.email, config.api_token)
        assert "application/json" in client.headers["Accept"]
    
    @patch.dict(os.environ, TEST_CONFIG)
    @patch('utils.jira_client.requests.get')
    def test_make_request_success(self, mock_get):
        """Test successful API request"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        config = JiraConfig()
        client = JiraClient(config)
        
        result = client._make_request("test-endpoint")
        
        assert result == {"key": "value"}
        mock_get.assert_called_once()
    
    @patch.dict(os.environ, TEST_CONFIG)
    @patch('utils.jira_client.requests.get')
    def test_make_request_failure(self, mock_get):
        """Test API request failure handling"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        import requests
        
        # Mock failed response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        config = JiraConfig()
        client = JiraClient(config)
        
        with pytest.raises(requests.exceptions.HTTPError):
            client._make_request("test-endpoint")
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_epics_no_filter(self):
        """Test getting epics without version filter"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the _make_request method
        client._make_request = Mock(return_value={"issues": MOCK_EPICS})
        
        result = client.get_epics()
        
        assert result == MOCK_EPICS
        # Verify correct JQL was used
        client._make_request.assert_called_once()
        call_args = client._make_request.call_args
        assert 'search' in call_args[0][0]
        # Fix: Access params correctly - call_args[0][1] is the params dict
        params = call_args[0][1]  # Second element of the positional args tuple
        assert 'issuetype = Epic' in params['jql']
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_epics_with_version_filter(self):
        """Test getting epics with version filter"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the _make_request method
        client._make_request = Mock(return_value={"issues": MOCK_EPICS})
        
        result = client.get_epics("v3")
        
        assert result == MOCK_EPICS
        # Verify version filter was applied
        client._make_request.assert_called_once()
        call_args = client._make_request.call_args
        # Fix: Access params correctly - call_args[0][1] is the params dict  
        params = call_args[0][1]  # Second element of the positional args tuple
        jql = params['jql']
        assert 'fixVersion = "v3"' in jql
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_stories_for_epic(self):
        """Test getting stories for a specific epic"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the _make_request method to return stories for different JQL queries
        def mock_request(endpoint, params=None):
            if params and 'jql' in params:
                jql = params['jql']
                if 'PROJ-100' in jql:
                    return {"issues": MOCK_STORIES["PROJ-100"]}
            return {"issues": []}
        
        client._make_request = Mock(side_effect=mock_request)
        
        result = client.get_stories_for_epic("PROJ-100")
        
        assert len(result) > 0
        # Should have tried multiple JQL patterns
        assert client._make_request.call_count >= 1
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_story_points(self):
        """Test extracting story points from a story"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Test with valid story points
        story_with_points = {
            "fields": {
                "customfield_10016": 8.0
            }
        }
        
        # Test with no story points
        story_without_points = {
            "fields": {}
        }
        
        # Test with invalid story points
        story_invalid_points = {
            "fields": {
                "customfield_10016": "invalid"
            }
        }
        
        assert client.get_story_points(story_with_points) == 8.0
        assert client.get_story_points(story_without_points) is None
        assert client.get_story_points(story_invalid_points) is None
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_project_versions(self):
        """Test getting project versions (with pagination fix)"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the _make_request method to return paginated response
        client._make_request = Mock(return_value=MOCK_VERSIONS)
        
        result = client.get_project_versions()
        
        # Should extract versions from the 'values' array
        assert len(result) == 2
        assert result[0]["name"] == "v3"  # Should be sorted
        assert result[1]["name"] == "v2"
        
        # Verify correct endpoint was called
        client._make_request.assert_called_once()
        call_args = client._make_request.call_args
        assert f'project/{config.project_key}/version' in call_args[0][0]
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_available_versions(self):
        """Test getting available version names"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock get_project_versions
        client.get_project_versions = Mock(return_value=MOCK_VERSIONS["values"])
        
        result = client.get_available_versions()
        
        assert result == ["v3", "v2"]
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_version_details(self):
        """Test getting details for a specific version"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock get_project_versions
        client.get_project_versions = Mock(return_value=MOCK_VERSIONS["values"])
        
        # Test existing version
        result = client.get_version_details("v3")
        assert result is not None
        assert result["name"] == "v3"
        assert result["id"] == "10047"
        
        # Test non-existing version
        result = client.get_version_details("v99")
        assert result is None
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_get_custom_field_id(self):
        """Test finding custom field ID by name"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the _make_request method
        client._make_request = Mock(return_value=MOCK_FIELDS)
        
        # Test finding existing field
        result = client.get_custom_field_id("Story Points")
        assert result == "customfield_10016"
        
        # Test finding non-existing field
        result = client.get_custom_field_id("Non-existing Field")
        assert result is None
    
    @patch.dict(os.environ, TEST_CONFIG)
    @patch('utils.jira_client.requests.get')
    def test_test_connection_success(self, mock_get):
        """Test successful connection test"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"displayName": "Test User"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        config = JiraConfig()
        client = JiraClient(config)
        
        result = client.test_connection()
        
        assert result == True
        mock_get.assert_called_once()
    
    @patch.dict(os.environ, TEST_CONFIG)
    @patch('utils.jira_client.requests.get')
    def test_test_connection_failure(self, mock_get):
        """Test connection test failure"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        import requests
        
        # Mock failed response
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        config = JiraConfig()
        client = JiraClient(config)
        
        result = client.test_connection()
        
        assert result == False


class TestJiraClientVersionFiltering:
    """Test version filtering functionality specifically"""
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_version_filtering_integration(self):
        """Test complete version filtering workflow"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the API responses
        def mock_request(endpoint, params=None):
            if 'version' in endpoint:
                return MOCK_VERSIONS
            elif 'search' in endpoint and params:
                jql = params.get('jql', '')
                if 'fixVersion = "v3"' in jql:
                    # Return only v3 epics
                    return {"issues": [epic for epic in MOCK_EPICS if any(
                        v.get("name") == "v3" for v in epic["fields"].get("fixVersions", [])
                    )]}
                else:
                    return {"issues": MOCK_EPICS}
            return {}
        
        client._make_request = Mock(side_effect=mock_request)
        
        # Test getting available versions
        versions = client.get_available_versions()
        assert "v3" in versions
        
        # Test getting epics with version filter
        epics = client.get_epics("v3")
        assert len(epics) > 0
        
        # Verify the filter was applied
        version_calls = [call for call in client._make_request.call_args_list 
                        if 'search' in call[0][0]]
        assert len(version_calls) > 0
        
        # Check that version filter was included in JQL
        jql_call = version_calls[0]
        # Fix: Access params correctly - call_args[0][1] is the params dict
        params = jql_call[0][1]  # Second element of the positional args tuple
        jql = params['jql']
        assert 'fixVersion = "v3"' in jql
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_version_api_response_parsing(self):
        """Test that version API response is parsed correctly"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock the exact response format from JIRA
        mock_response = {
            "self": "https://test.atlassian.net/rest/api/3/project/TEST/version?maxResults=50&startAt=0",
            "maxResults": 50,
            "startAt": 0,
            "total": 2,
            "isLast": True,
            "values": [
                {
                    "self": "https://test.atlassian.net/rest/api/3/version/10047",
                    "id": "10047",
                    "name": "v3",
                    "archived": False,
                    "released": False,
                    "projectId": 10144
                },
                {
                    "self": "https://test.atlassian.net/rest/api/3/version/10046",
                    "id": "10046",
                    "name": "v2",
                    "archived": False,
                    "released": True,
                    "projectId": 10144
                }
            ]
        }
        
        client._make_request = Mock(return_value=mock_response)
        
        # Test that get_project_versions extracts the values correctly
        versions = client.get_project_versions()
        
        assert len(versions) == 2
        assert versions[0]["name"] == "v3"
        assert versions[1]["name"] == "v2"
        assert versions[0]["id"] == "10047"
        assert versions[1]["id"] == "10046"
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_empty_version_response(self):
        """Test handling of empty version response"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock empty response
        mock_response = {
            "values": []
        }
        
        client._make_request = Mock(return_value=mock_response)
        
        versions = client.get_project_versions()
        available_versions = client.get_available_versions()
        
        assert versions == []
        assert available_versions == []
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_version_sorting(self):
        """Test that versions are sorted correctly"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock response with versions in different order
        mock_response = {
            "values": [
                {
                    "id": "10046",
                    "name": "v2",
                    "archived": False,
                    "released": True,
                    "releaseDate": "2024-01-15"
                },
                {
                    "id": "10047",
                    "name": "v3",
                    "archived": False,
                    "released": False,
                    "releaseDate": "2024-03-01"
                },
                {
                    "id": "10045",
                    "name": "v1",
                    "archived": False,
                    "released": True,
                    "releaseDate": "2023-12-01"
                }
            ]
        }
        
        client._make_request = Mock(return_value=mock_response)
        
        versions = client.get_project_versions()
        
        # Should be sorted by release date (newest first)
        assert versions[0]["name"] == "v3"  # 2024-03-01
        assert versions[1]["name"] == "v2"  # 2024-01-15
        assert versions[2]["name"] == "v1"  # 2023-12-01


class TestJiraClientErrorHandling:
    """Test error handling in JIRA client"""
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_version_api_error_handling(self):
        """Test handling of version API errors"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock API error
        client._make_request = Mock(side_effect=Exception("API Error"))
        
        # Should return empty list on error
        versions = client.get_project_versions()
        assert versions == []
        
        available_versions = client.get_available_versions()
        assert available_versions == []
    
    @patch.dict(os.environ, TEST_CONFIG)
    def test_custom_field_error_handling(self):
        """Test handling of custom field API errors"""
        from utils.config import JiraConfig
        from utils.jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        # Mock API error
        client._make_request = Mock(side_effect=Exception("API Error"))
        
        # Should return None on error
        field_id = client.get_custom_field_id("Story Points")
        assert field_id is None 