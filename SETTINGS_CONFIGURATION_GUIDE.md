# Settings Configuration Guide

The Jira Spec Sheet Sync tool supports comprehensive configuration through a JSON settings file. This allows you to customize pricing models, team compositions, risk assessments, and more without modifying code.

## Configuration File

The settings configuration is stored in `settings_config.json` in the project root. This file defines:

- Pricing and rate configurations
- Sprint planning defaults
- Team member velocity defaults
- Risk assessment thresholds
- Recommendation criteria
- UI formatting preferences

## File Structure

```json
{
  "description": "Settings configuration for Jira Spec Sheet Sync",
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
```

## Configuration Sections

### Pricing Configuration

Controls all monetary calculations and rates:

- `base_story_point_price`: Base cost per story point (€130 default)
- `experimental_variance`: Percentage variance for experimental work (0.3 = 30%)
- `base_hourly_rate`: Original hourly rate before discounts (€127.16)
- `hourly_rate_discount`: Discount percentage (0.25 = 25% discount)

Note: The final hourly rate is calculated dynamically as: `base_hourly_rate × (1 - hourly_rate_discount)` = €127.16 × 0.75 = €95.37

**Example Customization:**

```json
"pricing": {
  "base_story_point_price": 150,  // Premium pricing
  "experimental_variance": 0.2,   // Lower variance (20%)
  "base_hourly_rate": 160,        // Higher base rate
  "hourly_rate_discount": 0.25    // Same discount (final rate: €120)
}
```

### Sprint Planning Configuration

Defines sprint-related calculations and defaults:

- `default_sprint_length_weeks`: Standard sprint duration (2 weeks)
- `sprint_overhead_percentage`: Time lost to meetings, planning (15%)
- `working_days_per_week`: Working days for capacity calculation (5)
- `hours_per_story_point`: Estimated hours per story point (8)

**Example Customization:**

```json
"sprint_planning": {
  "default_sprint_length_weeks": 3,  // 3-week sprints
  "sprint_overhead_percentage": 0.20, // 20% overhead
  "hours_per_story_point": 6          // More efficient team
}
```

### Team Defaults Configuration

Defines velocity expectations for different roles:

- `senior_developer_velocity`: Story points per sprint (8)
- `mid_developer_velocity`: Story points per sprint (6)
- `junior_developer_velocity`: Story points per sprint (5)
- `tech_lead_velocity`: Story points per sprint (10)
- `designer_velocity`: Story points per sprint (6)
- `qa_engineer_velocity`: Story points per sprint (4)
- `devops_engineer_velocity`: Story points per sprint (7)

**Example Customization:**

```json
"team_defaults": {
  "senior_developer_velocity": 10,  // Higher senior velocity
  "junior_developer_velocity": 3,   // More conservative junior estimate
  "designer_velocity": 8            // High-performing design team
}
```

### Risk Assessment Configuration

Controls how stories are categorized by risk:

- `proven_threshold_story_points`: Max points for "proven" risk (3)
- `experimental_threshold_story_points`: Max points for "experimental" risk (8)
- `risk_priority`: Priority mapping for risk types

**Example Customization:**

```json
"risk_assessment": {
  "proven_threshold_story_points": 5,    // More conservative proven threshold
  "experimental_threshold_story_points": 13  // Larger experimental range
}
```

### Recommendations Configuration

Controls when automated recommendations are triggered:

- `large_project_threshold`: Story points considered "large" (100)
- `small_project_threshold`: Story points considered "small" (20)
- `significant_sprints_saved_threshold`: Sprints saved to recommend larger team (4)
- `high_experimental_percentage`: Percentage to flag experimental work (30%)
- `significant_dependent_percentage`: Percentage to flag dependent work (20%)

**Example Customization:**

```json
"recommendations": {
  "large_project_threshold": 150,        // Higher threshold for large projects
  "high_experimental_percentage": 25,    // Flag experimental work earlier
  "significant_sprints_saved_threshold": 2 // Recommend larger teams sooner
}
```

### UI Formatting Configuration

