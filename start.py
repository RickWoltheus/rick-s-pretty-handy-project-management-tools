#!/usr/bin/env python3
"""
Jira Spec Sheet Sync - Main Menu
Interactive menu system to run various tools in the project
"""

import os
import sys
import subprocess
from typing import Dict, List, Callable

class MenuSystem:
    """Interactive menu system for running project tools"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.running = True
    
    def _initialize_tools(self) -> Dict[str, Dict]:
        """Initialize available tools and their configurations"""
        return {
            "1": {
                "name": "🚀 Enhanced Spec Sheet Generator",
                "description": "Generate sophisticated spec sheets with risk-based pricing and sprint planning",
                "script": "spec-sheet/spec-sheet-generator.py",
                "function": self._run_spec_sheet_generator
            },
            "2": {
                "name": "📊 Basic JIRA Sync",
                "description": "Simple sync of JIRA epics and stories to spreadsheet",
                "script": "jira_sync.py",
                "function": self._run_basic_sync
            },
            "3": {
                "name": "🔍 Validate JIRA Setup",
                "description": "Check JIRA configuration and field mappings",
                "script": "utils/validate_jira_setup.py",
                "function": self._run_validation
            },
            "4": {
                "name": "⚙️  Setup & Configuration",
                "description": "Configure JIRA connection and environment settings",
                "script": "setup.py",
                "function": self._run_setup
                        },
            "5": {
                "name": "📝 View Configuration",
                "description": "Display current environment configuration",
                "script": None,
                "function": self._show_config
            },
            "6": {
                "name": "📚 Show Documentation", 
                "description": "Display helpful guides and documentation",
                "script": None,
                "function": self._show_documentation
            },
            "7": {
                "name": "👥 Team Management",
                "description": "Create and manage team members with persistent holiday storage",
                "script": "team/team_manager.py",
                "function": self._run_team_management
            },
            "8": {
                "name": "📅 Enhanced Timeline Generator",
                "description": "Generate project timelines with team integration and visual absences",
                "script": "timeline/enhanced_timeline_generator.py",
                "function": self._run_enhanced_timeline
            },
            "9": {
                "name": "📅 Timeline & Calendar Generator (Legacy)",
                "description": "Original timeline generator with manual team setup",
                "script": "timeline/timeline_generator.py",
                "function": self._run_timeline_generator
            },
            "10": {
                "name": "🎬 Timeline Demo",
                "description": "Demo the timeline generator with pre-configured example",
                "script": "timeline/demo_timeline.py", 
                "function": self._run_timeline_demo
            },
            "11": {
                "name": "🧪 Run Tests",
                "description": "Execute the test suite to verify functionality",
                "script": "run_tests.py",
                "function": self._run_tests
            }
        }
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 70)
        print("🎯 JIRA SPEC SHEET SYNC - MAIN MENU")
        print("=" * 70)
        
        for key, tool in self.tools.items():
            print(f"{key}. {tool['name']}")
            print(f"   {tool['description']}")
            print()
        
        print("0. 🚪 Exit")
        print("=" * 70)
    
    def get_user_choice(self) -> str:
        """Get user's menu choice"""
        while True:
            choice = input("Select an option (0-11): ").strip()
            if choice in list(self.tools.keys()) + ["0"]:
                return choice
            print("❌ Invalid choice. Please select a valid option.")
    
    def run_tool(self, choice: str):
        """Run the selected tool"""
        if choice == "0":
            self.running = False
            print("👋 Goodbye!")
            return
        
        tool = self.tools[choice]
        print(f"\n🔄 Running: {tool['name']}")
        print("-" * 50)
        
        try:
            tool['function']()
        except KeyboardInterrupt:
            print("\n⏹️  Tool interrupted by user")
        except Exception as e:
            print(f"\n❌ Error running tool: {e}")
        
        input("\nPress Enter to return to main menu...")
    
    def _run_spec_sheet_generator(self):
        """Run the enhanced spec sheet generator"""
        if not self._check_file_exists("spec-sheet/spec-sheet-generator.py"):
            return
        
        print("Starting Enhanced Spec Sheet Generator...")
        print("This tool provides:")
        print("• Risk-based pricing (Proven/Experimental/Dependent)")
        print("• Sprint planning and team composition analysis")
        print("• DoD impact calculations")
        print("• MoSCoW prioritization")
        print()
        
        # Run from parent directory with full path to avoid import issues
        script_path = os.path.join("spec-sheet", "spec-sheet-generator.py")
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()  # Ensure current directory is in Python path
        
        subprocess.run([sys.executable, script_path], env=env, check=True)
    
    def _run_basic_sync(self):
        """Run basic JIRA sync"""
        if not self._check_file_exists("jira_sync.py"):
            return
        
        print("Starting Basic JIRA Sync...")
        print("This will create a simple spreadsheet with:")
        print("• Epic and story hierarchy")
        print("• Story points")
        print("• Basic cost calculations")
        print()
        
        subprocess.run([sys.executable, "jira_sync.py"], check=True)
    
    def _run_validation(self):
        """Run JIRA setup validation"""
        if not self._check_file_exists("utils/validate_jira_setup.py"):
            return
        
        print("Starting JIRA Setup Validation...")
        print("This will check:")
        print("• JIRA connection")
        print("• Story Points field configuration")
        print("• Epic and story data")
        print("• Label configurations")
        print()
        
        subprocess.run([sys.executable, "utils/validate_jira_setup.py"], check=True)
    
    def _run_setup(self):
        """Run setup wizard"""
        if not self._check_file_exists("setup.py"):
            return
        
        print("Starting Setup Wizard...")
        print("This will help you:")
        print("• Create/update .env configuration")
        print("• Test JIRA connection")
        print("• Find Story Points field ID")
        print()
        
        subprocess.run([sys.executable, "setup.py"], check=True)
    

    
    def _run_timeline_generator(self):
        """Run the timeline and calendar generator"""
        if not self._check_file_exists("timeline/timeline_generator.py"):
            return
        
        print("Starting Timeline & Calendar Generator...")
        print("This tool provides:")
        print("• Project timeline generation from specified dates")
        print("• Team member capacity planning with FTE and skills")
        print("• Dutch national holiday integration (via API)")
        print("• Custom holiday management (company and personal)")
        print("• Sprint planning with realistic capacity calculations")
        print("• Calendar views with availability tracking")
        print("• Excel workbook output with multiple sheets")
        print()
        
        # Run from timeline directory with full path
        script_path = os.path.join("timeline", "timeline_generator.py")
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        subprocess.run([sys.executable, script_path], env=env, check=True)
    
    def _run_team_management(self):
        """Run the team management system"""
        if not self._check_file_exists("team/team_manager.py"):
            return
        
        print("Starting Team Management System...")
        print("This tool provides:")
        print("• Create and manage team members with persistent storage")
        print("• Define individual availability and roles")
        print("• Manage personal and company-wide holidays")
        print("• Set story points capacity per team member")
        print("• Store team data in JSON files for reuse")
        print()
        
        # Run from team directory with full path
        script_path = os.path.join("team", "team_manager.py")
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        subprocess.run([sys.executable, script_path], env=env, check=True)
    
    def _run_enhanced_timeline(self):
        """Run the enhanced timeline generator with team integration"""
        if not self._check_file_exists("timeline/enhanced_timeline_generator.py"):
            return
        
        print("Starting Enhanced Timeline Generator...")
        print("This tool provides:")
        print("• Loads team members from persistent storage")
        print("• Visual representation of team absences")
        print("• Daily capacity calculations with real team data")
        print("• Enhanced Excel output showing who's away when")
        print("• Project estimation based on actual team composition")
        print("• Holiday management integrated with team members")
        print()
        
        # Check if team members exist
        team_folder = "team"
        if not os.path.exists(team_folder) or not os.listdir(team_folder):
            print("⚠️ No team members found!")
            print("💡 Please create team members first using option 7 (Team Management)")
            input("\nPress Enter to continue...")
            return
        
        # Run from timeline directory with full path
        script_path = os.path.join("timeline", "enhanced_timeline_generator.py")
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        subprocess.run([sys.executable, script_path], env=env, check=True)
    
    def _run_timeline_demo(self):
        """Run the timeline demo with pre-configured settings"""
        if not self._check_file_exists("timeline/demo_timeline.py"):
            return
        
        print("Starting Timeline Demo...")
        print("This demo shows:")
        print("• Pre-configured team of 4 members with different roles/skills")
        print("• Dutch holiday integration for current and next year")
        print("• Custom company holidays and personal time off")
        print("• Realistic capacity calculations and sprint planning")
        print("• Generated Excel workbook with timeline analysis")
        print("• No user interaction required - runs automatically")
        print()
        
        # Run from timeline directory with full path
        script_path = os.path.join("timeline", "demo_timeline.py")
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        subprocess.run([sys.executable, script_path], env=env, check=True)
    
    def _show_config(self):
        """Display current configuration"""
        print("Current Configuration:")
        print("-" * 30)
        
        env_file = ".env"
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                
                # Filter out comments and empty lines, hide sensitive data
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, _, value = line.partition('=')
                        # Hide sensitive information
                        if any(sensitive in key.upper() for sensitive in ['TOKEN', 'PASSWORD', 'SECRET']):
                            print(f"{key}=***hidden***")
                        else:
                            print(f"{key}={value}")
            except Exception as e:
                print(f"❌ Error reading .env file: {e}")
        else:
            print("❌ No .env file found. Run Setup & Configuration first.")
        
        # Show available files
        print(f"\nAvailable Files:")
        print(f"• .env file: {'✅' if os.path.exists('.env') else '❌'}")
        print(f"• Spec sheet: {'✅' if os.path.exists('spec-sheet/spec-sheet.xlsx') else '❌'}")
        print(f"• Requirements: {'✅' if os.path.exists('requirements.txt') else '❌'}")
    
    def _show_documentation(self):
        """Show available documentation"""
        docs = {
            "README.md": "Main project documentation",
            "JIRA_MAPPING_GUIDE.md": "Guide for configuring JIRA field mappings",
            "SPRINT_PLANNING_GUIDE.md": "Sprint planning and team composition guide",
            "timeline/TIMELINE_GUIDE.md": "Timeline and calendar management guide",
            "env_template.txt": "Environment configuration template"
        }
        
        print("Available Documentation:")
        print("-" * 30)
        
        for doc, description in docs.items():
            exists = "✅" if os.path.exists(doc) else "❌"
            print(f"{exists} {doc}")
            print(f"   {description}")
            
            if os.path.exists(doc):
                view = input(f"   View {doc}? (y/N): ").strip().lower()
                if view == 'y':
                    self._display_file_content(doc)
            print()
    
    def _run_tests(self):
        """Run the test suite"""
        if not self._check_file_exists("run_tests.py"):
            return
        
        print("Starting Test Suite...")
        print("This will:")
        print("• Run unit tests for core functionality")
        print("• Test JIRA client with mock data")
        print("• Validate spec sheet generation")
        print("• Check sprint planning calculations")
        print()
        
        # Ask user what type of tests to run
        print("Test Options:")
        print("1. Run all tests")
        print("2. Run only unit tests")
        print("3. Run with coverage report")
        print("4. Run specific test file")
        print("0. Cancel")
        
        choice = input("Select test option (0-4): ").strip()
        
        if choice == "0":
            print("Test cancelled.")
            return
        elif choice == "1":
            # Run all tests
            subprocess.run([sys.executable, "run_tests.py", "--verbose"], check=True)
        elif choice == "2":
            # Run unit tests only
            subprocess.run([sys.executable, "run_tests.py", "--unit", "--verbose"], check=True)
        elif choice == "3":
            # Run with coverage
            subprocess.run([sys.executable, "run_tests.py", "--coverage", "--verbose"], check=True)
        elif choice == "4":
            # Run specific file
            test_files = [
                "test_spec_sheet_generator.py",
                "test_jira_client.py"
            ]
            print("\nAvailable test files:")
            for i, file in enumerate(test_files, 1):
                print(f"{i}. {file}")
            
            file_choice = input("Select test file (1-2): ").strip()
            if file_choice in ["1", "2"]:
                selected_file = test_files[int(file_choice) - 1]
                subprocess.run([sys.executable, "run_tests.py", "--file", selected_file, "--verbose"], check=True)
            else:
                print("Invalid file selection.")
        else:
            print("Invalid choice.")
    
    def _display_file_content(self, filename: str):
        """Display file content with pagination"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            page_size = 30
            
            for i in range(0, len(lines), page_size):
                page_lines = lines[i:i + page_size]
                print('\n'.join(page_lines))
                
                if i + page_size < len(lines):
                    cont = input("\n--- Press Enter for more, 'q' to quit ---")
                    if cont.lower() == 'q':
                        break
                print()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    def _check_file_exists(self, filepath: str) -> bool:
        """Check if required file exists"""
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            print("Please ensure all project files are present.")
            return False
        return True
    
    def run(self):
        """Main menu loop"""
        print("🎯 Welcome to Jira Spec Sheet Sync!")
        
        # Quick environment check
        if not os.path.exists('.env'):
            print("\n⚠️  No .env file found. You may want to run Setup & Configuration first.")
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                self.run_tool(choice)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("Press Enter to continue...")

def main():
    """Main entry point"""
    # Change to script directory to ensure relative paths work
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    menu = MenuSystem()
    menu.run()

if __name__ == "__main__":
    main() 