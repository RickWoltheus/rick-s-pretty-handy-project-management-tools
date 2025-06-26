# Sprint Planning & Team Composition Guide

## Overview

The enhanced Jira sync system now includes powerful sprint planning and team composition analysis features. These tools help you:

- **Calculate sprint estimates** based on story points and team velocity
- **Compare different team compositions** and their impact on timeline
- **Analyze project risk profiles** to make informed decisions
- **Generate recommendations** for optimal team sizing and project approach

## 🚀 Quick Start

### 1. Demo the Features

```bash
python demo_sprint_planning.py
```

### 2. Interactive Planning Tool

```bash
python sprint_planner.py
```

### 3. Include in Regular Sync

```bash
python enhanced_jira_sync.py
```

The enhanced sync will automatically add a "Sprint Planning" sheet to your spec sheet.

## 📊 Core Concepts

### Team Velocity

- **Base velocity**: Story points a team member can complete per sprint
- **FTE adjustment**: Velocity multiplied by Full Time Equivalent (0.0-1.0)
- **Sprint overhead**: 15% reduction for meetings, planning, and interruptions
- **Team velocity**: Sum of all effective member velocities

### Default Team Compositions

#### Small Team (2.5 FTE)

- 1x Senior Developer (1.0 FTE, 8 SP/sprint)
- 1x Junior Developer (1.0 FTE, 5 SP/sprint)
- 1x Designer (0.5 FTE, 6 SP/sprint)
- **Total velocity**: ~16 SP/sprint

#### Medium Team (5.5 FTE)

- 1x Tech Lead (1.0 FTE, 10 SP/sprint)
- 2x Senior Developer (2.0 FTE, 8 SP/sprint each)
- 1x Junior Developer (1.0 FTE, 5 SP/sprint)
- 1x Designer (1.0 FTE, 6 SP/sprint)
- 1x QA Engineer (0.5 FTE, 4 SP/sprint)
- **Total velocity**: ~34 SP/sprint

#### Large Team (10.5 FTE)

- 1x Tech Lead (1.0 FTE, 10 SP/sprint)
- 3x Senior Developer (3.0 FTE, 8 SP/sprint each)
- 2x Mid Developer (2.0 FTE, 6 SP/sprint each)
- 2x Junior Developer (2.0 FTE, 5 SP/sprint each)
- 1x Designer (1.0 FTE, 6 SP/sprint)
- 1x QA Engineer (1.0 FTE, 4 SP/sprint)
- 1x DevOps Engineer (0.5 FTE, 7 SP/sprint)
- **Total velocity**: ~61 SP/sprint

### Velocity Benchmarks (Industry Standards)

| Role             | Story Points/Sprint | Notes                         |
| ---------------- | ------------------- | ----------------------------- |
| Junior Developer | 3-5 SP              | Learning curve, simpler tasks |
| Mid Developer    | 5-7 SP              | Balanced experience           |
| Senior Developer | 7-10 SP             | Complex tasks, mentoring      |
| Tech Lead        | 8-12 SP             | Architecture, code review     |
| Designer (UI/UX) | 4-8 SP              | Depends on complexity         |
| QA Engineer      | 3-6 SP              | Testing, automation           |
| DevOps Engineer  | 5-8 SP              | Infrastructure, CI/CD         |

## 🛠️ Features

### 1. Sprint Estimation

Calculates how many sprints a project will take based on:

- Total story points
- Team composition and velocity
- Sprint length (default: 2 weeks)
- Sprint overhead (default: 15%)

### 2. Team Comparison

Compare different team sizes and see the impact:

- **Timeline differences** (sprints, weeks, months)
- **Cost implications** (larger teams = higher cost but faster delivery)
- **Risk considerations** (team coordination overhead)

### 3. Custom Team Builder

Create custom teams by specifying:

- **Role** (e.g., "Senior React Developer")
- **FTE** (0.1 to 1.0 - percentage of time dedicated)
- **Velocity** (story points per sprint for this role)

### 4. Risk Analysis

Analyzes your project's risk distribution:

- **Proven work**: Fixed pricing, clear scope
- **Experimental work**: ±30% variance, shared risk
- **Dependent work**: Hourly billing, external dependencies

### 5. Intelligent Recommendations

Based on your project characteristics:

- Team size suggestions
- Timeline vs. cost trade-offs
- Risk mitigation strategies
- Project phase recommendations

## 📈 Using the Interactive Tool

### Menu Options

1. **📊 Generate Full Sprint Analysis Report**

   - Complete project analysis
   - All team comparisons
   - Risk breakdown
   - Recommendations

2. **🏃 Quick Sprint Estimate**

   - Fast estimate for current project
   - Shows all team options

