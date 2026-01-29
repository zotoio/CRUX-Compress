#!/bin/bash
# CRUX Compress Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/zotoio/CRUX-Compress/main/install.sh | bash
#        curl -fsSL https://cdn.jsdelivr.net/gh/zotoio/CRUX-Compress@main/install.sh | bash
#        curl -fsSL .../install.sh | bash -s -- --backup --verbose
#        .crux/update.sh [-y] [--force] [--backup] [--verbose]
#
# Options:
#   -y         Non-interactive mode, assume yes to all confirmations
#   --force    Backup current installation and install regardless of version
#   --backup   Create backups of existing files before overwriting
#   --verbose  Show detailed progress
#   --help     Show this help message

set -e

# Configuration
REPO_OWNER="zotoio"
REPO_NAME="CRUX-Compress"
GITHUB_API="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest"
DOWNLOAD_BASE="https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download"
RAW_BASE="https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Options
BACKUP=false
VERBOSE=false
NON_INTERACTIVE=false
FORCE=false

# Detect script location for update.sh pattern
SCRIPT_DIR=""
PROJECT_ROOT=""

# Detect if running as update.sh from .crux directory
detect_script_location() {
    if [[ -n "${BASH_SOURCE[0]}" && "${BASH_SOURCE[0]}" != "" ]]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        # If script is in .crux directory, project root is parent
        if [[ "$(basename "$SCRIPT_DIR")" == ".crux" ]]; then
            PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
            cd "$PROJECT_ROOT"
        fi
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -y)
            NON_INTERACTIVE=true
            shift
            ;;
        --force)
            FORCE=true
            BACKUP=true  # Force always creates backup
            shift
            ;;
        --backup)
            BACKUP=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "CRUX Compress Installer"
            echo ""
            echo "Usage: curl -fsSL .../install.sh | bash -s -- [OPTIONS]"
            echo "       .crux/update.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -y         Non-interactive mode, assume yes to all confirmations"
            echo "  --force    Backup and install regardless of version"
            echo "  --backup   Create backups of existing files before overwriting"
            echo "  --verbose  Show detailed progress"
            echo "  --help     Show this help message"
            echo ""
            echo "This script installs CRUX Compress into the current directory."
            echo "It will create/update .cursor/ directory structure and add core files."
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

log() {
    echo -e "${BLUE}[CRUX]${NC} $1" >&2
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[CRUX]${NC} $1" >&2
    fi
}

log_success() {
    echo -e "${GREEN}[CRUX]${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}[CRUX]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[CRUX]${NC} $1" >&2
}

# Check if running within CRUX-Compress repository itself
check_not_in_crux_repo() {
    if [[ -f "CRUX.md" ]] && \
       grep -q "CRUX Rule Compression Specification" CRUX.md 2>/dev/null && \
       [[ -d "scripts" ]] && \
       [[ -f "scripts/create-crux-zip.sh" ]]; then
        log_error "Cannot install CRUX-Compress within its own repository."
        log_error "Run this script in a target project directory instead."
        exit 1
    fi
}

# Check for required tools
check_dependencies() {
    local missing=()
    
    if ! command -v curl &> /dev/null; then
        missing+=("curl")
    fi
    
    if ! command -v unzip &> /dev/null; then
        missing+=("unzip")
    fi
    
    if ! command -v zip &> /dev/null; then
        missing+=("zip")
    fi
    
    if ! command -v jq &> /dev/null; then
        # jq is optional, we can parse JSON with grep/sed if needed
        log_verbose "jq not found, using fallback JSON parsing"
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing[*]}"
        log_error "Please install them and try again."
        exit 1
    fi
}

# Detect git repository root
detect_git_root() {
    local git_root
    git_root=$(git rev-parse --show-toplevel 2>/dev/null) || true
    echo "$git_root"
}

