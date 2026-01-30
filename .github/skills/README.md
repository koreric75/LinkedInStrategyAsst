# Skills Directory

This directory contains reusable skill modules that extend AI capabilities for this project.

## Available Skills

### LinkedIn Publisher

**Location:** `linkedin-publisher/`  
**Description:** Create professional LinkedIn content and thought leadership posts that build authority  
**Category:** writing  
**Version:** 1.0.0  
**Author:** ID8Labs

#### When to Use
- Create compelling written content
- Develop clear messaging and communication
- Structure information effectively

#### Quick Commands
- `linkedin content` - Create LinkedIn content
- `review linkedin publisher` - Review and optimize
- `linkedin publisher best practices` - Get best practices

See [linkedin-publisher/SKILL.md](linkedin-publisher/SKILL.md) for complete documentation.

---

## About Skills

Skills are modular capabilities sourced from the [ID8Labs Skills Marketplace](https://github.com/eddiebe147/claude-settings) that provide domain-specific expertise and workflows.

Each skill includes:
- Clear objectives and use cases
- Step-by-step workflows
- Best practices and common pitfalls
- Success metrics and checklists

## Adding New Skills

Skills can be added from the marketplace using:
```bash
npx skills add https://github.com/eddiebe147/claude-settings --skill <skill-name>
```

Or manually by:
1. Creating a new directory in `.github/skills/`
2. Adding a `SKILL.md` file with the skill definition
3. Following the standard skill format (see existing skills for reference)
