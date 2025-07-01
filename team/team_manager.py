#!/usr/bin/env python3
"""
Team Management System
Handles team member creation, holiday management, and persistent storage
"""

import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import sys
sys.path.insert(0, '..')

@dataclass
class Holiday:
    """Represents a holiday for a team member"""
    start_date: str  # YYYY-MM-DD format
    end_date: str    # YYYY-MM-DD format
    name: str
    is_national: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Holiday':
        return cls(**data)

@dataclass
class TeamMember:
    """Represents a team member with their details and holidays"""
    name: str
    role: str
    availability: float = 1.0  # 0.0 to 1.0 (percentage available)
    story_points_per_sprint: float = 6.0
    hourly_rate: float = 95.37
    email: Optional[str] = None
    holidays: List[Holiday] = None
    
    def __post_init__(self):
        if self.holidays is None:
            self.holidays = []
    
    def add_holiday(self, start_date: str, end_date: str, name: str, is_national: bool = False):
        """Add a holiday for this team member"""
        holiday = Holiday(start_date, end_date, name, is_national)
        self.holidays.append(holiday)
    
    def get_holidays_in_range(self, start_date: date, end_date: date) -> List[Holiday]:
        """Get holidays that overlap with the given date range"""
        overlapping = []
        for holiday in self.holidays:
            h_start = datetime.strptime(holiday.start_date, '%Y-%m-%d').date()
            h_end = datetime.strptime(holiday.end_date, '%Y-%m-%d').date()
            
            # Check if holidays overlap with the range
            if h_start <= end_date and h_end >= start_date:
                overlapping.append(holiday)
        
        return overlapping
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['holidays'] = [holiday.to_dict() for holiday in self.holidays]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TeamMember':
        holidays_data = data.pop('holidays', [])
        member = cls(**data)
        member.holidays = [Holiday.from_dict(h) for h in holidays_data]
        return member

