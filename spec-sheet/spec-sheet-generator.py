#!/usr/bin/env python3
"""
Enhanced Jira to Spec Sheet Sync Tool
Syncs Jira epics and stories with the existing sophisticated pricing structure
Now includes sprint planning and team composition features
"""

import sys
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from utils.config import JiraConfig, SpreadsheetConfig
from utils.jira_client import JiraClient
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import math

# Team composition and sprint planning classes
class TeamMember:
    """Represents a team member with their role and capacity"""
    def __init__(self, role: str, fte: float, story_points_per_sprint: float, hourly_rate: float = 95.37):
        self.role = role
        self.fte = fte  # Full Time Equivalent (0.0 to 1.0)
        self.base_story_points_per_sprint = story_points_per_sprint
        self.hourly_rate = hourly_rate
        self.effective_velocity = story_points_per_sprint * fte
    
    def __str__(self):
        return f"{self.role} ({self.fte} FTE): {self.effective_velocity:.1f} SP/sprint"

class Team:
    """Represents a development team with various roles and capacities"""
    def __init__(self, name: str = "Development Team"):
        self.name = name
        self.members: List[TeamMember] = []
        self.sprint_length_weeks = 2  # Default 2-week sprints
        self.sprint_overhead = 0.15   # 15% overhead for meetings, planning, etc.
    
    def add_member(self, member: TeamMember):
        """Add a team member"""
        self.members.append(member)
    
    def get_total_velocity(self) -> float:
        """Calculate total team velocity per sprint"""
        total_velocity = sum(member.effective_velocity for member in self.members)
        # Apply sprint overhead reduction
        return total_velocity * (1 - self.sprint_overhead)
    
    def get_total_fte(self) -> float:
        """Get total FTE of the team"""
        return sum(member.fte for member in self.members)
    
    def get_composition_summary(self) -> str:
        """Get a summary of team composition"""
        if not self.members:
            return "Empty team"
        
        summary = f"{self.name} ({self.get_total_fte():.1f} total FTE):\n"
        for member in self.members:
            summary += f"  • {member}\n"
        summary += f"Total velocity: {self.get_total_velocity():.1f} SP/sprint"
        return summary