# Prompt for confirmation
confirm() {
    local prompt="$1"
    local default="${2:-Y}"
    
    if [[ "$NON_INTERACTIVE" == "true" ]]; then
        return 0
    fi
    
    local yn_hint
    if [[ "$default" == "Y" ]]; then
        yn_hint="[Y/n]"
    else
        yn_hint="[y/N]"
    fi
    
    read -p "$prompt $yn_hint " -n 1 -r
    echo
    
    if [[ -z "$REPLY" ]]; then
        if [[ "$default" == "Y" ]]; then
            return 0
        else
            return 1
        fi
    fi
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Get the latest release version from GitHub API
get_latest_version() {
    local version
    
    if command -v jq &> /dev/null; then
        version=$(curl -fsSL "$GITHUB_API" | jq -r '.tag_name' 2>/dev/null)
    else
        # Fallback: parse JSON with grep/sed
        version=$(curl -fsSL "$GITHUB_API" | grep -o '"tag_name": *"[^"]*"' | sed 's/.*"v\?\([^"]*\)".*/\1/')
    fi
    
    # Remove 'v' prefix if present
    version="${version#v}"
    
    if [[ -z "$version" || "$version" == "null" ]]; then
        log_error "Failed to fetch latest version from GitHub"
        exit 1
    fi
    
    echo "$version"
}

# Get currently installed version
get_installed_version() {
    if [[ -f ".crux/crux.json" ]]; then
        if command -v jq &> /dev/null; then
            jq -r '.version' ".crux/crux.json" 2>/dev/null
        else
            # Fallback: parse JSON with grep/sed
            grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' ".crux/crux.json" | sed 's/.*"\([^"]*\)"$/\1/'
        fi
    else
        echo ""
    fi
}

