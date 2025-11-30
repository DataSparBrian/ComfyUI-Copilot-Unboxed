#!/usr/bin/env python3
"""
Privacy Validator for ComfyUI-Copilot-Unboxed

This script scans the codebase for privacy violations including:
- Telemetry and analytics code
- Vendor-specific network calls
- Email collection
- Tracking pixels and beacons
- Forced registration flows
- Vendor lock-in patterns

Usage:
    python tools/privacy_validator.py --scan
    python tools/privacy_validator.py --scan --strict
    python tools/privacy_validator.py --scan --file path/to/file.tsx

Author: DataSparBrian (ComfyUI-Copilot-Unboxed fork)
License: MIT
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
MANIFEST_PATH = PROJECT_ROOT / "docs/maintenance/MODIFICATION_MANIFEST.json"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Known acceptable external services (user-controlled)
ACCEPTABLE_DOMAINS = {
    "api.openai.com",
    "openrouter.ai",
    "anthropic.com",
    "civitai.com",
    "huggingface.co",
    "modelscope.cn",
    "github.com",
    "githubusercontent.com"
}

# Vendor domains to flag
VENDOR_DOMAINS = {
    "alibaba",
    "aliyun",
    "alipay",
    "taobao",
    "tmall",
    "alicdn"
}

class PrivacyValidator:
    def __init__(self, strict=False, verbose=False):
        self.strict = strict
        self.verbose = verbose
        self.violations = []
        self.warnings = []
        self.passed_checks = []

        # Ensure reports directory exists
        REPORTS_DIR.mkdir(exist_ok=True)

    def log(self, message: str, force: bool = False):
        """Print message if verbose or forced"""
        if self.verbose or force:
            print(message)

    def scan_file(self, filepath: Path) -> List[Dict]:
        """Scan a single file for privacy violations"""
        if not filepath.exists() or not filepath.is_file():
            return []

        violations = []

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            # Run all checks
            violations.extend(self.check_telemetry_imports(filepath, lines))
            violations.extend(self.check_analytics_code(filepath, lines))
            violations.extend(self.check_vendor_endpoints(filepath, lines))
            violations.extend(self.check_email_collection(filepath, lines))
            violations.extend(self.check_tracking_pixels(filepath, lines))
            violations.extend(self.check_vendor_cdn_urls(filepath, lines))
            violations.extend(self.check_registration_flows(filepath, lines))
            violations.extend(self.check_api_key_generation(filepath, lines))

        except Exception as e:
            self.log(f"Error scanning {filepath}: {e}")

        return violations

    def check_telemetry_imports(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for telemetry-related imports"""
        violations = []
        patterns = [
            r"import\s+.*telemetry",
            r"import\s+.*analytics",
            r"from\s+.*telemetry",
            r"from\s+.*analytics",
            r"require\(['\"].*telemetry['\"]",
            r"require\(['\"].*analytics['\"]",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "critical",
                        "type": "telemetry_import",
                        "message": "Telemetry/analytics import detected",
                        "code": line.strip()
                    })

        return violations

    def check_analytics_code(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for analytics function calls"""
        violations = []
        patterns = [
            r"track_event\s*\(",
            r"trackEvent\s*\(",
            r"send_analytics\s*\(",
            r"sendAnalytics\s*\(",
            r"log_event\s*\(",
            r"logEvent\s*\(",
            r"record_metric\s*\(",
            r"recordMetric\s*\(",
            r"\.track\s*\(",
            r"\.analytics\s*\(",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "critical",
                        "type": "analytics_call",
                        "message": "Analytics function call detected",
                        "code": line.strip()
                    })

        return violations

    def check_vendor_endpoints(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for network calls to vendor endpoints"""
        violations = []

        # Patterns for network calls
        network_patterns = [
            r"fetch\s*\(['\"]([^'\"]+)['\"]",
            r"axios\.[a-z]+\s*\(['\"]([^'\"]+)['\"]",
            r"requests\.[a-z]+\s*\(['\"]([^'\"]+)['\"]",
            r"http\.request\s*\(['\"]([^'\"]+)['\"]",
            r"XMLHttpRequest.*open\s*\([^,]+,\s*['\"]([^'\"]+)['\"]",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in network_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    url = match.group(1)

                    # Check if URL contains vendor domains
                    is_vendor = False
                    for vendor in VENDOR_DOMAINS:
                        if vendor.lower() in url.lower():
                            is_vendor = True
                            break

                    # Check if URL is acceptable external service
                    is_acceptable = False
                    for acceptable in ACCEPTABLE_DOMAINS:
                        if acceptable.lower() in url.lower():
                            is_acceptable = True
                            break

                    # Check if URL is relative/local
                    is_local = url.startswith('/') or url.startswith('./') or url.startswith('../')
                    is_localhost = 'localhost' in url.lower() or '127.0.0.1' in url

                    if is_vendor:
                        violations.append({
                            "file": str(filepath),
                            "line": line_no,
                            "severity": "critical",
                            "type": "vendor_endpoint",
                            "message": f"Vendor endpoint call detected: {url}",
                            "code": line.strip()
                        })
                    elif not is_local and not is_localhost and not is_acceptable:
                        # Unknown external endpoint
                        severity = "warning" if not self.strict else "error"
                        violations.append({
                            "file": str(filepath),
                            "line": line_no,
                            "severity": severity,
                            "type": "unknown_endpoint",
                            "message": f"Unknown external endpoint: {url}",
                            "code": line.strip()
                        })

        return violations

    def check_email_collection(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for email collection patterns"""
        violations = []
        patterns = [
            r"<input\s+[^>]*type=['\"]email['\"]",
            r"validateEmail\s*\(",
            r"validate_email\s*\(",
            r"email.*validation",
            r"/api/user/create",
            r"/api/auth/register",
            r"collect.*email",
            r"register.*email",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if this is in ApiKeyModal.tsx (we're removing this)
                    in_api_modal = "ApiKeyModal" in str(filepath)

                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "critical" if in_api_modal else "warning",
                        "type": "email_collection",
                        "message": "Email collection pattern detected",
                        "code": line.strip()
                    })

        return violations

    def check_tracking_pixels(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for tracking pixels and beacons"""
        violations = []
        patterns = [
            r"<img[^>]*src=['\"][^'\"]*pixel[^'\"]*['\"]",
            r"<img[^>]*src=['\"][^'\"]*beacon[^'\"]*['\"]",
            r"<img[^>]*src=['\"][^'\"]*tracker[^'\"]*['\"]",
            r"new\s+Image\(\).*pixel",
            r"new\s+Image\(\).*beacon",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "critical",
                        "type": "tracking_pixel",
                        "message": "Tracking pixel/beacon detected",
                        "code": line.strip()
                    })

        return violations

    def check_vendor_cdn_urls(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for vendor CDN URLs"""
        violations = []

        for line_no, line in enumerate(lines, 1):
            # Check for vendor CDN URLs
            for vendor in VENDOR_DOMAINS:
                if f"{vendor}." in line.lower() and ("http://" in line.lower() or "https://" in line.lower()):
                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "error",
                        "type": "vendor_cdn",
                        "message": f"Vendor CDN URL detected: {vendor}",
                        "code": line.strip()[:100]  # Limit to 100 chars
                    })

        return violations

    def check_registration_flows(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for forced registration patterns"""
        violations = []
        patterns = [
            r"require.*registration",
            r"force.*register",
            r"must.*sign.*up",
            r"api.*key.*required.*email",
            r"create.*account.*required",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "warning",
                        "type": "forced_registration",
                        "message": "Potential forced registration pattern",
                        "code": line.strip()
                    })

        return violations

    def check_api_key_generation(self, filepath: Path, lines: List[str]) -> List[Dict]:
        """Check for API key generation via vendor service"""
        violations = []
        patterns = [
            r"/api/key/generate",
            r"/api/key/create",
            r"generateApiKey\s*\(",
            r"createApiKey\s*\(",
            r"requestApiKey\s*\(",
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    violations.append({
                        "file": str(filepath),
                        "line": line_no,
                        "severity": "error",
                        "type": "api_key_generation",
                        "message": "Vendor API key generation detected",
                        "code": line.strip()
                    })

        return violations

    def scan_directory(self, directory: Path, extensions: Set[str]) -> List[Dict]:
        """Recursively scan directory for files with given extensions"""
        all_violations = []

        for filepath in directory.rglob("*"):
            # Skip certain directories
            skip_dirs = {'.git', 'node_modules', '__pycache__', 'dist', 'build', '.next', 'reports'}
            if any(skip_dir in filepath.parts for skip_dir in skip_dirs):
                continue

            # Check file extension
            if filepath.suffix in extensions:
                self.log(f"Scanning: {filepath}")
                violations = self.scan_file(filepath)
                all_violations.extend(violations)

        return all_violations

    def generate_report(self, violations: List[Dict]) -> str:
        """Generate privacy violation report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_lines = []

        report_lines.append(f"# Privacy Validation Report")
        report_lines.append(f"Generated: {timestamp}")
        report_lines.append("=" * 60)
        report_lines.append("")

        # Group violations by severity
        critical = [v for v in violations if v['severity'] == 'critical']
        errors = [v for v in violations if v['severity'] == 'error']
        warnings = [v for v in violations if v['severity'] == 'warning']

        # Summary
        report_lines.append("## Summary")
        report_lines.append("")
        report_lines.append(f"- ❌ **Critical**: {len(critical)}")
        report_lines.append(f"- 🚨 **Errors**: {len(errors)}")
        report_lines.append(f"- ⚠️  **Warnings**: {len(warnings)}")
        report_lines.append(f"- **Total**: {len(violations)}")
        report_lines.append("")

        # Status
        if critical or errors:
            status = "❌ FAILED"
            report_lines.append(f"**Status**: {status} - Privacy violations found")
        elif warnings:
            status = "⚠️  WARNING" if self.strict else "✅ PASS"
            report_lines.append(f"**Status**: {status} - Review warnings")
        else:
            status = "✅ PASS"
            report_lines.append(f"**Status**: {status} - No privacy violations detected")

        report_lines.append("")

        # Detailed violations
        for severity, label, emoji in [
            ('critical', 'Critical Violations', '❌'),
            ('error', 'Errors', '🚨'),
            ('warning', 'Warnings', '⚠️')
        ]:
            items = [v for v in violations if v['severity'] == severity]
            if items:
                report_lines.append(f"## {emoji} {label}")
                report_lines.append("")

                # Group by type
                by_type = {}
                for item in items:
                    vtype = item['type']
                    if vtype not in by_type:
                        by_type[vtype] = []
                    by_type[vtype].append(item)

                for vtype, vitems in by_type.items():
                    report_lines.append(f"### {vtype.replace('_', ' ').title()} ({len(vitems)})")
                    report_lines.append("")
                    for item in vitems:
                        report_lines.append(f"- **{item['file']}:{item['line']}**")
                        report_lines.append(f"  - {item['message']}")
                        report_lines.append(f"  - ```{item['code'][:80]}```")
                        report_lines.append("")

        # Recommendations
        report_lines.append("## 📋 Recommendations")
        report_lines.append("")

        if critical:
            report_lines.append("### Critical Actions Required")
            report_lines.append("")
            unique_types = set(v['type'] for v in critical)
            for vtype in unique_types:
                report_lines.append(f"- Remove all `{vtype}` patterns immediately")
            report_lines.append("")

        if errors:
            report_lines.append("### Errors to Fix")
            report_lines.append("")
            unique_types = set(v['type'] for v in errors)
            for vtype in unique_types:
                report_lines.append(f"- Review and address `{vtype}` issues")
            report_lines.append("")

        if warnings:
            report_lines.append("### Warnings to Review")
            report_lines.append("")
            report_lines.append("- Review flagged items to ensure they are user-controlled")
            report_lines.append("- Update acceptable domains list if needed")
            report_lines.append("")

        if not violations:
            report_lines.append("✅ No action required - codebase is privacy-compliant")
            report_lines.append("")

        report_lines.append("---")
        report_lines.append("*Privacy validator for ComfyUI-Copilot-Unboxed*")

        return '\n'.join(report_lines)

    def save_report(self, report: str, violations: List[Dict]):
        """Save validation report"""
        timestamp = datetime.now().strftime("%Y-%m-%d")

        # Save markdown report
        md_path = REPORTS_DIR / f"privacy-scan-{timestamp}.md"
        with open(md_path, 'w') as f:
            f.write(report)
        self.log(f"Report saved: {md_path}", force=True)

        # Save JSON report
        json_path = REPORTS_DIR / f"privacy-scan-{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_violations": len(violations),
                "violations": violations
            }, f, indent=2)
        self.log(f"JSON report saved: {json_path}", force=True)

        return md_path, json_path

    def run_scan(self, target_file: str = None):
        """Run privacy validation scan"""
        self.log("Starting privacy validation...", force=True)

        # File extensions to scan
        extensions = {'.py', '.ts', '.tsx', '.js', '.jsx', '.json', '.html'}

        # Scan specific file or entire project
        if target_file:
            filepath = Path(target_file)
            violations = self.scan_file(filepath)
        else:
            violations = self.scan_directory(PROJECT_ROOT, extensions)

        # Generate and save report
        report = self.generate_report(violations)
        md_path, json_path = self.save_report(report, violations)

        # Print summary
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)

        # Return exit code
        critical = sum(1 for v in violations if v['severity'] == 'critical')
        errors = sum(1 for v in violations if v['severity'] == 'error')
        warnings = sum(1 for v in violations if v['severity'] == 'warning')

        if critical or errors:
            return 1  # Failure
        elif warnings and self.strict:
            return 1  # Failure in strict mode
        else:
            return 0  # Success

def main():
    parser = argparse.ArgumentParser(
        description="Privacy validator for ComfyUI-Copilot-Unboxed"
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Run privacy scan"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Scan specific file"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode - warnings fail the scan"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    if not args.scan:
        parser.print_help()
        return 1

    validator = PrivacyValidator(strict=args.strict, verbose=args.verbose)
    return validator.run_scan(target_file=args.file)

if __name__ == "__main__":
    sys.exit(main())
