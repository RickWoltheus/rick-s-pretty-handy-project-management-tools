#!/usr/bin/env python3
"""
Setup script for Jira to Spreadsheet Sync Tool
Helps users configure their environment
"""

import os
import sys
import shutil

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        response = input(".env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    try:
        shutil.copy('env_template.txt', '.env')
        print("✅ Created .env file from template")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def get_user_input():
    """Get configuration from user"""
    print("\n🔧 Let's configure your Jira connection:")
    print("=" * 50)
    
    config = {}
    
    # Jira Domain
    config['JIRA_DOMAIN'] = input("Enter your Jira domain (e.g., https://company.atlassian.net): ").strip()
    if not config['JIRA_DOMAIN'].startswith('http'):
        config['JIRA_DOMAIN'] = f"https://{config['JIRA_DOMAIN']}"
    
    # Email
    config['JIRA_EMAIL'] = input("Enter your Jira email: ").strip()
    
    # API Token
    print("\n📝 You'll need to create a Jira API token:")
    print("   1. Go to https://id.atlassian.com/manage-profile/security/api-tokens")
    print("   2. Click 'Create API token'")
    print("   3. Copy the generated token")
    config['JIRA_API_TOKEN'] = input("Enter your Jira API token: ").strip()
    
    # Project Key
    config['JIRA_PROJECT_KEY'] = input("Enter your Jira project key (e.g., PROJ): ").strip().upper()
    
    # Cost per story point
    cost_input = input("Enter cost per story point (default: 100): ").strip()
    config['COST_PER_STORY_POINT'] = cost_input if cost_input else "100"
    
    # Spreadsheet name
    excel_name = input("Enter spreadsheet filename (default: jira_cost_estimation.xlsx): ").strip()
    config['EXCEL_PATH'] = excel_name if excel_name else "jira_cost_estimation.xlsx"
    
    return config

def update_env_file(config):
    """Update .env file with user configuration"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace placeholders with actual values
        for key, value in config.items():
            # Find the line with this key and replace the value
            import re
            pattern = f"^{key}=.*$"
            replacement = f"{key}={value}"
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Updated .env file with your configuration")
        return True
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ('requests', 'requests'),
        ('openpyxl', 'openpyxl'),
        ('pandas', 'pandas'),
        ('python-dotenv', 'dotenv')
    ]
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed")
        return True

def test_configuration():
    """Test the Jira connection"""
    print("\n🔍 Testing Jira connection...")
    
    try:
        from config import JiraConfig
        from jira_client import JiraClient
        
        config = JiraConfig()
        client = JiraClient(config)
        
        if client.test_connection():
            print("✅ Jira connection successful!")
            
            # Try to find story points field
            print("\n🔍 Looking for Story Points field...")
            field_id = client.get_custom_field_id("Story Points")
            if field_id:
                print(f"✅ Found Story Points field: {field_id}")
                
                # Update .env with the correct field ID
                with open('.env', 'r') as f:
                    content = f.read()
                
                import re
                content = re.sub(
                    r'^JIRA_STORY_POINTS_FIELD=.*$',
                    f'JIRA_STORY_POINTS_FIELD={field_id}',
                    content,
                    flags=re.MULTILINE
                )
                
                with open('.env', 'w') as f:
                    f.write(content)
                
                print("✅ Updated .env with correct Story Points field ID")
            else:
                print("⚠️  Could not find Story Points field. You may need to create it in Jira or update the field ID manually.")
            
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Jira to Spreadsheet Sync - Setup Wizard")
    print("=" * 60)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies first:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Step 3: Get user configuration
    config = get_user_input()
    
    # Step 4: Update .env file
    if not update_env_file(config):
        sys.exit(1)
    
    # Step 5: Test configuration
    if test_configuration():
        print("\n🎉 Setup completed successfully!")
        print("\nYou can now run the sync with:")
        print("python jira_sync.py")
    else:
        print("\n⚠️  Setup completed but connection test failed.")
        print("Please check your configuration in .env and try again.")

if __name__ == "__main__":
    main() 