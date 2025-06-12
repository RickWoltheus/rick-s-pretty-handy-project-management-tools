# Jira to Spec Sheet Mapping Guide

This guide explains how to configure your Jira stories to work with the enhanced spec sheet sync system that matches your sophisticated pricing structure.

## 🏷️ Jira Labels for Risk Profiles

The enhanced sync system automatically determines risk profiles based on Jira labels. Add these labels to your stories:

### Risk Profile Mapping

| Risk Profile                     | Jira Labels                                       | Pricing Structure                    |
| -------------------------------- | ------------------------------------------------- | ------------------------------------ |
| **Proven** (Low Risk)            | `proven`, `low-risk`, `fixed`                     | Fixed price: €130/pt × (1 + 63% DoD) |
| **Experimental** (Moderate Risk) | `experimental`, `moderate-risk`, `research`       | Range: ±30% variance                 |
| **Dependant** (High Risk)        | `dependant`, `dependent`, `high-risk`, `external` | Hourly estimate: €95.37/hour         |

### Default Risk Assessment (if no labels)

- **≤ 3 story points**: Proven
- **4-8 story points**: Experimental
- **> 8 story points**: Dependant

## 🎯 MoSCoW Priority Mapping

The system maps Jira priorities and labels to MoSCoW categories:

### Priority Mapping

| MoSCoW          | Jira Priority       | Jira Labels                         |
| --------------- | ------------------- | ----------------------------------- |
| **Must Have**   | Highest, Blocker    | `must`, `must-have`                 |
| **Should Have** | High, Major         | `should`, `should-have`             |
| **Could Have**  | Medium, Normal      | `could`, `could-have`               |
| **Won't Have**  | Low, Minor, Trivial | `wont`, `wont-have`, `out-of-scope` |

## 💰 Pricing Calculation Examples

### Proven (Fixed Price)

```
Story Points: 5
Base Price: 5 × €130 = €650
DoD Impact: €650 × 1.63 = €1,059.50 (Fixed)
```

### Experimental (Range)

```
Story Points: 8
Base Price: 8 × €130 = €1,040
DoD Impact: €1,040 × 1.63 = €1,695.20
Range (±30%): €1,186.64 - €2,203.76
```

### Dependant (Hourly)

```
Story Points: 13
Estimated Hours: 13 × 8 = 104 hours
Hourly Rate: €95.37/hour (€127.16 with 25% discount)
Estimate: 104 × €95.37 = €9,918.48
```

## 🔧 Jira Configuration Steps

### 1. Create Risk Profile Labels

In your Jira project, create these labels:

- `proven`
- `experimental`
- `dependant`
- `low-risk`
- `moderate-risk`
- `high-risk`

### 2. Create MoSCoW Labels (Optional)

If you don't want to rely on priorities:

- `must-have`
- `should-have`
- `could-have`
- `wont-have`

### 3. Label Your Stories

For each story, add appropriate labels:

**Example 1: Simple login feature**

- Labels: `proven`, `must-have`
- Story Points: 3
- Result: Fixed price, Must Have priority

**Example 2: AI integration research**

- Labels: `experimental`, `could-have`
- Story Points: 8
- Result: Price range, Could Have priority

**Example 3: External API integration**

- Labels: `dependant`, `should-have`
- Story Points: 13
- Result: Hourly estimate, Should Have priority

## 📊 Quality Impact (Definition of Done)

The system automatically applies the 63% quality multiplier based on your Definition of Done sheet:

### Quality Standards Included:

- **Code Quality**: +4% (structure, best practices)
- **Code Review**: +2.5% (pull request reviews)
- **Documentation**: +4% (inline comments, README)
- **Performance**: +6.5% (optimization, smooth rendering)
- **Testing**: +6.5% (cross-browser, unit tests)
- **Security**: +4% (vulnerability mitigation)
- **And more...** (totaling ~63%)

## 🚀 Using the Enhanced Sync

### 1. Set up your `.env` file:

```bash
# Copy from env_template.txt
cp env_template.txt .env

# Edit with your Jira details
nano .env
```

### 2. Run the enhanced sync:

```bash
python enhanced_jira_sync.py
```

### 3. Check your spec sheet:

The system will completely regenerate your "Scope (Quantity)" sheet with:

- Proper header structure matching your original format
- Epic headers (blue background)
- Story rows with risk profiles and pricing
- Proper MoSCoW categorization
- All pricing calculations based on your established rates
- Project summary with totals at the bottom

## 🔍 Sync Behavior

### Complete Regeneration:

- **Scope (Quantity)** sheet is completely regenerated from Jira
- Jira becomes the single source of truth
- All existing content is replaced (no manual entries preserved)
- Fresh headers and formatting applied

### Column Mapping:

1. **Scope**: Story description and key
2. **MoSCoW**: Priority classification
3. **Risk Profile**: Proven/Experimental/Dependant
4. **Notes**: Story points information
5. **Proven columns**: Fixed pricing for proven items
6. **Experimental columns**: Min/max range for experimental
7. **Dependant columns**: Hourly estimates for dependant

### Summary Section:

- Total epics and stories count
- Total story points
- Cost breakdown by risk profile
- Grand total estimate (worst-case scenario)

## 💡 Tips for Best Results

### 1. Consistent Labeling

- Use consistent labels across your team
- Document your labeling strategy
- Regular label audits ensure accuracy

### 2. Story Point Calibration

- Align story points with your pricing model
- Consider the 8-hour per story point estimate for dependant items
- Factor in the 63% quality overhead

### 3. Epic Organization

- Use meaningful epic names
- Group related stories under appropriate epics
- Keep epic scope manageable

### 4. Regular Syncing

- Set up automated syncing (daily/weekly)
- Run sync before client meetings
- Update Jira first, then sync to spec sheet

## 🛠️ Troubleshooting

### Common Issues:

**"No pricing calculated"**

- Check if story has labels or story points
- Verify story points field is configured correctly

**"Wrong risk profile assigned"**

- Add explicit risk labels to stories
- Check label spelling (case-insensitive)

**"Missing stories in sync"**

- Verify epic-story linking in Jira
- Check JQL queries in the client code
- Ensure stories have the correct project key

**"Pricing doesn't match manual calculations"**

- Verify DoD impact percentage (default 63%)
- Check base story point price (default €130)
- Confirm experimental variance (default 30%)

## 🔄 Customization

You can modify the sync behavior by editing `enhanced_jira_sync.py`:

### Change Default Risk Assessment:

```python
def determine_risk_profile(self, story: Dict) -> str:
    # Modify the story point thresholds
    if story_points <= 2:  # Instead of 3
        return 'proven'
    # ... etc
```

### Adjust Pricing Calculations:

```python
def calculate_prices(self, story_points: float, risk_profile: str) -> Dict[str, float]:
    # Modify the DoD impact or base rates
    self.dod_impact_total = 0.70  # Instead of 0.63
```

### Add Custom Field Mapping:

```python
def get_custom_risk_field(self, story: Dict) -> str:
    # Map a custom Jira field to risk profile
    custom_field = story.get('fields', {}).get('customfield_xxxxx')
    return custom_field or 'experimental'
```
