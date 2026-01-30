# AI Agent Skills

This directory contains specialized AI agent skills that enhance the LinkedIn Strategy Assistant's capabilities.

## Available Skills

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

To add new skills from the resumeskills repository:

```bash
npx skills add https://github.com/paramchoudhary/resumeskills --skill <skill-name>
```

Or manually copy skill files to this directory following the same structure.
