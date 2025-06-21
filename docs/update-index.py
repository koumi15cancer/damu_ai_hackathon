#!/usr/bin/env python3
"""
Documentation Index Updater

This script helps maintain the documentation index by scanning for new
documentation files and suggesting updates to the index.md file.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set

def scan_documentation_files(docs_dir: str = "docs") -> Dict[str, List[str]]:
    """Scan the docs directory and categorize files by directory."""
    categories = {}
    
    for root, dirs, files in os.walk(docs_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md') and file != 'index.md':
                rel_path = os.path.relpath(root, docs_dir)
                if rel_path == '.':
                    category = 'root'
                else:
                    category = rel_path
                
                if category not in categories:
                    categories[category] = []
                
                file_path = os.path.join(rel_path, file)
                categories[category].append(file_path)
    
    return categories

def extract_title_from_markdown(file_path: str) -> str:
    """Extract the title from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for first # heading
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('# '):
                return line.strip()[2:].strip()
        
        # Fallback to filename
        return os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
    except Exception:
        return os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()

def generate_index_suggestions(categories: Dict[str, List[str]]) -> str:
    """Generate suggestions for the index.md file."""
    suggestions = []
    
    # Map category names to display names
    category_display = {
        'root': 'Main Documentation',
        'architecture': 'Architecture & System Design',
        'backend': 'Backend Documentation',
        'frontend': 'Frontend Documentation',
        'api': 'API Documentation',
        'setup': 'Setup & Configuration',
        'features': 'Feature Documentation',
        'testing': 'Testing & Quality Assurance',
        'troubleshooting': 'Troubleshooting',
        'data': 'Data & Storage',
        'advanced': 'Advanced Topics',
        'security': 'Security',
        'monitoring': 'Monitoring & Analytics',
        'analytics': 'Analytics',
        'contributing': 'Contributing',
        'qa': 'Quality Assurance'
    }
    
    for category, files in sorted(categories.items()):
        if not files:
            continue
            
        display_name = category_display.get(category, category.title())
        suggestions.append(f"\n### {display_name}")
        
        for file_path in sorted(files):
            title = extract_title_from_markdown(f"docs/{file_path}")
            suggestions.append(f"- **[{title}]({file_path})** - {title}")
    
    return '\n'.join(suggestions)

def check_missing_files(index_content: str, categories: Dict[str, List[str]]) -> List[str]:
    """Check for files that exist but aren't in the index."""
    # Extract all links from index content
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    indexed_files = set()
    
    for match in re.finditer(link_pattern, index_content):
        link_path = match.group(2)
        if link_path.endswith('.md'):
            indexed_files.add(link_path)
    
    # Find files that aren't indexed
    all_files = set()
    for files in categories.values():
        all_files.update(files)
    
    missing_files = all_files - indexed_files
    return sorted(missing_files)

def main():
    """Main function to update documentation index."""
    print("📚 Documentation Index Updater")
    print("=" * 50)
    
    # Scan for documentation files
    categories = scan_documentation_files()
    
    print(f"\n📁 Found {sum(len(files) for files in categories.values())} documentation files:")
    for category, files in sorted(categories.items()):
        if files:
            print(f"  {category}: {len(files)} files")
    
    # Check current index
    index_path = "docs/index.md"
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        missing_files = check_missing_files(index_content, categories)
        
        if missing_files:
            print(f"\n⚠️  Found {len(missing_files)} files not in index:")
            for file_path in missing_files:
                print(f"  - {file_path}")
        else:
            print("\n✅ All documentation files are indexed!")
    else:
        print(f"\n⚠️  Index file not found at {index_path}")
    
    # Generate suggestions
    print("\n📝 Suggested index structure:")
    suggestions = generate_index_suggestions(categories)
    print(suggestions)
    
    # Save suggestions to file
    suggestions_path = "docs/index-suggestions.md"
    with open(suggestions_path, 'w', encoding='utf-8') as f:
        f.write("# Documentation Index Suggestions\n\n")
        f.write("Generated suggestions for updating docs/index.md:\n\n")
        f.write(suggestions)
    
    print(f"\n💾 Suggestions saved to {suggestions_path}")
    print("\nTo update the index:")
    print("1. Review the suggestions")
    print("2. Update docs/index.md with new entries")
    print("3. Remove this script's output file")

if __name__ == "__main__":
    main() 