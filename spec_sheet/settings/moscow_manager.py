#!/usr/bin/env python3
"""
MoSCoW Priority Manager for Spec Sheet
Handles MoSCoW priority determination and filtering
"""

from typing import Dict, List, Tuple, Any


class MoscowManager:
    """Manages MoSCoW priority determination and filtering"""
    
    def __init__(self):
        self.available_priorities = ['Must Have', 'Should Have', 'Could Have', "Won't Have"]
    
    def get_moscow_priority(self, story: Dict[str, Any]) -> str:
        """Determine MoSCoW priority from Jira story"""
        # Check labels first for explicit MoSCoW indicators (higher priority)
        labels = story.get('fields', {}).get('labels', [])
        moscow_labels = [label.lower() for label in labels]
        
        if any(label in moscow_labels for label in ['must', 'must-have']):
            return 'Must Have'
        elif any(label in moscow_labels for label in ['should', 'should-have']):
            return 'Should Have'
        elif any(label in moscow_labels for label in ['could', 'could-have']):
            return 'Could Have'
        elif any(label in moscow_labels for label in ['wont', 'wont-have', 'out-of-scope']):
            return "Won't Have"
        
        # Fall back to priority field mapping if no explicit labels
        priority = story.get('fields', {}).get('priority', {})
        if priority:
            priority_name = priority.get('name', '').lower()
            
            # Map Jira priorities to MoSCoW
            if priority_name in ['highest', 'blocker']:
                return 'Must Have'
            elif priority_name in ['high', 'major']:
                return 'Should Have'
            elif priority_name in ['medium', 'normal']:
                return 'Could Have'
            elif priority_name in ['low', 'minor', 'trivial']:
                return "Won't Have"
        
        return 'Should Have'  # Default
    
    def get_moscow_priorities_interactive(self) -> List[str]:
        """Interactive method to select which MoSCoW priorities to include"""
        print("\n📋 MoSCoW Priority Filter:")
        print("Select which priorities to include in your spec sheet:")
        print("(You can select multiple priorities)")
        print()
        
        for i, priority in enumerate(self.available_priorities, 1):
            print(f"{i}. {priority}")
        print("5. All priorities (no filter)")
        print("0. Cancel")
        
        while True:
            try:
                choice = input(f"\nEnter your selection (1-5, or comma-separated for multiple): ").strip()
                
                if choice == "0":
                    print("❌ Operation cancelled.")
                    return None
                
                if choice == "5":
                    print("📊 Including all MoSCoW priorities")
                    return self.available_priorities
                
                # Handle comma-separated choices
                choices = [int(c.strip()) for c in choice.split(',')]
                selected_priorities = []
                
                for choice_num in choices:
                    if 1 <= choice_num <= 4:
                        priority = self.available_priorities[choice_num - 1]
                        if priority not in selected_priorities:
                            selected_priorities.append(priority)
                    else:
                        print(f"❌ Invalid choice: {choice_num}. Please select 1-5.")
                        break
                else:
                    # All choices were valid
                    if selected_priorities:
                        print(f"📊 Selected priorities: {', '.join(selected_priorities)}")
                        return selected_priorities
                    else:
                        print("❌ No priorities selected. Please select at least one.")
                
            except ValueError:
                print("❌ Please enter valid numbers separated by commas.")
            except KeyboardInterrupt:
                print("\n⏹️  Selection cancelled. Using all priorities.")
                return self.available_priorities
    
    def filter_stories_by_moscow(self, stories: List[Dict[str, Any]], 
                                selected_priorities: List[str]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        """Filter stories based on selected MoSCoW priorities"""
        if not selected_priorities:
            return stories, {}
        
        filtered_stories = []
        priority_counts = {priority: 0 for priority in self.available_priorities}
        filtered_counts = {priority: 0 for priority in selected_priorities}
        
        for story in stories:
            moscow_priority = self.get_moscow_priority(story)
            priority_counts[moscow_priority] += 1
            
            if moscow_priority in selected_priorities:
                filtered_stories.append(story)
                filtered_counts[moscow_priority] += 1
        
        # Report filtering results
        total_stories = len(stories)
        filtered_total = len(filtered_stories)
        
        if filtered_total < total_stories:
            print(f"   🔍 Filtered: {filtered_total}/{total_stories} stories match selected priorities")
            for priority in selected_priorities:
                if filtered_counts[priority] > 0:
                    print(f"      - {priority}: {filtered_counts[priority]} stories")
        
        return filtered_stories, priority_counts 