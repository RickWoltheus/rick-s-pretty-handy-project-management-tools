#!/usr/bin/env python3
"""
Jira Setup Validation Tool
Checks if all required fields and configurations are properly set up for the enhanced sync
"""

import sys
from collections import defaultdict
from config import JiraConfig
from jira_client import JiraClient

class JiraSetupValidator:
    """Validates Jira setup for optimal sync performance"""
    
    def __init__(self):
        try:
            self.jira_config = JiraConfig()
            self.jira_client = JiraClient(self.jira_config)
            self.validation_results = {
                'connection': False,
                'story_points_field': False,
                'epics_exist': False,
                'stories_exist': False,
                'epic_story_linking': False,
                'risk_labels': False,
                'moscow_labels': False,
                'recommendations': []
            }
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("🔍 Jira Setup Validation")
        print("=" * 60)
        
        # Test connection
        if not self._validate_connection():
            print("❌ Cannot proceed without valid Jira connection")
            return False
        
        # Validate story points field
        self._validate_story_points_field()
        
        # Validate issue types and data
        epics = self._validate_epics()
        stories = self._validate_stories()
        
        # Validate epic-story linking
        if epics and stories:
            self._validate_epic_story_linking(epics)
        
        # Validate labels
        self._validate_risk_labels(stories)
        self._validate_moscow_labels(stories)
        
        # Generate recommendations
        self._generate_recommendations()
        
        # Print summary
        self._print_validation_summary()
        
        return True
    
    def _validate_connection(self):
        """Test Jira connection"""
        print("\n🔗 Testing Jira Connection...")
        
        if self.jira_client.test_connection():
            self.validation_results['connection'] = True
            return True
        else:
            return False
    
    def _validate_story_points_field(self):
        """Validate story points custom field"""
        print("\n📊 Validating Story Points Field...")
        
        try:
            # Try to find the story points field
            field_id = self.jira_client.get_custom_field_id("Story Points")
            if field_id:
                print(f"✅ Story Points field found: {field_id}")
                if field_id == self.jira_config.story_points_field:
                    print("✅ Configuration matches discovered field")
                    self.validation_results['story_points_field'] = True
                else:
                    print(f"⚠️  Configuration mismatch!")
                    print(f"   Configured: {self.jira_config.story_points_field}")
                    print(f"   Discovered: {field_id}")
                    self.validation_results['recommendations'].append(
                        f"Update JIRA_STORY_POINTS_FIELD in .env to: {field_id}"
                    )
            else:
                print("❌ Story Points field not found")
                self.validation_results['recommendations'].append(
                    "Create a 'Story Points' custom field in Jira"
                )
                
                # Try to list all custom fields
                print("📋 Available custom fields:")
                result = self.jira_client._make_request('field')
                custom_fields = [f for f in result if f.get('id', '').startswith('customfield_')]
                for field in custom_fields[:10]:  # Show first 10
                    print(f"   {field.get('id')}: {field.get('name')}")
                if len(custom_fields) > 10:
                    print(f"   ... and {len(custom_fields) - 10} more")
        except Exception as e:
            print(f"❌ Error validating story points field: {e}")
    
    def _validate_epics(self):
        """Validate epics exist in project"""
        print("\n🎯 Validating Epics...")
        
        try:
            epics = self.jira_client.get_epics()
            if epics:
                print(f"✅ Found {len(epics)} epics")
                self.validation_results['epics_exist'] = True
                
                # Show epic details
                for epic in epics[:5]:  # Show first 5
                    key = epic['key']
                    summary = epic['fields']['summary']
                    print(f"   📋 {key}: {summary[:50]}...")
                
                if len(epics) > 5:
                    print(f"   ... and {len(epics) - 5} more epics")
                
                return epics
            else:
                print("⚠️  No epics found in project")
                self.validation_results['recommendations'].append(
                    "Create some epics in your Jira project to organize stories"
                )
                return []
        except Exception as e:
            print(f"❌ Error validating epics: {e}")
            return []
    
    def _validate_stories(self):
        """Validate stories exist in project"""
        print("\n📝 Validating Stories...")
        
        try:
            # Search for all stories in the project
            jql = f'project = {self.jira_config.project_key} AND issuetype = Story'
            params = {
                'jql': jql,
                'fields': f'summary,labels,priority,{self.jira_config.story_points_field},customfield_10273',
                'maxResults': 100
            }
            
            result = self.jira_client._make_request('search', params)
            stories = result.get('issues', [])
            
            if stories:
                print(f"✅ Found {len(stories)} stories")
                self.validation_results['stories_exist'] = True
                
                # Analyze story points
                stories_with_points = 0
                total_points = 0
                
                for story in stories:
                    story_points = self.jira_client.get_story_points(story)
                    if story_points:
                        stories_with_points += 1
                        total_points += story_points
                
                print(f"   📊 {stories_with_points}/{len(stories)} stories have story points")
                if stories_with_points > 0:
                    avg_points = total_points / stories_with_points
                    print(f"   📈 Average story points: {avg_points:.1f}")
                
                if stories_with_points < len(stories):
                    missing_points = len(stories) - stories_with_points
                    self.validation_results['recommendations'].append(
                        f"Add story points to {missing_points} stories for accurate pricing"
                    )
                
                return stories
            else:
                print("⚠️  No stories found in project")
                self.validation_results['recommendations'].append(
                    "Create some stories in your Jira project"
                )
                return []
        except Exception as e:
            print(f"❌ Error validating stories: {e}")
            return []
    
    def _validate_epic_story_linking(self, epics):
        """Validate epic-story linking"""
        print("\n🔗 Validating Epic-Story Linking...")
        
        linked_stories = 0
        total_epics_with_stories = 0
        
        for epic in epics:
            epic_key = epic['key']
            epic_summary = epic['fields']['summary']
            
            stories = self.jira_client.get_stories_for_epic(epic_key)
            if stories:
                linked_stories += len(stories)
                total_epics_with_stories += 1
                print(f"   📋 {epic_key}: {len(stories)} stories")
            else:
                print(f"   ⚠️  {epic_key}: No linked stories")
        
        if linked_stories > 0:
            print(f"✅ Found {linked_stories} stories linked to {total_epics_with_stories} epics")
            self.validation_results['epic_story_linking'] = True
        else:
            print("❌ No epic-story linking found")
            self.validation_results['recommendations'].extend([
                "Link your stories to epics using Epic Link field",
                "Or use the new Jira hierarchy (parent-child relationships)"
            ])
    
    def _validate_risk_labels(self, stories):
        """Validate Type of work field and risk profile configuration"""
        print("\n🏷️  Validating Type of Work Field...")
        
        type_of_work_field = "customfield_10273"  # Type of work field
        stories_with_type_of_work = 0
        work_type_usage = defaultdict(int)
        
        for story in stories:
            type_of_work_value = story.get('fields', {}).get(type_of_work_field)
            
            if type_of_work_value:
                stories_with_type_of_work += 1
                
                # Handle different field formats
                if isinstance(type_of_work_value, list):
                    work_types = [item.get('value', '') for item in type_of_work_value]
                elif isinstance(type_of_work_value, dict):
                    work_types = [type_of_work_value.get('value', '')]
                else:
                    work_types = [str(type_of_work_value)]
                
                for work_type in work_types:
                    if work_type:
                        work_type_usage[work_type] += 1
        
        if stories_with_type_of_work > 0:
            print(f"✅ {stories_with_type_of_work}/{len(stories)} stories have 'Type of work' field")
            self.validation_results['risk_labels'] = True
            
            print("   📊 Type of work usage:")
            for work_type, count in sorted(work_type_usage.items()):
                print(f"      {work_type}: {count} stories")
                
            print("   🏷️  Priority system: Dependant > Experimental > Proven")
        else:
            print("⚠️  No 'Type of work' field values found")
            print("   💡 Will fall back to story points for risk assessment:")
            print("      ≤ 3 pts → Proven (Fixed price)")
            print("      4-8 pts → Experimental (Range price)")
            print("      > 8 pts → Dependant (Hourly estimate)")
            
            self.validation_results['recommendations'].append(
                "Set 'Type of work' field values: Proven, Experimental, or Dependant"
            )
        
        # Also check for legacy risk labels
        risk_labels = ['proven', 'experimental', 'dependant', 'low-risk', 'moderate-risk', 'high-risk']
        stories_with_risk_labels = 0
        
        for story in stories:
            story_labels = [label.lower() for label in story.get('fields', {}).get('labels', [])]
            has_risk_label = any(label in risk_labels for label in story_labels)
            if has_risk_label:
                stories_with_risk_labels += 1
        
        if stories_with_risk_labels > 0:
            print(f"   📋 Note: {stories_with_risk_labels} stories also have legacy risk labels (will be ignored)")
    
    def _validate_moscow_labels(self, stories):
        """Validate MoSCoW priority labels"""
        print("\n🎯 Validating MoSCoW Priority Labels...")
        
        moscow_labels = ['must-have', 'should-have', 'could-have', 'wont-have', 'must', 'should', 'could', 'wont']
        stories_with_moscow_labels = 0
        priority_usage = defaultdict(int)
        
        for story in stories:
            story_labels = [label.lower() for label in story.get('fields', {}).get('labels', [])]
            has_moscow_label = any(label in moscow_labels for label in story_labels)
            
            if has_moscow_label:
                stories_with_moscow_labels += 1
                for label in story_labels:
                    if label in moscow_labels:
                        priority_usage[label] += 1
            
            # Also check Jira priority field
            priority = story.get('fields', {}).get('priority', {})
            if priority:
                priority_name = priority.get('name', '').lower()
                priority_usage[f"priority:{priority_name}"] += 1
        
        if stories_with_moscow_labels > 0:
            print(f"✅ {stories_with_moscow_labels}/{len(stories)} stories have MoSCoW labels")
            self.validation_results['moscow_labels'] = True
        else:
            print("⚠️  No MoSCoW labels found")
            print("   💡 Will use Jira priority field for MoSCoW mapping")
        
        if priority_usage:
            print("   📊 Priority/Label usage:")
            for priority, count in sorted(priority_usage.items()):
                print(f"      {priority}: {count} stories")
    
    def _generate_recommendations(self):
        """Generate setup recommendations"""
        print("\n💡 Setup Recommendations...")
        
        if not self.validation_results['recommendations']:
            print("✅ No recommendations - your setup looks good!")
            return
        
        for i, recommendation in enumerate(self.validation_results['recommendations'], 1):
            print(f"{i}. {recommendation}")
    
    def _print_validation_summary(self):
        """Print validation summary"""
        print("\n📋 Validation Summary")
        print("=" * 40)
        
        total_checks = len([k for k in self.validation_results.keys() if k != 'recommendations'])
        passed_checks = sum(1 for k, v in self.validation_results.items() if k != 'recommendations' and v)
        
        print(f"Overall Score: {passed_checks}/{total_checks} checks passed")
        
        status_icons = {True: "✅", False: "❌"}
        
        print(f"{status_icons[self.validation_results['connection']]} Jira Connection")
        print(f"{status_icons[self.validation_results['story_points_field']]} Story Points Field")
        print(f"{status_icons[self.validation_results['epics_exist']]} Epics Exist")
        print(f"{status_icons[self.validation_results['stories_exist']]} Stories Exist")
        print(f"{status_icons[self.validation_results['epic_story_linking']]} Epic-Story Linking")
        print(f"{status_icons[self.validation_results['risk_labels']]} Risk Profile Labels")
        print(f"{status_icons[self.validation_results['moscow_labels']]} MoSCoW Labels")
        
        if passed_checks == total_checks:
            print("\n🎉 Perfect setup! Your Jira is ready for enhanced sync.")
        elif passed_checks >= 4:
            print("\n👍 Good setup! The sync will work, but follow recommendations for optimal results.")
        else:
            print("\n⚠️  Setup needs work. Address the issues above before running sync.")

def main():
    """Main entry point"""
    validator = JiraSetupValidator()
    validator.run_full_validation()

if __name__ == "__main__":
    main() 