Controls visual appearance of generated spreadsheets:

- `header_color`: Hex color for headers ("366092")
- `epic_background_color`: Background color for epic rows ("E6F3FF")
- `section_background_color`: Background color for section headers ("D4EDDA")
- `default_column_widths`: Array of column widths
- `header_row_height`: Height of header rows (80)

**Example Customization:**

```json
"ui_formatting": {
  "header_color": "2E86AB",              // Blue header
  "epic_background_color": "A8DADC",     // Light blue-green epics
  "section_background_color": "F1FAEE",  // Light background
  "header_row_height": 100               // Taller headers
}
```

## Usage Examples

### Startup Company Configuration

Lower rates, smaller teams, conservative estimates:

```json
{
  "pricing": {
    "base_story_point_price": 80,
    "base_hourly_rate": 86.67,
    "hourly_rate_discount": 0.25
  },
  "team_defaults": {
    "senior_developer_velocity": 6,
    "junior_developer_velocity": 4
  }
}
```

### Enterprise Configuration

Higher rates, larger teams, strict quality standards:

```json
{
  "pricing": {
    "base_story_point_price": 200,
    "base_hourly_rate": 186.67,
    "hourly_rate_discount": 0.25
  },
  "sprint_planning": {
    "sprint_overhead_percentage": 0.25
  },
  "team_defaults": {
    "senior_developer_velocity": 10,
    "tech_lead_velocity": 12
  }
}
```

### Agile-Focused Configuration

Shorter sprints, lower overhead, optimized velocity:

```json
{
  "sprint_planning": {
    "default_sprint_length_weeks": 1,
    "sprint_overhead_percentage": 0.1,
    "hours_per_story_point": 6
  },
  "risk_assessment": {
    "proven_threshold_story_points": 2,
    "experimental_threshold_story_points": 5
  }
}
```

## Best Practices

### Rate Configuration

1. **Keep rates current**: Update hourly rates quarterly
2. **Document discounts**: Clear reasoning for discount percentages
3. **Regional adjustments**: Consider local market rates

### Team Velocity

1. **Use historical data**: Base velocities on actual team performance
2. **Account for experience**: Adjust for team composition changes
3. **Regular calibration**: Review and update quarterly

### Risk Thresholds

1. **Team-specific**: Adjust based on team's domain expertise
2. **Project context**: Consider complexity of the problem domain
3. **Conservative estimates**: Better to overestimate risk

### Sprint Planning

1. **Overhead tracking**: Monitor actual overhead vs. estimates
2. **Seasonal adjustments**: Account for holidays and vacation periods
3. **Process maturity**: Reduce overhead as team processes improve

## Validation and Testing

The tool validates configuration and provides feedback:

- ✅ Successful load with version and sections loaded
- ⚠️ Warnings for missing or invalid values
- ❌ Errors with fallback to defaults

## Configuration Management

### Version Control

1. Keep configuration files in version control
2. Document changes with clear commit messages
3. Tag configuration versions with releases

### Environment-Specific Configs

Consider separate configs for:

- Development/testing
- Client-specific customizations
- Regional variations

### Change Management

1. Test configuration changes in development
2. Review changes with stakeholders
3. Backup existing configs before updates
4. Monitor impact on generated estimates

## Troubleshooting

### Configuration Not Loading

- Check file exists at `settings_config.json` in project root
- Validate JSON syntax using a JSON validator
- Check file permissions and encoding (UTF-8)

### Unexpected Calculations

- Verify pricing section values
- Check team velocity configurations
- Ensure risk thresholds are logical (proven < experimental)

### UI Issues

- Validate hex color codes (6 digits, valid hex)
- Check column width arrays have correct length
- Ensure numeric values are within reasonable ranges

## Migration Guide

When upgrading from hardcoded values:

1. **Backup existing data**: Save current spec sheets
2. **Extract current settings**: Note your current rates and thresholds
3. **Create custom config**: Use current values in new configuration
4. **Test thoroughly**: Compare old vs. new calculations
5. **Document changes**: Note any differences for stakeholders
