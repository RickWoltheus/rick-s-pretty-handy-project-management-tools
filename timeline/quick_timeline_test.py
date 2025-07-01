#!/usr/bin/env python3
"""
Quick Timeline Test with Manual Story Points
Demonstrates timeline generation while JIRA story points are being assigned
"""

import sys
import os
from datetime import date, timedelta

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from timeline.timeline_generator import TimelineGenerator, TeamMemberInfo

def quick_timeline_test():
    """Quick timeline test with estimated story points"""
    print("🚀 Quick Timeline Test")
    print("=" * 50)
    print("This demonstrates timeline generation with estimated story points")
    print("while your JIRA issues are being properly story-pointed.\n")
    
    timeline = TimelineGenerator()
    
    # Add a simple test team
    timeline.add_team_member(TeamMemberInfo(
        name="Developer 1",
        role="Full Stack Developer", 
        fte=1.0,
        story_points_per_sprint=8,
        hourly_rate=95
    ))
    
    timeline.add_team_member(TeamMemberInfo(
        name="Developer 2",
        role="Frontend Developer",
        fte=0.8,
        story_points_per_sprint=6,
        hourly_rate=85
    ))
    
    # Load Dutch holidays
    from datetime import datetime
    current_year = datetime.now().year
    timeline.load_dutch_holidays(current_year, current_year + 1)
    
    # Estimate story points based on your issues
    estimated_story_points = {
        "Diagram download feature": 5,
        "Download podcast feature mobile": 8,
        "Availability on educa pro app": 3, 
        "Setup testing workflow": 5,
        "User interface for mobile users": 13,
        "Availability on ec-base monorepo": 8,
        "Bug fixes and polish": 8
    }
    
    total_estimated = sum(estimated_story_points.values())
    
    print(f"📊 Estimated Story Points for your project:")
    for feature, points in estimated_story_points.items():
        print(f"   • {feature}: {points} SP")
    print(f"   📋 Total: {total_estimated} SP")
    
    # Generate timeline
    start_date = date.today() + timedelta(days=7)  # Start next week
    timeline.generate_sprint_timeline(start_date, total_estimated, 2)
    
    # Save timeline
    filename = timeline.save_timeline_workbook("quick_timeline_test.xlsx")
    
    print(f"\n🎉 Quick Timeline Complete!")
    print(f"📊 Total Story Points: {total_estimated}")
    print(f"👥 Team Capacity: {timeline.team_members[0].story_points_per_sprint + timeline.team_members[1].story_points_per_sprint} SP/sprint")
    print(f"📅 Estimated Sprints: {len(timeline.sprints)}")
    print(f"💾 Saved: {filename}")
    print(f"\n💡 Next steps:")
    print(f"   1. Assign actual story points to your JIRA issues")
    print(f"   2. Run the spec sheet generator to update spec-sheet.xlsx")
    print(f"   3. Use the main timeline generator for accurate planning")

if __name__ == "__main__":
    quick_timeline_test() 