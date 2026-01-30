/**
 * LinkedIn Profile Scraper
 * 
 * This JavaScript snippet can be run directly in the browser console on a LinkedIn profile page
 * to extract profile data and copy it to clipboard in JSON format.
 * 
 * BROWSER COMPATIBILITY:
 * - Chrome/Edge: Version 105+ (recommended)
 * - Firefox: Version 121+
 * - Safari: Version 15.4+
 * Note: Uses modern CSS selectors. For older browsers, use manual text input instead.
 * 
 * INSTRUCTIONS:
 * 1. Navigate to your LinkedIn profile page (linkedin.com/in/your-profile)
 * 2. Open browser Developer Tools (F12 or Ctrl+Shift+I / Cmd+Option+I)
 * 3. Go to the Console tab
 * 4. Copy and paste this entire script
 * 5. Press Enter to run
 * 6. The data will be copied to your clipboard automatically
 * 7. Click "Import from Clipboard" in the LinkedIn Strategy Assistant app
 */

(function() {
  try {
    console.log('🔍 LinkedIn Profile Scraper - Starting extraction...');
    
    // Extract headline
    const headlineElement = document.querySelector('.text-body-medium.break-words, .top-card-layout__headline, h1.text-heading-xlarge + div.text-body-medium');
    const headline = headlineElement ? headlineElement.textContent.trim() : '';
    
    // Extract about section - try multiple selectors
    let about = '';
    const aboutSectionSelectors = [
      'section[data-section="summary"] .pv-about__summary-text .lt-line-clamp__raw-line',
      'section.artdeco-card .pv-shared-text-with-see-more span[aria-hidden="true"]',
      '#about + div .pv-shared-text-with-see-more .visually-hidden',
      '.pv-about-section .pv-about__summary-text',
      'section[data-generated-suggestion-target] .display-flex.full-width span[aria-hidden="true"]'
    ];
    
    for (const selector of aboutSectionSelectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent.trim()) {
        about = element.textContent.trim();
        break;
      }
    }
    
    // If not found, try getting from about section more generically
    if (!about) {
      // Find section with id="about" or class containing "about"
      const aboutSection = document.getElementById('about')?.closest('section') || 
                           document.querySelector('section.pv-about-section');
      if (aboutSection) {
        const spans = aboutSection.querySelectorAll('span');
        for (const span of spans) {
          const text = span.textContent.trim();
          if (text.length > 50 && !text.includes('Show')) {
            about = text;
            break;
          }
        }
      }
    }
    
    // Extract current role - first experience item
    let currentRole = '';
    const experienceSelectors = [
      '.experience-section .pv-entity__summary-info h3',
      '#experience ~ .pvs-list__outer-container .pvs-entity__caption-wrapper'
    ];
    
    for (const selector of experienceSelectors) {
      const element = document.querySelector(selector);
      if (element) {
        currentRole = element.textContent.trim();
        if (currentRole) break;
      }
    }
    
    // If still not found, try to get the most recent position using alternative approach
    if (!currentRole) {
      // Find experience section
      const experienceHeading = document.getElementById('experience');
      let experienceSection = null;
      if (experienceHeading) {
        experienceSection = experienceHeading.closest('section');
      }
      
      if (experienceSection) {
        const firstItem = experienceSection.querySelector('.pvs-list__outer-container .pvs-entity, .experience-section .pv-position-entity');
        if (firstItem) {
          const titleElement = firstItem.querySelector('.t-bold span, h3');
          const companyElement = firstItem.querySelector('.t-14.t-normal span, .pv-entity__secondary-title');
          if (titleElement) {
            currentRole = titleElement.textContent.trim();
            if (companyElement) {
              currentRole += ' at ' + companyElement.textContent.trim().split('·')[0].trim();
            }
          }
        }
      }
      
      // Fallback to any experience items if section-based search failed
      if (!currentRole) {
        const experienceItems = document.querySelectorAll('.pvs-list__outer-container .pvs-entity, .experience-section .pv-position-entity');
        if (experienceItems.length > 0) {
          const firstItem = experienceItems[0];
          const titleElement = firstItem.querySelector('.t-bold span, h3');
          const companyElement = firstItem.querySelector('.t-14.t-normal span, .pv-entity__secondary-title');
          if (titleElement) {
            currentRole = titleElement.textContent.trim();
            if (companyElement) {
              currentRole += ' at ' + companyElement.textContent.trim().split('·')[0].trim();
            }
          }
        }
      }
    }
    
    // Extract skills
    const skills = [];
    
    // Find skills section
    const skillsHeading = document.getElementById('skills');
    let skillsSection = null;
    if (skillsHeading) {
      skillsSection = skillsHeading.closest('section');
    }
    
    const skillSelectors = skillsSection 
      ? [skillsSection.querySelectorAll('.pvs-list__outer-container .pvs-entity span[aria-hidden="true"]')]
      : [document.querySelectorAll('.pv-skill-category-entity__name-text, .pv-skill-entity__skill-name')];
    
    skillSelectors.forEach(elements => {
      elements.forEach(el => {
        const skill = el.textContent.trim();
        // Filter out non-skill text (like "Show all" or numbers)
        if (skill && skill.length > 1 && !skill.match(/^\d+$/) && !skill.toLowerCase().includes('show')) {
          if (!skills.includes(skill)) {
            skills.push(skill);
          }
        }
      });
    });
    
    // Extract certifications
    const certifications = [];
    
    // Find certifications section
    const certsHeading = document.getElementById('licenses_and_certifications');
    let certsSection = null;
    if (certsHeading) {
      certsSection = certsHeading.closest('section');
    }
    
    const certSelectors = certsSection
      ? [certsSection.querySelectorAll('.pvs-list__outer-container .pvs-entity span[aria-hidden="true"]')]
      : [document.querySelectorAll('.pv-certifications-section .pv-certifications-section__list-item .pv-certification-entity__name, section[data-section="certifications"] .pv-entity__summary-info h3')];
    
    certSelectors.forEach(elements => {
      elements.forEach(el => {
        const cert = el.textContent.trim();
        // Filter out metadata like dates, org names in the same section
        if (cert && cert.length > 3 && !cert.match(/^\d{4}/) && !cert.toLowerCase().includes('show')) {
          if (!certifications.includes(cert)) {
            certifications.push(cert);
          }
        }
      });
    });
    
    // Build the data object
    const profileData = {
      headline: headline,
      about: about,
      current_role: currentRole,
      skills: skills.slice(0, 50).join(', '), // Limit to 50 skills
      certifications: certifications.slice(0, 20).join(', ') // Limit to 20 certs
    };
    
    // Convert to JSON
    const jsonData = JSON.stringify(profileData, null, 2);
    
    // Copy to clipboard
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(jsonData).then(() => {
        console.log('✅ Profile data copied to clipboard!');
        console.log('\n📋 Extracted Data:');
        console.log('─'.repeat(50));
        console.log('Headline:', profileData.headline || '(not found)');
        console.log('About:', (profileData.about || '(not found)').substring(0, 100) + '...');
        console.log('Current Role:', profileData.current_role || '(not found)');
        console.log('Skills:', profileData.skills ? `${profileData.skills.split(',').length} skills found` : '(not found)');
        console.log('Certifications:', profileData.certifications ? `${profileData.certifications.split(',').length} certifications found` : '(not found)');
        console.log('─'.repeat(50));
        console.log('\n✨ Next Steps:');
        console.log('1. Go to the LinkedIn Strategy Assistant app');
        console.log('2. Click the "Import from Clipboard" button');
        console.log('3. The data will automatically fill in the form fields');
        
        // Show a non-intrusive alert
        alert('✅ LinkedIn profile data copied to clipboard!\n\nNow go to the LinkedIn Strategy Assistant and click "Import from Clipboard".');
      }).catch(err => {
        console.error('❌ Failed to copy to clipboard:', err);
        console.log('\n📋 Copy this data manually:');
        console.log(jsonData);
        alert('Please copy the data from the console (F12) manually.');
      });
    } else {
      // Fallback for older browsers
      console.log('📋 Clipboard API not available. Please copy this data manually:');
      console.log(jsonData);
      alert('Please copy the JSON data from the console manually.');
    }
    
  } catch (error) {
    console.error('❌ Error extracting LinkedIn profile:', error);
    alert('Error extracting profile data. Please ensure you are on your LinkedIn profile page and try again.');
  }
})();
