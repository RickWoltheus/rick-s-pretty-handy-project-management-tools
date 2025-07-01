#!/usr/bin/env python3
"""
Timeline Workflow Orchestrator
Handles the coordination of different components for timeline generation
"""

from datetime import datetime, date
from typing import List, Optional
from timeline.holiday_manager import HolidayManager
from timeline.sprint_models import SprintCalculator
from timeline.calendar_generator import CalendarGenerator
from timeline.excel_generator import ExcelGenerator
from timeline.spec_sheet_loader import SpecSheetLoader


class TimelineOrchestrator:
    """Orchestrates the timeline generation workflow"""
    
    def __init__(self, team_members: List, holiday_manager: HolidayManager, sprint_calculator: SprintCalculator):
        self.team_members = team_members
        self.holiday_manager = holiday_manager
        self.sprint_calculator = sprint_calculator
        self.sprints = []
        self.project_start_date: Optional[date] = None
        self.project_end_date: Optional[date] = None
    
    def load_story_points_from_spec_sheet(self, spec_sheet_path: str = "spec-sheet.xlsx") -> float:
        """Load total story points from existing spec sheet"""
        return SpecSheetLoader.load_story_points_from_spec_sheet(spec_sheet_path)
    
    def load_dutch_holidays(self, start_year: int, end_year: int):
        """Load Dutch national holidays for the project timeline"""
        self.holiday_manager.load_dutch_holidays(start_year, end_year)
    
    def generate_sprint_timeline(self, start_date: date, total_story_points: float, sprint_length_weeks: int = 2):
        """Generate sprint timeline based on team capacity"""
        self.sprints = self.sprint_calculator.generate_sprint_timeline(
            start_date, total_story_points, self.team_members, sprint_length_weeks
        )
        
        if self.sprints:
            self.project_start_date = start_date
            self.project_end_date = self.sprints[-1].end_date
        
        return self.sprints
    
    def save_timeline_workbook(self, filename: str = None) -> str:
        """Save the complete timeline workbook"""
        # Create calendar generator for the Excel generator
        calendar_generator = CalendarGenerator(self.holiday_manager, self.sprints)
        
        # Create Excel generator
        excel_generator = ExcelGenerator(
            self.team_members,
            self.sprints,
            self.holiday_manager,
            calendar_generator,
            self.project_start_date,
            self.project_end_date
        )
        
        # Generate the workbook
        return excel_generator.create_timeline_workbook(filename)
    
    def execute_full_workflow(self, start_date: date, total_story_points: float, sprint_length_weeks: int = 2) -> str:
        """Execute the complete timeline generation workflow"""
        # Load Dutch holidays
        start_year = start_date.year
        end_year = start_year + 1  # Load holidays for current and next year
        self.load_dutch_holidays(start_year, end_year)
        
        # Generate sprint timeline
        print(f"\n🔄 Generating sprint timeline from {start_date}...")
        self.generate_sprint_timeline(start_date, total_story_points, sprint_length_weeks)
        
        # Save timeline workbook
        filename = self.save_timeline_workbook()
        
        # Print summary
        print(f"\n✅ Enhanced timeline generation complete!")
        print(f"📊 Timeline saved to: {filename}")
        print(f"🎯 Project duration: {self.project_start_date} to {self.project_end_date}")
        print(f"📈 Total sprints: {len(self.sprints)}")
        print(f"👥 Team members: {len(self.team_members)}")
        
        return filename 