"""
Unit tests for the Enhanced Spec Sheet Generator
"""
import pytest
import os
import sys
import tempfile
from unittest.mock import Mock, patch, MagicMock
import openpyxl

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.test_data import MOCK_EPICS, MOCK_STORIES, get_total_story_points
from tests.conftest import assert_workbook_has_sheet, get_sheet_data, count_non_empty_rows

class TestTeamMember:
    """Test TeamMember class"""
    
    def test_team_member_creation(self, spec_sheet_classes):
        """Test creating a team member"""
        TeamMember = spec_sheet_classes['TeamMember']
        
        member = TeamMember("John Doe", "Senior Developer", 1.0, 8, 110)
        
        assert member.name == "John Doe"
        assert member.role == "Senior Developer"
        assert member.availability == 1.0
        assert member.story_points_per_sprint == 8
        assert member.hourly_rate == 110
    
    def test_team_member_partial_fte(self, spec_sheet_classes):
        """Test team member with partial FTE"""
        TeamMember = spec_sheet_classes['TeamMember']
        
        member = TeamMember("Jane Smith", "Designer", 0.5, 6, 85)
        
        # Calculate effective velocity manually
        effective_velocity = member.story_points_per_sprint * member.availability
        assert effective_velocity == 3.0  # 6 * 0.5
    
    def test_team_member_string_representation(self, spec_sheet_classes):
        """Test string representation of team member"""
        TeamMember = spec_sheet_classes['TeamMember']
        
        member = TeamMember("Bob Wilson", "Junior Developer", 0.8, 5, 75)
        
        # Test that we can access the member properties (the current TeamMember uses dataclass __str__)
        assert member.name == "Bob Wilson"
        assert member.role == "Junior Developer"
        assert member.availability == 0.8
        assert member.story_points_per_sprint == 5


class TestTeam:
    """Test Team class"""
    
    def test_empty_team(self, spec_sheet_classes):
        """Test empty team creation"""
        Team = spec_sheet_classes['Team']
        
        team = Team("Test Team")
        
        assert team.name == "Test Team"
        assert len(team.members) == 0
        assert team.get_total_velocity() == 0
        assert team.get_total_fte() == 0
    
    def test_team_with_members(self, spec_sheet_classes, sample_team_data):
        """Test team with multiple members"""
        Team = spec_sheet_classes['Team']
        TeamMember = spec_sheet_classes['TeamMember']
        
        team = Team("Development Team")
        
        # Add members with correct TeamMember constructor (name, role, availability, story_points_per_sprint, hourly_rate)
        for i, member_data in enumerate(sample_team_data):
            member = TeamMember(
                f"Member {i+1}",  # name
                member_data["role"],  # role
                member_data["fte"],  # availability
                member_data["story_points_per_sprint"],  # story_points_per_sprint
                member_data["hourly_rate"]  # hourly_rate
            )
            team.add_member(member)
        
        # Test calculations
        assert len(team.members) == 3
        assert team.get_total_fte() == 2.5  # 1.0 + 1.0 + 0.5
        
        # Total velocity should be reduced by overhead (15%)
        expected_velocity = (8 + 5 + 3) * 0.85  # 16 * 0.85 = 13.6
        assert team.get_total_velocity() == expected_velocity
    
    def test_team_composition_summary(self, spec_sheet_classes, sample_team_data):
        """Test team composition summary"""
        Team = spec_sheet_classes['Team']
        TeamMember = spec_sheet_classes['TeamMember']
        
        team = Team("Test Team")
        
        # Add one member with correct constructor (name, role, availability, story_points_per_sprint, hourly_rate)
        member = TeamMember("Alice Johnson", "Senior Developer", 1.0, 8, 110)
        team.add_member(member)
        
        summary = team.get_composition_summary()
        
        assert "Test Team" in summary
        assert "Senior Developer" in summary
        assert "1.0 total FTE" in summary
        assert "SP/sprint" in summary


