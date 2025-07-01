#!/usr/bin/env python3
"""
Sprint Models and Calculations for Timeline Generation
Handles sprint data structures and capacity calculations
"""

from datetime import date, timedelta
from typing import List
from dataclasses import dataclass


@dataclass
class Sprint:
    """Sprint information with dates"""
    number: int
    start_date: date
    end_date: date
    story_points: float
    name: str = ""
    team_velocity: float = 0.0


class SprintCalculator:
    """Handles sprint timeline calculations and capacity planning"""
    
    def __init__(self, holiday_manager):
        self.holiday_manager = holiday_manager
    
    def calculate_working_days(self, start_date: date, end_date: date, member) -> int:
        """Calculate working days for a team member considering holidays"""
        working_days = 0
        current_date = start_date
        
        while current_date <= end_date:
            # Check if it's a weekday (Monday = 0, Sunday = 6)
            if current_date.weekday() < 5:  # Monday to Friday
                # Check if member is on holiday
                if not self.holiday_manager.is_holiday(current_date, member.name):
                    working_days += 1
            
            current_date += timedelta(days=1)
        
        return working_days
    
    def calculate_effective_capacity(self, member, start_date: date, end_date: date) -> float:
        """Calculate effective capacity for a team member"""
        working_days = self.calculate_working_days(start_date, end_date, member)
        return working_days * member.availability
    
    def generate_sprint_timeline(self, start_date: date, total_story_points: float, 
                               team_members: List, sprint_length_weeks: int = 2) -> List[Sprint]:
        """Generate sprint timeline based on team capacity"""
        if not team_members:
            print("❌ No team members available for sprint planning")
            return []
        
        # Calculate total team capacity per sprint
        sprint_days = sprint_length_weeks * 5  # Working days only
        
        # Calculate team velocity (story points per sprint)
        total_team_velocity = sum(member.story_points_per_sprint for member in team_members)
        
        print(f"📊 Team Analysis:")
        print(f"   Sprint length: {sprint_length_weeks} weeks ({sprint_days} working days)")
        print(f"   Team velocity: {total_team_velocity} story points per sprint")
        print(f"   Total story points needed: {total_story_points}")
        
        # Calculate number of sprints needed
        sprints_needed = max(1, round(total_story_points / total_team_velocity))
        actual_sprints_needed = total_story_points / total_team_velocity
        
        print(f"   Sprints needed: {actual_sprints_needed:.1f} (rounded to {sprints_needed})")
        
        # Generate sprints
        sprints = []
        remaining_story_points = total_story_points
        current_start_date = start_date
        
        for sprint_num in range(1, sprints_needed + 1):
            # Calculate sprint end date (skip weekends)
            sprint_end_date = current_start_date
            days_added = 0
            
            while days_added < sprint_days:
                sprint_end_date += timedelta(days=1)
                if sprint_end_date.weekday() < 5:  # Only count weekdays
                    days_added += 1
            
            # Calculate story points for this sprint
            if sprint_num == sprints_needed:
                # Last sprint gets remaining points
                sprint_story_points = remaining_story_points
            else:
                sprint_story_points = min(total_team_velocity, remaining_story_points)
            
            sprint = Sprint(
                number=sprint_num,
                start_date=current_start_date,
                end_date=sprint_end_date,
                story_points=sprint_story_points,
                name=f"Sprint {sprint_num}",
                team_velocity=total_team_velocity
            )
            
            sprints.append(sprint)
            remaining_story_points -= sprint_story_points
            
            # Next sprint starts the Monday after this one ends
            current_start_date = sprint_end_date + timedelta(days=1)
            while current_start_date.weekday() != 0:  # Find next Monday
                current_start_date += timedelta(days=1)
        
        print(f"\n📅 Generated {len(sprints)} sprints:")
        for sprint in sprints:
            print(f"   Sprint {sprint.number}: {sprint.start_date} to {sprint.end_date} ({sprint.story_points:.1f} SP)")
        
        return sprints 