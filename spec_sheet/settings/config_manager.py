#!/usr/bin/env python3
"""
Configuration Manager for Spec Sheet
Handles loading and managing settings and Definition of Done configurations
"""

import json
import os
from typing import Dict, Any


class ConfigManager:
    """Manages settings and DOD configuration loading"""
    
    def __init__(self, settings_config_path: str = "settings_config.json", 
                 dod_config_path: str = "dod_config.json"):
        self.settings_config_path = settings_config_path
        self.dod_config_path = dod_config_path
        self.settings_config = self._load_settings_config()
        self.dod_config = self._load_dod_config()
    
    def _load_settings_config(self) -> Dict[str, Any]:
        """Load settings configuration from JSON file"""
        try:
            if os.path.exists(self.settings_config_path):
                with open(self.settings_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✅ Loaded settings configuration from {self.settings_config_path}")
                return config
            else:
                print(f"⚠️  Settings config file not found at {self.settings_config_path}, using defaults")
                return self._get_default_settings_config()
        except Exception as e:
            print(f"❌ Error loading settings config: {e}, using defaults")
            return self._get_default_settings_config()
    
    def _get_default_settings_config(self) -> Dict[str, Any]:
        """Get default settings configuration if file doesn't exist"""
        return {
            "description": "Default settings configuration",
            "version": "1.0",
            "pricing": {
                "base_story_point_price": 130,
                "experimental_variance": 0.3,
                "base_hourly_rate": 127.16,
                "hourly_rate_discount": 0.25
            },
            "sprint_planning": {
                "default_sprint_length_weeks": 2,
                "sprint_overhead_percentage": 0.15,
                "working_days_per_week": 5,
                "hours_per_story_point": 8
            },
            "team_defaults": {
                "default_hourly_rate": 95.37,
                "senior_developer_velocity": 8,
                "mid_developer_velocity": 6,
                "junior_developer_velocity": 5,
                "tech_lead_velocity": 10,
                "designer_velocity": 6,
                "qa_engineer_velocity": 4,
                "devops_engineer_velocity": 7
            },
            "risk_assessment": {
                "proven_threshold_story_points": 3,
                "experimental_threshold_story_points": 8,
                "risk_priority": {
                    "proven": 1,
                    "experimental": 2,
                    "dependant": 3,
                    "dependent": 3
                }
            },
            "recommendations": {
                "large_project_threshold": 100,
                "small_project_threshold": 20,
                "significant_sprints_saved_threshold": 4,
                "high_experimental_percentage": 30,
                "significant_dependent_percentage": 20
            },
            "ui_formatting": {
                "header_color": "366092",
                "summary_header_color": "366092",
                "epic_background_color": "E6F3FF",
                "section_background_color": "D4EDDA",
                "default_column_widths": [50, 20, 20, 30, 15, 12, 15, 12, 12, 15, 20],
                "header_row_height": 80
            }
        }
    
    def _load_dod_config(self) -> Dict[str, Any]:
        """Load Definition of Done configuration from JSON file"""
        try:
            if os.path.exists(self.dod_config_path):
                with open(self.dod_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✅ Loaded DoD configuration from {self.dod_config_path}")
                return config
            else:
                print(f"⚠️  DoD config file not found at {self.dod_config_path}, using defaults")
                return self._get_default_dod_config()
        except Exception as e:
            print(f"❌ Error loading DoD config: {e}, using defaults")
            return self._get_default_dod_config()
    
    def _get_default_dod_config(self) -> Dict[str, Any]:
        """Get default DoD configuration if file doesn't exist"""
        return {
            "description": "Default Definition of Done configuration",
            "version": "1.0",
            "categories": [
                {
                    "name": "Code quality & documentation",
                    "items": [
                        {
                            "description": "Code is structured, modular, and follows best practices",
                            "moscow": "Must Have",
                            "impact_points": "8",
                            "impact_percentage": 0.04
                        },
                        {
                            "description": "Code is reviewed and approved via pull requests",
                            "moscow": "Must Have",
                            "impact_points": "5",
                            "impact_percentage": 0.03
                        }
                    ]
                },
                {
                    "name": "Performance & optimization",
                    "items": [
                        {
                            "description": "Performance is optimized for production use",
                            "moscow": "Should Have",
                            "impact_points": "13",
                            "impact_percentage": 0.07
                        }
                    ]
                }
            ]
        }
    
    def get_dod_impacts(self) -> Dict[str, float]:
        """Get DoD impacts from loaded configuration"""
        dod_impacts = {}
        
        for category in self.dod_config.get('categories', []):
            for item in category.get('items', []):
                description = item.get('description', '')
                impact_percentage = item.get('impact_percentage', 0.0)
                
                # Create a clean key from the description
                clean_key = description.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace('-', '_').replace('&', 'and')
                dod_impacts[clean_key] = impact_percentage
        
        print(f"📋 Loaded {len(dod_impacts)} DoD impacts from configuration")
        return dod_impacts
    
    def calculate_dod_impact_total(self) -> float:
        """Calculate total DoD impact from all loaded DoD impacts"""
        dod_impacts = self.get_dod_impacts()
        
        if not dod_impacts:
            print("⚠️  No DoD impacts loaded, using 0% impact")
            return 0.0
        
        total_impact = sum(dod_impacts.values())
        print(f"📊 Calculated total DoD impact: {total_impact:.1%} ({total_impact:.3f})")
        return total_impact
    
    def get_hourly_rate(self) -> float:
        """Calculate hourly rate dynamically from configuration"""
        pricing_config = self.settings_config["pricing"]
        return pricing_config["base_hourly_rate"] * (1 - pricing_config["hourly_rate_discount"]) 