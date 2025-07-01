# Timeline & Calendar Management Tool

## Overview

The Timeline Generator is a comprehensive project planning tool that creates realistic project timelines by considering:

- **Team member availability and capacity**
- **Dutch national holidays** (via API integration)
- **Custom company and personal holidays**
- **Sprint planning** with realistic capacity calculations
- **Calendar visualization** with color-coded availability
- **Integration** with existing spec sheets and JIRA

## Features

### 🎯 Core Capabilities

1. **Intelligent Timeline Generation**

   - Calculates realistic sprint timelines based on team capacity
   - Considers holidays, FTE, and working days
   - Handles varying team member availability

2. **Team Management**

   - Track team member skills, seniority, and hourly rates
   - Support for part-time and shared team members
   - Custom working days per team member

3. **Holiday Management**

   - Automatic Dutch national holidays via API
   - Custom company holidays
   - Personal holidays per team member
   - Calendar view with color-coded availability

4. **Excel Output**

   - Multiple sheets with comprehensive timeline data
   - Calendar views for easy visualization
   - Team member capacity and skills tracking
   - Sprint planning with working days calculations

5. **Integration**
   - Load story points from existing spec sheets
   - JIRA integration ready
   - Compatible with existing project tools

## Quick Start

### 1. Demo Mode (No Setup Required)

```bash
python demo_timeline.py
```

This runs a complete demo with sample team and realistic timeline generation.

### 2. Interactive Mode

```bash
python timeline_generator.py
```

This provides an interactive setup process for real projects.

### 3. Integration with Existing Spec Sheets

The tool automatically detects and can load story points from:

- `spec-sheet.xlsx`
- `jira_cost_estimation.xlsx`

## Generated Output

The tool creates an Excel workbook with four main sheets:

### 1. Team Members

- **Name, Role, FTE** - Basic team information
- **Story Points/Sprint** - Individual capacity
- **Hourly Rate** - For cost calculations
- **Seniority Level** - Junior/Mid/Senior/Lead
- **Skills** - Technology and domain expertise
- **Working Days** - Custom working schedule
- **Custom Holidays** - Personal time off

### 2. Holidays

- **Date** - Holiday date
- **Holiday Name** - Description
- **Type** - National vs Custom
- **Affected Members** - Who is affected (everyone or specific members)

### 3. Sprint Timeline

- **Sprint Details** - Start/end dates, duration
- **Story Points** - Planned work per sprint
- **Team Velocity** - Theoretical capacity
- **Working Days** - Actual working days considering holidays
- **Efficiency %** - Capacity utilization

### 4. Calendar View

- **Monthly calendars** - Visual timeline representation
- **Color coding:**
  - 🔵 Sprint days (light blue)
  - 🔴 Holidays (light red)
  - ⚫ Weekends (gray)

## Team Member Configuration

### Example Team Setup

```python
# Senior Full-Stack Developer
TeamMemberInfo(
    name="Alice Johnson",
    role="Senior Full-Stack Developer",
    fte=1.0,                           # Full time
    story_points_per_sprint=12,        # High capacity
    hourly_rate=120,                   # Senior rate
    seniority_level="Senior",
    skills=["Python", "React", "AWS"]
)

# Part-time Designer
TeamMemberInfo(
    name="Carol Williams",
    role="UI/UX Designer",
    fte=0.8,                           # 4 days per week
    story_points_per_sprint=6,         # Adjusted for PT
    hourly_rate=85,
    seniority_level="Senior",
    skills=["UI/UX", "Figma", "Design Systems"],
    working_days=[0, 1, 2, 3]         # Mon-Thu only
)

# Shared DevOps Engineer
TeamMemberInfo(
    name="David Chen",
    role="DevOps Engineer",
    fte=0.6,                           # 60% allocation
    story_points_per_sprint=4,         # Limited capacity
    hourly_rate=110,
    seniority_level="Senior",
    skills=["AWS", "Kubernetes", "CI/CD"]
)
```

### FTE (Full Time Equivalent) Guidelines

- **1.0** - Full time, 100% dedicated
- **0.8** - 4 days per week
- **0.6** - Shared across projects (60% allocation)
- **0.5** - Half time
- **0.4** - 2 days per week

### Story Points per Sprint Guidelines

