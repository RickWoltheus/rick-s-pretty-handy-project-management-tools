#!/usr/bin/env python3
"""
Holiday Management for Timeline Generation
Handles fetching and managing national and personal holidays
"""

import requests
from datetime import datetime, date
from typing import List
from dataclasses import dataclass, field


@dataclass
class HolidayInfo:
    """Holiday information for the timeline"""
    date: date
    name: str
    is_national: bool = True
    affected_members: List[str] = field(default_factory=list)  # Empty means affects everyone


class DutchHolidayAPI:
    """Fetches Dutch national holidays from open API"""
    
    @staticmethod
    def fetch_holidays(year: int) -> List[HolidayInfo]:
        """Fetch Dutch holidays for a specific year"""
        try:
            # Using Nederlandse feestdagen API
            url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/NL"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            holidays = []
            for holiday_data in response.json():
                holiday_date = datetime.strptime(holiday_data['date'], '%Y-%m-%d').date()
                holidays.append(HolidayInfo(
                    date=holiday_date,
                    name=holiday_data['name'],
                    is_national=True
                ))
            
            print(f"📅 Fetched {len(holidays)} Dutch national holidays for {year}")
            return holidays
            
        except Exception as e:
            print(f"⚠️  Could not fetch Dutch holidays for {year}: {e}")
            # Return some common Dutch holidays as fallback
            return DutchHolidayAPI._get_fallback_holidays(year)
    
    @staticmethod
    def _get_fallback_holidays(year: int) -> List[HolidayInfo]:
        """Fallback holidays when API is unavailable"""
        common_holidays = [
            (1, 1, "Nieuwjaarsdag"),
            (4, 27, "Koningsdag"),
            (5, 1, "Dag van de Arbeid"),
            (12, 25, "Eerste Kerstdag"),
            (12, 26, "Tweede Kerstdag"),
        ]
        
        holidays = []
        for month, day, name in common_holidays:
            try:
                holiday_date = date(year, month, day)
                holidays.append(HolidayInfo(
                    date=holiday_date,
                    name=name,
                    is_national=True
                ))
            except ValueError:
                continue  # Skip invalid dates
        
        return holidays


class HolidayManager:
    """Manages all holiday-related functionality for timeline generation"""
    
    def __init__(self):
        self.holidays: List[HolidayInfo] = []
    
    def load_dutch_holidays(self, start_year: int, end_year: int):
        """Load Dutch national holidays for the project timeline"""
        print(f"🇳🇱 Loading Dutch holidays from {start_year} to {end_year}...")
        
        for year in range(start_year, end_year + 1):
            year_holidays = DutchHolidayAPI.fetch_holidays(year)
            self.holidays.extend(year_holidays)
        
        print(f"📅 Loaded {len([h for h in self.holidays if h.is_national])} national holidays")
    
    def add_team_holidays(self, team_members):
        """Convert team member holidays to timeline holidays"""
        from datetime import timedelta
        
        for member in team_members:
            for holiday in member.holidays:
                # Convert date strings to date objects
                start_date = datetime.strptime(holiday.start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(holiday.end_date, '%Y-%m-%d').date()
                
                # Add each day in the holiday range
                current_date = start_date
                while current_date <= end_date:
                    timeline_holiday = HolidayInfo(
                        date=current_date,
                        name=holiday.name,
                        is_national=holiday.is_national,
                        affected_members=[member.name] if not holiday.is_national else []
                    )
                    self.holidays.append(timeline_holiday)
                    current_date += timedelta(days=1)
    
    def is_holiday(self, check_date: date, member_name: str = None) -> bool:
        """Check if a specific date is a holiday for a member"""
        for holiday in self.holidays:
            if holiday.date == check_date:
                if holiday.is_national or (member_name and member_name in holiday.affected_members):
                    return True
        return False
    
    def get_holidays_for_range(self, start_date: date, end_date: date) -> List[HolidayInfo]:
        """Get all holidays within a date range"""
        return [h for h in self.holidays if start_date <= h.date <= end_date] 