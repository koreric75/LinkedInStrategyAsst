# LinkedIn Profile Auto-Scraper

Automatically extract your LinkedIn profile data in seconds with zero manual effort!

## 🚀 Why Use the Auto-Scraper?

- **Save Time**: Extract all your profile data in 3 seconds instead of 5+ minutes of manual copy-pasting
- **Higher Accuracy**: Avoid typos and missing information
- **Privacy-First**: Runs 100% locally in your browser - no data sent to external servers
- **Zero Installation**: No browser extensions or downloads required

## 📋 Quick Start (3 Steps)

### Method 1: Console Script (Recommended)

1. **Copy the scraper**
   - Open [linkedin_scraper.js](/linkedin_scraper.js) in this repository
   - Click "Raw" and copy the entire content (Ctrl+A, Ctrl+C)

2. **Run on LinkedIn**
   - Go to your LinkedIn profile: `linkedin.com/in/your-profile`
   - Press `F12` (or `Ctrl+Shift+I` / `Cmd+Option+I` on Mac) to open Developer Tools
   - Click the **Console** tab
   - Paste the script and press `Enter`
   - You'll see a confirmation that data was copied to clipboard

3. **Import in the app**
   - Open the LinkedIn Strategy Assistant app
   - Click the **"Import from Clipboard"** button
   - All your profile fields will be auto-filled!

### Method 2: Bookmarklet (One-Click)

1. Open [docs/scraper-guide.html](/docs/scraper-guide.html) in your browser
2. Drag the "🚀 Scrape LinkedIn" button to your bookmarks bar
3. Visit your LinkedIn profile and click the bookmark
4. Import in the app with "Import from Clipboard"

## 🔧 What Data is Extracted?

The scraper automatically pulls:

- ✅ **Headline** - Your professional title
- ✅ **About Section** - Your full summary/bio
- ✅ **Current Role** - Your most recent job title and company
- ✅ **Skills** - All your listed skills (up to 50)
- ✅ **Certifications** - All your certifications (up to 20)

## 🔒 Privacy & Security

- **100% Client-Side**: The script runs entirely in your browser
- **No External Calls**: Zero network requests to external servers
- **Open Source**: Full code is visible in `linkedin_scraper.js`
- **Clipboard Only**: Data is only copied to your clipboard (never stored or transmitted)

## 🛠️ How It Works

1. The JavaScript scraper uses DOM selectors to find profile elements on LinkedIn
2. Extracts text content from headline, about, experience, skills, and certification sections
3. Formats the data as clean JSON
4. Copies to clipboard using the browser's Clipboard API
5. You manually paste it into the app via "Import from Clipboard"

## ❓ Troubleshooting

**"No data extracted"**
- Ensure you're on your own LinkedIn profile page (`linkedin.com/in/your-username`)
- Make sure your profile has public content (not entirely private)
- Try refreshing the LinkedIn page and running the script again

**"Clipboard is empty"**
- The script must be run successfully first (check Console for confirmation message)
- Some browsers may block clipboard access - check browser console for errors
- Try using a different browser (Chrome/Edge recommended)

**"Some fields are missing"**
- LinkedIn's HTML structure occasionally changes - some selectors may need updates
- Manually fill in any missing fields in the app
- Report the issue on GitHub so we can update the selectors

## 🌟 Benefits Over Manual Entry

| Manual Entry | Auto-Scraper |
|--------------|--------------|
| 5-10 minutes | **3 seconds** |
| Prone to typos | **100% accurate** |
| Easy to miss skills/certs | **Captures everything** |
| Tedious | **Effortless** |

## 📖 Technical Details

**Supported LinkedIn Layouts**:
- New LinkedIn design (2024+)
- Classic LinkedIn layout
- Mobile-responsive views

**Browser Compatibility**:
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ IE11 (Clipboard API not supported)

**Selectors Used**:
```javascript
Headline: '.text-body-medium.break-words', '.top-card-layout__headline'
About: 'section[data-section="summary"]', '.pv-about__summary-text'
Skills: 'section:has(#skills) .pvs-entity'
Experience: '.pvs-list__outer-container .pvs-entity'
Certifications: 'section:has(#licenses_and_certifications)'
```

## 🎯 Future Enhancements

- [ ] Browser extension for one-click scraping (no console needed)
- [ ] Auto-detect and notify of profile changes
- [ ] Support for extracting education and projects
- [ ] Multi-language support

## 📝 License

MIT License - Free to use and modify

## 🤝 Contributing

Found a bug or want to improve the scraper?
1. Fork the repository
2. Update `linkedin_scraper.js`
3. Test on your LinkedIn profile
4. Submit a pull request

---

**Made with ❤️ to save your time and improve your LinkedIn strategy**