3. **👥 Compare Team Compositions**

   - Side-by-side team comparison
   - Custom story point input

4. **🛠️ Create Custom Team**

   - Build your own team composition
   - See immediate estimates

5. **💡 Team Recommendations**

   - AI-generated suggestions
   - Based on project analysis

6. **📈 Project Risk Analysis**

   - Detailed risk breakdown
   - Mitigation strategies

7. **🔧 View Default Teams**

   - See all pre-configured teams
   - Understand velocity calculations

8. **💾 Export Analysis to Excel**
   - Add "Sprint Planning" sheet
   - Comprehensive analysis tables

## 🔍 Example Analysis Output

```
📊 Sprint Planning Analysis for 87 story points
============================================================

Small Team:
  Team Size: 2.5 FTE
  Velocity: 16.2 SP/sprint
  Duration: 6 sprints (12 weeks, 2.8 months)
  Team: 3 people

Medium Team:
  Team Size: 5.5 FTE
  Velocity: 34.0 SP/sprint
  Duration: 3 sprints (6 weeks, 1.4 months)
  Team: 5 people

Large Team:
  Team Size: 10.5 FTE
  Velocity: 61.2 SP/sprint
  Duration: 2 sprints (4 weeks, 0.9 months)
  Team: 7 people
```

## 💡 Best Practices

### Team Sizing Guidelines

- **Small projects (<30 SP)**: 1-2 developers sufficient
- **Medium projects (30-100 SP)**: 3-5 person team recommended
- **Large projects (>100 SP)**: Consider 6+ person team or project phases

### Risk Management

- **High experimental work (>30%)**: Add prototyping phase
- **Significant dependencies (>20%)**: Ensure external readiness
- **High overall risk**: Larger team + buffer time

### Velocity Considerations

- New teams start at 70% of expected velocity
- Velocity stabilizes after 3-4 sprints
- Account for holidays, vacations, and training
- Consider team coordination overhead for large teams

## 🏗️ Technical Implementation

### Core Classes

#### `TeamMember`

Represents individual team members with role, FTE, and velocity.

#### `Team`

Manages team composition and calculates total velocity.

#### `EnhancedSpecSheetSync`

Main class with sprint planning methods:

- `calculate_sprint_estimates()`
- `compare_team_options()`
- `generate_sprint_planning_report()`
- `add_sprint_planning_sheet()`

### Calculation Methods

```python
# Sprint calculation
sprints_needed = math.ceil(total_story_points / team_velocity)
weeks_needed = sprints_needed * sprint_length_weeks
months_needed = weeks_needed / 4.33

# Team velocity calculation
team_velocity = sum(member.velocity * member.fte for member in team.members)
effective_velocity = team_velocity * (1 - sprint_overhead)
```

## 📊 Excel Integration

The system automatically creates a "Sprint Planning" sheet with:

### Project Overview

- Total story points
- Number of epics
- Epic breakdown with story counts

### Team Comparison Table

- Team compositions
- Velocities and FTE
- Sprint/week/month estimates

### Risk Analysis

- Risk profile distribution
- Story count and point percentages
- Risk impact analysis

### Recommendations

- Data-driven suggestions
- Timeline optimization tips
- Risk mitigation strategies

## 🔧 Configuration

### Customizing Default Teams

Edit the `_create_default_teams()` method in `enhanced_jira_sync.py`:

```python
def _create_default_teams(self):
    teams = {}

    # Your custom team
    custom_team = Team("My Team")
    custom_team.add_member(TeamMember("Senior Dev", 1.0, 9))
    custom_team.add_member(TeamMember("Junior Dev", 1.0, 4))
    teams["custom"] = custom_team

    return teams
```

### Adjusting Sprint Settings

Modify these class attributes:

- `sprint_length_weeks = 2` # Sprint duration
- `sprint_overhead = 0.15` # Overhead percentage

## 🎯 Example Workflows

### Workflow 1: Project Planning

1. Run `python demo_sprint_planning.py`
2. Review team options and timelines
3. Select optimal team size
4. Export analysis to share with stakeholders

### Workflow 2: Custom Team Design

1. Run `python sprint_planner.py`
2. Choose option 4 (Create Custom Team)
3. Add team members based on available resources
4. Compare with default teams
5. Export final analysis

### Workflow 3: Regular Project Updates

1. Update Jira story points as project evolves
2. Run `python enhanced_jira_sync.py`
3. Check updated "Sprint Planning" sheet
4. Adjust team composition if needed

## 🚀 Advanced Features

### Risk-Based Recommendations

The system analyzes risk profiles and suggests:

- Prototyping phases for experimental work
- Dependency coordination for dependent work
- Team composition adjustments for high-risk projects