# Compare versions (returns 0 if $1 > $2, 1 if $1 == $2, 2 if $1 < $2)
compare_versions() {
    if [[ "$1" == "$2" ]]; then
        return 1
    fi
    
    local IFS=.
    local i
    local -a ver1 ver2
    read -ra ver1 <<< "$1"
    read -ra ver2 <<< "$2"
    
    for ((i=0; i<${#ver1[@]} || i<${#ver2[@]}; i++)); do
        local v1=${ver1[i]:-0}
        local v2=${ver2[i]:-0}
        
        if ((v1 > v2)); then
            return 0
        elif ((v1 < v2)); then
            return 2
        fi
    done
    
    return 1
}

# Get version change type (major, minor, patch)
get_version_change_type() {
    local old_ver="$1"
    local new_ver="$2"
    
    local IFS=.
    local -a old_parts new_parts
    read -ra old_parts <<< "$old_ver"
    read -ra new_parts <<< "$new_ver"
    
    local old_major=${old_parts[0]:-0}
    local old_minor=${old_parts[1]:-0}
    local new_major=${new_parts[0]:-0}
    local new_minor=${new_parts[1]:-0}
    
    if [[ "$new_major" != "$old_major" ]]; then
        echo "major"
    elif [[ "$new_minor" != "$old_minor" ]]; then
        echo "minor"
    else
        echo "patch"
    fi
}

# Get files from release manifest
get_manifest_files() {
    local manifest=".crux/crux-release-files.json"
    if [[ -f "$manifest" ]] && command -v jq &> /dev/null; then
        jq -r '.allFiles | keys[]' "$manifest" 2>/dev/null || true
    fi
}

# Create comprehensive backup zip
create_backup_zip() {
    local repo_name timestamp backup_zip
    repo_name=$(basename "$(pwd)")
    timestamp=$(date +%Y%m%d%H%M%S)
    
    mkdir -p "/tmp/crux/${repo_name}"
    backup_zip="/tmp/crux/${repo_name}/crux-backup-${repo_name}-${timestamp}.zip"
    
    log "Creating backup..."
    
    # Collect files to backup
    local files_to_backup=()
    
    # Add files from release manifest if available
    while IFS= read -r file; do
        if [[ -f "$file" ]]; then
            files_to_backup+=("$file")
        fi
    done < <(get_manifest_files)
    
    # Add standard CRUX files that might exist
    local standard_files=(
        "CRUX.md"
        "AGENTS.md"
        ".crux/crux.json"
        ".crux/crux-release-files.json"
        ".cursor/hooks.json"
        ".cursor/agents/crux-cursor-rule-manager.md"
        ".cursor/commands/crux-compress.md"
        ".cursor/hooks/crux-detect-changes.sh"
        ".cursor/hooks/crux-session-start.sh"
        ".cursor/rules/_CRUX-RULE.mdc"
        ".cursor/skills/CRUX-Utils/SKILL.md"
        ".cursor/skills/CRUX-Utils/scripts/crux-utils.sh"
    )
    
    for file in "${standard_files[@]}"; do
        if [[ -f "$file" ]]; then
            # Add if not already in list
            local found=false
            for existing in "${files_to_backup[@]}"; do
                if [[ "$existing" == "$file" ]]; then
                    found=true
                    break
                fi
            done
            if [[ "$found" == "false" ]]; then
                files_to_backup+=("$file")
            fi
        fi
    done
    
    # Add all *.crux.* files
    while IFS= read -r file; do
        if [[ -f "$file" ]]; then
            files_to_backup+=("$file")
        fi
    done < <(find . -name "*.crux.*" -type f 2>/dev/null | sed 's|^\./||')
    
    if [[ ${#files_to_backup[@]} -eq 0 ]]; then
        log_verbose "No files to backup"
        echo ""
        return
    fi
    
    # Create backup zip with relative paths
    cd "$(pwd)"
    if zip -q "$backup_zip" "${files_to_backup[@]}" 2>/dev/null; then
        log_verbose "Backup created: $backup_zip"
        echo "$backup_zip"
    else
        log_warn "Failed to create backup zip"
        echo ""
    fi
}

# Backup a file if it exists (legacy single-file backup)
backup_file() {
    local file="$1"
    if [[ -f "$file" && "$BACKUP" == "true" ]]; then
        local backup
        backup="${file}.backup.$(date +%Y%m%d%H%M%S)"
        cp "$file" "$backup"
        log_verbose "Backed up: $file -> $backup"
    fi
}

# Show colored diff between two files
show_file_diff() {
    local old_file="$1"
    local new_file="$2"
    
    if [[ ! -f "$old_file" ]] || [[ ! -f "$new_file" ]]; then
        return
    fi
    
    if command -v diff &>/dev/null; then
        # Check if terminal supports colors
        if [[ -t 1 ]] && command -v tput &>/dev/null && [[ $(tput colors 2>/dev/null) -ge 8 ]]; then
            diff --color=always -u "$old_file" "$new_file" 2>/dev/null | head -20 || true
        else
            diff -u "$old_file" "$new_file" 2>/dev/null | head -20 || true
        fi
    fi
}

# Get file checksum (portable across Linux/macOS)
get_checksum() {
    local file="$1"
    if command -v sha256sum &>/dev/null; then
        sha256sum "$file" 2>/dev/null | cut -d' ' -f1
    elif command -v shasum &>/dev/null; then
        shasum -a 256 "$file" 2>/dev/null | cut -d' ' -f1
    elif command -v md5sum &>/dev/null; then
        md5sum "$file" 2>/dev/null | cut -d' ' -f1
    elif command -v md5 &>/dev/null; then
        md5 -q "$file" 2>/dev/null
    else
        # Fallback: use file size + first/last bytes as pseudo-checksum
        stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null
    fi
}

# Preview files to be installed
preview_installation() {
    local staging_dir="$1"
    local show_diff="${2:-false}"
    
    echo ""
    echo "Files to be installed/updated:"
    echo ""
    
    while IFS= read -r file; do
        local rel_path="${file#"$staging_dir"/}"
        
        if [[ -f "$rel_path" ]]; then
            # File exists - compare checksums
            local existing_checksum staged_checksum
            existing_checksum=$(get_checksum "$rel_path")
            staged_checksum=$(get_checksum "$file")
            
            if [[ "$existing_checksum" == "$staged_checksum" ]]; then
                # Files are identical
                echo -e "  ${BLUE}[NO CHANGE]${NC} $rel_path"
            else
                # File will be updated
                echo -e "  ${YELLOW}[UPDATE]${NC} $rel_path"
                if [[ "$show_diff" == "true" ]]; then
                    show_file_diff "$rel_path" "$file"
                    echo ""
                fi
            fi
        else
            # New file
            echo -e "  ${GREEN}[CREATE]${NC} $rel_path"
        fi
    done < <(find "$staging_dir" -type f | sort)
    
    echo ""
}

# Upsert CRUX block into AGENTS.md
# If AGENTS.md exists with a CRUX block, replace it
# If AGENTS.md exists without a CRUX block, prepend it
# If AGENTS.md doesn't exist, create it with just the CRUX block
upsert_agents_crux_block() {
    local crux_block_file="$1"
    
    if [[ ! -f "$crux_block_file" ]]; then
        log_warn "No AGENTS.crux.md found, skipping AGENTS.md update"
        return
    fi
    
    local crux_content
    crux_content=$(cat "$crux_block_file")
    
    if [[ -f "AGENTS.md" ]]; then
        if grep -q '<CRUX' "AGENTS.md"; then
            # Replace existing CRUX block
            log_verbose "Updating existing CRUX block in AGENTS.md..."
            
            # Create temp file with replaced content
            local temp_file
            temp_file=$(mktemp)
            
            # Use awk to replace the block between <CRUX and </CRUX> (inclusive)
            awk -v new_block="$crux_content" '
                /<CRUX/ { in_block=1; print new_block; next }
                /<\/CRUX>/ { in_block=0; next }
                !in_block { print }
            ' "AGENTS.md" > "$temp_file"
            
            mv "$temp_file" "AGENTS.md"
            log_success "Updated CRUX block in AGENTS.md"
        else
            # Prepend CRUX block to existing AGENTS.md
            log_verbose "Prepending CRUX block to AGENTS.md..."
            
            local temp_file
            temp_file=$(mktemp)
            
            echo "$crux_content" > "$temp_file"
            echo "" >> "$temp_file"
            cat "AGENTS.md" >> "$temp_file"
            
            mv "$temp_file" "AGENTS.md"
            log_success "Added CRUX block to AGENTS.md"
        fi
    else
        # Create new AGENTS.md with just the CRUX block
        log_verbose "Creating AGENTS.md with CRUX block..."
        echo "$crux_content" > "AGENTS.md"
        log_success "Created AGENTS.md with CRUX block"
    fi
    
    # Remove the temporary AGENTS.crux.md file
    rm -f "$crux_block_file"
    log_verbose "Removed AGENTS.crux.md"
}

# Merge CRUX hooks into hooks.json
# If hooks.json doesn't exist, create it
# If it exists, upsert CRUX hooks into each array (avoiding duplicates)
merge_hooks_json() {
    local staging_hooks="$1"
    local target_hooks=".cursor/hooks.json"
    
    if [[ ! -f "$staging_hooks" ]]; then
        log_warn "No hooks.json in staging, skipping hooks merge"
        return
    fi
    
    mkdir -p .cursor
    
    if [[ ! -f "$target_hooks" ]]; then
        # No existing hooks.json - just copy the new one
        cp "$staging_hooks" "$target_hooks"
        log_success "Created $target_hooks"
        return
    fi
    
    # Existing hooks.json found - need to merge
    log_verbose "Merging CRUX hooks into existing $target_hooks..."
    
    if command -v jq &>/dev/null; then
        # Use jq for proper JSON merging
        local temp_file
        temp_file=$(mktemp)
        
        # Merge each hook array, avoiding duplicates based on command
        jq -s '
            # Define a function to merge hook arrays by command (avoiding duplicates)
            # Handle null arrays gracefully with // []
            def merge_hooks(existing; new):
                (existing // []) + [(new // [])[] | select(. as $n | (existing // []) | all(.command != $n.command))];
            
            # $existing is .[0], $new is .[1]
            .[0] as $existing | .[1] as $new |
            
            # Build merged hooks object, only including non-empty arrays
            (
                ["sessionStart", "afterFileEdit", "stop"] | 
                map(. as $hook | 
                    merge_hooks(($existing.hooks // {})[$hook]; ($new.hooks // {})[$hook]) |
                    if length > 0 then {($hook): .} else {} end
                ) | add // {}
            ) as $merged_hooks |
            
            # Preserve existing structure, update/add hooks
            $existing | .hooks = ((.hooks // {}) + $merged_hooks)
        ' "$target_hooks" "$staging_hooks" > "$temp_file"
        
        if [[ -s "$temp_file" ]]; then
            mv "$temp_file" "$target_hooks"
            log_success "Merged CRUX hooks into $target_hooks"
        else
            rm -f "$temp_file"
            log_warn "Failed to merge hooks.json with jq, copying fresh"
            cp "$staging_hooks" "$target_hooks"
        fi
    else
        # Fallback without jq - just copy (user will need to manually merge)
        log_warn "jq not available - overwriting hooks.json (manual merge may be needed)"
        cp "$staging_hooks" "$target_hooks"
    fi
}

# Download and stage the release (without installing)
download_and_stage() {
    local version="$1"
    local zip_name="CRUX-Compress-v${version}.zip"
    local download_url="${DOWNLOAD_BASE}/v${version}/${zip_name}"
    local staging_dir
    
    staging_dir=$(mktemp -d)
    
    log "Downloading CRUX Compress v${version}..."
    log_verbose "URL: $download_url"
    
    if ! curl -fsSL "$download_url" -o "$staging_dir/$zip_name"; then
        log_error "Failed to download release"
        rm -rf "$staging_dir"
        exit 1
    fi
    
    # Extract to staging directory
    if ! unzip -o -q "$staging_dir/$zip_name" -d "$staging_dir/content"; then
        log_error "Failed to extract archive"
        rm -rf "$staging_dir"
        exit 1
    fi
    
    rm "$staging_dir/$zip_name"
    echo "$staging_dir/content"
}

# Install from staging directory
install_from_staging() {
    local staging_dir="$1"
    
    log "Installing CRUX files..."
    
    # Save staging hooks.json path before copying (for merge later)
    local staging_hooks=""
    if [[ -f "$staging_dir/.cursor/hooks.json" ]]; then
        staging_hooks=$(mktemp)
        cp "$staging_dir/.cursor/hooks.json" "$staging_hooks"
    fi
    
    # Copy all files from staging to current directory, excluding hooks.json
    if command -v rsync &>/dev/null; then
        rsync -a --exclude='.cursor/hooks.json' "$staging_dir/" .
    else
        # Remove hooks.json from staging before copy to avoid overwrite
        rm -f "$staging_dir/.cursor/hooks.json" 2>/dev/null || true
        cp -r "$staging_dir/"* . 2>/dev/null || true
        cp -r "$staging_dir/".* . 2>/dev/null || true
    fi
    
    # Merge CRUX hooks into hooks.json (upsert, preserving user hooks)
    if [[ -n "$staging_hooks" && -f "$staging_hooks" ]]; then
        merge_hooks_json "$staging_hooks"
        rm -f "$staging_hooks"
    fi
    
    # Upsert CRUX block into AGENTS.md and remove AGENTS.crux.md
    if [[ -f "AGENTS.crux.md" ]]; then
        upsert_agents_crux_block "AGENTS.crux.md"
    fi
    
    # Make scripts executable
    chmod +x .cursor/hooks/crux-detect-changes.sh 2>/dev/null || true
    chmod +x .cursor/hooks/crux-session-start.sh 2>/dev/null || true
    chmod +x .cursor/skills/CRUX-Utils/scripts/crux-utils.sh 2>/dev/null || true
}

# Download update.sh for future updates
download_update_script() {
    mkdir -p .crux
    log_verbose "Downloading update script..."
    if curl -fsSL "${RAW_BASE}/install.sh" -o ".crux/update.sh" 2>/dev/null; then
        chmod +x ".crux/update.sh"
        log_verbose "Update script saved to .crux/update.sh"
    fi
}

# Show completion report
show_completion_report() {
    local version="$1"
    local backup_zip="$2"
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     Installation Complete!            ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
    echo ""
    log_success "CRUX Compress v${version} installed successfully!"
    echo ""
    
    if [[ -n "$backup_zip" && -f "$backup_zip" ]]; then
        echo "Backup saved to:"
        echo "  $backup_zip"
        echo ""
        echo "To revert this update:"
        echo -e "  ${CYAN}# Remove installed CRUX files${NC}"
        echo "  rm -rf .crux .cursor/agents/crux-cursor-rule-manager.md \\"
        echo "         .cursor/commands/crux-compress.md \\"
        echo "         .cursor/hooks/crux-detect-changes.sh \\"
        echo "         .cursor/hooks/crux-session-start.sh \\"
        echo "         .cursor/rules/_CRUX-RULE.mdc \\"
        echo "         .cursor/skills/CRUX-Utils CRUX.md"
        echo ""
        echo -e "  ${CYAN}# Restore from backup${NC}"
        echo "  unzip -o '$backup_zip'"
        echo ""
    fi
    
    echo "Next steps:"
    echo "  1. Ensure .cursor/hooks.json is recognized by Cursor"
    echo "  2. Add 'crux: true' to any rule files you want to compress"
    echo "  3. Use /crux-compress ALL to compress eligible files"
    echo ""
    echo "For updates, run:"
    echo "  .crux/update.sh"
    echo ""
    echo "Documentation: https://github.com/${REPO_OWNER}/${REPO_NAME}"
    echo ""
}

# Main installation flow
main() {
    # Clear terminal
    clear
    
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     CRUX Compress Installer           ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
    echo ""
    
    # Detect if running from .crux/update.sh
    detect_script_location
    
    # Check if running within CRUX-Compress repo itself
    check_not_in_crux_repo
    
    check_dependencies
    
    # Detect git repository
    local git_root
    git_root=$(detect_git_root)
    
    if [[ -n "$git_root" ]]; then
        log_verbose "Git repository detected: $git_root"
        cd "$git_root"
    else
        log_warn "Not in a git repository."
        echo ""
        echo "It's recommended to run this script from an initialized git repository."
        echo "You can initialize one with: git init"
        echo ""
        if ! confirm "Continue anyway and treat current directory as project root?"; then
            log "Installation cancelled."
            exit 0
        fi
    fi
    
    log "Checking for latest version..."
    local latest_version
    latest_version=$(get_latest_version)
    
    local installed_version
    installed_version=$(get_installed_version)
    
    local backup_zip=""
    local should_install=true
    local change_type=""
    
    if [[ -n "$installed_version" ]]; then
        log "Detected CRUX version: ${installed_version}"
        log "Latest version: v${latest_version}"
        echo ""
        
        if compare_versions "$latest_version" "$installed_version"; then
            # Newer version available
            change_type=$(get_version_change_type "$installed_version" "$latest_version")
            
            case "$change_type" in
                major)
                    echo -e "${YELLOW}MAJOR version update (${installed_version} → ${latest_version})${NC}"
                    echo ""
                    log_warn "This is a major version update!"
                    echo "After installation, regenerate all CRUX files using:"
                    echo "  /crux-compress ALL --force"
                    echo ""
                    ;;
                minor)
                    echo -e "${CYAN}Minor version update (${installed_version} → ${latest_version})${NC}"
                    echo ""
                    ;;
                patch)
                    echo -e "${GREEN}Patch update (${installed_version} → ${latest_version})${NC}"
                    echo ""
                    ;;
            esac
            
        elif [[ "$latest_version" == "$installed_version" ]]; then
            log_warn "Already at latest version (v${installed_version})"
            echo ""
            if [[ "$FORCE" == "true" ]]; then
                log "Force reinstall requested..."
            else
                echo "To reinstall anyway, run with --force"
                exit 0
            fi
        else
            log_warn "Installed version (v${installed_version}) is newer than latest release (v${latest_version})"
            echo ""
            if [[ "$FORCE" == "true" ]]; then
                log "Force downgrade requested..."
            elif ! confirm "Downgrade?"; then
                log "Installation cancelled."
                exit 0
            fi
        fi
        
        # Create backup for upgrades
        if [[ "$should_install" == "true" ]]; then
            backup_zip=$(create_backup_zip)
            if [[ -n "$backup_zip" ]]; then
                log_success "Backup created: $backup_zip"
            fi
        fi
    else
        log "Fresh installation of v${latest_version}"
    fi
    
    # Download and stage files
    local staging_dir
    staging_dir=$(download_and_stage "$latest_version")
    
    # Preview installation
    preview_installation "$staging_dir" "$VERBOSE"
    
    # Confirm installation
    if ! confirm "Proceed with installation?"; then
        rm -rf "$(dirname "$staging_dir")"
        log "Installation cancelled."
        exit 0
    fi
    
    # Install files
    install_from_staging "$staging_dir"
    
    # Cleanup staging
    rm -rf "$(dirname "$staging_dir")"
    
    # Download update script for future updates
    download_update_script
    
    # Show completion report
    show_completion_report "$latest_version" "$backup_zip"
}

# Only run main if executed directly (not sourced)
# Handle both direct execution and piped via curl (where BASH_SOURCE is empty)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]] || [[ -z "${BASH_SOURCE[0]}" ]]; then
    main
fi
