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

# Import modular components
from timeline.holiday_manager import HolidayManager
from timeline.sprint_models import SprintCalculator
from timeline.timeline_orchestrator import TimelineOrchestrator
from timeline.timeline_user_interface import TimelineUserInterface
from timeline.jira_integration import JiraIntegration

class EnhancedTimelineGenerator:
    """Enhanced timeline generator that loads team from persistent storage"""
    
    def __init__(self):
        self.team_manager = TeamManager()
        self.team_members: List[TeamMember] = []
        
        # Initialize modular components
        self.holiday_manager = HolidayManager()
        self.sprint_calculator = SprintCalculator(self.holiday_manager)
        self.ui = TimelineUserInterface()
        self.jira_integration = JiraIntegration()
        self.orchestrator: Optional[TimelineOrchestrator] = None
    
    def load_team_from_storage(self) -> bool:
        """Load team members from persistent storage and setup orchestrator"""
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
        
        # Initialize orchestrator with loaded team
        self.orchestrator = TimelineOrchestrator(
            self.team_members, 
            self.holiday_manager, 
            self.sprint_calculator
        )
        
        return True
    

    
    def run_interactive(self):
        """Run the enhanced timeline generator interactively"""
        self.ui.display_timeline_header()
        
        # Load team from storage
        if not self.load_team_from_storage():
            self.ui.display_no_team_members_error()
            return
        
        # Load story points from spec sheet
        self.ui.display_story_points_loading()
        total_story_points = self.orchestrator.load_story_points_from_spec_sheet()
        
        if total_story_points <= 0:
            self.ui.display_no_story_points_error()
            return
        
        # Get project start date
        self.ui.display_project_planning_header(total_story_points)
        start_date = self.ui.get_project_start_date()
        
        if start_date is None:
            return
        
        # Execute the full workflow using orchestrator
        self.orchestrator.execute_full_workflow(start_date, total_story_points)

def main():
    """Enhanced timeline generator main function"""
    generator = EnhancedTimelineGenerator()
    ui = TimelineUserInterface()
    
    while True:
        ui.display_main_menu()
        choice = ui.get_menu_choice()
        
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
            ui.display_invalid_choice()

if __name__ == "__main__":
    main() 