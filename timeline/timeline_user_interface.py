#!/usr/bin/env python3
"""
Timeline User Interface Handler
Handles user interactions and input validation for timeline generation
"""

from datetime import datetime, date
from typing import Optional, Tuple


class TimelineUserInterface:
    """Handles user interface interactions for timeline generation"""
    
    @staticmethod
    def get_project_start_date() -> Optional[date]:
        """Get and validate project start date from user input"""
        print(f"\n📅 Project Planning")
        try:
            start_date_str = input("Project start date (YYYY-MM-DD): ").strip()
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            return start_date
        except ValueError:
            print("❌ Invalid date format")
            return None
    
    @staticmethod
    def display_timeline_header():
        """Display the timeline generator header"""
        print("\n📅 ENHANCED TIMELINE GENERATOR")
        print("=" * 50)
    
    @staticmethod
    def display_no_team_members_error():
        """Display error message when no team members are found"""
        print("❌ Cannot continue without team members")
        print("💡 Please create team members first using Team Management")
    
    @staticmethod
    def display_no_story_points_error():
        """Display error message when no story points are found"""
        print("❌ No story points found in spec sheet")
        print("💡 Please generate a spec sheet first or ensure it contains story points")
    
    @staticmethod
    def display_story_points_loading():
        """Display message for story points loading"""
        print("\n📊 Loading story points from spec sheet...")
    
    @staticmethod
    def display_project_planning_header(total_story_points: float):
        """Display project planning header with story points"""
        print(f"\n📅 Project Planning ({total_story_points} story points)")
    
    @staticmethod
    def display_main_menu():
        """Display the main menu options"""
        print("\n" + "=" * 50)
        print("📅 ENHANCED TIMELINE GENERATOR")
        print("=" * 50)
        print("1. 📊 Generate Project Timeline")
        print("2. 👥 View Team Members")
        print("3. 🏖️  Manage Team (Create/Edit Members)")
        print("0. 🚪 Back to Main Menu")
        print("=" * 50)
    
    @staticmethod
    def get_menu_choice() -> str:
        """Get menu choice from user"""
        return input("Select option (0-3): ").strip()
    
    @staticmethod
    def display_invalid_choice():
        """Display invalid choice message"""
        print("❌ Invalid choice") 