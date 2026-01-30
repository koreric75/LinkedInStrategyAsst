#!/usr/bin/env node

const { program } = require('commander');
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');

program
  .name('skills')
  .description('CLI tool to manage AI skills for LinkedIn Strategy Assistant')
  .version('1.0.0');

program
  .command('add')
  .description('Add a skill from a GitHub repository')
  .argument('<repo-url>', 'GitHub repository URL')
  .option('--skill <name>', 'Specific skill name to add')
  .action(async (repoUrl, options) => {
    try {
      console.log(`📥 Fetching skill from ${repoUrl}...`);
      
      // Parse GitHub URL to get owner and repo
      const urlMatch = repoUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
      if (!urlMatch) {
        console.error('❌ Invalid GitHub URL. Expected format: https://github.com/owner/repo');
        process.exit(1);
      }

      const [, owner, repo] = urlMatch;
      const skillName = options.skill;

      if (!skillName) {
        console.error('❌ Please specify a skill name using --skill <name>');
        process.exit(1);
      }

      // Construct the raw GitHub URL for the skill file
      const skillFileUrl = `https://raw.githubusercontent.com/${owner}/${repo}/main/.github/skills/${skillName}/SKILL.md`;
      const alternateUrl = `https://raw.githubusercontent.com/${owner}/${repo}/master/.github/skills/${skillName}/SKILL.md`;

      console.log(`🔍 Looking for skill: ${skillName}`);
      
      let skillContent;
      let fetchUrl = skillFileUrl;
      
      // Try main branch first
      let response = await fetch(skillFileUrl);
      
      // If not found on main, try master
      if (!response.ok) {
        console.log(`   Trying alternate branch...`);
        response = await fetch(alternateUrl);
        fetchUrl = alternateUrl;
      }

      if (!response.ok) {
        console.error(`❌ Skill "${skillName}" not found in repository ${owner}/${repo}`);
        console.error(`   Tried: ${skillFileUrl}`);
        console.error(`   Tried: ${alternateUrl}`);
        process.exit(1);
      }

      skillContent = await response.text();

      // Determine skill location - check both .github/skills and skills directories
      const githubSkillsDir = path.join(process.cwd(), '.github', 'skills', skillName);
      const skillsDir = path.join(process.cwd(), 'skills', skillName);

      // Use skills/ directory (not .github/skills) based on the existing structure
      const targetDir = skillsDir;

      // Create the skill directory
      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }

      // Save the skill file
      const targetFile = path.join(targetDir, 'SKILL.md');
      fs.writeFileSync(targetFile, skillContent);

      console.log(`✅ Successfully added skill "${skillName}"`);
      console.log(`   Location: ${path.relative(process.cwd(), targetFile)}`);
      console.log(`   Source: ${fetchUrl}`);

      // Update the skills README
      updateSkillsReadme(skillName, repoUrl);

      console.log('\n🎉 Skill installation complete!');
      console.log(`\nTo use this skill, refer to: ${path.relative(process.cwd(), targetFile)}`);

    } catch (error) {
      console.error('❌ Error adding skill:', error.message);
      process.exit(1);
    }
  });

program
  .command('list')
  .description('List all installed skills')
  .action(() => {
    const skillsDirs = [
      path.join(process.cwd(), 'skills'),
      path.join(process.cwd(), '.github', 'skills')
    ];

    console.log('📚 Installed Skills:\n');
    
    let foundSkills = false;
    skillsDirs.forEach(dir => {
      if (fs.existsSync(dir)) {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        entries.forEach(entry => {
          if (entry.isDirectory() && entry.name !== 'node_modules') {
            const skillFile = path.join(dir, entry.name, 'SKILL.md');
            if (fs.existsSync(skillFile)) {
              console.log(`  • ${entry.name}`);
              console.log(`    ${path.relative(process.cwd(), skillFile)}`);
              foundSkills = true;
            }
          }
        });
      }
    });

    if (!foundSkills) {
      console.log('  No skills installed yet.');
    }
  });

function updateSkillsReadme(skillName, repoUrl) {
  const readmePath = path.join(process.cwd(), 'skills', 'README.md');
  
  if (!fs.existsSync(readmePath)) {
    console.log('⚠️  skills/README.md not found, skipping update');
    return;
  }

  let readme = fs.readFileSync(readmePath, 'utf8');
  
  // Check if skill is already listed
  if (readme.includes(`skills/${skillName}/SKILL.md`)) {
    console.log('   Skills README already contains this skill');
    return;
  }

  // Add the new skill to the Available Skills section
  const skillEntry = `\n### ${skillName.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
- **Location:** \`${skillName}/SKILL.md\`
- **Source:** ${repoUrl}
- **Description:** AI skill for LinkedIn Strategy Assistant
`;

  // Find the Available Skills section and add the new skill
  const availableSkillsMatch = readme.match(/## Available Skills\n/);
  if (availableSkillsMatch) {
    const insertPosition = availableSkillsMatch.index + availableSkillsMatch[0].length;
    readme = readme.slice(0, insertPosition) + skillEntry + readme.slice(insertPosition);
    fs.writeFileSync(readmePath, readme);
    console.log('   Updated skills/README.md');
  }
}

program.parse();