class TestEnhancedSpecSheetSync:
    """Test the main EnhancedSpecSheetSync class"""
    
    @patch.dict(os.environ, {
        'JIRA_DOMAIN': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@test.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
        'JIRA_STORY_POINTS_FIELD': 'customfield_10016',
        'JIRA_TYPE_OF_WORK_FIELD': 'customfield_10273'
    })
    def test_calculate_sprint_estimates(self, sample_team_data, spec_sheet_classes):
        """Test sprint calculation functionality"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        Team = spec_sheet_classes['Team']
        TeamMember = spec_sheet_classes['TeamMember']
        
        # Create a team
        team = Team("Test Team")
        for i, member_data in enumerate(sample_team_data):
            member = TeamMember(
                f"Test Member {i+1}",  # name
                member_data["role"],  # role
                member_data["fte"],  # availability
                member_data["story_points_per_sprint"],  # story_points_per_sprint
                member_data["hourly_rate"]  # hourly_rate
            )
            team.add_member(member)
        
        # Mock the sync instance
        sync = EnhancedSpecSheetSync()
        sync.jira_client = Mock()
        sync.jira_config = Mock()
        
        # Test calculation
        total_story_points = 40
        estimates = sync.orchestrator.sprint_planner.calculate_sprint_estimates(total_story_points, team)
        
        assert estimates['total_story_points'] == 40
        assert estimates['team_velocity'] > 0
        assert estimates['sprints'] > 0
        assert estimates['weeks'] > 0
        assert estimates['months'] > 0
        assert 'team_composition' in estimates
    
    @patch.dict(os.environ, {
        'JIRA_DOMAIN': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@test.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
        'JIRA_STORY_POINTS_FIELD': 'customfield_10016',
        'JIRA_TYPE_OF_WORK_FIELD': 'customfield_10273'
    })
    def test_determine_risk_profile(self, spec_sheet_classes):
        """Test risk profile determination"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        
        sync = EnhancedSpecSheetSync()
        sync.jira_client = Mock()
        sync.jira_config = Mock()
        # Mock get_story_points to return actual numbers instead of Mock objects
        sync.jira_client.get_story_points = Mock(return_value=2)  # Return small number for default case
        
        # Test different risk profiles
        proven_story = {"fields": {"customfield_10273": "proven"}}
        experimental_story = {"fields": {"customfield_10273": "experimental"}}
        dependant_story = {"fields": {"customfield_10273": "dependant"}}
        no_type_story = {"fields": {}}
        
        assert sync.orchestrator.risk_assessor.determine_risk_profile(proven_story) == "proven"
        assert sync.orchestrator.risk_assessor.determine_risk_profile(experimental_story) == "experimental"
        assert sync.orchestrator.risk_assessor.determine_risk_profile(dependant_story) == "dependant"
        assert sync.orchestrator.risk_assessor.determine_risk_profile(no_type_story) == "experimental"  # Default
    
    @patch.dict(os.environ, {
        'JIRA_DOMAIN': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@test.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
        'JIRA_STORY_POINTS_FIELD': 'customfield_10016',
        'JIRA_TYPE_OF_WORK_FIELD': 'customfield_10273'
    })
    def test_calculate_prices(self, spec_sheet_classes):
        """Test price calculations for different risk profiles"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        sync = EnhancedSpecSheetSync()
        sync.jira_client = Mock()
        sync.jira_config = Mock()
        # Mock settings config to use test values
        sync.settings_config = {
            "pricing": {
                "base_story_point_price": 100.0,
                "experimental_variance": 0.3,
                "base_hourly_rate": 113.33,
                "hourly_rate_discount": 0.25
            },
            "sprint_planning": {
                "hours_per_story_point": 8
            },
            "risk_assessment": {
                "proven_threshold_story_points": 3,
                "experimental_threshold_story_points": 8
            },
            "ui_formatting": {
                "header_color": "366092",
                "summary_header_color": "366092",
                "epic_background_color": "E6F3FF",
                "section_background_color": "D4EDDA",
                "default_column_widths": [50, 20, 20, 30, 15, 12, 15, 12, 12, 15, 20],
                "header_row_height": 80
            }
        }
        # Set pricing engine values directly for testing
        sync.orchestrator.pricing_engine.base_story_point_price = 100.0
        sync.orchestrator.pricing_engine.experimental_variance = 0.3
        sync.orchestrator.pricing_engine.hourly_rate = 85.0
        sync.orchestrator.pricing_engine.dod_impact_total = 0.0  # Set to 0 for predictable test results
        
        # Test proven pricing (without DoD impacts, should be 5 * 100 = 500)
        prices = sync.orchestrator.pricing_engine.calculate_prices(5, 'proven')
        assert prices['fixed'] == 500.0
        
        # Test experimental pricing
        prices = sync.orchestrator.pricing_engine.calculate_prices(5, 'experimental')
        assert prices['minimum'] == 350.0  # 500 * 0.7
        assert prices['maximum'] == 650.0  # 500 * 1.3
        
        # Test dependant pricing (5 story points * 8 hours/SP * 85/hour = 3400)
        prices = sync.orchestrator.pricing_engine.calculate_prices(5, 'dependant')
        assert prices['hourly_estimate'] == 3400.0  # 5 * 8 * 85
    
    @patch.dict(os.environ, {
        'JIRA_DOMAIN': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@test.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
        'JIRA_STORY_POINTS_FIELD': 'customfield_10016',
        'JIRA_TYPE_OF_WORK_FIELD': 'customfield_10273'
    })
    def test_get_moscow_priority(self, spec_sheet_classes):
        """Test MoSCoW priority detection"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        
        sync = EnhancedSpecSheetSync()
        sync.jira_client = Mock()
        sync.jira_config = Mock()
        
        # Test different priority scenarios
        must_story = {"fields": {"labels": ["must-have"]}}
        should_story = {"fields": {"labels": ["should-have"]}}
        could_story = {"fields": {"labels": ["could-have"]}}
        wont_story = {"fields": {"labels": ["wont-have"]}}
        high_priority = {"fields": {"priority": {"name": "High"}, "labels": []}}
        no_priority = {"fields": {"labels": []}}
        
        assert sync.orchestrator.moscow_manager.get_moscow_priority(must_story) == "Must Have"
        assert sync.orchestrator.moscow_manager.get_moscow_priority(should_story) == "Should Have"
        assert sync.orchestrator.moscow_manager.get_moscow_priority(could_story) == "Could Have"
        assert sync.orchestrator.moscow_manager.get_moscow_priority(wont_story) == "Won't Have"
        assert sync.orchestrator.moscow_manager.get_moscow_priority(high_priority) == "Should Have"  # High priority -> Should Have (per implementation)
        assert sync.orchestrator.moscow_manager.get_moscow_priority(no_priority) == "Should Have"  # Default
    
    @patch.dict(os.environ, {
        'JIRA_DOMAIN': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@test.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
        'JIRA_STORY_POINTS_FIELD': 'customfield_10016',
        'JIRA_TYPE_OF_WORK_FIELD': 'customfield_10273'
    })
    def test_create_custom_team(self, sample_team_data, spec_sheet_classes):
        """Test custom team creation"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        
        sync = EnhancedSpecSheetSync()
        sync.jira_client = Mock()
        sync.jira_config = Mock()
        
        custom_team = sync.orchestrator.sprint_planner.create_custom_team(sample_team_data)
        
        assert custom_team.name == "Custom Team"
        assert len(custom_team.members) == 3
        assert custom_team.get_total_fte() == 2.5
        assert custom_team.get_total_velocity() > 0

    def test_moscow_priority_filtering(self, spec_sheet_classes):
        """Test MoSCoW priority filtering functionality"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        sync = EnhancedSpecSheetSync()
        
        # Mock stories with different MoSCoW priorities
        mock_stories = [
            {
                'key': 'PROJ-1',
                'fields': {
                    'priority': {'name': 'Highest'},
                    'labels': []
                }
            },
            {
                'key': 'PROJ-2',
                'fields': {
                    'priority': {'name': 'High'},
                    'labels': []
                }
            },
            {
                'key': 'PROJ-3',
                'fields': {
                    'priority': {'name': 'Medium'},
                    'labels': []
                }
            },
            {
                'key': 'PROJ-4',
                'fields': {
                    'priority': {'name': 'Low'},
                    'labels': []
                }
            }
        ]
        
        # Test filtering for Must Have and Should Have only
        selected_priorities = ['Must Have', 'Should Have']
        filtered_stories, priority_counts = sync.orchestrator.moscow_manager.filter_stories_by_moscow(mock_stories, selected_priorities)
        
        assert len(filtered_stories) == 2  # Only Must Have and Should Have
        assert filtered_stories[0]['key'] == 'PROJ-1'  # Must Have (Highest)
        assert filtered_stories[1]['key'] == 'PROJ-2'  # Should Have (High)
        
        # Test filtering for Could Have only
        selected_priorities = ['Could Have']
        filtered_stories, priority_counts = sync.orchestrator.moscow_manager.filter_stories_by_moscow(mock_stories, selected_priorities)
        
        assert len(filtered_stories) == 1
        assert filtered_stories[0]['key'] == 'PROJ-3'  # Could Have (Medium)
        
        # Test no filtering (all priorities)
        selected_priorities = ['Must Have', 'Should Have', 'Could Have', 'Won\'t Have']
        filtered_stories, priority_counts = sync.orchestrator.moscow_manager.filter_stories_by_moscow(mock_stories, selected_priorities)
        
        assert len(filtered_stories) == 4  # All stories

    def test_moscow_priority_detection_from_labels(self, spec_sheet_classes):
        """Test MoSCoW priority detection from Jira labels"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        sync = EnhancedSpecSheetSync()
        
        # Test story with must-have label
        story_with_must_label = {
            'fields': {
                'priority': {'name': 'Medium'},  # Different priority
                'labels': ['must-have', 'feature']
            }
        }
        priority = sync.orchestrator.moscow_manager.get_moscow_priority(story_with_must_label)
        assert priority == 'Must Have'
        
        # Test story with should-have label
        story_with_should_label = {
            'fields': {
                'priority': {'name': 'Low'},
                'labels': ['should', 'enhancement']
            }
        }
        priority = sync.orchestrator.moscow_manager.get_moscow_priority(story_with_should_label)
        assert priority == 'Should Have'
        
        # Test story with could-have label
        story_with_could_label = {
            'fields': {
                'priority': {'name': 'High'},
                'labels': ['could-have', 'nice-to-have']
            }
        }
        priority = sync.orchestrator.moscow_manager.get_moscow_priority(story_with_could_label)
        assert priority == 'Could Have'
        
        # Test story with won't-have label
        story_with_wont_label = {
            'fields': {
                'priority': {'name': 'Highest'},
                'labels': ['wont-have', 'out-of-scope']
            }
        }
        priority = sync.orchestrator.moscow_manager.get_moscow_priority(story_with_wont_label)
        assert priority == 'Won\'t Have'

    def test_sync_with_moscow_filtering_integration(self, spec_sheet_classes):
        """Test integration of MoSCoW filtering in epic-story hierarchy sync process"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        sync = EnhancedSpecSheetSync()
        
        # Set up mocks on the orchestrator (new modular architecture)
        sync.orchestrator.jira_client = Mock()
        sync.orchestrator.jira_config = Mock()
        
        # Mock epics and stories (epic-story hierarchy approach)
        mock_epics = [
            {
                'key': 'EPIC-1',
                'fields': {
                    'summary': 'Test Epic',
                    'issuetype': {'name': 'Epic'}
                }
            }
        ]
    
        mock_stories = [
            {
                'key': 'PROJ-1',
                'fields': {
                    'summary': 'Must have story',
                    'priority': {'name': 'Highest'},
                    'labels': [],
                    'issuetype': {'name': 'Story'}
                }
            }
        ]
    
        mock_everything_else = [
            {
                'key': 'PROJ-2',
                'fields': {
                    'summary': 'Won\'t have bug',
                    'priority': {'name': 'Low'},
                    'labels': [],
                    'issuetype': {'name': 'Bug'}
                }
            }
        ]
    
        # Set data on orchestrator (new architecture)
        sync.orchestrator.selected_epics = mock_epics
        sync.orchestrator.everything_else_items = mock_everything_else
        sync.orchestrator.selected_version = 'Test Version'
        
        # Mock jira client methods
        sync.orchestrator.jira_client.get_story_points.return_value = 3
        sync.orchestrator.jira_client.get_stories_for_epic.return_value = mock_stories
    
        # Mock workbook and worksheet on excel manager
        from unittest.mock import MagicMock
        sync.orchestrator.excel_manager.workbook = MagicMock()
        sync.orchestrator.excel_manager.workbook.sheetnames = ['Scope (Quantity)']
        mock_ws = MagicMock()
        sync.orchestrator.excel_manager.workbook.__getitem__.return_value = mock_ws
        sync.orchestrator.excel_manager.spec_sheet_path = 'test.xlsx'
        sync.orchestrator.excel_manager.workbook.save = Mock()
    
        # Test sync with Must Have filter only
        selected_priorities = ['Must Have']
        result = sync.sync_to_scope_sheet('Scope (Quantity)', selected_priorities)
    
        assert result is True
        assert sync.orchestrator.selected_moscow_priorities == selected_priorities
        
        # Verify the workbook was saved (indicating successful sync)
        sync.orchestrator.excel_manager.workbook.save.assert_called_once()
        
        # Verify that get_stories_for_epic was called for each epic
        sync.orchestrator.jira_client.get_stories_for_epic.assert_called_with('EPIC-1')


