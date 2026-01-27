#!/bin/bash
# CRUX Compress Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/zotoio/CRUX-Compress/main/install.sh | bash
#        curl -fsSL .../install.sh | bash -s -- --backup --verbose
#
# Options:
#   --backup   Create backups of existing files before overwriting
#   --verbose  Show detailed progress
#   --help     Show this help message

set -e

# Configuration
REPO_OWNER="zotoio"
REPO_NAME="CRUX-Compress"
GITHUB_API="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest"
DOWNLOAD_BASE="https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Options
BACKUP=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
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
            echo ""
            echo "Options:"
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
    echo -e "${BLUE}[CRUX]${NC} $1"
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[CRUX]${NC} $1"
    fi
}

log_success() {
    echo -e "${GREEN}[CRUX]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[CRUX]${NC} $1"
}

log_error() {
    echo -e "${RED}[CRUX]${NC} $1"
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
    if [[ -f "VERSION" ]]; then
        tr -d '[:space:]' < "VERSION"
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

# Backup a file if it exists
backup_file() {
    local file="$1"
    if [[ -f "$file" && "$BACKUP" == "true" ]]; then
        local backup
        backup="${file}.backup.$(date +%Y%m%d%H%M%S)"
        cp "$file" "$backup"
        log_verbose "Backed up: $file -> $backup"
    fi
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

# Download and extract the release
download_and_extract() {
    local version="$1"
    local zip_name="CRUX-Compress-v${version}.zip"
    local download_url="${DOWNLOAD_BASE}/v${version}/${zip_name}"
    local temp_dir
    
    temp_dir=$(mktemp -d)
    trap 'rm -rf "$temp_dir"' EXIT
    
    log "Downloading CRUX Compress v${version}..."
    log_verbose "URL: $download_url"
    
    if ! curl -fsSL "$download_url" -o "$temp_dir/$zip_name"; then
        log_error "Failed to download release"
        exit 1
    fi
    
    # Backup existing files if requested (BEFORE extraction overwrites them)
    if [[ "$BACKUP" == "true" ]]; then
        log "Creating backups of existing files..."
        backup_file "CRUX.md"
        backup_file "AGENTS.md"
        backup_file "VERSION"
        backup_file ".cursor/hooks.json"
        backup_file ".cursor/agents/crux-cursor-rule-manager.md"
        backup_file ".cursor/commands/crux-compress.md"
        backup_file ".cursor/hooks/detect-crux-changes.sh"
        backup_file ".cursor/rules/_CRUX-RULE.mdc"
        backup_file ".cursor/skills/CRUX-Utils/SKILL.md"
        backup_file ".cursor/skills/CRUX-Utils/scripts/crux-utils.sh"
    fi
    
    log "Installing CRUX files..."
    log_verbose "Extracting archive..."
    
    # Extract directly to current directory, overlaying existing files
    if ! unzip -o -q "$temp_dir/$zip_name" -d .; then
        log_error "Failed to extract archive"
        exit 1
    fi
    
    # Upsert CRUX block into AGENTS.md and remove AGENTS.crux.md
    if [[ -f "AGENTS.crux.md" ]]; then
        upsert_agents_crux_block "AGENTS.crux.md"
    fi
    
    # Make scripts executable
    chmod +x .cursor/hooks/detect-crux-changes.sh 2>/dev/null || true
    chmod +x .cursor/skills/CRUX-Utils/scripts/crux-utils.sh 2>/dev/null || true
    
    log_success "CRUX Compress v${version} installed successfully!"
}

# Main installation flow
main() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     CRUX Compress Installer           ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
    echo ""
    
    check_dependencies
    
    log "Checking for latest version..."
    local latest_version
    latest_version=$(get_latest_version)
    
    local installed_version
    installed_version=$(get_installed_version)
    
    if [[ -n "$installed_version" ]]; then
        log "Current version: v${installed_version}"
        log "Latest version:  v${latest_version}"
        
        if compare_versions "$latest_version" "$installed_version"; then
            log "Upgrading from v${installed_version} to v${latest_version}..."
        elif [[ "$latest_version" == "$installed_version" ]]; then
            log_warn "Already at latest version (v${installed_version})"
            read -p "Reinstall anyway? [y/N] " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log "Installation cancelled."
                exit 0
            fi
        else
            log_warn "Installed version (v${installed_version}) is newer than latest release (v${latest_version})"
            read -p "Downgrade? [y/N] " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log "Installation cancelled."
                exit 0
            fi
        fi
    else
        log "Fresh installation of v${latest_version}"
    fi
    
    download_and_extract "$latest_version"
    
    echo ""
    log_success "Installation complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure .cursor/hooks.json is recognized by Cursor"
    echo "  2. Add 'crux: true' to any rule files you want to compress"
    echo "  3. Use /crux-compress ALL to compress eligible files"
    echo ""
    echo "Documentation: https://github.com/${REPO_OWNER}/${REPO_NAME}"
    echo ""
}

# Only run main if executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
