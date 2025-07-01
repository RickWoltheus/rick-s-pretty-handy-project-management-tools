#!/usr/bin/env python3
"""
Pricing Engine for Spec Sheet
Handles cost calculations based on risk profiles and story points
"""

from typing import Dict, Any
from spec_sheet.settings.config_manager import ConfigManager


class PricingEngine:
    """Handles price calculations based on risk profiles and configurations"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.settings_config = config_manager.settings_config
        self.base_story_point_price = self.settings_config["pricing"]["base_story_point_price"]
        self.experimental_variance = self.settings_config["pricing"]["experimental_variance"]
        self.hourly_rate = config_manager.get_hourly_rate()
        self.dod_impact_total = config_manager.calculate_dod_impact_total()
    
    def calculate_prices(self, story_points: float, risk_profile: str) -> Dict[str, float]:
        """Calculate prices based on risk profile and story points using configurable settings"""
        base_price = story_points * self.base_story_point_price
        
        # Apply DoD impact
        base_price_with_dod = base_price * (1 + self.dod_impact_total)
        
        prices = {'base': base_price, 'base_with_dod': base_price_with_dod}
        
        if risk_profile == 'proven':
            prices['fixed'] = base_price_with_dod
            
        elif risk_profile == 'experimental':
            variance = self.experimental_variance
            prices['minimum'] = base_price_with_dod * (1 - variance)
            prices['maximum'] = base_price_with_dod * (1 + variance)
            
        elif risk_profile == 'dependant':
            # Estimate based on hourly rate using configurable hours per story point
            estimated_hours = story_points * self.settings_config["sprint_planning"]["hours_per_story_point"]
            prices['hourly_estimate'] = estimated_hours * self.hourly_rate
        
        return prices
    
    def calculate_epic_totals(self, epics: list, get_stories_func, get_story_points_func, 
                            determine_risk_profile_func) -> Dict[str, float]:
        """Calculate total costs across all epics"""
        total_proven_cost = 0
        total_experimental_min = 0
        total_experimental_max = 0
        total_dependant_estimate = 0
        
        for epic in epics:
            stories = get_stories_func(epic['key'])
            for story in stories:
                story_points = get_story_points_func(story) or 0
                risk_profile = determine_risk_profile_func(story)
                prices = self.calculate_prices(story_points, risk_profile)
                
                if risk_profile == 'proven':
                    total_proven_cost += prices.get('fixed', 0)
                elif risk_profile == 'experimental':
                    total_experimental_min += prices.get('minimum', 0)
                    total_experimental_max += prices.get('maximum', 0)
                elif risk_profile == 'dependant':
                    total_dependant_estimate += prices.get('hourly_estimate', 0)
        
        return {
            'proven': total_proven_cost,
            'experimental_min': total_experimental_min,
            'experimental_max': total_experimental_max,
            'dependant': total_dependant_estimate,
            'grand_total': total_proven_cost + total_experimental_max + total_dependant_estimate
        } 