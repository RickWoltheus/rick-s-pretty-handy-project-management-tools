#!/usr/bin/env python3
"""
Demo Timeline Generator
Shows the capabilities of the timeline tool with pre-configured settings
"""

import sys
import os
from datetime import date, timedelta

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from timeline.timeline_generator import TimelineGenerator, TeamMemberInfo, HolidayInfo

def demo_timeline():
    """Demonstrate timeline generation capabilities"""
    print("🎬 Timeline Generator Demo")
    print("=" * 60)
    print("📋 This demo shows all features of the timeline generator:")
    print("   • Integration with existing spec sheets")
    print("   • Dutch national holiday integration")
    print("   • Team capacity calculations")
    print("   • Sprint planning with realistic timelines")
    print("   • Calendar views with availability")
    
    timeline = TimelineGenerator()
    
    # Set up demo team
    print("\n👥 Setting up demo team...")
    timeline.add_team_member(TeamMemberInfo(
        name="Alice Johnson",
        role="Senior Full-Stack Developer",
        fte=1.0,
        story_points_per_sprint=12,
        hourly_rate=120,
        seniority_level="Senior",
        skills=["Python", "React", "TypeScript", "AWS", "PostgreSQL"]
    ))
    
    timeline.add_team_member(TeamMemberInfo(
        name="Bob Smith", 
        role="Mid-Level Backend Developer",
        fte=1.0,
        story_points_per_sprint=8,
        hourly_rate=95,
        seniority_level="Mid",
        skills=["Python", "Django", "Docker", "Redis", "MongoDB"]
    ))
    
    timeline.add_team_member(TeamMemberInfo(
        name="Carol Williams",
        role="UI/UX Designer & Frontend Dev",
        fte=0.8,  # Part-time
        story_points_per_sprint=6,
        hourly_rate=85,
        seniority_level="Senior",
        skills=["UI/UX", "Figma", "React", "CSS", "Design Systems"]
    ))
    
    timeline.add_team_member(TeamMemberInfo(
        name="David Chen",
        role="DevOps Engineer",
        fte=0.6,  # Shared across projects
        story_points_per_sprint=4,
        hourly_rate=110,
        seniority_level="Senior",
        skills=["AWS", "Kubernetes", "CI/CD", "Terraform", "Monitoring"]
    ))
    
    # Load Dutch holidays
    from datetime import datetime
    current_year = datetime.now().year
    timeline.load_dutch_holidays(current_year, current_year + 1)
    
    # Add some realistic custom holiday ranges
    timeline.add_workdays_holiday_range(
        start_date=date(2025, 7, 21),
        end_date=date(2025, 7, 25),
        name="Company Summer Break - Week 1",
        is_national=False
    )
    
    timeline.add_holiday_range(
        start_date=date(2025, 12, 23),
        end_date=date(2025, 12, 24),
        name="Christmas Break",
        is_national=False
    )
    
    timeline.add_holiday_range(
        start_date=date(2025, 12, 30),
        end_date=date(2025, 12, 31),
        name="Year-end Break",
        is_national=False
    )
    
    # Personal holiday range example
    timeline.add_workdays_holiday_range(
        start_date=date(2025, 8, 15),
        end_date=date(2025, 8, 22),
        name="Alice's Summer Vacation",
        is_national=False,
        affected_members=["Alice Johnson"]
    )
    
    # Try to load from existing spec sheet
    print("\n📊 Loading story points from spec sheet...")
    total_story_points = timeline.load_story_points_from_spec_sheet("spec-sheet.xlsx")
    
    if total_story_points == 0:
        print("📋 Using demo story points (150 SP)")
        total_story_points = 150
    
    # Set demo project start date
    start_date = date.today() + timedelta(days=14)  # Start in 2 weeks
    
    print(f"\n📅 Demo project timeline:")
    print(f"   • Start date: {start_date}")
    print(f"   • Total story points: {total_story_points}")
    print(f"   • Team size: {len(timeline.team_members)} members")
    print(f"   • Sprint length: 2 weeks")
    
    # Generate timeline
    timeline.generate_sprint_timeline(start_date, total_story_points, 2)
    
    # Save timeline
    filename = timeline.save_timeline_workbook("demo_timeline.xlsx")
    
    # Show detailed summary
    print(f"\n🎉 Demo Timeline Complete!")
    print("=" * 60)
    
    if timeline.team_members:
        total_capacity = sum(m.story_points_per_sprint * m.fte for m in timeline.team_members)
        print(f"👥 Team Composition:")
        for member in timeline.team_members:
            effective_sp = member.story_points_per_sprint * member.fte
            print(f"   • {member.name} ({member.role})")
            print(f"     - {member.fte} FTE, {effective_sp:.1f} effective SP/sprint")
            print(f"     - Skills: {', '.join(member.skills[:3])}{'...' if len(member.skills) > 3 else ''}")
        
        print(f"\n📊 Timeline Analysis:")
        print(f"   • Total team capacity: {total_capacity:.1f} SP/sprint")
        print(f"   • Story points to deliver: {total_story_points}")
        print(f"   • Sprints needed: {len(timeline.sprints)}")
        print(f"   • Project duration: {(timeline.project_end_date - timeline.project_start_date).days} days")
        
        if timeline.sprints:
            efficiency_rates = []
            for sprint in timeline.sprints:
                if sprint.team_velocity > 0:
                    efficiency = (sprint.story_points / sprint.team_velocity) * 100
                    efficiency_rates.append(efficiency)
            
            avg_efficiency = sum(efficiency_rates) / len(efficiency_rates) if efficiency_rates else 0
            print(f"   • Average capacity utilization: {avg_efficiency:.1f}%")
        
        print(f"\n🏖️  Holiday Impact:")
        national_holidays = [h for h in timeline.holidays if h.is_national]
        custom_holidays = [h for h in timeline.holidays if not h.is_national]
        print(f"   • Dutch national holidays: {len(national_holidays)}")
        print(f"   • Custom company/personal holidays: {len(custom_holidays)}")
        
        print(f"\n📋 Generated Files:")
        print(f"   • {filename}")
        print(f"     - Team Members sheet with skills and capacity")
        print(f"     - Holidays management with dates and affected members")
        print(f"     - Sprint Timeline with working days calculations")
        print(f"     - Calendar View with color-coded availability")
        
        print(f"\n🔧 Integration Features:")
        print(f"   ✅ JIRA connection available") if timeline.jira_available else print(f"   ⚠️  JIRA connection not configured")
        print(f"   ✅ Dutch holiday API integration")
        print(f"   ✅ Spec sheet integration")
        print(f"   ✅ Team capacity calculations")
        print(f"   ✅ Calendar view generation")
        
        print(f"\n💡 Next Steps:")
        print(f"   1. Open {filename} to view the detailed timeline")
        print(f"   2. Modify team members in the 'Team Members' sheet")
        print(f"   3. Add/edit holidays in the 'Holidays' sheet")
        print(f"   4. Review sprint planning in 'Sprint Timeline'")
        print(f"   5. Check calendar view for availability overview")
        print(f"   6. Run with real data: python timeline_generator.py")

if __name__ == "__main__":
    demo_timeline() 