class EnhancedSpecSheetSync:
    """Enhanced class for synchronizing Jira with the sophisticated spec sheet structure"""
    
    def __init__(self):
        try:
            self.jira_config = JiraConfig()
            self.jira_client = JiraClient(self.jira_config)
            
            # Load existing spec sheet structure
            self.spec_sheet_path = "spec-sheet.xlsx"
            self.base_story_point_price = 130  # €130 per story point
            self.experimental_variance = 0.3  # 30% variance
            self.hourly_rate = 127.16 * 0.75  # €127.16/h with 25% discount
            self.dod_impact_total = 0.63  # 63% total DoD impact
            
            # Type of work field configuration
            self.type_of_work_field = self.jira_config.type_of_work_field
            self.risk_priority = {  # Higher number = higher risk (takes priority)
                'proven': 1,
                'experimental': 2,
                'dependant': 3,
                'dependent': 3  # Alternative spelling
            }
            
            # Sprint planning configuration
            self.sprint_planning_enabled = True
            self.default_teams = self._create_default_teams()
            
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    
    def _create_default_teams(self) -> Dict[str, Team]:
        """Create default team compositions for analysis"""
        teams = {}
        
        # Small team
        small_team = Team("Small Team")
        small_team.add_member(TeamMember("Senior Developer", 1.0, 8))
        small_team.add_member(TeamMember("Junior Developer", 1.0, 5))
        small_team.add_member(TeamMember("Designer", 0.5, 6))
        teams["small"] = small_team
        
        # Medium team
        medium_team = Team("Medium Team")
        medium_team.add_member(TeamMember("Tech Lead", 1.0, 10))
        medium_team.add_member(TeamMember("Senior Developer", 2.0, 8))
        medium_team.add_member(TeamMember("Junior Developer", 1.0, 5))
        medium_team.add_member(TeamMember("Designer", 1.0, 6))
        medium_team.add_member(TeamMember("QA Engineer", 0.5, 4))
        teams["medium"] = medium_team
        
        # Large team
        large_team = Team("Large Team")
        large_team.add_member(TeamMember("Tech Lead", 1.0, 10))
        large_team.add_member(TeamMember("Senior Developer", 3.0, 8))
        large_team.add_member(TeamMember("Mid Developer", 2.0, 6))
        large_team.add_member(TeamMember("Junior Developer", 2.0, 5))
        large_team.add_member(TeamMember("Designer", 1.0, 6))
        large_team.add_member(TeamMember("QA Engineer", 1.0, 4))
        large_team.add_member(TeamMember("DevOps Engineer", 0.5, 7))
        teams["large"] = large_team
        
        return teams
    
    def calculate_sprint_estimates(self, total_story_points: float, team: Team) -> Dict[str, any]:
        """Calculate sprint estimates for a given team and story points"""
        team_velocity = team.get_total_velocity()
        
        if team_velocity <= 0:
            return {
                'sprints': 0,
                'weeks': 0,
                'months': 0,
                'team_velocity': 0,
                'error': 'Team has no effective velocity'
            }
        
        sprints_needed = math.ceil(total_story_points / team_velocity)
        weeks_needed = sprints_needed * team.sprint_length_weeks
        months_needed = weeks_needed / 4.33  # Average weeks per month
        
        return {
            'sprints': sprints_needed,
            'weeks': weeks_needed,
            'months': months_needed,
            'team_velocity': team_velocity,
            'team_composition': team.get_composition_summary(),
            'total_story_points': total_story_points,
            'story_points_per_sprint': team_velocity
        }
    
    def compare_team_options(self, total_story_points: float) -> Dict[str, Dict[str, any]]:
        """Compare different team compositions and their impact on timeline"""
        comparison = {}
        
        print(f"\n📊 Sprint Planning Analysis for {total_story_points} story points")
        print("=" * 60)
        
        for team_name, team in self.default_teams.items():
            estimates = self.calculate_sprint_estimates(total_story_points, team)
            comparison[team_name] = estimates
            
            print(f"\n{team.name}:")
            print(f"  Team Size: {team.get_total_fte():.1f} FTE")
            print(f"  Velocity: {estimates['team_velocity']:.1f} SP/sprint")
            print(f"  Duration: {estimates['sprints']} sprints ({estimates['weeks']} weeks, {estimates['months']:.1f} months)")
            print(f"  Team: {len(team.members)} people")
        
        return comparison
    
    def create_custom_team(self, team_composition: List[Dict]) -> Team:
        """Create a custom team from a list of team member specifications"""
        custom_team = Team("Custom Team")
        
        for member_spec in team_composition:
            role = member_spec.get('role', 'Developer')
            fte = member_spec.get('fte', 1.0)
            velocity = member_spec.get('story_points_per_sprint', 6)
            hourly_rate = member_spec.get('hourly_rate', 95.37)
            
            member = TeamMember(role, fte, velocity, hourly_rate)
            custom_team.add_member(member)
        
        return custom_team
    
    def generate_sprint_planning_report(self, epics: List[Dict] = None) -> Dict[str, any]:
        """Generate comprehensive sprint planning report"""
        if epics is None:
            epics = self.jira_client.get_epics()
        
        # Calculate total story points across all epics
        total_story_points = 0
        epic_breakdown = {}
        
        for epic in epics:
            epic_key = epic['key']
            stories = self.jira_client.get_stories_for_epic(epic_key)
            epic_points = sum(self.jira_client.get_story_points(story) or 0 for story in stories)
            epic_breakdown[epic_key] = {
                'summary': epic['fields']['summary'],
                'story_points': epic_points,
                'story_count': len(stories)
            }
            total_story_points += epic_points
        
        # Compare team options
        team_comparison = self.compare_team_options(total_story_points)
        
        # Risk analysis based on story types
        risk_breakdown = self._analyze_risk_distribution(epics)
        
        return {
            'total_story_points': total_story_points,
            'epic_breakdown': epic_breakdown,
            'team_comparison': team_comparison,
            'risk_breakdown': risk_breakdown,
            'recommendations': self._generate_recommendations(total_story_points, team_comparison, risk_breakdown)
        }
    
    def _analyze_risk_distribution(self, epics: List[Dict]) -> Dict[str, any]:
        """Analyze the distribution of risk profiles across stories"""
        risk_counts = {'proven': 0, 'experimental': 0, 'dependant': 0}
        risk_story_points = {'proven': 0, 'experimental': 0, 'dependant': 0}
        
        for epic in epics:
            stories = self.jira_client.get_stories_for_epic(epic['key'])
            for story in stories:
                risk_profile = self.determine_risk_profile(story)
                story_points = self.jira_client.get_story_points(story) or 0
                
                risk_counts[risk_profile] += 1
                risk_story_points[risk_profile] += story_points
        
        total_stories = sum(risk_counts.values())
        total_points = sum(risk_story_points.values())
        
        return {
            'counts': risk_counts,
            'story_points': risk_story_points,
            'percentages': {
                risk: (count / total_stories * 100) if total_stories > 0 else 0
                for risk, count in risk_counts.items()
            },
            'story_point_percentages': {
                risk: (points / total_points * 100) if total_points > 0 else 0
                for risk, points in risk_story_points.items()
            }
        }
    
    def _generate_recommendations(self, total_story_points: float, team_comparison: Dict, risk_breakdown: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Timeline recommendations
        small_sprints = team_comparison.get('small', {}).get('sprints', 0)
        large_sprints = team_comparison.get('large', {}).get('sprints', 0)
        
        if small_sprints > 0 and large_sprints > 0:
            time_saved = small_sprints - large_sprints
            if time_saved > 4:
                recommendations.append(f"Consider larger team - saves {time_saved} sprints ({time_saved * 2} weeks)")
        
        # Risk-based recommendations
        experimental_pct = risk_breakdown.get('story_point_percentages', {}).get('experimental', 0)
        dependant_pct = risk_breakdown.get('story_point_percentages', {}).get('dependant', 0)
        
        if experimental_pct > 30:
            recommendations.append("High experimental work (>30%) - consider prototyping phase")
        
        if dependant_pct > 20:
            recommendations.append("Significant dependent work (>20%) - ensure external dependencies are ready")
        
        # Story points recommendations
        if total_story_points > 100:
            recommendations.append("Large project - consider breaking into phases or releases")
        
        if total_story_points < 20:
            recommendations.append("Small project - single developer might be sufficient")
        
        return recommendations

    def add_sprint_planning_sheet(self):
        """Add a new sheet for sprint planning analysis"""
        sheet_name = 'Sprint Planning'
        
        # Remove existing sheet if it exists
        if sheet_name in self.workbook.sheetnames:
            self.workbook.remove(self.workbook[sheet_name])
        
        # Create new sheet
        ws = self.workbook.create_sheet(sheet_name)
        
        # Generate sprint planning report
        report = self.generate_sprint_planning_report()
        
        # Set up headers and content
        self._setup_sprint_planning_sheet(ws, report)
        
        # Save workbook
        self.workbook.save(self.spec_sheet_path)
        print(f"✅ Added sprint planning analysis to {sheet_name} sheet")
    
    def _setup_sprint_planning_sheet(self, ws, report: Dict):
        """Set up the sprint planning sheet with analysis data"""
        current_row = 1
        
        # Title
        title_cell = ws.cell(row=current_row, column=1)
        title_cell.value = "Sprint Planning & Team Composition Analysis"
        title_cell.font = Font(bold=True, size=16)
        current_row += 3
        
        # Project Summary
        ws.cell(row=current_row, column=1).value = "Project Overview"
        ws.cell(row=current_row, column=1).font = Font(bold=True, size=14)
        current_row += 1
        
        ws.cell(row=current_row, column=1).value = "Total Story Points:"
        ws.cell(row=current_row, column=2).value = report['total_story_points']
        current_row += 1
        
        ws.cell(row=current_row, column=1).value = "Number of Epics:"
        ws.cell(row=current_row, column=2).value = len(report['epic_breakdown'])
        current_row += 2
        
        # Epic Breakdown
        ws.cell(row=current_row, column=1).value = "Epic Breakdown"
        ws.cell(row=current_row, column=1).font = Font(bold=True, size=12)
        current_row += 1
        
        # Epic headers
        headers = ["Epic Key", "Summary", "Story Points", "Story Count"]
        for i, header in enumerate(headers, 1):
            cell = ws.cell(row=current_row, column=i)
            cell.value = header
            cell.font = Font(bold=True)
        current_row += 1
        
        # Epic data
        for epic_key, epic_data in report['epic_breakdown'].items():
            ws.cell(row=current_row, column=1).value = epic_key
            ws.cell(row=current_row, column=2).value = epic_data['summary']
            ws.cell(row=current_row, column=3).value = epic_data['story_points']
            ws.cell(row=current_row, column=4).value = epic_data['story_count']
            current_row += 1
        
        current_row += 2
        
        # Team Comparison
        ws.cell(row=current_row, column=1).value = "Team Composition Comparison"
        ws.cell(row=current_row, column=1).font = Font(bold=True, size=14)
        current_row += 1
        
        # Team comparison headers
        team_headers = ["Team Size", "Total FTE", "Velocity (SP/sprint)", "Sprints Needed", "Weeks", "Months"]
        for i, header in enumerate(team_headers, 2):
            cell = ws.cell(row=current_row, column=i)
            cell.value = header
            cell.font = Font(bold=True)
        current_row += 1
        
        # Team comparison data
        for team_name, estimates in report['team_comparison'].items():
            ws.cell(row=current_row, column=1).value = team_name.title()
            ws.cell(row=current_row, column=2).value = len(self.default_teams[team_name].members)
            ws.cell(row=current_row, column=3).value = f"{self.default_teams[team_name].get_total_fte():.1f}"
            ws.cell(row=current_row, column=4).value = f"{estimates['team_velocity']:.1f}"
            ws.cell(row=current_row, column=5).value = estimates['sprints']
            ws.cell(row=current_row, column=6).value = estimates['weeks']
            ws.cell(row=current_row, column=7).value = f"{estimates['months']:.1f}"
            current_row += 1
        
        current_row += 2
        
        # Risk Analysis
        ws.cell(row=current_row, column=1).value = "Risk Profile Analysis"
        ws.cell(row=current_row, column=1).font = Font(bold=True, size=14)
        current_row += 1
        
        # Risk headers
        risk_headers = ["Risk Profile", "Stories", "Story Points", "% of Stories", "% of Story Points"]
        for i, header in enumerate(risk_headers, 1):
            cell = ws.cell(row=current_row, column=i)
            cell.value = header
            cell.font = Font(bold=True)
        current_row += 1
        
        # Risk data
        for risk_profile in ['proven', 'experimental', 'dependant']:
            ws.cell(row=current_row, column=1).value = risk_profile.title()
            ws.cell(row=current_row, column=2).value = report['risk_breakdown']['counts'][risk_profile]
            ws.cell(row=current_row, column=3).value = report['risk_breakdown']['story_points'][risk_profile]
            ws.cell(row=current_row, column=4).value = f"{report['risk_breakdown']['percentages'][risk_profile]:.1f}%"
            ws.cell(row=current_row, column=5).value = f"{report['risk_breakdown']['story_point_percentages'][risk_profile]:.1f}%"
            current_row += 1
        
        current_row += 2
        
        # Recommendations
        if report['recommendations']:
            ws.cell(row=current_row, column=1).value = "Recommendations"
            ws.cell(row=current_row, column=1).font = Font(bold=True, size=14)
            current_row += 1
            
            for i, recommendation in enumerate(report['recommendations'], 1):
                ws.cell(row=current_row, column=1).value = f"{i}. {recommendation}"
                current_row += 1
        
        # Adjust column widths
        column_widths = [25, 50, 15, 15, 15, 15, 15]
        for i, width in enumerate(column_widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
    
    def load_spec_sheet_structure(self):
        """Load the existing spec sheet or create a new one"""
        try:
            if os.path.exists(self.spec_sheet_path):
                self.workbook = openpyxl.load_workbook(self.spec_sheet_path)
                
                # Load DoD impacts
                self.dod_impacts = self._load_dod_impacts()
                
                # Load settings
                self.settings = self._load_settings()
                
                print("✅ Loaded existing spec sheet structure")
            else:
                print(f"📝 Spec sheet not found at {self.spec_sheet_path}, creating new one...")
                self._create_new_spec_sheet()
                print("✅ Created new spec sheet with default structure")
            
            return True
            
        except Exception as e:
            print(f"❌ Error with spec sheet: {e}")
            return False
    
    def _load_dod_impacts(self) -> Dict[str, float]:
        """Load Definition of Done impacts from the spec sheet"""
        dod_impacts = {}
        try:
            df = pd.read_excel(self.spec_sheet_path, sheet_name='Definition of Done (Quality)')
            
            for idx, row in df.iterrows():
                if pd.notna(row.iloc[0]) and pd.notna(row.iloc[3]):
                    description = str(row.iloc[0])
                    impact = float(row.iloc[3])
                    if impact > 0:
                        dod_impacts[description] = impact
                        
        except Exception as e:
            print(f"Warning: Could not load DoD impacts: {e}")
            
        return dod_impacts
    
    def _load_settings(self) -> Dict[str, any]:
        """Load settings from the spec sheet"""
        settings = {
            'base_story_point_price': 130,
            'experimental_variance': 0.3,
            'hourly_rate': 95.37  # 127.16 * 0.75
        }
        
        try:
            df = pd.read_excel(self.spec_sheet_path, sheet_name='Settings')
            
            for idx, row in df.iterrows():
                if pd.notna(row.iloc[0]):
                    setting_name = str(row.iloc[0]).lower()
                    if 'base price of 1 story point' in setting_name and pd.notna(row.iloc[1]):
                        settings['base_story_point_price'] = float(row.iloc[1])
                    elif 'experimental' in setting_name and 'range' in setting_name and pd.notna(row.iloc[1]):
                        settings['experimental_variance'] = float(row.iloc[1])
                        
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")
            
        return settings
    
    def _create_new_spec_sheet(self):
        """Create a new spec sheet with all required sheets"""
        self.workbook = openpyxl.Workbook()
        
        # Remove default sheet
        if 'Sheet' in self.workbook.sheetnames:
            self.workbook.remove(self.workbook['Sheet'])
        
        # Create Scope (Quantity) sheet
        scope_sheet = self.workbook.create_sheet('Scope (Quantity)')
        
        # Create Definition of Done sheet with default values
        dod_sheet = self.workbook.create_sheet('Definition of Done (Quality)')
        self._setup_default_dod_sheet(dod_sheet)
        
        # Create Settings sheet with default values
        settings_sheet = self.workbook.create_sheet('Settings')
        self._setup_default_settings_sheet(settings_sheet)
        
        # Set default values
        self.dod_impacts = self._get_default_dod_impacts()
        self.settings = self._load_settings()
        
        # Save the new workbook
        self.workbook.save(self.spec_sheet_path)
    
    def _setup_default_dod_sheet(self, ws):
        """Set up default Definition of Done sheet"""
        headers = [
            "Definition of Done",
            "MoSCoW",
            "Price Impact",
            "Price Impact %"
        ]
        
        for i, header in enumerate(headers, 1):
            ws.cell(row=1, column=i).value = header
            ws.cell(row=1, column=i).font = Font(bold=True)
        
        # Add some default DoD items
        dod_items = [
            ("Code quality & documentation", "Must Have", "", 0.04),
            ("Code is reviewed and approved via pull requests", "Must Have", "", 0.025),
            ("Code is well-documented", "Should Have", "", 0.04),
            ("Performance optimization", "Should Have", "", 0.065),
            ("Testing & Cross-browser compatibility", "Must Have", "", 0.065),
            ("Security vulnerabilities are identified", "Must Have", "", 0.04),
        ]
        
        for i, (desc, moscow, impact_desc, impact_pct) in enumerate(dod_items, 2):
            ws.cell(row=i, column=1).value = desc
            ws.cell(row=i, column=2).value = moscow
            ws.cell(row=i, column=3).value = impact_desc
            ws.cell(row=i, column=4).value = impact_pct
    
    def _setup_default_settings_sheet(self, ws):
        """Set up default Settings sheet"""
        settings_data = [
            ("Range for Experimental pricing (up & down)", 0.3),
            ("Base price of 8 story points", 1040),
            ("Base price of 1 story point", 130),
            ("Hourly rate", 95.37),
        ]
        
        ws.cell(row=1, column=1).value = "Settings"
        ws.cell(row=1, column=1).font = Font(bold=True)
        
        for i, (setting, value) in enumerate(settings_data, 2):
            ws.cell(row=i, column=1).value = setting
            ws.cell(row=i, column=2).value = value
    
    def _get_default_dod_impacts(self):
        """Get default DoD impacts when no sheet exists"""
        return {
            "code_quality": 0.04,
            "code_review": 0.025,
            "documentation": 0.04,
            "performance": 0.065,
            "testing": 0.065,
            "security": 0.04
        }
    
    def determine_risk_profile(self, story: Dict) -> str:
        """Determine risk profile based on Type of work field with priority system"""
        
        # First, check the Type of work custom field
        type_of_work_value = story.get('fields', {}).get(self.type_of_work_field)
        
        if type_of_work_value:
            # Handle both single values and arrays
            if isinstance(type_of_work_value, list):
                work_types = [item.get('value', '').lower() for item in type_of_work_value]
            elif isinstance(type_of_work_value, dict):
                work_types = [type_of_work_value.get('value', '').lower()]
            elif isinstance(type_of_work_value, str):
                # Handle comma-separated values or single value
                work_types = [wt.strip().lower() for wt in type_of_work_value.split(',')]
            else:
                work_types = []
            
            # Find the highest priority (most risky) type
            highest_priority = 0
            selected_risk = 'experimental'  # default
            
            for work_type in work_types:
                # Check for exact matches or partial matches
                for risk_type, priority in self.risk_priority.items():
                    if risk_type in work_type or work_type in risk_type:
                        if priority > highest_priority:
                            highest_priority = priority
                            selected_risk = risk_type if risk_type != 'dependent' else 'dependant'
            
            if highest_priority > 0:
                print(f"   🏷️  Type of work: {', '.join(work_types)} → {selected_risk}")
                return selected_risk
        
        # Fallback 1: Check labels for risk indicators (legacy support)
        labels = story.get('fields', {}).get('labels', [])
        risk_labels = [label.lower() for label in labels]
        
        if any(label in risk_labels for label in ['proven', 'low-risk', 'fixed']):
            return 'proven'
        elif any(label in risk_labels for label in ['experimental', 'moderate-risk', 'research']):
            return 'experimental'
        elif any(label in risk_labels for label in ['dependant', 'dependent', 'high-risk', 'external']):
            return 'dependant'
        
        # Fallback 2: Default risk assessment based on story points
        story_points = self.jira_client.get_story_points(story)
        if story_points:
            if story_points <= 3:
                return 'proven'
            elif story_points <= 8:
                return 'experimental'
            else:
                return 'dependant'
        
        print(f"   ⚠️  No Type of work field, using default: experimental")
        return 'experimental'  # Default to experimental
    
    def calculate_prices(self, story_points: float, risk_profile: str) -> Dict[str, float]:
        """Calculate prices based on risk profile and story points"""
        base_price = story_points * self.settings['base_story_point_price']
        
        # Apply DoD impact
        base_price_with_dod = base_price * (1 + self.dod_impact_total)
        
        prices = {'base': base_price, 'base_with_dod': base_price_with_dod}
        
        if risk_profile == 'proven':
            prices['fixed'] = base_price_with_dod
            
        elif risk_profile == 'experimental':
            variance = self.settings['experimental_variance']
            prices['minimum'] = base_price_with_dod * (1 - variance)
            prices['maximum'] = base_price_with_dod * (1 + variance)
            
        elif risk_profile == 'dependant':
            # Estimate based on hourly rate
            estimated_hours = story_points * 8  # Rough estimate: 8 hours per story point
            prices['hourly_estimate'] = estimated_hours * self.settings['hourly_rate']
        
        return prices
    
    def get_moscow_priority(self, story: Dict) -> str:
        """Determine MoSCoW priority from Jira story"""
        priority = story.get('fields', {}).get('priority', {})
        if priority:
            priority_name = priority.get('name', '').lower()
            
            # Map Jira priorities to MoSCoW
            if priority_name in ['highest', 'blocker']:
                return 'Must Have'
            elif priority_name in ['high', 'major']:
                return 'Should Have'
            elif priority_name in ['medium', 'normal']:
                return 'Could Have'
            elif priority_name in ['low', 'minor', 'trivial']:
                return "Won't Have"
        
        # Check labels for MoSCoW indicators
        labels = story.get('fields', {}).get('labels', [])
        moscow_labels = [label.lower() for label in labels]
        
        if any(label in moscow_labels for label in ['must', 'must-have']):
            return 'Must Have'
        elif any(label in moscow_labels for label in ['should', 'should-have']):
            return 'Should Have'
        elif any(label in moscow_labels for label in ['could', 'could-have']):
            return 'Could Have'
        elif any(label in moscow_labels for label in ['wont', 'wont-have', 'out-of-scope']):
            return "Won't Have"
        
        return 'Should Have'  # Default
    
    def sync_to_scope_sheet(self, sheet_name: str = 'Scope (Quantity)'):
        """Sync Jira data to the specified scope sheet - completely regenerate from Jira"""
        print(f"🔄 Regenerating sheet: {sheet_name} from Jira data")
        
        # Get Jira data
        epics = self.jira_client.get_epics()
        if not epics:
            print("⚠️  No epics found in Jira project")
            return False
        
        # Load the worksheet
        if sheet_name not in self.workbook.sheetnames:
            print(f"❌ Sheet '{sheet_name}' not found in spec sheet")
            return False
        
        ws = self.workbook[sheet_name]
        
        # Clear existing content but preserve the header structure
        self._clear_and_setup_sheet(ws)
        
        # Start adding data after headers (row 4 to account for header structure)
        current_row = 4
        
        print(f"📝 Starting fresh sync at row {current_row}")
        
        total_items = 0
        
        for epic in epics:
            epic_key = epic['key']
            epic_summary = epic['fields']['summary']
            
            print(f"\n📊 Processing epic: {epic_key} - {epic_summary}")
            
            # Add epic header
            self._add_epic_header(ws, current_row, epic_key, epic_summary)
            current_row += 1
            
            # Get stories for this epic
            stories = self.jira_client.get_stories_for_epic(epic_key)
            print(f"   Found {len(stories)} stories")
            
            for story in stories:
                story_key = story['key']
                story_summary = story['fields']['summary']
                story_points = self.jira_client.get_story_points(story) or 0
                
                # Determine risk profile and pricing
                risk_profile = self.determine_risk_profile(story)
                moscow_priority = self.get_moscow_priority(story)
                prices = self.calculate_prices(story_points, risk_profile)
                
                print(f"   - {story_key}: {story_points} pts, {risk_profile}, {moscow_priority}")
                
                # Add story row
                self._add_story_row(ws, current_row, {
                    'key': story_key,
                    'summary': story_summary,
                    'story_points': story_points,
                    'moscow': moscow_priority,
                    'risk_profile': risk_profile,
                    'prices': prices
                })
                
                current_row += 1
                total_items += 1
            
            # Add spacing between epics
            current_row += 1
        
        # Add summary row at the end
        if total_items > 0:
            self._add_summary_section(ws, current_row + 1, epics)
        
        # Save the workbook
        self.workbook.save(self.spec_sheet_path)
        print(f"\n✅ Sync completed! Generated {total_items} items in {sheet_name}")
        
        return True
    
    def _clear_and_setup_sheet(self, ws):
        """Clear existing content and set up the sheet with proper headers"""
        # Clear all existing content
        ws.delete_rows(1, ws.max_row)
        
        # Set up the header structure matching the original format
        self._setup_original_headers(ws)
        
        print("🧹 Cleared existing content and set up fresh headers")
    
    def _setup_original_headers(self, ws):
        """Set up the original spec sheet header structure"""
        # Main header row 1 - complex header with scope description
        scope_header = ("Scope\n\nWhat is in scope (features, functionality, integrations) and what is out of scope. "
                       "We define risk profiles transparently. This visibility helps to allocate resources effectively, "
                       "avoid unmanageable scope creep, and ultimately create a shared commitment.\n\n"
                       "* Prices are all-in, meaning they include project management and end-to-end delivery of the product. "
                       "Prices are ex. VAT.")
        
        ws.cell(row=1, column=1).value = scope_header
        ws.cell(row=1, column=2).value = "MoSCoW\n\nMust Have\nShould Have\nCould Have\nWon't Have (out of scope)"
        ws.cell(row=1, column=3).value = "Risk Profile\n\nLow (Proven)\nModerate (Experimental)\nHigh (Dependant)"
        ws.cell(row=1, column=4).value = "Notes\n\n"
        ws.cell(row=1, column=5).value = "Proven\nLow risk profile.\n\nPrice is fixed. Scope is clear and we own this work."
        ws.cell(row=1, column=6).value = "Price\nFixed"
        ws.cell(row=1, column=7).value = "Experimental\nModerate risk profile.\n\nPrice can be 30% lower or higher but never more. We share the risk when the work is experimental."
        ws.cell(row=1, column=8).value = "Price\nMinimum"
        ws.cell(row=1, column=9).value = "Price\nMaximum"
        ws.cell(row=1, column=10).value = "Dependant\nHigh risk profile.\n\nPrice is estimation, but will be pay-by-hour. We depend on to-be-delivered APIs or externally employed team members."
        ws.cell(row=1, column=11).value = "Price\nEstimate, but will be pay-by-hour.\n\nOur rate on 05-02-2025 is €127,16/h - 25% discount."
        
        # Style the headers to match original format
        header_font = Font(bold=True, size=9)
        for col in range(1, 12):
            cell = ws.cell(row=1, column=col)
            cell.font = header_font
            # Wrap text for better display
            cell.alignment = Alignment(wrap_text=True, vertical='top')
        
        # Set appropriate column widths
        column_widths = [50, 20, 20, 30, 15, 12, 15, 12, 12, 15, 20]
        for i, width in enumerate(column_widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = width
        
        # Set row height for header
        ws.row_dimensions[1].height = 80
    
    def _add_summary_section(self, ws, start_row, epics):
        """Add a summary section with totals at the end"""
        current_row = start_row + 1
        
        # Add summary header
        ws.cell(row=current_row, column=1).value = "PROJECT SUMMARY"
        summary_font = Font(bold=True, size=12, color="FFFFFF")
        summary_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for col in range(1, 12):
            cell = ws.cell(row=current_row, column=col)
            cell.font = summary_font
            cell.fill = summary_fill
        
        current_row += 2
        
        # Calculate totals
        total_epics = len(epics)
        total_stories = sum(len(self.jira_client.get_stories_for_epic(epic['key'])) for epic in epics)
        total_story_points = 0
        total_proven_cost = 0
        total_experimental_min = 0
        total_experimental_max = 0
        total_dependant_estimate = 0
        
        for epic in epics:
            stories = self.jira_client.get_stories_for_epic(epic['key'])
            for story in stories:
                story_points = self.jira_client.get_story_points(story) or 0
                total_story_points += story_points
                
                risk_profile = self.determine_risk_profile(story)
                prices = self.calculate_prices(story_points, risk_profile)
                
                if risk_profile == 'proven':
                    total_proven_cost += prices.get('fixed', 0)
                elif risk_profile == 'experimental':
                    total_experimental_min += prices.get('minimum', 0)
                    total_experimental_max += prices.get('maximum', 0)
                elif risk_profile == 'dependant':
                    total_dependant_estimate += prices.get('hourly_estimate', 0)
        
        # Add summary data
        ws.cell(row=current_row, column=1).value = f"Total Epics: {total_epics}"
        current_row += 1
        ws.cell(row=current_row, column=1).value = f"Total Stories: {total_stories}"
        current_row += 1
        ws.cell(row=current_row, column=1).value = f"Total Story Points: {total_story_points}"
        current_row += 2
        
        ws.cell(row=current_row, column=1).value = "COST SUMMARY:"
        current_row += 1
        
        if total_proven_cost > 0:
            ws.cell(row=current_row, column=1).value = "Proven (Fixed):"
            ws.cell(row=current_row, column=6).value = f"€{total_proven_cost:,.2f}"
            current_row += 1
        
        if total_experimental_min > 0:
            ws.cell(row=current_row, column=1).value = "Experimental (Range):"
            ws.cell(row=current_row, column=8).value = f"€{total_experimental_min:,.2f}"
            ws.cell(row=current_row, column=9).value = f"€{total_experimental_max:,.2f}"
            current_row += 1
        
        if total_dependant_estimate > 0:
            ws.cell(row=current_row, column=1).value = "Dependant (Estimate):"
            ws.cell(row=current_row, column=11).value = f"€{total_dependant_estimate:,.2f}"
            current_row += 1
        
        # Add grand total estimate
        grand_total = total_proven_cost + total_experimental_max + total_dependant_estimate
        current_row += 1
        ws.cell(row=current_row, column=1).value = "ESTIMATED TOTAL (worst case):"
        ws.cell(row=current_row, column=11).value = f"€{grand_total:,.2f}"
        
        # Style the totals
        total_font = Font(bold=True, size=11)
        for row in range(start_row + 3, current_row + 1):
            ws.cell(row=row, column=1).font = total_font
    
    def _add_epic_header(self, ws, row, epic_key, epic_summary):
        """Add an epic header row"""
        ws.cell(row=row, column=1).value = f"[EPIC] {epic_summary} ({epic_key})"
        
        # Style the epic header
        epic_font = Font(bold=True, color="000000")
        epic_fill = PatternFill(start_color="E6F3FF", end_color="E6F3FF", fill_type="solid")
        
        for col in range(1, 12):
            cell = ws.cell(row=row, column=col)
            cell.font = epic_font
            cell.fill = epic_fill
    
    def _add_story_row(self, ws, row, story_data):
        """Add a story row with all pricing information"""
        # Column mapping based on the original structure
        ws.cell(row=row, column=1).value = f"  └─ {story_data['summary']} ({story_data['key']})"
        ws.cell(row=row, column=2).value = story_data['moscow']
        ws.cell(row=row, column=3).value = story_data['risk_profile'].title()
        ws.cell(row=row, column=4).value = f"Story Points: {story_data['story_points']}"
        
        # Add pricing based on risk profile
        prices = story_data['prices']
        
        if story_data['risk_profile'] == 'proven':
            ws.cell(row=row, column=5).value = story_data['story_points']  # Story points
            ws.cell(row=row, column=6).value = prices.get('fixed', 0)  # Fixed price
            
        elif story_data['risk_profile'] == 'experimental':
            ws.cell(row=row, column=7).value = story_data['story_points']  # Story points
            ws.cell(row=row, column=8).value = prices.get('minimum', 0)  # Min price
            ws.cell(row=row, column=9).value = prices.get('maximum', 0)  # Max price
            
        elif story_data['risk_profile'] == 'dependant':
            ws.cell(row=row, column=10).value = story_data['story_points']  # Story points
            ws.cell(row=row, column=11).value = prices.get('hourly_estimate', 0)  # Hourly estimate
    
    def test_connections(self) -> bool:
        """Test connections to Jira and spec sheet"""
        print("🔄 Testing connections...")
        
        # Test Jira connection
        if not self.jira_client.test_connection():
            return False
        
        # Test spec sheet access
        if not self.load_spec_sheet_structure():
            return False
        
        print("✅ All connections successful")
        return True
    
    def sync_all_sheets(self):
        """Sync to all sheets - Jira as single source of truth"""
        # Sync the main scope sheet
        sheet_name = 'Scope (Quantity)'
        
        if sheet_name in self.workbook.sheetnames:
            print(f"\n🔄 Regenerating: {sheet_name}")
            success = self.sync_to_scope_sheet(sheet_name)
            
            # Add sprint planning analysis if main sync successful
            if success and self.sprint_planning_enabled:
                try:
                    print(f"\n🔄 Adding sprint planning analysis...")
                    self.add_sprint_planning_sheet()
                    print("✅ Sprint planning analysis added")
                except Exception as e:
                    print(f"⚠️  Warning: Could not add sprint planning sheet: {e}")
            

                
        else:
            print(f"❌ Sheet '{sheet_name}' not found in workbook")
    


def main():
    """Main entry point"""
    print("🚀 Enhanced Jira to Spec Sheet Sync Tool")
    print("=" * 60)
    
    sync = EnhancedSpecSheetSync()
    
    # Test connections first
    if not sync.test_connections():
        print("\n❌ Connection test failed. Please check your configuration.")
        sys.exit(1)
    
    # Perform sync
    try:
        sync.sync_all_sheets()
        print("\n🎉 All done! Check your spec sheet for updated Jira data.")
    except Exception as e:
        print(f"\n💥 Sync failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 