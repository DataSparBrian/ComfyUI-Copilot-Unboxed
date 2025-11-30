#!/usr/bin/env python3
"""
Upstream Repository Monitor for ComfyUI-Copilot-Unboxed

This script monitors the upstream AIDC-AI/ComfyUI-Copilot repository for changes,
categorizes them according to fork modification rules, and generates reports.

Usage:
    python tools/upstream_monitor.py --check
    python tools/upstream_monitor.py --check --verbose
    python tools/upstream_monitor.py --from-commit abc123

Author: DataSparBrian (ComfyUI-Copilot-Unboxed fork)
Original Project: AIDC-AI/ComfyUI-Copilot
License: MIT
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set
import re

# Repository URLs
UPSTREAM_REPO = "https://github.com/AIDC-AI/ComfyUI-Copilot.git"
UPSTREAM_BRANCH = "main"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = PROJECT_ROOT / "docs/maintenance/MODIFICATION_MANIFEST.json"
REPORTS_DIR = PROJECT_ROOT / "reports"

class UpstreamMonitor:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.manifest = self.load_manifest()
        self.merge_rules = self.manifest.get("merge_rules", {})

        # Ensure reports directory exists
        REPORTS_DIR.mkdir(exist_ok=True)

    def log(self, message: str, force: bool = False):
        """Print message if verbose or forced"""
        if self.verbose or force:
            print(message)

    def load_manifest(self) -> Dict:
        """Load the modification manifest"""
        try:
            with open(MANIFEST_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.log("Warning: Modification manifest not found", force=True)
            return {}

    def save_manifest(self):
        """Save the updated manifest"""
        with open(MANIFEST_PATH, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def setup_upstream_remote(self):
        """Ensure upstream remote is configured"""
        self.log("Setting up upstream remote...")
        try:
            # Check if upstream remote exists
            result = subprocess.run(
                ["git", "remote", "get-url", "upstream"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode != 0:
                # Add upstream remote
                subprocess.run(
                    ["git", "remote", "add", "upstream", UPSTREAM_REPO],
                    check=True,
                    cwd=PROJECT_ROOT
                )
                self.log(f"Added upstream remote: {UPSTREAM_REPO}", force=True)
            else:
                self.log(f"Upstream remote already configured: {result.stdout.strip()}")

        except subprocess.CalledProcessError as e:
            self.log(f"Error setting up upstream remote: {e}", force=True)
            return False

        return True

    def fetch_upstream(self):
        """Fetch latest changes from upstream"""
        self.log("Fetching upstream changes...", force=True)
        try:
            subprocess.run(
                ["git", "fetch", "upstream", UPSTREAM_BRANCH],
                check=True,
                cwd=PROJECT_ROOT
            )
            self.log("Upstream fetch successful", force=True)
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Error fetching upstream: {e}", force=True)
            return False

    def get_last_synced_commit(self) -> str:
        """Get the last commit we synced from upstream"""
        return self.manifest.get("upstream_info", {}).get("last_synced_commit", None)

    def get_commit_range(self, from_commit: str = None) -> str:
        """Get the range of commits to analyze"""
        if from_commit:
            return f"{from_commit}..upstream/{UPSTREAM_BRANCH}"

        last_sync = self.get_last_synced_commit()
        if last_sync and last_sync != "TBD":
            return f"{last_sync}..upstream/{UPSTREAM_BRANCH}"

        # No previous sync, check last 50 commits
        return f"upstream/{UPSTREAM_BRANCH}~50..upstream/{UPSTREAM_BRANCH}"

    def get_upstream_commits(self, commit_range: str) -> List[Dict]:
        """Get list of commits in the range"""
        self.log(f"Analyzing commit range: {commit_range}")

        try:
            result = subprocess.run(
                [
                    "git", "log", commit_range,
                    "--pretty=format:%H|%an|%ae|%ai|%s",
                    "--no-merges"
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode != 0:
                self.log("No new commits found or error getting commits")
                return []

            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 5:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    })

            return commits

        except subprocess.CalledProcessError as e:
            self.log(f"Error getting commits: {e}", force=True)
            return []

    def get_changed_files(self, commit_range: str) -> List[str]:
        """Get list of files changed in commit range"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", commit_range],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode != 0:
                return []

            files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            return files

        except subprocess.CalledProcessError as e:
            self.log(f"Error getting changed files: {e}", force=True)
            return []

    def categorize_file(self, filepath: str) -> Tuple[str, str]:
        """
        Categorize a file according to merge rules

        Returns: (category, reason)
        Categories: safe_auto_merge, manual_review, always_block, always_keep_local, unknown
        """
        # Check always_block first
        for pattern in self.merge_rules.get("always_block", []):
            if self._matches_pattern(filepath, pattern):
                return ("always_block", f"Matches block pattern: {pattern}")

        # Check always_keep_local
        for pattern in self.merge_rules.get("always_keep_local", []):
            if self._matches_pattern(filepath, pattern):
                return ("always_keep_local", f"Fork-specific file: {pattern}")

        # Check manual_review_required
        for pattern in self.merge_rules.get("manual_review_required", []):
            if self._matches_pattern(filepath, pattern):
                return ("manual_review", f"Requires manual review: {pattern}")

        # Check auto_merge_patterns
        for pattern in self.merge_rules.get("auto_merge_patterns", []):
            if self._matches_pattern(filepath, pattern):
                return ("safe_auto_merge", f"Safe to auto-merge: {pattern}")

        # Unknown file - be cautious
        return ("unknown", "Not in any known pattern - needs classification")

    def _matches_pattern(self, filepath: str, pattern: str) -> bool:
        """Check if filepath matches glob pattern"""
        pattern = pattern.replace("**", ".*").replace("*", "[^/]*")
        pattern = f"^{pattern}$"
        return bool(re.match(pattern, filepath))

    def detect_risky_patterns(self, filepath: str, commit_range: str) -> List[str]:
        """Detect potentially risky patterns in file changes"""
        risks = []

        # Get the diff for this file
        try:
            result = subprocess.run(
                ["git", "diff", commit_range, "--", filepath],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )

            if result.returncode != 0:
                return risks

            diff_content = result.stdout.lower()
            added_lines = [line for line in diff_content.split('\n') if line.startswith('+')]

            # Check for risky patterns
            risky_patterns = {
                "analytics": r"(analytics|telemetry|track_event|track_user)",
                "email_collection": r"(email.*validation|collect.*email|user.*create|registration)",
                "vendor_endpoints": r"(alibaba|aliyun|taobao).*\.(com|cn)",
                "tracking_pixels": r"(pixel|beacon|tracker)\.(png|gif)",
                "phone_home": r"(phone.*home|report.*usage|send.*stats)",
                "api_key_gen": r"(generate.*key|create.*key|request.*key)",
            }

            for added_line in added_lines:
                for risk_type, pattern in risky_patterns.items():
                    if re.search(pattern, added_line):
                        risks.append(f"{risk_type}: {added_line[:80]}")

        except subprocess.CalledProcessError:
            pass

        return risks

    def is_new_file(self, filepath: str, commit_range: str) -> bool:
        """Check if this is a new file (not just modified)"""
        try:
            # Check if file exists in the starting commit of range
            start_commit = commit_range.split('..')[0]
            result = subprocess.run(
                ["git", "cat-file", "-e", f"{start_commit}:{filepath}"],
                capture_output=True,
                cwd=PROJECT_ROOT
            )
            return result.returncode != 0  # Non-zero means file didn't exist
        except subprocess.CalledProcessError:
            return True

    def analyze_changes(self, commit_range: str) -> Dict:
        """Analyze all changes in the commit range"""
        self.log("Analyzing changes...", force=True)

        commits = self.get_upstream_commits(commit_range)
        changed_files = self.get_changed_files(commit_range)

        categorized = {
            "safe_auto_merge": [],
            "manual_review": [],
            "always_block": [],
            "always_keep_local": [],
            "unknown": []
        }

        high_risk_items = []
        new_files = []

        for filepath in changed_files:
            category, reason = self.categorize_file(filepath)

            # Detect risky patterns
            risks = self.detect_risky_patterns(filepath, commit_range)
            is_new = self.is_new_file(filepath, commit_range)

            file_info = {
                "path": filepath,
                "reason": reason,
                "risks": risks,
                "is_new": is_new
            }

            categorized[category].append(file_info)

            # Flag high-risk items
            if risks or category == "always_block":
                high_risk_items.append(file_info)

            if is_new:
                new_files.append(file_info)

        return {
            "commits": commits,
            "categorized_files": categorized,
            "high_risk_items": high_risk_items,
            "new_files": new_files,
            "total_files_changed": len(changed_files)
        }

    def generate_report(self, analysis: Dict, commit_range: str) -> str:
        """Generate a human-readable report"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        report_lines = []

        report_lines.append(f"# Upstream Changes Report - {timestamp}")
        report_lines.append("=" * 60)
        report_lines.append("")
        report_lines.append(f"**Fork**: ComfyUI-Copilot-Unboxed")
        report_lines.append(f"**Upstream**: AIDC-AI/ComfyUI-Copilot")
        report_lines.append(f"**Commit Range**: {commit_range}")
        report_lines.append("")

        # Summary
        report_lines.append("## Summary")
        report_lines.append("")
        report_lines.append(f"- **Commits**: {len(analysis['commits'])}")
        report_lines.append(f"- **Files Changed**: {analysis['total_files_changed']}")
        report_lines.append(f"- **New Files**: {len(analysis['new_files'])}")
        report_lines.append(f"- **High-Risk Items**: {len(analysis['high_risk_items'])}")
        report_lines.append("")

        # Category breakdown
        report_lines.append("## Category Breakdown")
        report_lines.append("")
        cat = analysis['categorized_files']
        report_lines.append(f"- ✅ **Safe Auto-Merge**: {len(cat['safe_auto_merge'])} files")
        report_lines.append(f"- ⚠️  **Manual Review Required**: {len(cat['manual_review'])} files")
        report_lines.append(f"- ❌ **Block/Reject**: {len(cat['always_block'])} files")
        report_lines.append(f"- 📝 **Fork-Specific (Ignore)**: {len(cat['always_keep_local'])} files")
        report_lines.append(f"- ❓ **Unknown/Unclassified**: {len(cat['unknown'])} files")
        report_lines.append("")

        # High-risk items
        if analysis['high_risk_items']:
            report_lines.append("## ⚠️  HIGH-RISK ITEMS - REVIEW CAREFULLY")
            report_lines.append("")
            for item in analysis['high_risk_items']:
                report_lines.append(f"### `{item['path']}`")
                report_lines.append(f"- **Status**: {'NEW FILE' if item['is_new'] else 'MODIFIED'}")
                report_lines.append(f"- **Category**: {item.get('category', 'Unknown')}")
                if item['risks']:
                    report_lines.append(f"- **Risks Detected**:")
                    for risk in item['risks']:
                        report_lines.append(f"  - {risk}")
                report_lines.append("")

        # New files
        if analysis['new_files']:
            report_lines.append("## 📄 New Files")
            report_lines.append("")
            for item in analysis['new_files']:
                report_lines.append(f"- `{item['path']}` - {item['reason']}")
            report_lines.append("")

        # Detailed file listings
        for category, files in analysis['categorized_files'].items():
            if not files:
                continue

            emoji_map = {
                "safe_auto_merge": "✅",
                "manual_review": "⚠️",
                "always_block": "❌",
                "always_keep_local": "📝",
                "unknown": "❓"
            }

            report_lines.append(f"## {emoji_map.get(category, '•')} {category.replace('_', ' ').title()}")
            report_lines.append("")
            for item in files:
                report_lines.append(f"- `{item['path']}`")
                if item['risks']:
                    report_lines.append(f"  - ⚠️ Risks: {', '.join(item['risks'][:2])}")
            report_lines.append("")

        # Recent commits
        if analysis['commits']:
            report_lines.append("## Recent Upstream Commits")
            report_lines.append("")
            for commit in analysis['commits'][:10]:  # Show last 10
                report_lines.append(f"- `{commit['hash'][:8]}` - {commit['message']}")
                report_lines.append(f"  - By: {commit['author']} ({commit['date']})")
            if len(analysis['commits']) > 10:
                report_lines.append(f"... and {len(analysis['commits']) - 10} more commits")
            report_lines.append("")

        # Action items
        report_lines.append("## 📋 Action Items")
        report_lines.append("")
        action_count = 0
        if cat['manual_review']:
            report_lines.append(f"1. ⚠️  Review {len(cat['manual_review'])} files manually")
            action_count += 1
        if cat['always_block']:
            report_lines.append(f"{action_count + 1}. ❌ Block {len(cat['always_block'])} files from merge")
            action_count += 1
        if cat['unknown']:
            report_lines.append(f"{action_count + 1}. ❓ Classify {len(cat['unknown'])} unknown files")
            action_count += 1
        if analysis['high_risk_items']:
            report_lines.append(f"{action_count + 1}. 🔍 Investigate {len(analysis['high_risk_items'])} high-risk items")
            action_count += 1
        if cat['safe_auto_merge']:
            report_lines.append(f"{action_count + 1}. ✅ Apply {len(cat['safe_auto_merge'])} safe auto-merge files (after privacy scan)")

        if action_count == 0:
            report_lines.append("- ✅ No action required - all changes categorized")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append(f"*Report generated: {datetime.now().isoformat()}*")

        return '\n'.join(report_lines)

    def save_report(self, report: str, analysis: Dict):
        """Save the report to files"""
        timestamp = datetime.now().strftime("%Y-%m-%d")

        # Save markdown report
        md_path = REPORTS_DIR / f"upstream-changes-{timestamp}.md"
        with open(md_path, 'w') as f:
            f.write(report)
        self.log(f"Report saved: {md_path}", force=True)

        # Save JSON report
        json_path = REPORTS_DIR / f"upstream-changes-{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        self.log(f"JSON report saved: {json_path}", force=True)

        return md_path, json_path

    def run_check(self, from_commit: str = None):
        """Main function to run upstream check"""
        self.log("Starting upstream monitoring...", force=True)

        # Setup and fetch
        if not self.setup_upstream_remote():
            return False

        if not self.fetch_upstream():
            return False

        # Analyze changes
        commit_range = self.get_commit_range(from_commit)
        self.log(f"Analyzing commits: {commit_range}", force=True)

        analysis = self.analyze_changes(commit_range)

        if not analysis['commits']:
            self.log("No new commits found upstream.", force=True)
            return True

        # Generate and save report
        report = self.generate_report(analysis, commit_range)
        md_path, json_path = self.save_report(report, analysis)

        # Print summary
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)

        return True

def main():
    parser = argparse.ArgumentParser(
        description="Monitor upstream AIDC-AI/ComfyUI-Copilot for changes"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for upstream changes"
    )
    parser.add_argument(
        "--from-commit",
        type=str,
        help="Specific commit to start from (default: last synced)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    if not args.check:
        parser.print_help()
        return 1

    monitor = UpstreamMonitor(verbose=args.verbose)
    success = monitor.run_check(from_commit=args.from_commit)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