class TeamManager:
    """Manages team members and their persistent storage"""
    
    def __init__(self, team_folder: str = "team"):
        self.team_folder = team_folder
        self.ensure_team_folder()
    
    def ensure_team_folder(self):
        """Create team folder if it doesn't exist"""
        if not os.path.exists(self.team_folder):
            os.makedirs(self.team_folder)
            print(f"📁 Created team folder: {self.team_folder}")
    
    def get_member_file_path(self, name: str) -> str:
        """Get the file path for a team member"""
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in name)
        safe_name = safe_name.replace(' ', '_').lower()
        return os.path.join(self.team_folder, f"{safe_name}.json")
    
    def save_member(self, member: TeamMember) -> bool:
        """Save a team member to disk"""
        try:
            file_path = self.get_member_file_path(member.name)
            with open(file_path, 'w') as f:
                json.dump(member.to_dict(), f, indent=2)
            print(f"💾 Saved team member: {member.name} to {file_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving team member {member.name}: {e}")
            return False
    
    def load_member(self, name: str) -> Optional[TeamMember]:
        """Load a team member from disk"""
        try:
            file_path = self.get_member_file_path(name)
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return TeamMember.from_dict(data)
        except Exception as e:
            print(f"❌ Error loading team member {name}: {e}")
            return None
    
    def list_members(self) -> List[str]:
        """List all saved team members"""
        try:
            if not os.path.exists(self.team_folder):
                return []
            
            members = []
            for file in os.listdir(self.team_folder):
                if file.endswith('.json'):
                    # Load to get actual name
                    file_path = os.path.join(self.team_folder, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        members.append(data['name'])
            
            return sorted(members)
        except Exception as e:
            print(f"❌ Error listing team members: {e}")
            return []
    
    def load_all_members(self) -> List[TeamMember]:
        """Load all team members"""
        members = []
        for name in self.list_members():
            member = self.load_member(name)
            if member:
                members.append(member)
        return members
    
    def delete_member(self, name: str) -> bool:
        """Delete a team member"""
        try:
            file_path = self.get_member_file_path(name)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️  Deleted team member: {name}")
                return True
            else:
                print(f"⚠️  Team member not found: {name}")
                return False
        except Exception as e:
            print(f"❌ Error deleting team member {name}: {e}")
            return False
    
    def create_member_interactive(self) -> Optional[TeamMember]:
        """Interactively create a new team member"""
        print("\n👤 Create New Team Member")
        print("=" * 30)
        
        try:
            # Basic info
            name = input("Name: ").strip()
            if not name:
                print("❌ Name is required")
                return None
            
            # Check if already exists
            existing = self.load_member(name)
            if existing:
                overwrite = input(f"⚠️  '{name}' already exists. Overwrite? (y/N): ").strip().lower()
                if overwrite != 'y':
                    print("❌ Cancelled")
                    return None
            
            role = input("Role (e.g., Developer, Designer, QA): ").strip() or "Developer"
            
            # Availability
            while True:
                try:
                    availability_input = input("Availability (0.0-1.0, default 1.0): ").strip()
                    if not availability_input:
                        availability = 1.0
                        break
                    availability = float(availability_input)
                    if 0.0 <= availability <= 1.0:
                        break
                    print("❌ Availability must be between 0.0 and 1.0")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Story points per sprint
            while True:
                try:
                    sp_input = input("Story points per sprint (default 6.0): ").strip()
                    if not sp_input:
                        story_points = 6.0
                        break
                    story_points = float(sp_input)
                    if story_points > 0:
                        break
                    print("❌ Story points must be positive")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Hourly rate
            while True:
                try:
                    rate_input = input("Hourly rate (default €95.37): ").strip()
                    if not rate_input:
                        hourly_rate = 95.37
                        break
                    hourly_rate = float(rate_input)
                    if hourly_rate > 0:
                        break
                    print("❌ Hourly rate must be positive")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Email (optional)
            email = input("Email (optional): ").strip() or None
            
            # Create member
            member = TeamMember(
                name=name,
                role=role,
                availability=availability,
                story_points_per_sprint=story_points,
                hourly_rate=hourly_rate,
                email=email
            )
            
            print(f"\n📋 Team Member Summary:")
            print(f"   Name: {member.name}")
            print(f"   Role: {member.role}")
            print(f"   Availability: {member.availability * 100:.0f}%")
            print(f"   Story Points/Sprint: {member.story_points_per_sprint}")
            print(f"   Hourly Rate: €{member.hourly_rate:.2f}")
            if member.email:
                print(f"   Email: {member.email}")
            
            # Add holidays
            print(f"\n🏖️  Add Holidays for {member.name}")
            print("(You can add multiple holidays. Press Enter with empty name to finish)")
            
            while True:
                holiday_name = input("\nHoliday name (Enter to finish): ").strip()
                if not holiday_name:
                    break
                
                start_date = self._get_date_input("Start date (YYYY-MM-DD): ")
                if not start_date:
                    continue
                
                end_date = self._get_date_input("End date (YYYY-MM-DD): ")
                if not end_date:
                    continue
                
                if start_date > end_date:
                    print("❌ Start date cannot be after end date")
                    continue
                
                is_national = input("Is this a national holiday? (y/N): ").strip().lower() == 'y'
                
                member.add_holiday(start_date.strftime('%Y-%m-%d'), 
                                 end_date.strftime('%Y-%m-%d'), 
                                 holiday_name, 
                                 is_national)
                
                print(f"✅ Added holiday: {holiday_name} ({start_date} to {end_date})")
            
            # Save member
            if self.save_member(member):
                print(f"\n✅ Team member '{member.name}' created successfully!")
                return member
            else:
                print(f"\n❌ Failed to save team member")
                return None
                
        except KeyboardInterrupt:
            print("\n❌ Cancelled")
            return None
    
    def _get_date_input(self, prompt: str) -> Optional[date]:
        """Get a valid date input from user"""
        while True:
            try:
                date_str = input(prompt).strip()
                if not date_str:
                    return None
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD (e.g., 2024-12-25)")
    
    def add_holiday_to_member(self, member_name: str) -> bool:
        """Add a holiday to an existing team member"""
        member = self.load_member(member_name)
        if not member:
            print(f"❌ Team member '{member_name}' not found")
            return False
        
        print(f"\n🏖️  Add Holiday for {member.name}")
        
        holiday_name = input("Holiday name: ").strip()
        if not holiday_name:
            print("❌ Holiday name is required")
            return False
        
        start_date = self._get_date_input("Start date (YYYY-MM-DD): ")
        if not start_date:
            return False
        
        end_date = self._get_date_input("End date (YYYY-MM-DD): ")
        if not end_date:
            return False
        
        if start_date > end_date:
            print("❌ Start date cannot be after end date")
            return False
        
        is_national = input("Is this a national holiday? (y/N): ").strip().lower() == 'y'
        
        member.add_holiday(start_date.strftime('%Y-%m-%d'), 
                         end_date.strftime('%Y-%m-%d'), 
                         holiday_name, 
                         is_national)
        
        if self.save_member(member):
            print(f"✅ Added holiday '{holiday_name}' to {member.name}")
            return True
        else:
            print(f"❌ Failed to save holiday")
            return False
    
    def show_member_details(self, member_name: str):
        """Show detailed information about a team member"""
        member = self.load_member(member_name)
        if not member:
            print(f"❌ Team member '{member_name}' not found")
            return
        
        print(f"\n👤 {member.name}")
        print("=" * (len(member.name) + 4))
        print(f"Role: {member.role}")
        print(f"Availability: {member.availability * 100:.0f}%")
        print(f"Story Points/Sprint: {member.story_points_per_sprint}")
        print(f"Hourly Rate: €{member.hourly_rate:.2f}")
        if member.email:
            print(f"Email: {member.email}")
        
        if member.holidays:
            print(f"\n🏖️  Holidays ({len(member.holidays)}):")
            for holiday in member.holidays:
                holiday_type = "🌍 National" if holiday.is_national else "👤 Personal"
                print(f"   {holiday_type} {holiday.name}: {holiday.start_date} to {holiday.end_date}")
        else:
            print(f"\n🏖️  No holidays defined")
    
    def list_all_members(self):
        """List all team members with summary"""
        members = self.list_members()
        
        if not members:
            print("👥 No team members found. Create some with option 1!")
            return
        
        print(f"\n👥 Team Members ({len(members)}):")
        print("=" * 30)
        
        for name in members:
            member = self.load_member(name)
            if member:
                holiday_count = len(member.holidays)
                print(f"   👤 {member.name} ({member.role}) - {holiday_count} holidays")
        
        print(f"\n💡 Use 'Show Member Details' to see full information")

def main():
    """Team management CLI"""
    manager = TeamManager()
    
    while True:
        print("\n" + "=" * 50)
        print("👥 TEAM MANAGEMENT")
        print("=" * 50)
        print("1. 👤 Create New Team Member")
        print("2. 📋 List All Team Members") 
        print("3. 🔍 Show Member Details")
        print("4. 🏖️  Add Holiday to Member")
        print("5. 🗑️  Delete Team Member")
        print("0. 🚪 Back to Main Menu")
        print("=" * 50)
        
        choice = input("Select option (0-5): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            manager.create_member_interactive()
        elif choice == '2':
            manager.list_all_members()
        elif choice == '3':
            members = manager.list_members()
            if not members:
                print("👥 No team members found")
                continue
            
            print("\nSelect team member:")
            for i, name in enumerate(members, 1):
                print(f"{i}. {name}")
            
            try:
                idx = int(input(f"Enter choice (1-{len(members)}): ")) - 1
                if 0 <= idx < len(members):
                    manager.show_member_details(members[idx])
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == '4':
            members = manager.list_members()
            if not members:
                print("👥 No team members found")
                continue
            
            print("\nSelect team member:")
            for i, name in enumerate(members, 1):
                print(f"{i}. {name}")
            
            try:
                idx = int(input(f"Enter choice (1-{len(members)}): ")) - 1
                if 0 <= idx < len(members):
                    manager.add_holiday_to_member(members[idx])
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == '5':
            members = manager.list_members()
            if not members:
                print("👥 No team members found")
                continue
            
            print("\nSelect team member to delete:")
            for i, name in enumerate(members, 1):
                print(f"{i}. {name}")
            
            try:
                idx = int(input(f"Enter choice (1-{len(members)}): ")) - 1
                if 0 <= idx < len(members):
                    confirm = input(f"⚠️  Really delete '{members[idx]}'? (y/N): ").strip().lower()
                    if confirm == 'y':
                        manager.delete_member(members[idx])
                    else:
                        print("❌ Cancelled")
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a valid number")
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 