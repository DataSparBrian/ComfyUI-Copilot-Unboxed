# Upstream Synchronization Strategy

> **Fork**: ComfyUI-Copilot-Unboxed
> **Upstream**: AIDC-AI/ComfyUI-Copilot
> **Last Updated**: 2025-11-30

This document outlines the strategy and process for maintaining synchronization with the upstream repository while preserving the privacy-focused modifications of this fork.

---

## Philosophy

We aim to stay close to upstream to benefit from the excellent development work of the AIDC-AI team. Our modifications are surgical and focused on removing vendor lock-in only. We want to:

1. **Benefit from upstream improvements** - Bug fixes, new features, performance enhancements
2. **Minimize maintenance burden** - Automation reduces manual merge conflicts
3. **Preserve privacy modifications** - Block vendor lock-in from reintroduction
4. **Maintain respectful relationship** - Credit upstream work, contribute fixes when possible
5. **Stay sustainable** - Process must be efficient enough to maintain long-term

---

## Upstream Information

- **Repository**: `https://github.com/AIDC-AI/ComfyUI-Copilot`
- **Branch**: `main`
- **Maintainer**: Alibaba International Digital Commerce (AIDC-AI)
- **License**: MIT (compatible with our fork)
- **Original Project Quality**: Excellent - well-architected, feature-rich ComfyUI assistant

---

## Sync Frequency

### Weekly Automated Check

- **Schedule**: Every Sunday at 00:00 UTC
- **Method**: GitHub Actions workflow (`.github/workflows/upstream-sync.yml`)
- **Actions**:
  1. Fetch upstream changes
  2. Run automated categorization
  3. Create GitHub issue if changes found
  4. Generate diff report
  5. Run privacy validator scan

### Manual Sync Triggers

Perform manual sync immediately when:
- Critical security vulnerability fixed upstream
- Major bug affecting core functionality
- New ComfyUI compatibility updates
- Significant new features announced

---

## Change Classification System

### Category 1: Safe Auto-Merge (Green)

**Characteristics**:
- Changes to core business logic files
- Bug fixes in service layer
- Performance improvements
- UI component enhancements (non-promotional)
- Test additions/improvements
- Dependency security updates

**Files Typically Safe**:
```
backend/service/**/*.py
ui/src/components/ui/**/*.tsx
ui/src/components/debug/**/*.tsx
ui/src/utils/*.ts (after network call scan)
backend/dao/**/*.py
```

**Process**:
1. Automated privacy scan passes
2. No network call additions detected
3. No modification to fork-specific files
4. Auto-apply and test

### Category 2: Review Required (Yellow)

**Characteristics**:
- Changes to API controllers
- Modifications to configuration files
- Updates to chat components
- Changes to API client files
- New external service integrations
- Large refactors

**Files Requiring Review**:
```
backend/controller/**/*.py
ui/src/components/chat/**/*.tsx
ui/src/apis/**/*.ts
ui/src/config.ts
public/**/*
```

**Process**:
1. Automated categorization flags for review
2. Manual inspection of changes
3. Privacy impact assessment
4. Selective merge with re-application of privacy mods
5. Full test suite run

### Category 3: Block/Reject (Red)

**Characteristics**:
- New telemetry or analytics code
- Email collection features
- Vendor registration requirements
- Promotional content additions
- Vendor cloud service integrations
- Privacy policy / terms of service changes

**Files to Block**:
```
backend/utils/track_utils.py (always block)
Any new *analytics*.py files
Any new *telemetry*.py files
```

**Patterns to Block**:
- Network calls to vendor domains
- Email validation/collection UI
- API key generation via vendor service
- QR code additions
- Social media promotional badges
- Forced registration flows

**Process**:
1. Automated detection flags
2. Manual confirmation
3. Add to block list in manifest
4. Document reason
5. Monitor for reintroduction in future syncs

### Category 4: Fork-Specific (Blue)

**Characteristics**:
- README and documentation
- Fork maintenance tools
- CI/CD workflows
- Modification manifest
- Architecture map

**Files Always Local**:
```
README.md
README_CN.md
docs/maintenance/**/*
tools/**/*
.github/workflows/upstream-sync.yml
```

**Process**:
- Never merge from upstream
- Monitor upstream README for new feature docs
- Adapt useful documentation additions manually

