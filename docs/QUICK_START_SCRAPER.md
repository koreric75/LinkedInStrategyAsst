# Quick Start Guide: LinkedIn Auto-Scraper

Extract your LinkedIn profile data in **3 seconds** instead of 5-10 minutes of manual copying!

## Step 1: Get the Scraper Script

1. Go to the repository: https://github.com/koreric75/LinkedInStrategyAsst
2. Open the file `linkedin_scraper.js`
3. Click the **"Raw"** button
4. Press `Ctrl+A` (or `Cmd+A` on Mac) to select all
5. Press `Ctrl+C` (or `Cmd+C` on Mac) to copy

**Alternative:** Open [docs/scraper-guide.html](docs/scraper-guide.html) and click "Copy Scraper Script"

## Step 2: Run on Your LinkedIn Profile

1. **Open your LinkedIn profile**
   - Go to https://www.linkedin.com/in/your-username
   - Make sure you're logged in and viewing YOUR profile

2. **Open Developer Console**
   - Press `F12` on your keyboard
   - OR right-click anywhere → "Inspect" → click "Console" tab
   - OR `Ctrl+Shift+I` (Windows/Linux) / `Cmd+Option+I` (Mac)

3. **Paste and Run**
   - Click in the Console input area
   - Press `Ctrl+V` (or `Cmd+V`) to paste the script
   - Press `Enter` to run

4. **Confirmation**
   - You'll see: `✅ LinkedIn profile data copied to clipboard!`
   - An alert will also appear confirming the copy

## Step 3: Import in the App

1. **Open LinkedIn Strategy Assistant**
   - Go to the app URL (locally or deployed)

2. **Click "Import from Clipboard"**
   - Look for the blue "Auto-Extract from LinkedIn" section
   - Click the green **"Import Data"** button

3. **Verify**
   - All fields should auto-fill instantly
   - Check that your headline, about, skills, etc. are populated
   - Make any manual corrections if needed

4. **Continue with Analysis**
   - Upload your resume
   - Select your strategy mode
   - Click "Generate Strategy"

## Common Questions

### Q: Is this safe to use?
**A:** Yes! The script runs 100% locally in your browser. It doesn't send any data to external servers. It only copies your profile information to your clipboard.

### Q: Do I need to run this every time?
**A:** No! Once you've imported your data, it stays in the form. You only need to run the scraper again if your profile changes or you clear the form.

### Q: What if some fields are missing?
**A:** LinkedIn occasionally changes their HTML structure. If some fields don't populate:
1. Manually fill in the missing fields
2. Report the issue on GitHub so we can update the scraper

### Q: Can I save the bookmarklet for easier use?
**A:** Yes! Open `docs/scraper-guide.html` in your browser and drag the "Scrape LinkedIn" button to your bookmarks bar. Then you can just click it whenever you're on your profile.

### Q: Does this work on mobile?
**A:** The scraper works best on desktop browsers (Chrome, Firefox, Edge, Safari). Mobile browser console access is limited. For mobile, use the manual text input instead.

### Q: What data is extracted?
The scraper gets:
- Your headline
- Your About/Summary section
- Your current role
- All your skills (up to 50)
- All your certifications (up to 20)

### Q: Why do I see "Clipboard is empty" error?
**A:** This means the scraper didn't run successfully. Make sure:
1. You're on your LinkedIn profile page (not someone else's)
2. You pasted the entire script in the Console
3. You pressed Enter to run it
4. You saw the success message

## Troubleshooting

### "Cannot read property of null"
- You might not be on a LinkedIn profile page
- Try refreshing the page and running again

### "Clipboard access denied"
- Your browser blocked clipboard access
- Try using a different browser (Chrome recommended)
- Check browser console for error details

### "Script won't paste in Console"
- Some browsers warn about pasting in console
- Type "allow pasting" and press Enter first
- Or open the scraper-guide.html and use the copy button

### Missing skills or certifications
- LinkedIn limits how many items show initially
- Click "Show all skills" on LinkedIn first
- Then run the scraper again

## Pro Tips

### Bookmarklet Method (Fastest)
1. Open `docs/scraper-guide.html`
2. Drag the "Scrape LinkedIn" button to your bookmarks bar
3. Now just click that bookmark whenever you're on your profile
4. Data copied instantly!

### Console Snippet Method
1. In Chrome DevTools, go to Sources → Snippets
2. Create new snippet called "LinkedIn Scraper"
3. Paste the script there
4. Right-click → Run whenever needed

### Keep Script Handy
- Bookmark the `linkedin_scraper.js` raw URL
- Or save it to a text file on your computer
- Or use the docs/scraper-guide.html page

## What's Next?

After importing your LinkedIn data:
1. Upload your resume (PDF/DOC)
2. Choose your strategy mode:
   - **Get Hired**: Job search optimization
   - **Grow Connections**: Network expansion
   - **Influence Market**: Thought leadership
3. Click "Generate Strategy"
4. Review your personalized recommendations!

---

**Need Help?** 
- Check the [full documentation](SCRAPER_README.md)
- Open an issue on GitHub
- Review the example screenshots in docs/

**Time Saved:** ~5-10 minutes per analysis 🎉
