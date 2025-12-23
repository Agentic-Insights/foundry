#!/usr/bin/env python3
"""
Plugin Validation Script for Claude Code Marketplace

Validates plugin.json, marketplace.json, and integrates with skills-ref
for comprehensive plugin structure validation.
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Validation patterns
PLUGIN_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$')
SEMVER_PATTERN = re.compile(
    r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$'
)

# Common SPDX licenses
SPDX_LICENSES = {
    'MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause',
    'ISC', 'GPL-3.0', 'LGPL-3.0', 'MPL-2.0',
}


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: str  # 'error', 'warning', 'info'
    check: str
    message: str
    file: str
    line: Optional[int] = None


@dataclass
class ValidationResult:
    """Results from validation"""
    status: str  # 'passed', 'warning', 'failed'
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    info: List[ValidationIssue] = field(default_factory=list)

    def add_error(self, check: str, message: str, file: str, line: Optional[int] = None):
        self.errors.append(ValidationIssue('error', check, message, file, line))
        if self.status != 'failed':
            self.status = 'failed'

    def add_warning(self, check: str, message: str, file: str, line: Optional[int] = None):
        self.warnings.append(ValidationIssue('warning', check, message, file, line))
        if self.status == 'passed':
            self.status = 'warning'

    def add_info(self, check: str, message: str, file: str):
        self.info.append(ValidationIssue('info', check, message, file))


class PluginJsonValidator:
    """Validates individual plugin.json files"""

    def __init__(self, plugin_path: Path):
        self.plugin_path = plugin_path
        self.plugin_json_path = plugin_path / '.claude-plugin' / 'plugin.json'

    def validate(self) -> ValidationResult:
        result = ValidationResult(status='passed')

        if not self.plugin_json_path.exists():
            result.add_error(
                'file_exists',
                f'plugin.json not found',
                str(self.plugin_json_path)
            )
            return result

        # Load JSON
        try:
            with open(self.plugin_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(
                'json_syntax',
                f'Invalid JSON: {e.msg}',
                str(self.plugin_json_path),
                e.lineno
            )
            return result
        except Exception as e:
            result.add_error(
                'file_read',
                f'Failed to read file: {e}',
                str(self.plugin_json_path)
            )
            return result

        # Validate required fields
        if 'name' not in data:
            result.add_error(
                'required_field',
                'Missing required field: name',
                str(self.plugin_json_path)
            )
        else:
            self._validate_name(data['name'], result)

        # Validate optional but recommended fields
        if 'version' in data:
            self._validate_version(data['version'], result)

        if 'author' in data:
            self._validate_author(data['author'], result)

        if 'license' in data:
            self._validate_license(data['license'], result)

        if 'repository' in data:
            self._validate_repository(data['repository'], result)

        if 'keywords' in data:
            self._validate_keywords(data['keywords'], result)

        # Validate paths
        for field in ['commands', 'agents', 'skills']:
            if field in data:
                self._validate_paths(field, data[field], result)

        return result

    def _validate_name(self, name: Any, result: ValidationResult):
        """Validate plugin name format"""
        if not isinstance(name, str):
            result.add_error(
                'name_type',
                f'Plugin name must be string, got {type(name).__name__}',
                str(self.plugin_json_path)
            )
            return

        if not PLUGIN_NAME_PATTERN.match(name):
            result.add_error(
                'name_format',
                f'Plugin name "{name}" must be kebab-case, lowercase, no spaces',
                str(self.plugin_json_path)
            )

    def _validate_version(self, version: Any, result: ValidationResult):
        """Validate semantic versioning"""
        if not isinstance(version, str):
            result.add_error(
                'version_type',
                f'Version must be string, got {type(version).__name__}',
                str(self.plugin_json_path)
            )
            return

        if not SEMVER_PATTERN.match(version):
            result.add_error(
                'version_format',
                f'Version "{version}" must follow semantic versioning (MAJOR.MINOR.PATCH)',
                str(self.plugin_json_path)
            )

    def _validate_author(self, author: Any, result: ValidationResult):
        """Validate author field format"""
        if isinstance(author, str):
            result.add_error(
                'author_format',
                f'Author must be object with "name" field, not string. Found: "{author}"',
                str(self.plugin_json_path)
            )
            result.add_info(
                'author_fix',
                f'Change to: {{"name": "{author}"}}',
                str(self.plugin_json_path)
            )
        elif isinstance(author, dict):
            if 'name' not in author:
                result.add_error(
                    'author_name',
                    'Author object must have "name" field',
                    str(self.plugin_json_path)
                )
        else:
            result.add_error(
                'author_type',
                f'Author must be object, got {type(author).__name__}',
                str(self.plugin_json_path)
            )

    def _validate_license(self, license: Any, result: ValidationResult):
        """Validate license field"""
        if not isinstance(license, str):
            result.add_error(
                'license_type',
                f'License must be string, got {type(license).__name__}',
                str(self.plugin_json_path)
            )
            return

        if license not in SPDX_LICENSES:
            result.add_warning(
                'license_spdx',
                f'License "{license}" not in common SPDX list. Consider: {", ".join(sorted(SPDX_LICENSES))}',
                str(self.plugin_json_path)
            )

    def _validate_repository(self, repository: Any, result: ValidationResult):
        """Validate repository URL"""
        if not isinstance(repository, str):
            result.add_error(
                'repository_type',
                f'Repository must be string, got {type(repository).__name__}',
                str(self.plugin_json_path)
            )
            return

        if not repository.startswith(('http://', 'https://')):
            result.add_warning(
                'repository_url',
                f'Repository should be a valid URL',
                str(self.plugin_json_path)
            )

    def _validate_keywords(self, keywords: Any, result: ValidationResult):
        """Validate keywords array"""
        if not isinstance(keywords, list):
            result.add_error(
                'keywords_type',
                f'Keywords must be array, got {type(keywords).__name__}',
                str(self.plugin_json_path)
            )
            return

        for i, keyword in enumerate(keywords):
            if not isinstance(keyword, str):
                result.add_error(
                    'keyword_type',
                    f'Keyword at index {i} must be string, got {type(keyword).__name__}',
                    str(self.plugin_json_path)
                )

    def _validate_paths(self, field: str, paths: Any, result: ValidationResult):
        """Validate path fields"""
        if isinstance(paths, str):
            paths = [paths]
        elif not isinstance(paths, list):
            result.add_error(
                f'{field}_type',
                f'{field} must be string or array, got {type(paths).__name__}',
                str(self.plugin_json_path)
            )
            return

        for path_str in paths:
            if not isinstance(path_str, str):
                continue

            # Check for absolute paths
            if path_str.startswith('/'):
                result.add_error(
                    f'{field}_absolute',
                    f'Path "{path_str}" must be relative, not absolute',
                    str(self.plugin_json_path)
                )

            # Check for ./ prefix (warning only)
            if not path_str.startswith('./'):
                result.add_warning(
                    f'{field}_prefix',
                    f'Path "{path_str}" should start with ./ prefix',
                    str(self.plugin_json_path)
                )

            # Check if path exists
            full_path = self.plugin_path / path_str.lstrip('./')
            if not full_path.exists():
                result.add_error(
                    f'{field}_exists',
                    f'Path "{path_str}" does not exist',
                    str(self.plugin_json_path)
                )


class MarketplaceValidator:
    """Validates marketplace.json and cross-references with plugins"""

    def __init__(self, marketplace_root: Path):
        self.root = marketplace_root
        self.marketplace_json = marketplace_root / '.claude-plugin' / 'marketplace.json'

    def validate(self) -> ValidationResult:
        result = ValidationResult(status='passed')

        if not self.marketplace_json.exists():
            result.add_error(
                'file_exists',
                'marketplace.json not found',
                str(self.marketplace_json)
            )
            return result

        # Load JSON
        try:
            with open(self.marketplace_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(
                'json_syntax',
                f'Invalid JSON: {e.msg}',
                str(self.marketplace_json),
                e.lineno
            )
            return result

        # Validate required fields
        for field in ['name', 'owner', 'plugins']:
            if field not in data:
                result.add_error(
                    'required_field',
                    f'Missing required field: {field}',
                    str(self.marketplace_json)
                )

        if 'owner' in data and not isinstance(data['owner'], dict):
            result.add_error(
                'owner_type',
                'Owner must be object',
                str(self.marketplace_json)
            )
        elif 'owner' in data and 'name' not in data['owner']:
            result.add_error(
                'owner_name',
                'Owner must have "name" field',
                str(self.marketplace_json)
            )

        # Validate plugins array
        if 'plugins' not in data:
            return result

        if not isinstance(data['plugins'], list):
            result.add_error(
                'plugins_type',
                f'Plugins must be array, got {type(data["plugins"]).__name__}',
                str(self.marketplace_json)
            )
            return result

        plugin_names = set()
        for i, plugin_entry in enumerate(data['plugins']):
            self._validate_plugin_entry(plugin_entry, i, plugin_names, result)

        return result

    def _validate_plugin_entry(
        self,
        entry: Dict[str, Any],
        index: int,
        plugin_names: set,
        result: ValidationResult
    ):
        """Validate a single plugin entry in marketplace.json"""
        # Check required fields
        if 'name' not in entry:
            result.add_error(
                'plugin_name_missing',
                f'Plugin at index {index} missing "name" field',
                str(self.marketplace_json)
            )
            return

        name = entry['name']

        # Check for duplicates
        if name in plugin_names:
            result.add_error(
                'duplicate_plugin',
                f'Duplicate plugin name: "{name}"',
                str(self.marketplace_json)
            )
        plugin_names.add(name)

        if 'source' not in entry:
            result.add_error(
                'plugin_source_missing',
                f'Plugin "{name}" missing "source" field',
                str(self.marketplace_json)
            )
            return

        source = entry['source']

        # Validate source path
        if not isinstance(source, str):
            result.add_error(
                'source_type',
                f'Plugin "{name}" source must be string',
                str(self.marketplace_json)
            )
            return

        # Check source path exists
        source_path = self.root / source.lstrip('./')
        if not source_path.exists():
            result.add_error(
                'source_path_missing',
                f'Plugin "{name}" source path does not exist: {source}',
                str(self.marketplace_json)
            )
            return

        # Check plugin.json exists in source
        plugin_json_path = source_path / '.claude-plugin' / 'plugin.json'
        if not plugin_json_path.exists():
            result.add_error(
                'plugin_json_missing',
                f'Plugin "{name}" missing .claude-plugin/plugin.json at {source}',
                str(self.marketplace_json)
            )
            return

        # Load actual plugin.json and check consistency
        try:
            with open(plugin_json_path, 'r') as f:
                plugin_data = json.load(f)

            # Verify name matches
            if plugin_data.get('name') != name:
                result.add_error(
                    'name_mismatch',
                    f'Plugin name mismatch: marketplace says "{name}", plugin.json says "{plugin_data.get("name")}"',
                    str(self.marketplace_json)
                )

            # Verify version consistency
            if 'version' in entry and 'version' in plugin_data:
                if entry['version'] != plugin_data['version']:
                    result.add_error(
                        'version_mismatch',
                        f'Plugin "{name}" version mismatch: marketplace={entry["version"]}, plugin.json={plugin_data["version"]}',
                        str(self.marketplace_json)
                    )

            # Verify author format
            if 'author' in entry:
                if isinstance(entry['author'], str):
                    result.add_error(
                        'author_format_marketplace',
                        f'Plugin "{name}" author in marketplace.json must be object, not string',
                        str(self.marketplace_json)
                    )

        except Exception as e:
            result.add_warning(
                'plugin_json_read',
                f'Could not read plugin.json for "{name}": {e}',
                str(self.marketplace_json)
            )


class SkillsValidator:
    """Validates skills using skills-ref tool"""

    def __init__(self, plugin_path: Path):
        self.plugin_path = plugin_path

    def discover_skills(self) -> List[Path]:
        """Find all skill directories"""
        skills_dir = self.plugin_path / 'skills'
        if not skills_dir.exists():
            return []

        skills = []
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
                skills.append(skill_dir)

        return skills

    def validate_skill(self, skill_path: Path) -> ValidationResult:
        """Validate a single skill using skills-ref"""
        result = ValidationResult(status='passed')

        # Check SKILL.md exists
        skill_md = skill_path / 'SKILL.md'
        if not skill_md.exists():
            result.add_error(
                'skill_md_missing',
                'SKILL.md file not found',
                str(skill_path)
            )
            return result

        # Run skills-ref validate
        try:
            cmd = [
                'uvx',
                '--from', 'git+https://github.com/agentskills/agentskills#subdirectory=skills-ref',
                'skills-ref', 'validate',
                str(skill_path)
            ]

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if proc.returncode != 0:
                result.add_error(
                    'skills_ref_validation',
                    f'skills-ref validation failed:\n{proc.stdout}\n{proc.stderr}',
                    str(skill_path)
                )

        except subprocess.TimeoutExpired:
            result.add_error(
                'skills_ref_timeout',
                'skills-ref validation timed out (30s)',
                str(skill_path)
            )
        except FileNotFoundError:
            result.add_error(
                'skills_ref_missing',
                'uvx not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh',
                str(skill_path)
            )
        except Exception as e:
            result.add_error(
                'skills_ref_error',
                f'Failed to run skills-ref: {e}',
                str(skill_path)
            )

        return result


def print_text_results(
    root_result: Optional[ValidationResult],
    marketplace_result: Optional[ValidationResult],
    plugin_results: Dict[str, ValidationResult],
    skill_results: Dict[str, ValidationResult],
):
    """Print validation results in text format"""
    console.print("\n[bold blue]🔍 Validating Claude Plugins Marketplace...[/bold blue]\n")

    # Root plugin
    if root_result:
        _print_result("Root Plugin (.claude-plugin/plugin.json)", root_result)

    # Marketplace
    if marketplace_result:
        _print_result("Marketplace Registry (.claude-plugin/marketplace.json)", marketplace_result)

    # Individual plugins
    for name, result in plugin_results.items():
        _print_result(f"Plugin: {name}", result)

    # Skills
    if skill_results:
        console.print("\n[bold cyan]🎯 Skills Validation[/bold cyan]")
        for skill_name, result in skill_results.items():
            status_icon = "✅" if result.status == "passed" else ("⚠️" if result.status == "warning" else "❌")
            console.print(f"   {status_icon} {skill_name}")

    # Summary
    console.print("\n" + "━" * 60)
    console.print("[bold]Summary:[/bold]")

    passed = sum(1 for r in plugin_results.values() if r.status == "passed")
    warnings = sum(1 for r in plugin_results.values() if r.status == "warning")
    failed = sum(1 for r in plugin_results.values() if r.status == "failed")

    console.print(f"  ✅ {passed} plugins passed")
    if warnings:
        console.print(f"  ⚠️  {warnings} plugins with warnings")
    if failed:
        console.print(f"  ❌ {failed} plugins failed")
    console.print(f"  🎯 {len(skill_results)} skills validated")


def _print_result(title: str, result: ValidationResult):
    """Print a single validation result"""
    if result.status == "passed":
        console.print(f"\n[green]✅ {title}[/green]")
    elif result.status == "warning":
        console.print(f"\n[yellow]⚠️  {title}[/yellow]")
    else:
        console.print(f"\n[red]❌ {title}[/red]")

    # Print errors
    for error in result.errors:
        location = f" ({error.file}" + (f":{error.line}" if error.line else "") + ")"
        console.print(f"   [red]❌ Error: {error.message}[/red]{location}")

    # Print warnings
    for warning in result.warnings:
        location = f" ({warning.file}" + (f":{warning.line}" if warning.line else "") + ")"
        console.print(f"   [yellow]⚠️  Warning: {warning.message}[/yellow]{location}")

    # Print info
    for info in result.info:
        console.print(f"   [dim]ℹ️  {info.message}[/dim]")


def print_json_results(
    root_result: Optional[ValidationResult],
    marketplace_result: Optional[ValidationResult],
    plugin_results: Dict[str, ValidationResult],
    skill_results: Dict[str, ValidationResult],
):
    """Print validation results in JSON format"""
    output = {
        "root_plugin": _result_to_dict(root_result) if root_result else None,
        "marketplace": _result_to_dict(marketplace_result) if marketplace_result else None,
        "plugins": {name: _result_to_dict(result) for name, result in plugin_results.items()},
        "skills": {name: _result_to_dict(result) for name, result in skill_results.items()},
        "summary": {
            "total_plugins": len(plugin_results),
            "plugins_passed": sum(1 for r in plugin_results.values() if r.status == "passed"),
            "plugins_warnings": sum(1 for r in plugin_results.values() if r.status == "warning"),
            "plugins_failed": sum(1 for r in plugin_results.values() if r.status == "failed"),
            "total_skills": len(skill_results),
            "skills_passed": sum(1 for r in skill_results.values() if r.status == "passed"),
            "skills_failed": sum(1 for r in skill_results.values() if r.status in ["warning", "failed"]),
        }
    }

    print(json.dumps(output, indent=2))


def _result_to_dict(result: ValidationResult) -> Dict[str, Any]:
    """Convert ValidationResult to dictionary"""
    return {
        "status": result.status,
        "errors": [
            {
                "check": issue.check,
                "message": issue.message,
                "file": issue.file,
                "line": issue.line
            }
            for issue in result.errors
        ],
        "warnings": [
            {
                "check": issue.check,
                "message": issue.message,
                "file": issue.file,
                "line": issue.line
            }
            for issue in result.warnings
        ]
    }


@click.command()
@click.option('--plugin', type=click.Path(exists=True, path_type=Path), help='Validate specific plugin')
@click.option('--skip-skills', is_flag=True, help='Skip skills validation (faster)')
@click.option('--output', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--no-color', is_flag=True, help='Disable colored output')
def main(plugin, skip_skills, output, verbose, no_color):
    """Validate Claude Code plugins in the marketplace"""
    if no_color:
        console.no_color = True

    # Determine marketplace root
    if plugin:
        marketplace_root = plugin.parent.parent if plugin.parent.name == 'plugins' else Path.cwd()
    else:
        marketplace_root = Path.cwd()

    # Validate root plugin
    root_result = None
    root_plugin_path = marketplace_root / '.claude-plugin' / 'plugin.json'
    if root_plugin_path.exists():
        validator = PluginJsonValidator(marketplace_root)
        root_result = validator.validate()

    # Validate marketplace.json
    marketplace_result = None
    marketplace_json_path = marketplace_root / '.claude-plugin' / 'marketplace.json'
    if marketplace_json_path.exists():
        validator = MarketplaceValidator(marketplace_root)
        marketplace_result = validator.validate()

    # Validate individual plugins
    plugin_results = {}
    skill_results = {}

    if plugin:
        # Validate single plugin
        plugins_to_validate = [plugin]
    else:
        # Validate all plugins
        plugins_dir = marketplace_root / 'plugins'
        plugins_to_validate = [p for p in plugins_dir.iterdir() if p.is_dir()] if plugins_dir.exists() else []

    for plugin_path in plugins_to_validate:
        plugin_name = plugin_path.name

        # Validate plugin.json
        validator = PluginJsonValidator(plugin_path)
        plugin_results[plugin_name] = validator.validate()

        # Validate skills
        if not skip_skills:
            skills_validator = SkillsValidator(plugin_path)
            skills = skills_validator.discover_skills()

            for skill_path in skills:
                skill_name = f"{plugin_name}/{skill_path.name}"
                skill_results[skill_name] = skills_validator.validate_skill(skill_path)

    # Print results
    if output == 'json':
        print_json_results(root_result, marketplace_result, plugin_results, skill_results)
    else:
        print_text_results(root_result, marketplace_result, plugin_results, skill_results)

    # Exit code
    has_errors = (
        (root_result and root_result.status == 'failed') or
        (marketplace_result and marketplace_result.status == 'failed') or
        any(r.status == 'failed' for r in plugin_results.values()) or
        any(r.status == 'failed' for r in skill_results.values())
    )

    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