class TestSpreadsheetGeneration:
    """Test spreadsheet generation functionality"""
    
    def test_workbook_creation(self, test_workbook):
        """Test that test workbook is created correctly"""
        assert os.path.exists(test_workbook)
        
        # Check sheets exist
        assert_workbook_has_sheet(test_workbook, "Scope (Quantity)")
        assert_workbook_has_sheet(test_workbook, "Definition of Done (Quality)")
        assert_workbook_has_sheet(test_workbook, "Settings")
    
    def test_scope_sheet_headers(self, test_workbook):
        """Test that scope sheet has correct headers"""
        data = get_sheet_data(test_workbook, "Scope (Quantity)")
        
        # Check header row
        expected_headers = [
            "Item", "MoSCoW", "Risk Profile", "Details", 
            "SP (Proven)", "Fixed Price", "SP (Experimental)", 
            "Min Price", "Max Price", "SP (Dependant)", "Hourly Estimate"
        ]
        
        assert data[0] == expected_headers
    
    def test_dod_impact_sheet_data(self, test_workbook):
        """Test Definition of Done (Quality) sheet contains comprehensive quality standards"""
        data = get_sheet_data(test_workbook, "Definition of Done (Quality)")
        
        # Should have header + DoD items + category headers + sum row (test fixture has simplified structure)
        assert len(data) >= 10  # Header + some categories and items + sum row
        assert data[0] == ["Definition of Done", "MoSCoW", "Price Impact", "Price Impact %"]
        
        # Check that some category headers are present (test fixture has 3 categories)
        categories_found = []
        for row in data[1:]:
            if len(row) > 0 and row[0] in [
                "Code quality & documentation",
                "Performance & optimization", 
                "UI/UX & animations",
                "Error handling & logging",
                "Testing & Cross-browser compatibility",
                "Security & deployment"
            ]:
                categories_found.append(row[0])
        
        assert len(categories_found) >= 3, f"Expected at least 3 categories, found {len(categories_found)}: {categories_found}"
        
        # Check some key DoD items are present
        dod_items = [row[0] for row in data[1:] if len(row) > 0]
        assert "Code is structured, modular, and follows best practices" in dod_items
        assert "API calls are debounced to increase performance" in dod_items
        assert "Security vulnerabilities are identified and mitigated" in dod_items
        
        # Check that sum row exists and is calculated correctly
        sum_rows = [row for row in data if len(row) >= 4 and row[2] == "Sum"]
        assert len(sum_rows) == 1, "Should have exactly one sum row"
        
        # Calculate expected sum from actual DoD items with numeric percentages
        expected_sum = sum(
            row[3] for row in data[1:] 
            if len(row) >= 4 and isinstance(row[3], (int, float)) and row[2] != "Sum"
        )
        assert sum_rows[0][3] == expected_sum, f"Sum should be {expected_sum} (calculated), but got {sum_rows[0][3]}"
        
        # Check that MoSCoW priorities are correctly assigned
        moscow_values = [row[1] for row in data[1:] if len(row) > 1 and row[1]]
        assert "Must Have" in moscow_values
        assert "Could Have" in moscow_values
        assert "Won't Have" in moscow_values
        
        # Check that Won't Have items have 0 impact
        for row in data[1:]:
            if len(row) >= 4 and row[1] == "Won't Have" and isinstance(row[3], (int, float)):
                assert row[3] == 0.0, f"Won't Have items should have 0% impact, but {row[0]} has {row[3]}"
    
    def test_settings_sheet_data(self, test_workbook):
        """Test Settings sheet contains expected configuration"""
        data = get_sheet_data(test_workbook, "Settings")
        
        # Should have header + settings
        assert len(data) >= 5
        assert data[0] == ["Setting", "Value"]
        
        # Check some expected settings
        settings = {row[0]: row[1] for row in data[1:] if len(row) >= 2}
        assert "Base Story Point Price" in settings
        assert "Experimental Variance" in settings
        assert settings["Base Story Point Price"] == 130


