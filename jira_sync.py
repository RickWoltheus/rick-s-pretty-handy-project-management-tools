#!/usr/bin/env python3
"""
Jira to Spreadsheet Sync Tool
Syncs Jira epics and stories with cost estimation spreadsheet
"""

import sys
from datetime import datetime
from typing import List, Dict, Tuple
from config import JiraConfig, SpreadsheetConfig
from jira_client import JiraClient
from spreadsheet_manager import SpreadsheetManager

class JiraSpreadsheetSync:
    """Main class for synchronizing Jira with spreadsheets"""
    
    def __init__(self):
        try:
            self.jira_config = JiraConfig()
            self.spreadsheet_config = SpreadsheetConfig()
            self.jira_client = JiraClient(self.jira_config)
            self.spreadsheet_manager = SpreadsheetManager(self.spreadsheet_config)
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    
    def test_connections(self) -> bool:
        """Test connections to Jira and spreadsheet"""
        print("🔄 Testing connections...")
        
        # Test Jira connection
        if not self.jira_client.test_connection():
            return False
        
        # Test spreadsheet access
        try:
            self.spreadsheet_manager.load_or_create_workbook()
            print("✅ Spreadsheet access confirmed")
            return True
        except Exception as e:
            print(f"❌ Spreadsheet error: {e}")
            return False
    
    def sync_data(self) -> bool:
        """Main sync function"""
        print(f"\n🚀 Starting sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Load spreadsheet
            self.spreadsheet_manager.load_or_create_workbook()
            
            # Get data from Jira
            print("📥 Fetching epics from Jira...")
            epics = self.jira_client.get_epics()
            
            if not epics:
                print("⚠️  No epics found in Jira project")
                return False
            
            print(f"📋 Found {len(epics)} epics")
            
            # Clear existing data
            self.spreadsheet_manager.clear_data_rows()
            
            # Process each epic
            current_row = self.spreadsheet_config.data_start_row
            grand_total_points = 0
            grand_total_cost = 0
            
            for epic in epics:
                epic_key = epic['key']
                epic_summary = epic['fields']['summary']
                
                print(f"\n📊 Processing epic: {epic_key} - {epic_summary}")
                
                # Add epic header row
                self.spreadsheet_manager.add_epic_row(epic_key, epic_summary, current_row)
                current_row += 1
                
                # Get stories for this epic
                stories = self.jira_client.get_stories_for_epic(epic_key)
                print(f"   Found {len(stories)} stories")
                
                epic_total_points = 0
                
                # Process each story
                for story in stories:
                    story_key = story['key']
                    story_summary = story['fields']['summary']
                    story_points = self.jira_client.get_story_points(story)
                    
                    print(f"   - {story_key}: {story_points or 0} points")
                    
                    # Add story row
                    self.spreadsheet_manager.add_story_row(
                        story_key, story_summary, story_points, current_row
                    )
                    
                    if story_points:
                        epic_total_points += story_points
                    
                    current_row += 1
                
                # Add epic summary row
                if stories:
                    self.spreadsheet_manager.add_epic_summary_row(
                        epic_key, epic_total_points, current_row
                    )
                    current_row += 1
                
                # Add to grand totals
                grand_total_points += epic_total_points
                grand_total_cost += epic_total_points * self.spreadsheet_config.cost_per_story_point
                
                # Add spacing between epics
                current_row += 1
            
            # Add grand total
            self.spreadsheet_manager.add_grand_total_row(
                grand_total_points, grand_total_cost, current_row
            )
            
            # Save spreadsheet
            self.spreadsheet_manager.save()
            
            print(f"\n✅ Sync completed successfully!")
            print(f"   📊 Total Story Points: {grand_total_points}")
            print(f"   💰 Total Estimated Cost: ${grand_total_cost:,.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Sync failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def find_story_points_field(self):
        """Helper function to find the correct story points field ID"""
        print("🔍 Searching for Story Points custom field...")
        print("ℹ️  Note: Consider using the new field discovery tool: python field_discovery.py")
        print()
        
        field_id = self.jira_client.get_custom_field_id("Story Points")
        if field_id:
            print(f"✅ Found Story Points field: {field_id}")
            print(f"Update your .env file with: JIRA_STORY_POINTS_FIELD={field_id}")
        else:
            print("❌ Could not find Story Points field")
            print("Please check your Jira instance and ensure the field exists")
            print()
            print("💡 Try the enhanced field discovery tool for more options:")
            print("   python field_discovery.py --story-points")

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--find-field":
        sync = JiraSpreadsheetSync()
        sync.find_story_points_field()
        return
    
    print("🔄 Jira to Spreadsheet Sync Tool")
    print("=" * 50)
    
    sync = JiraSpreadsheetSync()
    
    # Test connections first
    if not sync.test_connections():
        print("\n❌ Connection test failed. Please check your configuration.")
        sys.exit(1)
    
    # Perform sync
    if sync.sync_data():
        print("\n🎉 All done! Check your spreadsheet for updated data.")
    else:
        print("\n💥 Sync failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 