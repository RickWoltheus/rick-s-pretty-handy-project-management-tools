#!/usr/bin/env python3
"""
Risk Assessment Engine for Spec Sheet
Determines risk profiles from Jira story data
"""

from typing import Dict, Any
from spec_sheet.settings.config_manager import ConfigManager


class RiskAssessor:
    """Determines risk profiles based on Jira story data and configuration"""
    
    def __init__(self, config_manager: ConfigManager, type_of_work_field: str):
        self.config_manager = config_manager
        self.settings_config = config_manager.settings_config
        self.type_of_work_field = type_of_work_field
        self.risk_priority = self.settings_config["risk_assessment"]["risk_priority"]
    
    def determine_risk_profile(self, story: Dict[str, Any]) -> str:
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
        
        # Fallback 2: Default risk assessment based on story points using configurable thresholds
        story_points = self._get_story_points_from_story(story)
        if story_points:
            risk_config = self.settings_config["risk_assessment"]
            if story_points <= risk_config["proven_threshold_story_points"]:
                return 'proven'
            elif story_points <= risk_config["experimental_threshold_story_points"]:
                return 'experimental'
            else:
                return 'dependant'
        
        print(f"   ⚠️  No Type of work field, using default: experimental")
        return 'experimental'  # Default to experimental
    
    def _get_story_points_from_story(self, story: Dict[str, Any]) -> float:
        """Extract story points from a story (helper method)"""
        # This is a simplified version - the actual implementation would depend on
        # how the JiraClient extracts story points
        story_points_field = story.get('fields', {}).get('customfield_10016')  # Example field
        if story_points_field:
            return float(story_points_field)
        return 0.0
    
    def analyze_risk_distribution(self, epics: list, get_stories_func, get_story_points_func) -> Dict[str, Any]:
        """Analyze the distribution of risk profiles across stories"""
        risk_counts = {'proven': 0, 'experimental': 0, 'dependant': 0}
        risk_story_points = {'proven': 0, 'experimental': 0, 'dependant': 0}
        
        for epic in epics:
            stories = get_stories_func(epic['key'])
            for story in stories:
                risk_profile = self.determine_risk_profile(story)
                story_points = get_story_points_func(story) or 0
                
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