Based on 2-week sprints and experience level:

- **Junior Developer**: 5-7 SP
- **Mid Developer**: 6-9 SP
- **Senior Developer**: 8-12 SP
- **Lead Developer**: 6-10 SP (less hands-on coding)
- **Designer**: 4-8 SP (depending on complexity)
- **DevOps**: 3-6 SP (supporting role)

## Holiday Management

### Dutch National Holidays

Automatically fetched from `date.nager.at` API for Netherlands:

- New Year's Day (Nieuwjaarsdag)
- King's Day (Koningsdag) - April 27
- Liberation Day (Bevrijdingsdag) - May 5
- Christmas (Eerste/Tweede Kerstdag) - Dec 25/26
- And more...

### Custom Holiday Examples

#### Single Day Holidays

```python
# Company-wide holidays
timeline.add_custom_holiday(HolidayInfo(
    date=date(2025, 7, 21),
    name="Company Summer Break",
    is_national=False
))

# Personal holidays
timeline.add_custom_holiday(HolidayInfo(
    date=date(2025, 8, 15),
    name="Alice's Vacation",
    is_national=False,
    affected_members=["Alice Johnson"]
))
```

#### Holiday Ranges (Recommended)

For vacation periods, company shutdowns, and extended time off, use holiday ranges:

```python
# Full vacation week (includes weekends)
timeline.add_holiday_range(
    start_date=date(2025, 8, 1),
    end_date=date(2025, 8, 7),
    name="Summer Vacation Week",
    is_national=False,
    affected_members=["Alice Johnson"]
)

# Company shutdown - workdays only (automatically skips weekends)
timeline.add_workdays_holiday_range(
    start_date=date(2025, 12, 22),
    end_date=date(2025, 12, 31),
    name="Christmas Company Shutdown",
    is_national=False
)

# Personal time off - workdays only
timeline.add_workdays_holiday_range(
    start_date=date(2025, 6, 15),
    end_date=date(2025, 6, 19),
    name="Bob's Summer Vacation",
    is_national=False,
    affected_members=["Bob Smith"]
)
```

**Benefits of Holiday Ranges:**

- ✅ **Efficiency**: Add multiple days with one command
- ✅ **Workdays Option**: `add_workdays_holiday_range()` automatically skips weekends
- ✅ **Clear Naming**: Shows the full vacation period
- ✅ **Flexible**: Can affect specific team members or everyone
- ✅ **Validation**: Prevents invalid date ranges

## Integration Examples

### With Existing Spec Sheets

The tool automatically scans for story point columns in common sheet names:

- "Scope (Quantity)"
- "Scope"
- "Timeline"
- "Summary"

Keywords detected: "story point", "sp", "points"

### With JIRA

When JIRA is configured (via existing config), the tool can:

- ✅ Access project information
- 🚧 Load team members (planned feature)
- 🚧 Import actual sprint data (planned feature)

## Timeline Calculation Logic

### Capacity Calculation

```
Effective Capacity = Base SP/Sprint × FTE × (Working Days / Baseline Days)
```

Where:

- **Base SP/Sprint** - Individual capacity rating
- **FTE** - Full Time Equivalent (0.0 to 1.0)
- **Working Days** - Actual working days in sprint (excluding holidays)
- **Baseline Days** - Standard sprint working days (10 for 2-week sprint)

### Sprint Planning

1. **Calculate team capacity** for each sprint period
2. **Account for holidays** and non-working days
3. **Allocate story points** up to team capacity
4. **Continue until all story points** are planned

### Example Calculation

For a 2-week sprint (14 calendar days):

- **Baseline working days**: 10 (excluding weekends)
- **Actual working days**: 8 (2 holidays in sprint)
- **Capacity adjustment**: 8/10 = 0.8

Team member with 10 SP/sprint base capacity:

```
Effective Capacity = 10 × 1.0 × (8/10) = 8 SP
```

## Use Cases

### 1. Project Planning

- **Input**: Total story points from spec sheet
- **Output**: Realistic timeline with sprint breakdown
- **Benefits**: Accurate delivery estimates

### 2. Resource Planning

- **Input**: Team composition and availability
- **Output**: Capacity analysis and bottleneck identification
- **Benefits**: Optimized team allocation

