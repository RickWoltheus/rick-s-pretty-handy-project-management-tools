#!/usr/bin/env python3
"""
Sprint Planning Engine for Spec Sheet
Handles sprint estimates and team composition analysis using existing team system
"""

import math
from typing import Dict, List, Any
from spec_sheet.settings.config_manager import ConfigManager
from team.team_manager import TeamMember, TeamManager


class Team:
    """Represents a development team with various roles and capacities"""
    def __init__(self, name: str = "Development Team", settings_config: Dict = None):
        self.name = name
        self.members: List[TeamMember] = []
        
        # Use configurable settings or defaults
        if settings_config:
            self.sprint_length_weeks = settings_config["sprint_planning"]["default_sprint_length_weeks"]
            self.sprint_overhead = settings_config["sprint_planning"]["sprint_overhead_percentage"]
        else:
            self.sprint_length_weeks = 2  # Default 2-week sprints
            self.sprint_overhead = 0.15   # 15% overhead for meetings, planning, etc.
    
    def add_member(self, member: TeamMember):
        """Add a team member"""
        self.members.append(member)
    
    def get_total_velocity(self) -> float:
        """Calculate total team velocity per sprint"""
        total_velocity = sum(member.story_points_per_sprint * member.availability for member in self.members)
        # Apply sprint overhead reduction
        return total_velocity * (1 - self.sprint_overhead)
    
    def get_total_fte(self) -> float:
        """Get total FTE of the team"""
        return sum(member.availability for member in self.members)
    
    def get_composition_summary(self) -> str:
        """Get a summary of team composition"""
        if not self.members:
            return "Empty team"
        
        summary = f"{self.name} ({self.get_total_fte():.1f} total FTE):\n"
        for member in self.members:
            effective_velocity = member.story_points_per_sprint * member.availability
            summary += f"  • {member.role} ({member.availability} FTE): {effective_velocity:.1f} SP/sprint\n"
        summary += f"Total velocity: {self.get_total_velocity():.1f} SP/sprint"
        return summary


