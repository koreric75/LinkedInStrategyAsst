# AI Agent Skills

This directory contains specialized AI agent skills that enhance the LinkedIn Strategy Assistant's capabilities.

## Available Skills

### LinkedIn Integration
- **Location:** `linkedin/SKILL.md`
- **Source:** https://github.com/andrejones92/canifi-life-os
- **Description:** Integrate LinkedIn profile data and career strategies with personal life OS systems

This skill provides:
- LinkedIn data synchronization with life OS
- Career goal tracking and alignment
- Content strategy and engagement tracking
- Network quality metrics
- Professional development integration

### LinkedIn Profile Optimizer
- **Location:** `linkedin-profile-optimizer/SKILL.md`
- **Source:** https://github.com/paramchoudhary/resumeskills
- **Description:** Comprehensive guidelines for optimizing LinkedIn profiles for searchability, recruiter visibility, and engagement

This skill provides:
- Profile section optimization (headline, about, experience)
- Keyword optimization strategies
- Profile completeness checklist
- Recruiter visibility best practices
- Resume-to-LinkedIn sync guidelines

## Usage

These skills are used by AI agents to provide more targeted and expert guidance when analyzing LinkedIn profiles and generating career strategies. The skills are integrated into the strategy generation pipeline to enhance the quality of recommendations.

## Adding New Skills

To add new skills from external repositories:

```bash
npx skills add <repository-url> --skill <skill-name>
```

Examples:
```bash
# Add a skill from canifi-life-os
npx skills add https://github.com/andrejones92/canifi-life-os --skill linkedin

# Add a skill from resumeskills
npx skills add https://github.com/paramchoudhary/resumeskills --skill <skill-name>
```

Or manually copy skill files to this directory following the same structure.

## Managing Skills

List all installed skills:
```bash
npx skills list
```
