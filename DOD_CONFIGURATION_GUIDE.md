# Definition of Done Configuration Guide

The Jira Spec Sheet Sync tool now supports configurable Definition of Done (DoD) standards through a JSON configuration file. This allows you to customize quality standards and their pricing impacts without modifying code.

## Configuration File

The DoD configuration is stored in `dod_config.json` in the project root. This file defines:

- Categories of quality standards
- Individual DoD items within each category
- MoSCoW prioritization for each item
- Impact points (story point equivalent)
- Impact percentage (cost multiplier)

## File Structure

```json
{
  "description": "Definition of Done configuration for Jira Spec Sheet Sync",
  "version": "1.0",
  "categories": [
    {
      "name": "Category Name",
      "items": [
        {
          "description": "DoD item description",
          "moscow": "Must Have|Should Have|Could Have|Won't Have",
          "impact_points": "8",
          "impact_percentage": 0.04
        }
      ]
    }
  ]
}
```

## Fields Explanation

### Category Level

- `name`: Display name for the category section in the spec sheet

### Item Level

- `description`: Clear description of the quality standard
- `moscow`: MoSCoW prioritization (Must Have, Should Have, Could Have, Won't Have)
- `impact_points`: Story point equivalent for the work required (for reference)
- `impact_percentage`: Decimal percentage impact on pricing (e.g., 0.04 = 4%)

## Default Categories

The tool comes with these pre-configured categories:

1. **Code quality & documentation**

   - Code structure and best practices
   - Code review processes
   - Testing requirements
   - Documentation standards

2. **Performance & optimization**

   - API performance requirements
   - Rendering optimization
   - State management efficiency

3. **UI/UX & animations**

   - Animation performance
   - User interaction standards
   - Accessibility requirements

4. **Error handling & logging**

   - Error handling patterns
   - Logging requirements
   - Fallback mechanisms

5. **Testing & Cross-browser compatibility**

   - Browser testing requirements
   - Test coverage standards
   - Edge case handling

6. **Security & deployment**
   - Security standards
   - CI/CD requirements
   - Deployment validation

## Customization Examples

### Adding a New Category

```json
{
  "name": "Data & Analytics",
  "items": [
    {
      "description": "User analytics tracking is implemented",
      "moscow": "Should Have",
      "impact_points": "5",
      "impact_percentage": 0.03
    },
    {
      "description": "GDPR compliance for data handling",
      "moscow": "Must Have",
      "impact_points": "13",
      "impact_percentage": 0.08
    }
  ]
}
```

### Modifying Impact Percentages

You can adjust the impact percentages based on your team's experience:

```json
{
  "description": "Security vulnerabilities are identified and mitigated",
  "moscow": "Must Have",
  "impact_points": "8",
  "impact_percentage": 0.06 // Increased from 0.04 for stricter security
}
```

### Setting Won't Have Items

Items marked as "Won't Have" should have 0% impact:

```json
{
  "description": "Automated end-to-end testing suite",
  "moscow": "Won't Have",
  "impact_points": "21",
  "impact_percentage": 0.0 // No cost impact for out-of-scope items
}
```

## Impact Calculation

The tool automatically:

1. Sums all impact percentages from enabled items
2. Applies the total percentage to story point pricing
3. Shows the calculated total in the DoD sheet

**Formula**: `Final Price = Base Price × (1 + Total DoD Impact)`

Example:

- Base price: €1,300 (10 story points × €130)
- DoD impact: 66% (0.66)
- Final price: €1,300 × 1.66 = €2,158

## Best Practices

### Impact Percentage Guidelines

- **Low impact** (1-3%): Simple standards with minimal overhead
- **Medium impact** (4-7%): Standards requiring moderate additional work
- **High impact** (8%+): Complex standards requiring significant effort

### MoSCoW Prioritization

- **Must Have**: Essential standards that cannot be compromised
- **Should Have**: Important standards that add significant value
- **Could Have**: Nice-to-have standards for premium quality
- **Won't Have**: Standards explicitly excluded from current scope

### Configuration Management

1. Keep the configuration file in version control
2. Document changes with clear commit messages
3. Review impact percentage changes with the team
4. Test configuration changes before using in client proposals

## Validation

The tool validates the configuration and provides feedback:

- ✅ Successful load with item count
- ⚠️ Warnings for missing or invalid items
- ❌ Errors with fallback to defaults

## Troubleshooting

### Configuration Not Loading

- Check file exists at `dod_config.json` in project root
- Validate JSON syntax using a JSON validator
- Check file permissions

### Unexpected Impact Totals

- Review individual impact percentages
- Ensure "Won't Have" items have 0.0 impact
- Check for duplicate or missing items

### Missing Categories in Spec Sheet

- Verify categories array in JSON
- Check category names and item arrays
- Ensure valid impact percentages (0.0-1.0 range)

## Example Customization Scenarios

### Conservative Approach (Lower Impacts)

Reduce impact percentages by 20-30% for established teams with strong processes.

### Strict Quality Approach (Higher Impacts)

Increase impact percentages by 30-50% for teams prioritizing exceptional quality.

### Agile Iteration Approach

Mark testing items as "Won't Have" and focus on "Must Have" delivery standards.

### Enterprise Approach

Add comprehensive security, compliance, and documentation requirements.