class SprintPlanner:
    """Handles sprint planning and team composition analysis"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.settings_config = config_manager.settings_config
        self.team_manager = TeamManager()
        self.default_teams = self._create_default_teams()
        self.current_team = self._load_current_team()
    
    def _create_default_teams(self) -> Dict[str, Team]:
        """Create default team compositions for analysis using configurable settings"""
        teams = {}
        team_defaults = self.settings_config["team_defaults"]
        
        # Small team
        small_team = Team("Small Team", self.settings_config)
        small_team.add_member(TeamMember("Senior Developer", "Senior Developer", 1.0, team_defaults["senior_developer_velocity"]))
        small_team.add_member(TeamMember("Junior Developer", "Junior Developer", 1.0, team_defaults["junior_developer_velocity"]))
        small_team.add_member(TeamMember("Designer", "Designer", 0.5, team_defaults["designer_velocity"]))
        teams["small"] = small_team
        
        # Medium team
        medium_team = Team("Medium Team", self.settings_config)
        medium_team.add_member(TeamMember("Tech Lead", "Tech Lead", 1.0, team_defaults["tech_lead_velocity"]))
        medium_team.add_member(TeamMember("Senior Developer", "Senior Developer", 2.0, team_defaults["senior_developer_velocity"]))
        medium_team.add_member(TeamMember("Junior Developer", "Junior Developer", 1.0, team_defaults["junior_developer_velocity"]))
        medium_team.add_member(TeamMember("Designer", "Designer", 1.0, team_defaults["designer_velocity"]))
        medium_team.add_member(TeamMember("QA Engineer", "QA Engineer", 0.5, team_defaults["qa_engineer_velocity"]))
        teams["medium"] = medium_team
        
        # Large team
        large_team = Team("Large Team", self.settings_config)
        large_team.add_member(TeamMember("Tech Lead", "Tech Lead", 1.0, team_defaults["tech_lead_velocity"]))
        large_team.add_member(TeamMember("Senior Developer", "Senior Developer", 3.0, team_defaults["senior_developer_velocity"]))
        large_team.add_member(TeamMember("Mid Developer", "Mid Developer", 2.0, team_defaults["mid_developer_velocity"]))
        large_team.add_member(TeamMember("Junior Developer", "Junior Developer", 2.0, team_defaults["junior_developer_velocity"]))
        large_team.add_member(TeamMember("Designer", "Designer", 1.0, team_defaults["designer_velocity"]))
        large_team.add_member(TeamMember("QA Engineer", "QA Engineer", 1.0, team_defaults["qa_engineer_velocity"]))
        large_team.add_member(TeamMember("DevOps Engineer", "DevOps Engineer", 0.5, team_defaults["devops_engineer_velocity"]))
        teams["large"] = large_team
        
        return teams
    
    def _load_current_team(self, verbose: bool = False) -> Team:
        """Load the current team from TeamManager with actual configured members"""
        current_team = Team("Current Team", self.settings_config)
        
        # Load all team members from the team manager
        team_members = self.team_manager.load_all_members()
        
        if team_members:
            for member in team_members:
                current_team.add_member(member)
            if verbose:
                print(f"📋 Loaded {len(team_members)} team members from configuration")
        elif verbose:
            print("⚠️  No team members found in configuration")
            print("💡 Use Team Management (option 6) to create team members")
        
        return current_team
    
    def get_current_team_info(self) -> Dict[str, Any]:
        """Get information about the current configured team"""
        if not self.current_team.members:
            return {
                'has_team': False,
                'message': 'No team members configured. Use Team Management to add members.',
                'total_fte': 0,
                'total_velocity': 0,
                'member_count': 0
            }
        
        return {
            'has_team': True,
            'total_fte': self.current_team.get_total_fte(),
            'total_velocity': self.current_team.get_total_velocity(),
            'member_count': len(self.current_team.members),
            'composition': self.current_team.get_composition_summary(),
            'members': [
                {
                    'name': member.name,
                    'role': member.role,
                    'availability': member.availability,
                    'velocity': member.story_points_per_sprint,
                    'effective_velocity': member.story_points_per_sprint * member.availability
                }
                for member in self.current_team.members
            ]
        }
    
    def display_current_team_info(self):
        """Display current team information in a user-friendly format"""
        team_info = self.get_current_team_info()
        
        print("\n" + "=" * 60)
        print("👥 CURRENT TEAM CONFIGURATION")
        print("=" * 60)
        
        if not team_info['has_team']:
            print("⚠️  " + team_info['message'])
            return
        
        print(f"Team Size: {team_info['member_count']} members")
        print(f"Total FTE: {team_info['total_fte']:.1f}")
        print(f"Expected Velocity: {team_info['total_velocity']:.1f} story points/sprint")
        print(f"Sprint Overhead: {self.current_team.sprint_overhead * 100:.0f}%")
        
        print(f"\n📊 Team Members:")
        for member in team_info['members']:
            fte_pct = member['availability'] * 100
            print(f"   • {member['name']} ({member['role']})")
            print(f"     Availability: {fte_pct:.0f}% | Velocity: {member['velocity']:.1f} SP/sprint | Effective: {member['effective_velocity']:.1f} SP/sprint")
        
        print(f"\n💡 To modify the team, use Team Management (option 6 in main menu)")
        print("=" * 60)
    
    def refresh_current_team(self):
        """Refresh the current team data from TeamManager (useful if team members were added/modified)"""
        print("🔄 Refreshing team configuration...")
        self.current_team = self._load_current_team(verbose=True)
        return self.current_team
    
    def calculate_sprint_estimates(self, total_story_points: float, team: Team) -> Dict[str, Any]:
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
    
    def compare_team_options(self, total_story_points: float) -> Dict[str, Dict[str, Any]]:
        """Compare different team compositions and their impact on timeline"""
        comparison = {}
        
        print(f"\n📊 Sprint Planning Analysis for {total_story_points} story points")
        print("=" * 60)
        
        # Include current team if it has members
        if self.current_team.members:
            estimates = self.calculate_sprint_estimates(total_story_points, self.current_team)
            comparison['current'] = estimates
            
            print(f"\n🎯 {self.current_team.name} (Your Configured Team):")
            print(f"  Team Size: {self.current_team.get_total_fte():.1f} FTE")
            print(f"  Velocity: {estimates['team_velocity']:.1f} SP/sprint")
            print(f"  Duration: {estimates['sprints']} sprints ({estimates['weeks']} weeks, {estimates['months']:.1f} months)")
            print(f"  Team: {len(self.current_team.members)} people")
        
        # Compare with default team sizes
        for team_name, team in self.default_teams.items():
            estimates = self.calculate_sprint_estimates(total_story_points, team)
            comparison[team_name] = estimates
            
            print(f"\n{team.name}:")
            print(f"  Team Size: {team.get_total_fte():.1f} FTE")
            print(f"  Velocity: {estimates['team_velocity']:.1f} SP/sprint")
            print(f"  Duration: {estimates['sprints']} sprints ({estimates['weeks']} weeks, {estimates['months']:.1f} months)")
            print(f"  Team: {len(team.members)} people")
        
        return comparison
    
    def create_custom_team(self, team_composition: List[Dict[str, Any]]) -> Team:
        """Create a custom team from a list of team member specifications"""
        custom_team = Team("Custom Team", self.settings_config)
        
        for member_spec in team_composition:
            name = member_spec.get('name', 'Team Member')
            role = member_spec.get('role', 'Developer')
            # Check for both 'fte' and 'availability' for backward compatibility
            availability = member_spec.get('fte', member_spec.get('availability', 1.0))
            velocity = member_spec.get('story_points_per_sprint', 6)
            hourly_rate = member_spec.get('hourly_rate', 95.37)
            
            member = TeamMember(name, role, availability, velocity, hourly_rate)
            custom_team.add_member(member)
        
        return custom_team
    
    def generate_recommendations(self, total_story_points: float, team_comparison: Dict[str, Dict], 
                               risk_breakdown: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis using configurable thresholds"""
        recommendations = []
        rec_config = self.settings_config["recommendations"]
        sprint_config = self.settings_config["sprint_planning"]
        
        # Timeline recommendations
        small_sprints = team_comparison.get('small', {}).get('sprints', 0)
        large_sprints = team_comparison.get('large', {}).get('sprints', 0)
        
        if small_sprints > 0 and large_sprints > 0:
            time_saved = small_sprints - large_sprints
            if time_saved > rec_config["significant_sprints_saved_threshold"]:
                weeks_saved = time_saved * sprint_config["default_sprint_length_weeks"]
                recommendations.append(f"Consider larger team - saves {time_saved} sprints ({weeks_saved} weeks)")
        
        # Risk-based recommendations
        experimental_pct = risk_breakdown.get('story_point_percentages', {}).get('experimental', 0)
        dependant_pct = risk_breakdown.get('story_point_percentages', {}).get('dependant', 0)
        
        if experimental_pct > rec_config["high_experimental_percentage"]:
            recommendations.append(f"High experimental work (>{rec_config['high_experimental_percentage']}%) - consider prototyping phase")
        
        if dependant_pct > rec_config["significant_dependent_percentage"]:
            recommendations.append(f"Significant dependent work (>{rec_config['significant_dependent_percentage']}%) - ensure external dependencies are ready")
        
        # Story points recommendations
        if total_story_points > rec_config["large_project_threshold"]:
            recommendations.append("Large project - consider breaking into phases or releases")
        
        if total_story_points < rec_config["small_project_threshold"]:
            recommendations.append("Small project - single developer might be sufficient")
        
        return recommendations
    
    def create_sprint_planning_sheet_data(self, epics: List[Dict[str, Any]], 
                                        get_stories_func, get_story_points_func, 
                                        determine_risk_profile_func) -> Dict[str, Any]:
        """Generate data for sprint planning sheet"""
        # Calculate total story points across all epics
        total_story_points = 0
        epic_breakdown = {}
        
        for epic in epics:
            epic_key = epic['key']
            stories = get_stories_func(epic_key)
            epic_points = sum(get_story_points_func(story) or 0 for story in stories)
            epic_breakdown[epic_key] = {
                'summary': epic['fields']['summary'],
                'story_points': epic_points,
                'story_count': len(stories)
            }
            total_story_points += epic_points
        
        # Compare team options
        team_comparison = self.compare_team_options(total_story_points)
        
        # Risk analysis based on story types
        from spec_sheet.settings.risk_assessor import RiskAssessor
        risk_assessor = RiskAssessor(self.config_manager, "")  # Type of work field would be passed in
        risk_breakdown = risk_assessor.analyze_risk_distribution(epics, get_stories_func, get_story_points_func)
        
        return {
            'total_story_points': total_story_points,
            'epic_breakdown': epic_breakdown,
            'team_comparison': team_comparison,
            'risk_breakdown': risk_breakdown,
            'recommendations': self.generate_recommendations(total_story_points, team_comparison, risk_breakdown)
        } 