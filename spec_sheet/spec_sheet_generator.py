#!/usr/bin/env python3
"""
Enhanced Jira to Spec Sheet Sync Tool - Refactored
Simplified facade that uses modular components for better maintainability
"""

import sys
import os
from spec_sheet.spec_sheet_orchestrator import SpecSheetOrchestrator


class EnhancedSpecSheetSync:
    """Simplified facade for the spec sheet sync functionality"""
    
    def __init__(self):
        try:
            self.orchestrator = SpecSheetOrchestrator()
            print("✅ Enhanced Spec Sheet Sync initialized with modular architecture")
        except Exception as e:
            print(f"❌ Configuration error: {e}")
            sys.exit(1)
    
    def test_connections(self) -> bool:
        """Test connections to Jira and spec sheet"""
        return self.orchestrator.test_connections()
    
    def sync_all_sheets(self, selected_priorities=None):
        """Sync to all sheets - main entry point"""
        return self.orchestrator.sync_all_sheets()
    
    def get_epics_by_version_interactive(self):
        """Interactive epic selection by version - delegated to orchestrator"""
        return self.orchestrator.select_version_and_epics()
    
    def get_moscow_priorities_interactive(self):
        """Interactive MoSCoW priority selection - delegated to orchestrator"""
        return self.orchestrator.select_moscow_priorities()


def main():
    """Main entry point"""
    print("🚀 Enhanced Jira to Spec Sheet Sync Tool (Modular Architecture)")
    print("=" * 60)
    
    sync = EnhancedSpecSheetSync()
    
    # Test connections first
    if not sync.test_connections():
        print("\n❌ Connection test failed. Please check your configuration.")
        sys.exit(1)
    
    # Interactive workflow
    try:
        # Step 1: Select version/release and get epics
        if not sync.get_epics_by_version_interactive():
            print("⏹️  Epic selection cancelled or failed.")
            return
        
        # Step 2: Select MoSCoW priorities to include
        if not sync.get_moscow_priorities_interactive():
            print("⏹️  Priority selection cancelled or failed.")
            return
        
        # Step 3: Perform sync
        if sync.sync_all_sheets():
            priority_filter = (f" with {', '.join(sync.orchestrator.selected_moscow_priorities)} priorities" 
                             if len(sync.orchestrator.selected_moscow_priorities) < 4 else "")
            print(f"\n🎉 All done! Synced '{sync.orchestrator.selected_version}'{priority_filter} to your spec sheet.")
        else:
            print("\n❌ Sync failed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled.")
        return
    except Exception as e:
        print(f"\n💥 Sync failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 