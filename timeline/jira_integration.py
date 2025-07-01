#!/usr/bin/env python3
"""
JIRA Integration Handler
Handles JIRA connection setup and availability checking
"""

from typing import Tuple, Optional
from utils.config import JiraConfig
from utils.jira_client import JiraClient


class JiraIntegration:
    """Handles JIRA integration for timeline generation"""
    
    def __init__(self):
        self.jira_config: Optional[JiraConfig] = None
        self.jira_client: Optional[JiraClient] = None
        self.jira_available: bool = False
        self._setup_jira_connection()
    
    def _setup_jira_connection(self):
        """Try to establish JIRA connection"""
        try:
            self.jira_config = JiraConfig()
            self.jira_client = JiraClient(self.jira_config)
            self.jira_available = True
            print("✅ JIRA integration available")
        except Exception as e:
            self.jira_available = False
            print("⚠️  JIRA not available - timeline will work without JIRA integration")
    
    def is_available(self) -> bool:
        """Check if JIRA integration is available"""
        return self.jira_available
    
    def get_jira_client(self) -> Optional[JiraClient]:
        """Get the JIRA client if available"""
        return self.jira_client if self.jira_available else None
    
    def get_jira_config(self) -> Optional[JiraConfig]:
        """Get the JIRA config if available"""
        return self.jira_config if self.jira_available else None 