### 3. Holiday Impact Analysis

- **Input**: Planned holidays and team schedules
- **Output**: Timeline impact assessment
- **Benefits**: Proactive planning for holiday periods

### 4. Sprint Retrospectives

- **Input**: Actual vs planned capacity
- **Output**: Efficiency analysis and adjustment recommendations
- **Benefits**: Continuous improvement

## Advanced Features

### Multiple Sprint Lengths

Support for different sprint durations:

- **1 week sprints** - Rapid iteration
- **2 week sprints** - Standard agile (default)
- **3 week sprints** - Longer planning cycles
- **4+ week sprints** - Waterfall-style phases

### Custom Working Patterns

Different working schedules per team member:

```python
# Standard Mon-Fri
working_days=[0, 1, 2, 3, 4]

# 4-day work week (Mon-Thu)
working_days=[0, 1, 2, 3]

# Part-time (Mon, Wed, Fri)
working_days=[0, 2, 4]
```

### Skill-Based Planning

Track team member skills for:

- **Technology matching** - Right person for the task
- **Cross-training planning** - Skill development paths
- **Risk assessment** - Single points of failure

## Integration with Existing Tools

### Spec Sheet Integration

Works seamlessly with existing spec sheets:

1. **Reads story points** from configured columns
2. **Preserves existing data** structure
3. **Adds timeline analysis** as separate output

### JIRA Integration

Ready for JIRA integration:

- Uses existing JIRA client configuration
- Can extend to pull team and sprint data
- Maintains compatibility with current workflows

### Excel Compatibility

Generated files work with:

- **Microsoft Excel** (2016+)
- **Google Sheets** (with import)
- **LibreOffice Calc**
- **Apple Numbers**

## Best Practices

### Team Setup

1. **Accurate FTE values** - Critical for capacity calculation
2. **Conservative SP estimates** - Better to under-promise
3. **Regular updates** - Keep team info current
4. **Skill tracking** - Helps with task allocation

### Holiday Planning

1. **Plan company holidays early** - Include in initial setup
2. **Encourage personal holiday planning** - Earlier is better
3. **Buffer for unexpected time off** - Build in contingency
4. **Review impact quarterly** - Adjust as needed

### Timeline Management

1. **Start with realistic dates** - Don't compress unrealistically
2. **Review capacity regularly** - Team changes over time
3. **Account for ramp-up time** - New team members need time
4. **Include non-development work** - Meetings, admin, etc.

## Troubleshooting

### Common Issues

**"No story points found in spec sheet"**

- Check sheet names match expected patterns
- Verify column headers contain "story point", "sp", or "points"
- Ensure data is in rows 6+ (after headers)

**"Could not fetch Dutch holidays"**

- Check internet connection
- API may be temporarily unavailable (fallback holidays used)
- Firewall may be blocking date.nager.at

**"Timeline seems unrealistic"**

- Review team member SP/sprint values
- Check FTE values are correct
- Verify holiday dates are accurate
- Consider if sprint length is appropriate

### Performance Tips

- **Large teams (10+)**: Consider grouping by skill sets
- **Long projects (6+ months)**: Plan in phases
- **Complex holidays**: Use affected_members to limit scope

## Future Enhancements

### Planned Features

1. **JIRA Team Import** - Automatically load team from JIRA
2. **Velocity Tracking** - Compare planned vs actual sprint performance
3. **Risk Analysis** - Identify potential timeline risks
4. **Resource Optimization** - Suggest team composition improvements
5. **Multi-project Planning** - Handle shared resources across projects
6. **Reporting Dashboard** - Executive summary views

### API Enhancements

1. **Multiple Holiday Sources** - Support for various countries
2. **Team Calendar Integration** - Google Calendar, Outlook sync
3. **Time Tracking Integration** - Harvest, Toggl compatibility
4. **Slack Notifications** - Sprint start/end reminders

---

## Getting Started

1. **Run the demo**: `python demo_timeline.py`
2. **Try interactive mode**: `python timeline_generator.py`
3. **Open generated Excel files** to explore features
4. **Customize team settings** for your project
5. **Integrate with existing workflows**

The timeline generator is designed to complement your existing project management tools while providing realistic, data-driven timeline planning with proper consideration of team availability and holidays.
