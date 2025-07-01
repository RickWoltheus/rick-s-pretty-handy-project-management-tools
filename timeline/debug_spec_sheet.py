#!/usr/bin/env python3
"""
Debug script to analyze spec sheet contents and help troubleshoot story point detection
"""

import sys
import os
from datetime import date

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from timeline.timeline_generator import TimelineGenerator

def debug_spec_sheet(file_path):
    """Debug a spec sheet to understand its structure"""
    print(f"🔍 Debug Analysis for: {file_path}")
    print("=" * 60)
    
    timeline = TimelineGenerator()
    
    # This will run our enhanced debugging version
    story_points = timeline.load_story_points_from_spec_sheet(file_path)
    
    print(f"\n📊 Final Result: {story_points} story points found")
    
    return story_points

def main():
    """Main debug function"""
    spec_files = ["spec-sheet.xlsx", "jira_cost_estimation.xlsx"]
    
    print("🔍 Spec Sheet Debug Tool")
    print("=" * 60)
    print("This tool will analyze your spec sheets to understand why story points aren't being detected.\n")
    
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            print(f"\n📋 Found: {spec_file}")
            debug_spec_sheet(spec_file)
            print("\n" + "="*60 + "\n")
        else:
            print(f"❌ Not found: {spec_file}")
    
    # Also check current directory for any .xlsx files
    print("\n🔍 Other Excel files in current directory:")
    for file in os.listdir("."):
        if file.endswith(".xlsx") and file not in spec_files:
            print(f"📄 Found: {file}")
            choice = input(f"Analyze {file}? (y/n): ").strip().lower()
            if choice == 'y':
                debug_spec_sheet(file)
                print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main() 