---

## Automated Sync Workflow

### 1. Upstream Monitoring (`tools/upstream_monitor.py`)

```bash
# Run weekly via GitHub Actions or manually
python tools/upstream_monitor.py --check
```

**What it does**:
1. Fetches upstream `main` branch
2. Compares with last synced commit (from manifest)
3. Categorizes changed files using manifest rules
4. Identifies new files
5. Flags high-risk changes:
   - New network calls
   - New `*.analytics.*` files
   - New `*telemetry*` files
   - Changes to files in `manual_review_required` list
6. Generates categorized report:
   - `reports/upstream-changes-YYYY-MM-DD.md`
   - `reports/upstream-changes-YYYY-MM-DD.json`

**Output**:
```
Upstream Changes Report - 2025-11-30
=====================================

Summary:
- 15 commits since last sync
- 23 files changed
- 3 new files added

Category Breakdown:
✅ Safe Auto-Merge: 12 files
⚠️ Review Required: 8 files
❌ Block/Reject: 2 files
📝 Fork-Specific: 1 file

High-Risk Items:
- backend/utils/analytics_new.py (NEW FILE - analytics pattern)
- ui/src/components/chat/ApiKeyModal.tsx (email collection code)

Action Required:
- Review 8 files manually
- Block 2 files from merge
- Run privacy validator after merge
```

### 2. Privacy Validation (`tools/privacy_validator.py`)

```bash
# Run before and after any upstream merge
python tools/privacy_validator.py --scan
```

**What it scans for**:

1. **Network Call Patterns**:
   ```python
   # Suspicious patterns
   - fetch('https://.*alibaba')
   - requests.post(.*/user/create')
   - axios.post('.*analytics')
   - XMLHttpRequest to non-local hosts
   ```

2. **Telemetry Indicators**:
   ```python
   - import analytics
   - import telemetry
   - track_event(
   - send_telemetry(
   - collect_metrics(
   ```

3. **Email Collection**:
   ```typescript
   - <input type="email"
   - validateEmail(
   - /api/user/create
   - privacy policy links to vendor domains
   ```

4. **Vendor Lock-In**:
   ```python
   - Hardcoded vendor API endpoints
   - Forced registration checks
   - License key validation to vendor servers
   ```

**Output**:
```
Privacy Validation Report
=========================

✅ PASS: No telemetry imports found
✅ PASS: No analytics code detected
⚠️ WARN: Found 2 network calls to external domains:
  - ui/src/utils/civitUtils.ts:45 (CivitAI API - user choice, OK)
  - backend/utils/modelscope_gateway.py:123 (ModelScope - user choice, OK)
❌ FAIL: Email collection found:
  - ui/src/components/chat/ApiKeyModal.tsx:246 (NEEDS REMOVAL)

Status: FAILED - Manual review required
```

### 3. Selective Merge Tool (`tools/apply_upstream_changes.py`)

```bash
# Apply changes from specific upstream commit
python tools/apply_upstream_changes.py --from-commit abc123def

# Apply with automatic privacy fixes
python tools/apply_upstream_changes.py --from-commit abc123def --auto-fix-privacy
```

**What it does**:
1. Reads MODIFICATION_MANIFEST.json
2. Cherry-picks upstream commits
3. For modified files:
   - Attempts three-way merge
   - Re-applies privacy modifications
   - Flags conflicts for manual resolution
4. Skips files in `always_block` list
5. Keeps files in `always_keep_local` list
6. Runs privacy validator
7. Creates review-ready branch
8. Updates manifest with new baseline commit

**Conflict Resolution**:
```
File: ui/src/components/chat/ApiKeyModal.tsx
Status: MODIFIED in both fork and upstream
Fork Changes: Email collection removed (lines 246-270)
Upstream Changes: Added new API key validation (lines 280-300)

Resolution Strategy:
1. Accept upstream's new validation feature
2. Re-apply email removal from fork
3. Test combined result
4. Mark for manual review if auto-merge fails
```

---

## Manual Sync Process

### Step-by-Step Workflow

#### 1. Prepare Environment

