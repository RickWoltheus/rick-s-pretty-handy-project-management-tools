# Team Management System Guide

## Overview

The Team Management System provides persistent storage and management of team members, their availability, roles, and holidays. This creates a reusable team database for timeline planning and project estimation.

## Key Features

### 🏗️ **Persistent Team Storage**

- Team members saved as individual JSON files in `team/` folder
- Persistent across multiple timeline generations
- Easy backup and sharing of team configurations

### 👤 **Comprehensive Team Member Profiles**

- **Name & Role**: Developer, Designer, QA, etc.
- **Availability**: Percentage (0.0-1.0) for part-time members
- **Story Points Capacity**: Per-sprint capacity for planning
- **Hourly Rate**: For cost calculations
- **Email**: Optional contact information

### 🏖️ **Holiday Management**

- **Personal Holidays**: Individual vacation, sick days, etc.
- **National Holidays**: Company-wide holidays
- **Date Ranges**: Multi-day holiday support
- **Integration**: Automatically considered in timeline planning

## Getting Started

### 1. Create Team Members

Run the Team Management tool from the main menu (option 7):

```bash
python3 start.py
# Select option 7: Team Management
# Select option 1: Create New Team Member
```

**Example Team Member:**

```
Name: Sarah Johnson
Role: Senior Developer
Availability: 1.0 (100%)
Story Points/Sprint: 8.0
Hourly Rate: €95.37
Email: sarah@company.com

Holidays:
- Summer Vacation: 2024-07-15 to 2024-07-26
- Christmas Break: 2024-12-23 to 2024-12-31
```

### 2. Add Holidays

You can add holidays during team member creation or later:

```bash
# In Team Management menu
# Select option 4: Add Holiday to Member
```

**Holiday Types:**

- **Personal**: Individual vacation, medical appointments
- **National**: Company-wide holidays affecting everyone

### 3. Use in Timeline Planning

Once team members are created, the Enhanced Timeline Generator automatically loads them:

```bash
python3 start.py
# Select option 8: Enhanced Timeline Generator
```

## File Structure

```
team/
├── __init__.py
├── team_manager.py          # Main team management system
├── TEAM_GUIDE.md           # This guide
├── sarah_johnson.json      # Individual team member files
├── john_doe.json
└── alice_smith.json
```

## Team Member JSON Format

```json
{
  "name": "Sarah Johnson",
  "role": "Senior Developer",
  "availability": 1.0,
  "story_points_per_sprint": 8.0,
  "hourly_rate": 95.37,
  "email": "sarah@company.com",
  "holidays": [
    {
      "start_date": "2024-07-15",
      "end_date": "2024-07-26",
      "name": "Summer Vacation",
      "is_national": false
    },
    {
      "start_date": "2024-12-25",
      "end_date": "2024-12-26",
      "name": "Christmas",
      "is_national": true
    }
  ]
}
```

## Enhanced Timeline Features

### 📊 **Visual Timeline**

- **Excel Output**: Enhanced timeline showing team absences
- **Daily Capacity**: Real team availability calculations
- **Absence Indicators**: Visual representation of who's away when

### 📈 **Project Estimation**

- **Story Point Capacity**: Based on actual team composition
- **Availability Impact**: Considers part-time members and holidays
- **Timeline Optimization**: Suggests timeline adjustments

### 🎯 **Team Insights**

- **Capacity Planning**: Daily and sprint-level planning
- **Resource Allocation**: Optimal team utilization
- **Risk Analysis**: Impact of absences on delivery

## Example Excel Timeline Output

| Date       | Day       | Working Day | Team Capacity | Sarah (Developer)  | John (Designer)     | Alice (QA)          |
| ---------- | --------- | ----------- | ------------- | ------------------ | ------------------- | ------------------- |
| 2024-07-15 | Monday    | Yes         | 2.0           | 🏖️ Summer Vacation | 💼 Available (100%) | 💼 Available (100%) |
| 2024-07-16 | Tuesday   | Yes         | 2.0           | 🏖️ Summer Vacation | 💼 Available (100%) | 💼 Available (100%) |
| 2024-12-25 | Wednesday | No          | 0.0           | 🌍 Christmas       | 🌍 Christmas        | 🌍 Christmas        |

## Best Practices

### 🎯 **Team Setup**

- **Start Early**: Create team profiles before timeline planning
- **Be Realistic**: Set accurate availability percentages
- **Update Regularly**: Keep holiday information current

### 📋 **Holiday Management**

- **Plan Ahead**: Add known holidays/vacations early
- **Communicate**: Share team calendar with stakeholders
- **Buffer Time**: Account for unexpected absences

### 📊 **Timeline Planning**

- **Review Capacity**: Check team availability before committing
- **Adjust Scope**: Consider reducing scope during low-capacity periods
- **Plan Dependencies**: Avoid critical work during key absences

## Integration with JIRA

The team system integrates seamlessly with JIRA data:

1. **Story Points**: Team capacity used for realistic sprint planning
2. **Cost Estimation**: Hourly rates applied to timeline calculations
3. **Resource Planning**: Team skills mapped to JIRA issue types

## Troubleshooting

### Common Issues

**Team folder not found:**

```bash
# The system will automatically create the team folder
# No action needed - just start creating team members
```

**Import errors:**

```bash
# Make sure you're running from the project root
cd /path/to/jira-spec-sheet-sync
python3 start.py
```

**Team member file corruption:**

```bash
# Delete the corrupted .json file and recreate the team member
rm team/corrupted_member.json
```

### Support

- Check the main project README for environment setup
- Use the validation tool (option 3) to verify JIRA configuration
- Review logs for specific error messages

## Advanced Usage

### Bulk Team Import

For large teams, you can manually create JSON files:

```bash
# Copy template and modify
cp team/template_member.json team/new_member.json
# Edit the file with team member details
```

### Team Analytics

The system provides capacity analytics:

- Total team capacity per sprint
- Holiday impact analysis
- Optimal timeline recommendations

### Custom Integrations

Team data can be used in other tools:

- Load team JSON files in custom scripts
- Export to other project management tools
- Create custom reporting dashboards

---

**💡 Pro Tip**: Start with a small team and gradually add members as you get comfortable with the system. The persistent storage means you only need to set up each team member once!
