"""
Test data and fixtures for Jira Spec Sheet Sync tests
"""
from typing import Dict, List

# Mock JIRA Epic data
MOCK_EPICS = [
    {
        "key": "PROJ-100",
        "fields": {
            "summary": "User Authentication System",
            "description": "Implement complete user authentication system with OAuth2 support",
            "status": {"name": "In Progress"},
            "fixVersions": [{"name": "v3"}]
        }
    },
    {
        "key": "PROJ-200", 
        "fields": {
            "summary": "Payment Integration",
            "description": "Integrate Stripe payment processing",
            "status": {"name": "To Do"},
            "fixVersions": [{"name": "v3"}]
        }
    },
    {
        "key": "PROJ-300",
        "fields": {
            "summary": "Analytics Dashboard",
            "description": "Create comprehensive analytics dashboard",
            "status": {"name": "To Do"},
            "fixVersions": [{"name": "v3"}]
        }
    }
]

# Mock JIRA Story data
MOCK_STORIES = {
    "PROJ-100": [  # Stories for User Authentication Epic
        {
            "key": "PROJ-101",
            "fields": {
                "summary": "Design login page UI",
                "description": "Create wireframes and mockups for login page",
                "status": {"name": "Done"},
                "labels": ["frontend", "design"],
                "priority": {"name": "High"},
                "customfield_10016": 3.0,  # Story points
                "customfield_10273": "proven"  # Type of work
            }
        },
        {
            "key": "PROJ-102", 
            "fields": {
                "summary": "Implement OAuth2 authentication",
                "description": "Integrate OAuth2 with Google and GitHub providers",
                "status": {"name": "In Progress"},
                "labels": ["backend", "security"],
                "priority": {"name": "High"},
                "customfield_10016": 8.0,  # Story points
                "customfield_10273": "experimental"  # Type of work
            }
        },
        {
            "key": "PROJ-103",
            "fields": {
                "summary": "Set up user session management",
                "description": "Implement secure session management with Redis",
                "status": {"name": "To Do"},
                "labels": ["backend", "security"],
                "priority": {"name": "Medium"},
                "customfield_10016": 5.0,  # Story points
                "customfield_10273": "dependant"  # Type of work
            }
        }
    ],
    "PROJ-200": [  # Stories for Payment Integration Epic
        {
            "key": "PROJ-201",
            "fields": {
                "summary": "Research payment gateway options",
                "description": "Compare Stripe, PayPal, and other payment options",
                "status": {"name": "Done"},
                "labels": ["research"],
                "priority": {"name": "High"},
                "customfield_10016": 2.0,  # Story points
                "customfield_10273": "proven"  # Type of work
            }
        },
        {
            "key": "PROJ-202",
            "fields": {
                "summary": "Implement Stripe payment processing",
                "description": "Set up Stripe SDK and payment flow",
                "status": {"name": "To Do"},
                "labels": ["backend", "payment"],
                "priority": {"name": "High"},
                "customfield_10016": 13.0,  # Story points
                "customfield_10273": "experimental"  # Type of work
            }
        }
    ],
    "PROJ-300": [  # Stories for Analytics Dashboard Epic
        {
            "key": "PROJ-301",
            "fields": {
                "summary": "Design dashboard layout",
                "description": "Create dashboard wireframes and user flow",
                "status": {"name": "To Do"},
                "labels": ["frontend", "design"],
                "priority": {"name": "Medium"},
                "customfield_10016": 5.0,  # Story points
                "customfield_10273": "proven"  # Type of work
            }
        },
        {
            "key": "PROJ-302",
            "fields": {
                "summary": "Implement real-time data visualization",
                "description": "Create interactive charts using D3.js",
                "status": {"name": "To Do"},
                "labels": ["frontend", "dataviz"],
                "priority": {"name": "Low"},
                "customfield_10016": 8.0,  # Story points
                "customfield_10273": "dependant"  # Type of work
            }
        }
    ]
}

# Mock project versions
MOCK_VERSIONS = {
    "values": [
        {
            "id": "10047",
            "name": "v3",
            "archived": False,
            "released": False,
            "projectId": 10144,
            "releaseDate": "2024-03-01"
        },
        {
            "id": "10046",
            "name": "v2",
            "archived": False,
            "released": True,
            "projectId": 10144,
            "releaseDate": "2024-01-15"
        }
    ]
}

# Mock JIRA field definitions
MOCK_FIELDS = [
    {
        "id": "customfield_10016",
        "name": "Story Points",
        "custom": True,
        "schema": {"type": "number"}
    },
    {
        "id": "customfield_10273", 
        "name": "Type of Work",
        "custom": True,
        "schema": {"type": "option"}
    }
]

# Test configuration
TEST_CONFIG = {
    "JIRA_DOMAIN": "https://test-domain.atlassian.net",
    "JIRA_EMAIL": "test@example.com",
    "JIRA_API_TOKEN": "test-token",
    "JIRA_PROJECT_KEY": "PROJ",
    "JIRA_STORY_POINTS_FIELD": "customfield_10016",
    "JIRA_TYPE_OF_WORK_FIELD": "customfield_10273"
}

def get_mock_epic_by_key(epic_key: str) -> Dict:
    """Get mock epic by key"""
    for epic in MOCK_EPICS:
        if epic["key"] == epic_key:
            return epic
    return None

def get_mock_stories_for_epic(epic_key: str) -> List[Dict]:
    """Get mock stories for an epic"""
    return MOCK_STORIES.get(epic_key, [])

def get_total_story_points() -> float:
    """Calculate total story points across all mock data"""
    total = 0
    for stories in MOCK_STORIES.values():
        for story in stories:
            sp = story["fields"].get("customfield_10016", 0)
            if sp:
                total += sp
    return total

def get_stories_by_risk_profile() -> Dict[str, List[Dict]]:
    """Group mock stories by risk profile"""
    profiles = {"proven": [], "experimental": [], "dependant": []}
    
    for stories in MOCK_STORIES.values():
        for story in stories:
            risk_profile = story["fields"].get("customfield_10273", "proven")
            if risk_profile in profiles:
                profiles[risk_profile].append(story)
    
    return profiles 