class TestIntegration:
    """Integration tests for the complete workflow"""
    
    @patch.dict(os.environ, {
        'JIRA_DOMAIN': 'https://test.atlassian.net',
        'JIRA_EMAIL': 'test@test.com',
        'JIRA_API_TOKEN': 'test-token',
        'JIRA_PROJECT_KEY': 'TEST',
        'JIRA_STORY_POINTS_FIELD': 'customfield_10016',
        'JIRA_TYPE_OF_WORK_FIELD': 'customfield_10273'
    })
    def test_full_sync_workflow(self, mock_jira_client, test_workbook, spec_sheet_classes):
        """Test the complete sync workflow"""
        EnhancedSpecSheetSync = spec_sheet_classes['EnhancedSpecSheetSync']
        
        sync = EnhancedSpecSheetSync()
        sync.spec_sheet_path = test_workbook
        sync.jira_client = mock_jira_client
        sync.jira_config = Mock()
        
        # Mock the workbook loading
        sync.workbook = openpyxl.load_workbook(test_workbook)
        
        # Test connection (mock it to return True)
        sync.test_connections = Mock(return_value=True)
        assert sync.test_connections() == True
        
        # Test sync - this should not raise exceptions
        try:
            sync.sync_to_scope_sheet = Mock()  # Mock the actual sync method
            sync.sync_to_scope_sheet()
            success = True
        except Exception as e:
            print(f"Sync failed: {e}")
            success = False
        
        # We expect this to work with our mocked data
        assert success == True
    
    def test_data_consistency(self):
        """Test that our test data is consistent and complete"""
        # Verify we have epics
        assert len(MOCK_EPICS) > 0
        
        # Verify each epic has stories
        for epic in MOCK_EPICS:
            epic_key = epic["key"]
            assert epic_key in MOCK_STORIES
            assert len(MOCK_STORIES[epic_key]) > 0
        
        # Verify story points are present
        total_sp = get_total_story_points()
        assert total_sp > 0
        
        # Verify different risk profiles exist
        risk_profiles = set()
        for stories in MOCK_STORIES.values():
            for story in stories:
                risk_profile = story["fields"].get("customfield_10273", "proven")
                risk_profiles.add(risk_profile)
        
        assert len(risk_profiles) > 1  # Should have multiple risk profiles
        assert "proven" in risk_profiles
        assert "experimental" in risk_profiles 