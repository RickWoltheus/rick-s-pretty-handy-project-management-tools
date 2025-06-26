#!/usr/bin/env python3
"""
JIRA Field Discovery Tool
Interactive tool to find and configure any JIRA custom field
"""

import sys
import os
import re
from typing import List, Dict, Optional
from .config import JiraConfig
from .jira_client import JiraClient

class FieldDiscovery:
    """Interactive field discovery and configuration tool"""
    
    def __init__(self):
        try:
            self.jira_config = JiraConfig()
            self.jira_client = JiraClient(self.jira_config)
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    
    def discover_fields(self, search_term: str = None) -> List[Dict]:
        """Discover all custom fields or search for specific ones"""
        print("🔍 Discovering JIRA fields...")
        
        try:
            result = self.jira_client._make_request('field')
            
            # Filter fields based on search term if provided
            if search_term:
                filtered_fields = []
                search_lower = search_term.lower()
                for field in result:
                    field_name = field.get('name', '').lower()
                    field_id = field.get('id', '').lower()
                    if search_lower in field_name or search_lower in field_id:
                        filtered_fields.append(field)
                return filtered_fields
            else:
                # Return all custom fields (those starting with 'customfield_')
                return [f for f in result if f.get('id', '').startswith('customfield_')]
                
        except Exception as e:
            print(f"❌ Error discovering fields: {e}")
            return []
    
    def display_fields(self, fields: List[Dict], limit: int = 20):
        """Display fields in a formatted table"""
        if not fields:
            print("❌ No fields found matching your criteria")
            return
        
        print(f"\n📋 Found {len(fields)} field(s):")
        print("-" * 80)
        print(f"{'#':<3} {'Field ID':<20} {'Field Name':<30} {'Type':<15}")
        print("-" * 80)
        
        for i, field in enumerate(fields[:limit], 1):
            field_id = field.get('id', 'N/A')
            field_name = field.get('name', 'N/A')
            field_type = field.get('schema', {}).get('type', 'N/A')
            
            # Truncate long names
            if len(field_name) > 28:
                field_name = field_name[:25] + "..."
            
            print(f"{i:<3} {field_id:<20} {field_name:<30} {field_type:<15}")
        
        if len(fields) > limit:
            print(f"\n... and {len(fields) - limit} more fields")
            print("Use a more specific search term to narrow results")
    
    def interactive_search(self):
        """Interactive field search and configuration"""
        print("🎯 Interactive JIRA Field Discovery")
        print("=" * 50)
        
        # Test connection first
        if not self.jira_client.test_connection():
            print("❌ Cannot connect to JIRA. Please check your configuration.")
            return
        
        while True:
            print("\nOptions:")
            print("1. Search for fields by name")
            print("2. List all custom fields")
            print("3. Find specific common fields")
            print("4. Update environment configuration")
            print("0. Exit")
            
            choice = input("\nSelect an option (0-4): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self._search_by_name()
            elif choice == "2":
                self._list_all_custom_fields()
            elif choice == "3":
                self._find_common_fields()
            elif choice == "4":
                self._update_configuration()
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _search_by_name(self):
        """Search for fields by name"""
        search_term = input("Enter field name to search for: ").strip()
        if not search_term:
            print("❌ Please enter a search term")
            return
        
        fields = self.discover_fields(search_term)
        self.display_fields(fields)
        
        if fields:
            self._offer_configuration_update(fields)
    
    def _list_all_custom_fields(self):
        """List all custom fields"""
        fields = self.discover_fields()
        self.display_fields(fields, limit=30)
        
        if fields:
            self._offer_configuration_update(fields)
    
    def _find_common_fields(self):
        """Find common fields that are typically used"""
        common_fields = [
            "Story Points",
            "Epic Link",
            "Epic Name",
            "Sprint",
            "Team",
            "Fix Version/s",
            "Affects Version/s",
            "Original Estimate",
            "Remaining Estimate",
            "Time Spent",
            "Business Value",
            "Risk",
            "Acceptance Criteria"
        ]
        
        print("\n🔍 Searching for common fields...")
        found_fields = {}
        
        for field_name in common_fields:
            fields = self.discover_fields(field_name)
            if fields:
                # Find the best match (exact or closest)
                best_match = None
                for field in fields:
                    if field.get('name', '').lower() == field_name.lower():
                        best_match = field
                        break
                if not best_match and fields:
                    best_match = fields[0]  # Take first match
                
                if best_match:
                    found_fields[field_name] = best_match
        
        if found_fields:
            print(f"\n✅ Found {len(found_fields)} common fields:")
            print("-" * 60)
            for field_name, field in found_fields.items():
                print(f"• {field_name}: {field.get('id')} ({field.get('name')})")
            
            # Offer to update configuration
            if found_fields.get("Story Points"):
                update = input(f"\nUpdate JIRA_STORY_POINTS_FIELD to {found_fields['Story Points']['id']}? (y/N): ").strip().lower()
                if update == 'y':
                    self._update_env_field("JIRA_STORY_POINTS_FIELD", found_fields['Story Points']['id'])
        else:
            print("❌ No common fields found")
    
    def _offer_configuration_update(self, fields: List[Dict]):
        """Offer to update configuration with found field"""
        if not fields:
            return
        
        print(f"\nWould you like to update your .env configuration?")
        field_num = input("Enter field number (or 0 to skip): ").strip()
        
        try:
            field_idx = int(field_num) - 1
            if 0 <= field_idx < len(fields):
                selected_field = fields[field_idx]
                field_id = selected_field.get('id')
                field_name = selected_field.get('name')
                
                print(f"\nSelected: {field_name} ({field_id})")
                
                # Suggest configuration variable name
                suggested_var = self._suggest_env_var_name(field_name)
                env_var = input(f"Environment variable name (default: {suggested_var}): ").strip()
                if not env_var:
                    env_var = suggested_var
                
                self._update_env_field(env_var, field_id)
        except (ValueError, IndexError):
            if field_num != "0":
                print("❌ Invalid field number")
    
    def _suggest_env_var_name(self, field_name: str) -> str:
        """Suggest an environment variable name based on field name"""
        # Convert field name to env var format
        env_name = field_name.upper()
        env_name = re.sub(r'[^A-Z0-9]', '_', env_name)
        env_name = re.sub(r'_+', '_', env_name)
        env_name = env_name.strip('_')
        
        return f"JIRA_{env_name}_FIELD"
    
    def _update_configuration(self):
        """Update environment configuration interactively"""
        print("\n⚙️ Update Environment Configuration")
        print("-" * 40)
        
        env_var = input("Environment variable name: ").strip().upper()
        if not env_var:
            print("❌ Please enter a variable name")
            return
        
        field_value = input("Field ID or value: ").strip()
        if not field_value:
            print("❌ Please enter a field ID or value")
            return
        
        self._update_env_field(env_var, field_value)
    
    def _update_env_field(self, env_var: str, field_id: str):
        """Update a field in the .env file"""
        env_file = ".env"
        
        if not os.path.exists(env_file):
            print(f"❌ .env file not found. Please run setup first.")
            return
        
        try:
            # Read current content
            with open(env_file, 'r') as f:
                content = f.read()
            
            # Check if variable already exists
            pattern = f"^{env_var}=.*$"
            if re.search(pattern, content, re.MULTILINE):
                # Update existing variable
                content = re.sub(pattern, f"{env_var}={field_id}", content, flags=re.MULTILINE)
                action = "Updated"
            else:
                # Add new variable
                content += f"\n{env_var}={field_id}\n"
                action = "Added"
            
            # Write back to file
            with open(env_file, 'w') as f:
                f.write(content)
            
            print(f"✅ {action} {env_var}={field_id} in .env file")
            
        except Exception as e:
            print(f"❌ Error updating .env file: {e}")
    
    def quick_find(self, field_name: str):
        """Quick find for a specific field (for command line use)"""
        print(f"🔍 Searching for '{field_name}' field...")
        
        if not self.jira_client.test_connection():
            return
        
        fields = self.discover_fields(field_name)
        
        if fields:
            print(f"✅ Found {len(fields)} matching field(s):")
            self.display_fields(fields)
            
            # If exactly one match, offer to update config
            if len(fields) == 1:
                field = fields[0]
                field_id = field.get('id')
                
                # Determine environment variable name
                if field_name.lower() == "story points":
                    env_var = "JIRA_STORY_POINTS_FIELD"
                else:
                    env_var = self._suggest_env_var_name(field_name)
                
                update = input(f"\nUpdate {env_var} to {field_id}? (y/N): ").strip().lower()
                if update == 'y':
                    self._update_env_field(env_var, field_id)
        else:
            print(f"❌ No fields found matching '{field_name}'")

def main():
    """Main entry point"""
    discovery = FieldDiscovery()
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "--find":
            if len(sys.argv) > 2:
                field_name = " ".join(sys.argv[2:])
                discovery.quick_find(field_name)
            else:
                print("Usage: python field_discovery.py --find <field_name>")
        elif sys.argv[1] == "--story-points":
            # Backward compatibility - quick find for Story Points
            discovery.quick_find("Story Points")
        else:
            print("Usage:")
            print("  python field_discovery.py                    # Interactive mode")
            print("  python field_discovery.py --find <field>     # Find specific field")  
            print("  python field_discovery.py --story-points     # Quick Story Points discovery")
    else:
        # Interactive mode
        discovery.interactive_search()

if __name__ == "__main__":
    main() 