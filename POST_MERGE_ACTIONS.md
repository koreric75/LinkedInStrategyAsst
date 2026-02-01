# Post-PR Merge Actions for v1.2.0 Release

This document outlines the steps to complete the v1.2.0 release after the PR is merged.

## Prerequisites
- PR #[number] merged to main branch
- All tests passing
- Documentation updated

## Step 1: Push Git Tag

The git tag `v1.2.0` has been created locally but needs to be pushed to the remote repository.

```bash
# After PR merge, checkout main and pull latest
git checkout main
git pull origin main

# Create and push the tag (if not already created)
git tag -a v1.2.0 -m "Release v1.2.0 - LinkedIn Profile Optimizer Enhancement"

# Push the tag
git push origin v1.2.0
```

## Step 2: Create GitHub Release

1. Go to https://github.com/koreric75/LinkedInStrategyAsst/releases/new
2. Select tag: `v1.2.0`
3. Release title: `v1.2.0 - LinkedIn Profile Optimizer Enhancement`
4. Description: Copy from `RELEASE_NOTES_v1.2.0.md`
5. Add any additional release assets if needed
6. Click "Publish release"

### Suggested Release Description Template

```markdown
# LinkedIn Strategy Assistant v1.2.0

🎉 **LinkedIn Profile Optimizer Enhancement Release**

## Highlights

- 🚀 Enhanced LinkedIn Profile Optimizer with expert recommendations
- 📅 5-week detailed strategic roadmaps (expanded from 4 weeks)
- ✅ Up to 6 immediate fixes (expanded from 5)
- 💡 Headline optimization with proven formulas
- 📝 About section structure guidance
- 🎯 Skills optimization for all 50 LinkedIn slots
- ⭐ Profile completeness assessment

## What's New

[Copy content from RELEASE_NOTES_v1.2.0.md sections]

## Installation

### Docker
```bash
docker pull ghcr.io/koreric75/linkedin-strategy-backend:1.2.0
docker run -p 8080:8080 ghcr.io/koreric75/linkedin-strategy-backend:1.2.0
```

### Cloud Run
```bash
gcloud builds submit --substitutions=_LOCATION=us-central1
```

## Documentation
- [Full Release Notes](RELEASE_NOTES_v1.2.0.md)
- [Release Package Details](RELEASE_PACKAGE_v1.2.0.md)
- [Changelog](CHANGELOG.md)
- [User Guide](USER_GUIDE.md)

## Upgrade from v1.1.0
No breaking changes - simply redeploy with the new version.

---

**Full Changelog**: https://github.com/koreric75/LinkedInStrategyAsst/compare/v1.1.0...v1.2.0
```

## Step 3: Deploy to Cloud Run

Deploy the updated backend to Google Cloud Run:

```bash
# Navigate to project directory
cd /path/to/LinkedInStrategyAsst

# Submit build to Cloud Build
gcloud builds submit --substitutions=_LOCATION=us-central1

# Verify deployment
curl https://linkedin-strategy-backend-796550517938.us-central1.run.app/health
# Should return: {"status":"ok","version":"1.2.0",...}
```

## Step 4: Deploy Flutter Web Client (Optional)

If you want to update the Flutter web client:

```bash
# Navigate to Flutter app
cd flutter_app

# Build web version
flutter build web

# Deploy to Firebase Hosting
firebase deploy --only hosting
```

## Step 5: Verify Deployment

### 1. Health Check
```bash
curl https://linkedin-strategy-backend-796550517938.us-central1.run.app/health
```

Expected response:
```json
{
  "status": "ok",
  "version": "1.2.0",
  "firebase_enabled": false,
  "vision_api_available": true
}
```

### 2. Functional Test
```bash
cd test_data
python test_text_input.py
```

Expected results:
- Profile score: 80-90
- Immediate fixes: 6 items
- Strategic roadmap: 5 weeks

### 3. Flutter App Test
Visit https://linkedin-strategy-app.storage.googleapis.com/index.html and test:
- Text input mode with all three strategic modes
- Screenshot mode (optional)
- Resume upload
- Dashboard display

## Step 6: Update External Documentation

Update any external links or documentation:
- [ ] Cost dashboard (if needed)
- [ ] Live demo links
- [ ] API documentation links
- [ ] Social media announcements

## Step 7: Publish NPM Package (Optional)

If you want to publish the skills CLI to npm:

```bash
# Update package.json if needed
# Remove "publish_to: 'none'" from package.json

# Login to npm
npm login

# Publish package
npm publish
```

**Note:** Currently set to not publish (`publish_to: 'none'` in package.json)

## Step 8: Announce Release

Consider announcing the release:
- GitHub Discussions
- Social media
- Email to users
- Blog post

### Announcement Template

```
🎉 LinkedIn Strategy Assistant v1.2.0 is now available!

New in this release:
✨ Enhanced LinkedIn Profile Optimizer
📅 5-week strategic roadmaps
💡 Expert-level recommendations
🎯 Profile completeness assessment

Try it now: [link to live demo]
Learn more: https://github.com/koreric75/LinkedInStrategyAsst/releases/tag/v1.2.0

#LinkedInOptimization #CareerGrowth #AITools
```

## Rollback Plan (If Needed)

If issues are discovered after deployment:

```bash
# Rollback Cloud Run to previous revision
gcloud run services update-traffic linkedin-strategy-backend \
  --to-revisions=linkedin-strategy-backend-00004-5zd=100 \
  --region=us-central1

# Or deploy previous version
docker pull gcr.io/linkedin-strategy-ai-assistant/linkedin-strategy-backend:1.1.0
# ... redeploy
```

## Monitoring

After deployment, monitor:
- Cloud Run logs for errors
- Application performance metrics
- User feedback on GitHub issues
- Cost dashboard for billing changes

```bash
# View Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Check Cloud Run metrics
gcloud run services describe linkedin-strategy-backend --region=us-central1
```

## Checklist

After completing all steps:
- [ ] Tag pushed to GitHub
- [ ] GitHub release created and published
- [ ] Backend deployed to Cloud Run
- [ ] Flutter web client deployed (optional)
- [ ] Health endpoint verified (version 1.2.0)
- [ ] Functional tests passed
- [ ] External documentation updated
- [ ] Release announced
- [ ] Monitoring in place

## Support

If you encounter issues:
1. Check [TESTING_GUIDE.md](TESTING_GUIDE.md) for troubleshooting
2. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help
3. Open an issue on GitHub with details

---

**Prepared By:** GitHub Copilot Agent  
**Date:** February 1, 2026  
**Next Review:** After deployment completion