### Intelligent Scaling

Recommendations adapt based on:

- Project size (story points)
- Risk distribution
- Team velocity differences
- Timeline constraints

### Cost-Timeline Trade-offs

Analyze the cost impact of different team sizes:

- Larger teams = higher cost but faster delivery
- Smaller teams = lower cost but longer timeline
- Sweet spot analysis for optimal ROI

## 📞 Support

For questions about sprint planning features:

1. Check the demo scripts for examples
2. Review this guide for detailed explanations
3. Examine the code comments for technical details
4. Test with the interactive tool for hands-on learning

---

_This sprint planning system uses proven agile methodologies and industry-standard velocity benchmarks to provide accurate project estimates and team recommendations._

## 🎯 Sprint Review Presentations

The system now also includes comprehensive sprint review presentation generation:

### Sprint Review Features

#### **Multi-Format Generation**

- **Excel**: Professional multi-sheet workbook with detailed analysis
- **HTML**: Interactive web presentation with progress bars and styling
- **Markdown**: Clean, version-control friendly documentation

#### **Comprehensive Analysis**

- Sprint metrics and completion rates
- Epic progress tracking
- Story-level detail with status and risk profiles
- Achievement highlights and challenge identification
- Next sprint preview and recommendations

#### **Smart Insights**

- Automatic achievement detection (completion rates, epic completions, experimental work)
- Challenge identification (blockers, incomplete high-value stories, dependencies)
- Focus area recommendations for next sprint
- Carry-over analysis and planning

### Quick Start - Sprint Reviews

```bash
# Demo sprint review features
python demo_sprint_review.py

# Generate current sprint review
python sprint_review_generator.py

# Custom sprint period
python -c "
from sprint_review_generator import SprintReviewGenerator
generator = SprintReviewGenerator()
files = generator.create_all_formats(sprint_number=15, days_back=10)
print('Generated:', files)
"
```

### Sprint Review Output Example

#### Excel Format

- **Sprint Review Overview**: Executive summary with key metrics
- **Sprint Metrics**: Detailed completion charts and epic breakdown
- **Sprint Stories**: Complete story list with status and risk
- **Epic Progress**: Epic-level progress tracking with color coding
- **Next Sprint Preview**: Planning insights for upcoming sprint

#### HTML Format

- Interactive web presentation
- Progress bars and visual indicators
- Professional styling with responsive design
- Easy sharing via email or web hosting
- Print-friendly for stakeholder meetings

#### Markdown Format

- GitHub/GitLab compatible documentation
- Clean table layouts for metrics
- Version control friendly
- Easy editing and customization

### Integration with Sprint Planning

The sprint review system integrates seamlessly with sprint planning:

1. **End of Sprint**: Generate review presentations
2. **Retrospective**: Use detailed analysis for team discussions
3. **Next Sprint Planning**: Leverage carry-over and focus area insights
4. **Stakeholder Communication**: Share professional presentations

### Customization Options

#### Sprint Detection

```python
# Automatic sprint number estimation
generator.create_all_formats()

# Custom sprint and duration
generator.create_all_formats(sprint_number=15, days_back=10)
```

#### Achievement Criteria

Modify `_generate_achievements()` method to customize success thresholds:

- Completion rate thresholds (90%, 70%)
- Epic completion detection
- Experimental work achievements
- Velocity milestones

#### Challenge Detection

Modify `_generate_challenges()` method to customize warning conditions:

- Low completion rate alerts (<50%)
- High-value story tracking (8+ points)
- Dependency blocker detection
- Story vs point completion mismatches

### Automated Workflows

#### End-of-Sprint Automation

```bash
# Add to end-of-sprint script
python sprint_review_generator.py
# Email generated files to stakeholders
```

#### CI/CD Integration

```yaml
# GitHub Actions example
- name: Generate Sprint Review
  run: python sprint_review_generator.py
- name: Upload Artifacts
  uses: actions/upload-artifact@v2
  with:
    name: sprint-review
    path: sprint_review_*.{xlsx,html,md}
```

### Best Practices

#### **For Teams**

- Run at the end of each sprint for consistency
- Use Excel format for detailed retrospectives
- Archive Markdown versions for project history
- Customize achievement/challenge criteria for your team

#### **For Stakeholders**

- Share HTML version with remote stakeholders
- Use Excel format for detailed analysis and reports
- Include in sprint review meetings
- Distribute via email or internal websites

#### **For Documentation**

- Commit Markdown versions to version control
- Link from project README files
- Include in release notes
- Archive for compliance and auditing

The sprint review system complements the sprint planning tools to provide a complete agile workflow solution.
