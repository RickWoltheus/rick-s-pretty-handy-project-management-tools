#!/usr/bin/env python3
"""
Enhanced Timeline Generator with Team Integration
Maintains original timeline behavior but uses persistent team management system:
- Reads story points from spec sheet (like original)
- Only asks for start date (like original) 
- Creates same Excel format (like original)
- Integrates with persistent team management (new feature)
"""

import sys
import os
from datetime import datetime, date
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import team management
from team.team_manager import TeamManager, TeamMember
from utils.config import JiraConfig
from utils.jira_client import JiraClient

# Import modular components
from timeline.holiday_manager import HolidayManager
from timeline.sprint_models import SprintCalculator
from timeline.calendar_generator import CalendarGenerator
from timeline.excel_generator import ExcelGenerator
from timeline.spec_sheet_loader import SpecSheetLoader

class EnhancedTimelineGenerator:
    """Enhanced timeline generator that loads team from persistent storage"""
    
    def __init__(self):
        self.team_manager = TeamManager()
        self.team_members: List[TeamMember] = []
        self.project_start_date: Optional[date] = None
        self.project_end_date: Optional[date] = None
        
        # Initialize modular components
        self.holiday_manager = HolidayManager()
        self.sprint_calculator = SprintCalculator(self.holiday_manager)
        self.sprints = []
        
        # Try to connect to JIRA for integration
        try:
            self.jira_config = JiraConfig()
            self.jira_client = JiraClient(self.jira_config)
            self.jira_available = True
            print("✅ JIRA integration available")
        except:
            self.jira_available = False
            print("⚠️  JIRA not available - timeline will work without JIRA integration")
    
    def load_team_from_storage(self) -> bool:
        """Load team members from persistent storage"""
        self.team_members = self.team_manager.load_all_members()
        
        if not self.team_members:
            print("❌ No team members found in storage")
            return False
        
        print(f"✅ Loaded {len(self.team_members)} team members from storage:")
        for member in self.team_members:
            holiday_count = len(member.holidays)
            print(f"   👤 {member.name} ({member.role}) - {member.availability*100:.0f}% - {holiday_count} holidays")
        
        # Convert team member holidays to timeline holidays using holiday manager
        self.holiday_manager.add_team_holidays(self.team_members)
        
        return True
    
    def load_dutch_holidays(self, start_year: int, end_year: int):
        """Load Dutch national holidays for the project timeline"""
        self.holiday_manager.load_dutch_holidays(start_year, end_year)
    
    def generate_sprint_timeline(self, start_date: date, total_story_points: float, sprint_length_weeks: int = 2):
        """Generate sprint timeline based on team capacity using sprint calculator"""
        self.sprints = self.sprint_calculator.generate_sprint_timeline(
            start_date, total_story_points, self.team_members, sprint_length_weeks
        )
        
        if self.sprints:
            self.project_start_date = start_date
            self.project_end_date = self.sprints[-1].end_date
        
        return self.sprints
    
    def load_story_points_from_spec_sheet(self, spec_sheet_path: str = "spec-sheet.xlsx") -> float:
        """Load total story points from existing spec sheet using SpecSheetLoader"""
        return SpecSheetLoader.load_story_points_from_spec_sheet(spec_sheet_path)
    
    def save_timeline_workbook(self, filename: str = None):
        """Save the complete timeline workbook using ExcelGenerator"""
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
    

    
    def run_interactive(self):
        """Run the enhanced timeline generator interactively"""
        print("\n📅 ENHANCED TIMELINE GENERATOR")
        print("=" * 50)
        
        # Load team from storage
        if not self.load_team_from_storage():
            print("❌ Cannot continue without team members")
            print("💡 Please create team members first using Team Management")
            return
        
        # Load story points from spec sheet
        print("\n📊 Loading story points from spec sheet...")
        total_story_points = self.load_story_points_from_spec_sheet()
        
        if total_story_points <= 0:
            print("❌ No story points found in spec sheet")
            print("💡 Please generate a spec sheet first or ensure it contains story points")
            return
        
        # Get project start date
        print(f"\n📅 Project Planning ({total_story_points} story points)")
        try:
            start_date_str = input("Project start date (YYYY-MM-DD): ").strip()
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid date format")
            return
        
        # Load Dutch holidays
        start_year = start_date.year
        end_year = start_year + 1  # Load holidays for current and next year
        self.load_dutch_holidays(start_year, end_year)
        
        # Generate sprint timeline
        print(f"\n🔄 Generating sprint timeline from {start_date}...")
        self.generate_sprint_timeline(start_date, total_story_points)
        
        # Save timeline workbook
        filename = self.save_timeline_workbook()
        
        print(f"\n✅ Enhanced timeline generation complete!")
        print(f"📊 Timeline saved to: {filename}")
        print(f"🎯 Project duration: {self.project_start_date} to {self.project_end_date}")
        print(f"📈 Total sprints: {len(self.sprints)}")
        print(f"👥 Team members: {len(self.team_members)}")

def main():
    """Enhanced timeline generator main function"""
    generator = EnhancedTimelineGenerator()
    
    while True:
        print("\n" + "=" * 50)
        print("📅 ENHANCED TIMELINE GENERATOR")
        print("=" * 50)
        print("1. 📊 Generate Project Timeline")
        print("2. 👥 View Team Members")
        print("3. 🏖️  Manage Team (Create/Edit Members)")
        print("0. 🚪 Back to Main Menu")
        print("=" * 50)
        
        choice = input("Select option (0-3): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            generator.run_interactive()
        elif choice == '2':
            generator.team_manager.list_all_members()
        elif choice == '3':
            from team.team_manager import main as team_main
            team_main()
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 