```bash
# Ensure you're on the main fork branch
git checkout claude/comfyui-privacy-fork-01H6ThSwyV7sK2ExZhQH6bzg

# Create a sync branch
git checkout -b sync/upstream-YYYY-MM-DD

# Add upstream remote if not exists
git remote add upstream https://github.com/AIDC-AI/ComfyUI-Copilot.git || true

# Fetch upstream
git fetch upstream
```

#### 2. Run Automated Analysis

```bash
# Check what's new upstream
python tools/upstream_monitor.py --check --verbose

# Review the generated report
cat reports/upstream-changes-$(date +%Y-%m-%d).md
```

#### 3. Review Changes by Category

**For Safe Auto-Merge Files**:
```bash
# Let the tool handle it
python tools/apply_upstream_changes.py --category safe --auto-apply
```

**For Review Required Files**:
```bash
# Review each file manually
for file in $(cat reports/review-required-files.txt); do
  echo "=== Reviewing $file ==="
  git diff upstream/main -- $file
  # Decide: accept, reject, or modify
done
```

**For Block/Reject Files**:
```bash
# Document why we're blocking
echo "Blocking: backend/utils/analytics.py - vendor telemetry" >> docs/maintenance/BLOCKED_FILES.md
```

#### 4. Apply Selected Changes

```bash
# Cherry-pick specific commits
git cherry-pick abc123..def456

# Or merge with strategy
git merge -X ours upstream/main

# Re-apply privacy modifications
python tools/apply_upstream_changes.py --reapply-privacy-mods
```

#### 5. Validate Privacy

```bash
# Full privacy scan
python tools/privacy_validator.py --scan --strict

# Manual review of flagged items
cat reports/privacy-scan-$(date +%Y-%m-%d).txt
```

#### 6. Test Functionality

```bash
# Install dependencies
pip install -r requirements.txt

# Test BYOK configurations
# - OpenAI API
# - LMStudio local
# - OpenRouter
# - Custom endpoints

# Test core features
# - Workflow generation
# - Debug functionality
# - Workflow rewriting
# - Parameter tuning
```

#### 7. Update Documentation

```bash
# Update manifest with new baseline
python tools/update_manifest.py --new-baseline def456

# Verify changes
git diff docs/maintenance/MODIFICATION_MANIFEST.json
```

#### 8. Commit and Push

```bash
# Commit with descriptive message
git commit -m "sync: Merge upstream improvements from AIDC-AI/ComfyUI-Copilot

Merged changes:
- Bug fixes for workflow generation (commit abc123)
- Performance improvements in debug agent (commit def456)
- UI enhancements for node search (commit ghi789)

Privacy modifications re-applied:
- Email collection remains removed
- Vendor registration remains blocked
- All telemetry checks passed

Upstream work by: AIDC-AI team
Fork maintainer: DataSparBrian
Privacy validation: PASSED"

# Push to fork
git push origin sync/upstream-YYYY-MM-DD

# Create PR for review (if team environment)
gh pr create --title "Upstream sync: YYYY-MM-DD" --body "See commit message for details"
```

---

## Conflict Resolution Strategies

### Strategy 1: Accept Theirs + Re-apply Privacy

**When**: Upstream made significant improvements to a file we modified for privacy

```bash
# Accept upstream version
git checkout --theirs path/to/file.tsx

# Re-apply privacy modifications
python tools/apply_upstream_changes.py --file path/to/file.tsx --reapply-privacy

# Test
npm run test
```

### Strategy 2: Accept Ours + Extract Feature

**When**: Upstream added a feature to a heavily modified file

```bash
# Keep our version
git checkout --ours path/to/file.tsx

# Manually extract and adapt the new feature
# Review: git show upstream/main:path/to/file.tsx

# Apply feature without vendor lock-in
code path/to/file.tsx
```

### Strategy 3: Three-Way Manual Merge

**When**: Complex changes on both sides

```bash
# Use merge tool
git mergetool path/to/file.tsx

# Carefully merge:
# - Keep privacy modifications
# - Integrate useful upstream changes
# - Remove any new vendor lock-in
```

---

## Privacy Re-Application Automation

The `apply_upstream_changes.py` tool can automatically re-apply known privacy modifications:

```python
# Example: ApiKeyModal.tsx privacy modifications
PRIVACY_MODS = {
    "ui/src/components/chat/ApiKeyModal.tsx": [
        {
            "action": "remove_function",
            "name": "handleSendEmail",
            "lines": (246, 270)
        },
        {
            "action": "remove_jsx",
            "description": "email input field",
            "lines": (336, 362)
        },
        {
            "action": "remove_jsx",
            "description": "privacy policy links",
            "lines": (363, 381)
        }
    ]
}
```

---

## Communication with Upstream

### When to Contribute Back

Consider opening PRs to upstream for:
- Bug fixes that don't relate to vendor features
- Performance improvements
- Test coverage additions
- Documentation clarifications
- ComfyUI compatibility fixes

### How to Report Issues Found During Sync

When discovering bugs during privacy testing:

1. Verify bug exists in upstream (not fork-specific)
2. Create minimal reproduction case
3. Open issue in upstream repo
4. Credit: "Found during testing of ComfyUI-Copilot-Unboxed fork"
5. Provide fix if possible
6. Remain respectful and constructive

### Example Issue/PR Message:

> **Bug Report**: Workflow generation fails with custom endpoints
>
> Found while testing the privacy-focused ComfyUI-Copilot-Unboxed fork. This bug also affects the main repository.
>
> **Steps to reproduce**: [...]
>
> **Expected behavior**: [...]
>
> **Actual behavior**: [...]
>
> **Proposed fix**: See attached PR
>
> Thank you to the AIDC-AI team for this excellent tool!

---

## Monitoring Upstream Activity

### GitHub Watch Settings

- **Releases**: Watch for new tagged releases
- **Issues**: Monitor for bug reports that might affect us
- **Pull Requests**: Watch for major refactors
- **Discussions**: Engage with community

### RSS/Notification Setup

```bash
# GitHub CLI watch
gh repo view AIDC-AI/ComfyUI-Copilot --web

# Star for notifications
gh repo star AIDC-AI/ComfyUI-Copilot
```

---

## Rollback Plan

If a sync introduces issues:

```bash
# Return to pre-sync state
git checkout claude/comfyui-privacy-fork-01H6ThSwyV7sK2ExZhQH6bzg
git reset --hard HEAD~1  # If already merged

# Or revert specific commit
git revert <sync-commit-hash>

# Document the issue
echo "YYYY-MM-DD: Rolled back upstream sync due to [reason]" >> docs/maintenance/SYNC_LOG.md
```

---

## Success Metrics

Track sync health:

- **Sync Frequency**: Should maintain weekly checks
- **Merge Success Rate**: Target >80% of safe category auto-merged
- **Privacy Compliance**: 100% - all scans must pass
- **Functionality Preservation**: All core features work after sync
- **Time to Sync**: Should be <2 hours manual effort
- **Upstream Divergence**: Monitor how far behind we fall

---

## Version Compatibility Matrix

| Fork Version | Upstream Commit | ComfyUI Version | Status |
|--------------|----------------|-----------------|--------|
| 1.0.0 | TBD | TBD | In Development |

---

## Emergency Procedures

### Critical Upstream Security Update

```bash
# Immediate sync bypass normal weekly schedule
git fetch upstream
git checkout -b hotfix/security-YYYY-MM-DD

# Cherry-pick security commit(s)
git cherry-pick <security-commit-hash>

# Fast-track testing
python tools/privacy_validator.py --scan --quick
npm run test

# Emergency merge
git checkout claude/comfyui-privacy-fork-01H6ThSwyV7sK2ExZhQH6bzg
git merge hotfix/security-YYYY-MM-DD
git push origin claude/comfyui-privacy-fork-01H6ThSwyV7sK2ExZhQH6bzg
```

### Upstream Major Refactor

If upstream does major refactor:

1. Pause regular syncs
2. Create detailed comparison report
3. Evaluate: rebase fork vs. continue independent
4. If rebase needed:
   - Create new fork from upstream HEAD
   - Re-apply all privacy modifications
   - Comprehensive testing
   - Update all documentation

---

## Acknowledgments

This sync strategy ensures we can maintain a sustainable fork while:
- Respecting the excellent work of the AIDC-AI team
- Benefiting from their continued development
- Preserving the privacy-focused mission of this fork
- Minimizing maintenance burden through automation

Thank you to the original ComfyUI-Copilot developers for creating such a well-architected, maintainable codebase!
