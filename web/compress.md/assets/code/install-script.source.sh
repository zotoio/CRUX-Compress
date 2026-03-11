#!/usr/bin/env bash
# ==============================================================================
# System Health Check & Report Generator
# ==============================================================================
#
# A comprehensive system health checking script that gathers information about
# the current machine, runs various diagnostics, and produces a formatted
# report. Designed to be safe to run on any system without side effects.
#
# Usage:
#   ./script-original.sh                    # Run all checks, output to stdout
#   ./script-original.sh --output report    # Save report to report.txt
#   ./script-original.sh --json             # Output as JSON
#   ./script-original.sh --section disk     # Run only disk section
#   ./script-original.sh --verbose          # Include extra detail
#   ./script-original.sh --help             # Show usage information
#
# Exit Codes:
#   0 - All checks passed
#   1 - One or more warnings detected
#   2 - One or more critical issues found
#   3 - Script error (invalid arguments, missing dependencies)
#
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Constants & Configuration
# ------------------------------------------------------------------------------

readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
readonly TIMESTAMP="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
readonly HOSTNAME_SHORT="$(hostname -s 2>/dev/null || echo 'unknown')"

# Thresholds for health checks
readonly DISK_WARN_PERCENT=80
readonly DISK_CRIT_PERCENT=95
readonly MEM_WARN_PERCENT=85
readonly MEM_CRIT_PERCENT=95
readonly LOAD_WARN_MULTIPLIER=2
readonly LOAD_CRIT_MULTIPLIER=4
readonly UPTIME_WARN_DAYS=90
readonly MAX_ZOMBIE_PROCS=5

# Output formatting
readonly COLOR_RED='\033[0;31m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_YELLOW='\033[1;33m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_CYAN='\033[0;36m'
readonly COLOR_BOLD='\033[1m'
readonly COLOR_RESET='\033[0m'

# Report sections available
readonly ALL_SECTIONS=("system" "cpu" "memory" "disk" "network" "process" "security" "environment")

# Global state
declare -a WARNINGS=()
declare -a CRITICALS=()
declare -a REPORT_LINES=()
OUTPUT_FILE=""
OUTPUT_FORMAT="text"
SELECTED_SECTIONS=()
VERBOSE=false
USE_COLOR=true

# ------------------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------------------

# Print a message to stderr for logging purposes
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date '+%H:%M:%S')"

    case "$level" in
        INFO)  echo "[$timestamp] INFO:  $message" >&2 ;;
        WARN)  echo "[$timestamp] WARN:  $message" >&2 ;;
        ERROR) echo "[$timestamp] ERROR: $message" >&2 ;;
        DEBUG)
            if [[ "$VERBOSE" == true ]]; then
                echo "[$timestamp] DEBUG: $message" >&2
            fi
            ;;
    esac
}

# Append a line to the report buffer
report_add() {
    REPORT_LINES+=("$1")
}

# Print a formatted section header
section_header() {
    local title="$1"
    local width=60
    local padding
    padding=$(( (width - ${#title} - 2) / 2 ))
    local line
    line="$(printf '%*s' "$width" '' | tr ' ' '=')"
    local pad_str
    pad_str="$(printf '%*s' "$padding" '')"

    report_add ""
    report_add "$line"
    report_add "${pad_str} ${title} ${pad_str}"
    report_add "$line"
}

# Format a key-value pair for display
format_kv() {
    local key="$1"
    local value="$2"
    local width="${3:-30}"
    printf "  %-${width}s %s" "$key:" "$value"
}

# Determine status label based on value and thresholds
status_label() {
    local value="$1"
    local warn_threshold="$2"
    local crit_threshold="$3"

    if (( value >= crit_threshold )); then
        echo "CRITICAL"
    elif (( value >= warn_threshold )); then
        echo "WARNING"
    else
        echo "OK"
    fi
}

# Add a colored status indicator
format_status() {
    local status="$1"
    if [[ "$USE_COLOR" == true ]]; then
        case "$status" in
            OK)       echo -e "${COLOR_GREEN}[OK]${COLOR_RESET}" ;;
            WARNING)  echo -e "${COLOR_YELLOW}[WARNING]${COLOR_RESET}" ;;
            CRITICAL) echo -e "${COLOR_RED}[CRITICAL]${COLOR_RESET}" ;;
            INFO)     echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET}" ;;
        esac
    else
        echo "[$status]"
    fi
}

# Record a warning for the final summary
record_warning() {
    local message="$1"
    WARNINGS+=("$message")
    log WARN "$message"
}

# Record a critical issue for the final summary
record_critical() {
    local message="$1"
    CRITICALS+=("$message")
    log ERROR "$message"
}

# Check if a command exists
command_exists() {
    command -v "$1" &>/dev/null
}

# Safely read a file, returning a default if it doesn't exist
safe_read() {
    local file="$1"
    local default="${2:-N/A}"
    if [[ -r "$file" ]]; then
        cat "$file" 2>/dev/null || echo "$default"
    else
        echo "$default"
    fi
}

# Convert bytes to human-readable format
human_bytes() {
    local bytes="$1"
    if (( bytes >= 1073741824 )); then
        printf "%.1f GB" "$(echo "scale=1; $bytes / 1073741824" | bc 2>/dev/null || echo '?')"
    elif (( bytes >= 1048576 )); then
        printf "%.1f MB" "$(echo "scale=1; $bytes / 1048576" | bc 2>/dev/null || echo '?')"
    elif (( bytes >= 1024 )); then
        printf "%.1f KB" "$(echo "scale=1; $bytes / 1024" | bc 2>/dev/null || echo '?')"
    else
        printf "%d B" "$bytes"
    fi
}

# Convert seconds to a human-readable duration string
human_duration() {
    local total_seconds="$1"
    local days=$(( total_seconds / 86400 ))
    local hours=$(( (total_seconds % 86400) / 3600 ))
    local minutes=$(( (total_seconds % 3600) / 60 ))

    if (( days > 0 )); then
        printf "%dd %dh %dm" "$days" "$hours" "$minutes"
    elif (( hours > 0 )); then
        printf "%dh %dm" "$hours" "$minutes"
    else
        printf "%dm" "$minutes"
    fi
}

# Calculate a simple percentage
calc_percent() {
    local used="$1"
    local total="$2"
    if (( total == 0 )); then
        echo 0
        return
    fi
    echo $(( (used * 100) / total ))
}

# ------------------------------------------------------------------------------
# System Information Section
# ------------------------------------------------------------------------------

check_system_info() {
    section_header "SYSTEM INFORMATION"
    log INFO "Gathering system information..."

    # Basic system identification
    local os_name
    os_name="$(uname -s 2>/dev/null || echo 'Unknown')"

    local os_release="Unknown"
    if [[ -f /etc/os-release ]]; then
        os_release="$(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d'"' -f2)"
    elif command_exists sw_vers; then
        os_release="macOS $(sw_vers -productVersion 2>/dev/null || echo '?')"
    fi

    local kernel_version
    kernel_version="$(uname -r 2>/dev/null || echo 'Unknown')"

    local architecture
    architecture="$(uname -m 2>/dev/null || echo 'Unknown')"

    local uptime_seconds=0
    if [[ -f /proc/uptime ]]; then
        uptime_seconds="$(awk '{printf "%d", $1}' /proc/uptime 2>/dev/null || echo 0)"
    elif command_exists sysctl; then
        local boot_time
        boot_time="$(sysctl -n kern.boottime 2>/dev/null | awk '{print $4}' | tr -d ',')"
        if [[ -n "$boot_time" ]]; then
            uptime_seconds=$(( $(date +%s) - boot_time ))
        fi
    fi

    local uptime_human
    uptime_human="$(human_duration "$uptime_seconds")"
    local uptime_days=$(( uptime_seconds / 86400 ))

    # Current user and shell
    local current_user
    current_user="$(whoami 2>/dev/null || echo 'unknown')"
    local current_shell
    current_shell="$(basename "${SHELL:-unknown}")"

    # Timezone
    local timezone
    timezone="$(date +%Z 2>/dev/null || echo 'Unknown')"

    report_add "$(format_kv 'Hostname' "$HOSTNAME_SHORT")"
    report_add "$(format_kv 'OS' "$os_release")"
    report_add "$(format_kv 'Kernel' "$os_name $kernel_version")"
    report_add "$(format_kv 'Architecture' "$architecture")"
    report_add "$(format_kv 'Uptime' "$uptime_human ($uptime_days days)")"
    report_add "$(format_kv 'Current User' "$current_user")"
    report_add "$(format_kv 'Shell' "$current_shell")"
    report_add "$(format_kv 'Timezone' "$timezone")"
    report_add "$(format_kv 'Report Time' "$TIMESTAMP")"

    # Uptime check
    if (( uptime_days > UPTIME_WARN_DAYS )); then
        record_warning "System uptime is $uptime_days days (threshold: $UPTIME_WARN_DAYS). Consider scheduling a reboot."
    fi

    if [[ "$VERBOSE" == true ]]; then
        report_add ""
        report_add "  Additional Details:"
        report_add "$(format_kv '  Script Version' "$SCRIPT_VERSION")"
        report_add "$(format_kv '  Script Path' "$SCRIPT_DIR")"
        report_add "$(format_kv '  PID' "$$")"
        report_add "$(format_kv '  PPID' "$PPID")"
    fi
}

# ------------------------------------------------------------------------------
# CPU Section
# ------------------------------------------------------------------------------

check_cpu() {
    section_header "CPU INFORMATION"
    log INFO "Checking CPU status..."

    # CPU model and count
    local cpu_model="Unknown"
    local cpu_cores=1
    local cpu_threads=1

    if [[ -f /proc/cpuinfo ]]; then
        cpu_model="$(grep -m1 'model name' /proc/cpuinfo 2>/dev/null | cut -d':' -f2 | xargs || echo 'Unknown')"
        cpu_cores="$(grep -c '^processor' /proc/cpuinfo 2>/dev/null || echo 1)"
        cpu_threads="$cpu_cores"
    elif command_exists sysctl; then
        cpu_model="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Unknown')"
        cpu_cores="$(sysctl -n hw.ncpu 2>/dev/null || echo 1)"
        cpu_threads="$cpu_cores"
    fi

    # Load averages
    local load_1="" load_5="" load_15=""
    if [[ -f /proc/loadavg ]]; then
        read -r load_1 load_5 load_15 _ _ < /proc/loadavg 2>/dev/null
    elif command_exists sysctl; then
        local loadavg
        loadavg="$(sysctl -n vm.loadavg 2>/dev/null | tr -d '{}')"
        load_1="$(echo "$loadavg" | awk '{print $1}')"
        load_5="$(echo "$loadavg" | awk '{print $2}')"
        load_15="$(echo "$loadavg" | awk '{print $3}')"
    fi

    report_add "$(format_kv 'CPU Model' "$cpu_model")"
    report_add "$(format_kv 'CPU Cores/Threads' "$cpu_cores / $cpu_threads")"
    report_add "$(format_kv 'Load Average (1m)' "${load_1:-N/A}")"
    report_add "$(format_kv 'Load Average (5m)' "${load_5:-N/A}")"
    report_add "$(format_kv 'Load Average (15m)' "${load_15:-N/A}")"

    # Load assessment
    if [[ -n "$load_1" ]]; then
        local load_int
        load_int="$(printf '%.0f' "$load_1" 2>/dev/null || echo 0)"
        local warn_load=$(( cpu_cores * LOAD_WARN_MULTIPLIER ))
        local crit_load=$(( cpu_cores * LOAD_CRIT_MULTIPLIER ))
        local load_status
        load_status="$(status_label "$load_int" "$warn_load" "$crit_load")"
        report_add "$(format_kv 'Load Status' "$(format_status "$load_status") (warn>$warn_load, crit>$crit_load)")"

        if [[ "$load_status" == "CRITICAL" ]]; then
            record_critical "CPU load ($load_1) exceeds critical threshold ($crit_load) for $cpu_cores cores"
        elif [[ "$load_status" == "WARNING" ]]; then
            record_warning "CPU load ($load_1) exceeds warning threshold ($warn_load) for $cpu_cores cores"
        fi
    fi

    # Top CPU consumers (if available)
    if [[ "$VERBOSE" == true ]] && command_exists ps; then
        report_add ""
        report_add "  Top 5 CPU Consumers:"
        report_add "  $(printf '%-8s %-6s %-6s %s' 'PID' '%CPU' '%MEM' 'COMMAND')"
        while IFS= read -r line; do
            report_add "  $line"
        done < <(ps aux --sort=-%cpu 2>/dev/null | head -6 | tail -5 | awk '{printf "%-8s %-6s %-6s %s\n", $2, $3, $4, $11}' 2>/dev/null || echo "  (unable to list processes)")
    fi
}

# ------------------------------------------------------------------------------
# Memory Section
# ------------------------------------------------------------------------------

check_memory() {
    section_header "MEMORY INFORMATION"
    log INFO "Checking memory status..."

    local mem_total=0 mem_used=0 mem_free=0 mem_available=0
    local swap_total=0 swap_used=0 swap_free=0

    if [[ -f /proc/meminfo ]]; then
        mem_total="$(awk '/^MemTotal:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
        mem_free="$(awk '/^MemFree:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
        mem_available="$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
        swap_total="$(awk '/^SwapTotal:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
        swap_free="$(awk '/^SwapFree:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"

        # Values from /proc/meminfo are in KB
        mem_total=$(( mem_total * 1024 ))
        mem_free=$(( mem_free * 1024 ))
        mem_available=$(( mem_available * 1024 ))
        mem_used=$(( mem_total - mem_available ))
        swap_total=$(( swap_total * 1024 ))
        swap_free=$(( swap_free * 1024 ))
        swap_used=$(( swap_total - swap_free ))
    elif command_exists vm_stat; then
        # macOS memory
        local page_size
        page_size="$(sysctl -n hw.pagesize 2>/dev/null || echo 4096)"
        local pages_free pages_active pages_inactive pages_wired
        pages_free="$(vm_stat 2>/dev/null | awk '/Pages free/ {gsub(/\./,""); print $3}')"
        pages_active="$(vm_stat 2>/dev/null | awk '/Pages active/ {gsub(/\./,""); print $3}')"
        pages_inactive="$(vm_stat 2>/dev/null | awk '/Pages inactive/ {gsub(/\./,""); print $3}')"
        pages_wired="$(vm_stat 2>/dev/null | awk '/Pages wired/ {gsub(/\./,""); print $4}')"

        mem_total="$(sysctl -n hw.memsize 2>/dev/null || echo 0)"
        mem_free=$(( (pages_free + pages_inactive) * page_size ))
        mem_used=$(( (pages_active + pages_wired) * page_size ))
        mem_available=$(( mem_total - mem_used ))
    fi

    local mem_percent
    mem_percent="$(calc_percent "$mem_used" "$mem_total")"
    local mem_status
    mem_status="$(status_label "$mem_percent" "$MEM_WARN_PERCENT" "$MEM_CRIT_PERCENT")"

    report_add "$(format_kv 'Total Memory' "$(human_bytes "$mem_total")")"
    report_add "$(format_kv 'Used Memory' "$(human_bytes "$mem_used") (${mem_percent}%)")"
    report_add "$(format_kv 'Available Memory' "$(human_bytes "$mem_available")")"
    report_add "$(format_kv 'Memory Status' "$(format_status "$mem_status")")"

    if (( swap_total > 0 )); then
        local swap_percent
        swap_percent="$(calc_percent "$swap_used" "$swap_total")"
        report_add "$(format_kv 'Swap Total' "$(human_bytes "$swap_total")")"
        report_add "$(format_kv 'Swap Used' "$(human_bytes "$swap_used") (${swap_percent}%)")"
    else
        report_add "$(format_kv 'Swap' "Not configured")"
    fi

    if [[ "$mem_status" == "CRITICAL" ]]; then
        record_critical "Memory usage at ${mem_percent}% (threshold: ${MEM_CRIT_PERCENT}%)"
    elif [[ "$mem_status" == "WARNING" ]]; then
        record_warning "Memory usage at ${mem_percent}% (threshold: ${MEM_WARN_PERCENT}%)"
    fi

    # Top memory consumers
    if [[ "$VERBOSE" == true ]] && command_exists ps; then
        report_add ""
        report_add "  Top 5 Memory Consumers:"
        report_add "  $(printf '%-8s %-6s %-6s %s' 'PID' '%MEM' '%CPU' 'COMMAND')"
        while IFS= read -r line; do
            report_add "  $line"
        done < <(ps aux --sort=-%mem 2>/dev/null | head -6 | tail -5 | awk '{printf "%-8s %-6s %-6s %s\n", $2, $4, $3, $11}' 2>/dev/null || echo "  (unable to list processes)")
    fi
}

# ------------------------------------------------------------------------------
# Disk Section
# ------------------------------------------------------------------------------

check_disk() {
    section_header "DISK INFORMATION"
    log INFO "Checking disk usage..."

    report_add "  $(printf '%-25s %8s %8s %8s %5s  %s' 'FILESYSTEM' 'SIZE' 'USED' 'AVAIL' 'USE%' 'STATUS')"
    report_add "  $(printf '%s' "$(printf '%*s' 78 '' | tr ' ' '-')")"

    local has_issue=false

    while IFS= read -r line; do
        local filesystem size used avail percent mount
        filesystem="$(echo "$line" | awk '{print $1}')"
        size="$(echo "$line" | awk '{print $2}')"
        used="$(echo "$line" | awk '{print $3}')"
        avail="$(echo "$line" | awk '{print $4}')"
        percent="$(echo "$line" | awk '{print $5}' | tr -d '%')"
        mount="$(echo "$line" | awk '{print $6}')"

        # Skip virtual/pseudo filesystems
        case "$filesystem" in
            tmpfs|devtmpfs|none|overlay|shm) continue ;;
        esac

        local disk_status
        disk_status="$(status_label "$percent" "$DISK_WARN_PERCENT" "$DISK_CRIT_PERCENT")"
        local status_indicator
        status_indicator="$(format_status "$disk_status")"

        # Truncate filesystem name if too long
        if (( ${#filesystem} > 24 )); then
            filesystem="...${filesystem: -21}"
        fi

        report_add "  $(printf '%-25s %8s %8s %8s %4s%%  %s' "$filesystem" "$size" "$used" "$avail" "$percent" "$status_indicator")"

        if [[ "$disk_status" == "CRITICAL" ]]; then
            record_critical "Disk ${mount} is ${percent}% full (threshold: ${DISK_CRIT_PERCENT}%)"
            has_issue=true
        elif [[ "$disk_status" == "WARNING" ]]; then
            record_warning "Disk ${mount} is ${percent}% full (threshold: ${DISK_WARN_PERCENT}%)"
            has_issue=true
        fi
    done < <(df -h 2>/dev/null | tail -n +2 || echo "  (unable to read disk info)")

    # Inode usage (Linux only)
    if [[ "$VERBOSE" == true ]] && [[ -f /proc/mounts ]]; then
        report_add ""
        report_add "  Inode Usage:"
        while IFS= read -r line; do
            local inode_percent
            inode_percent="$(echo "$line" | awk '{print $5}' | tr -d '%')"
            if [[ -n "$inode_percent" ]] && (( inode_percent > DISK_WARN_PERCENT )); then
                local inode_mount
                inode_mount="$(echo "$line" | awk '{print $6}')"
                report_add "  $(format_kv "$inode_mount inodes" "${inode_percent}% used $(format_status WARNING)")"
                record_warning "Inode usage on $inode_mount is ${inode_percent}%"
            fi
        done < <(df -i 2>/dev/null | tail -n +2 || true)
    fi
}

# ------------------------------------------------------------------------------
# Network Section
# ------------------------------------------------------------------------------

check_network() {
    section_header "NETWORK INFORMATION"
    log INFO "Checking network status..."

    # Network interfaces
    local interfaces_found=0
    if command_exists ip; then
        report_add "  Active Interfaces:"
        while IFS= read -r iface; do
            if [[ -z "$iface" ]] || [[ "$iface" == "lo" ]]; then
                continue
            fi
            local ip_addr
            ip_addr="$(ip -4 addr show "$iface" 2>/dev/null | awk '/inet / {print $2}' | head -1)"
            local state
            state="$(ip link show "$iface" 2>/dev/null | awk '/state/ {print $9}')"
            if [[ -n "$ip_addr" ]]; then
                report_add "  $(format_kv "  $iface" "$ip_addr (state: ${state:-unknown})")"
                interfaces_found=$(( interfaces_found + 1 ))
            fi
        done < <(ip -o link show 2>/dev/null | awk -F': ' '{print $2}' | cut -d'@' -f1)
    elif command_exists ifconfig; then
        report_add "  Active Interfaces:"
        while IFS= read -r iface; do
            if [[ -z "$iface" ]] || [[ "$iface" == "lo0" ]]; then
                continue
            fi
            local ip_addr
            ip_addr="$(ifconfig "$iface" 2>/dev/null | awk '/inet / {print $2}')"
            if [[ -n "$ip_addr" ]]; then
                report_add "  $(format_kv "  $iface" "$ip_addr")"
                interfaces_found=$(( interfaces_found + 1 ))
            fi
        done < <(ifconfig -l 2>/dev/null | tr ' ' '\n')
    fi

    if (( interfaces_found == 0 )); then
        report_add "  $(format_kv 'Interfaces' "None detected $(format_status WARNING)")"
        record_warning "No active network interfaces detected"
    fi

    # DNS resolution check (non-destructive)
    report_add ""
    report_add "  DNS Resolution:"
    local dns_targets=("localhost")
    for target in "${dns_targets[@]}"; do
        if command_exists getent; then
            if getent hosts "$target" &>/dev/null; then
                report_add "  $(format_kv "  $target" "Resolves $(format_status OK)")"
            else
                report_add "  $(format_kv "  $target" "Failed $(format_status WARNING)")"
                record_warning "DNS resolution failed for $target"
            fi
        elif command_exists host; then
            if host "$target" &>/dev/null; then
                report_add "  $(format_kv "  $target" "Resolves $(format_status OK)")"
            else
                report_add "  $(format_kv "  $target" "Failed $(format_status WARNING)")"
            fi
        fi
    done

    # Listening ports summary
    if [[ "$VERBOSE" == true ]]; then
        report_add ""
        report_add "  Listening Ports (top 10):"
        if command_exists ss; then
            while IFS= read -r line; do
                report_add "  $line"
            done < <(ss -tlnp 2>/dev/null | head -11 || echo "  (unable to list ports)")
        elif command_exists netstat; then
            while IFS= read -r line; do
                report_add "  $line"
            done < <(netstat -tlnp 2>/dev/null | head -11 || echo "  (unable to list ports)")
        fi
    fi
}

# ------------------------------------------------------------------------------
# Process Section
# ------------------------------------------------------------------------------

check_processes() {
    section_header "PROCESS INFORMATION"
    log INFO "Checking process status..."

    # Process counts
    local total_procs=0
    local running_procs=0
    local sleeping_procs=0
    local zombie_procs=0

    if command_exists ps; then
        total_procs="$(ps aux 2>/dev/null | wc -l | tr -d ' ')"
        total_procs=$(( total_procs - 1 ))  # Subtract header
        running_procs="$(ps aux 2>/dev/null | awk '$8 ~ /R/ {count++} END {print count+0}')"
        sleeping_procs="$(ps aux 2>/dev/null | awk '$8 ~ /S/ {count++} END {print count+0}')"
        zombie_procs="$(ps aux 2>/dev/null | awk '$8 ~ /Z/ {count++} END {print count+0}')"
    fi

    report_add "$(format_kv 'Total Processes' "$total_procs")"
    report_add "$(format_kv 'Running' "$running_procs")"
    report_add "$(format_kv 'Sleeping' "$sleeping_procs")"
    report_add "$(format_kv 'Zombie' "$zombie_procs")"

    # Zombie process check
    if (( zombie_procs > MAX_ZOMBIE_PROCS )); then
        local zombie_status
        zombie_status="$(format_status CRITICAL)"
        report_add "$(format_kv 'Zombie Status' "$zombie_status (max: $MAX_ZOMBIE_PROCS)")"
        record_critical "$zombie_procs zombie processes detected (threshold: $MAX_ZOMBIE_PROCS)"
    elif (( zombie_procs > 0 )); then
        report_add "$(format_kv 'Zombie Status' "$(format_status WARNING) ($zombie_procs found)")"
        record_warning "$zombie_procs zombie process(es) detected"
    else
        report_add "$(format_kv 'Zombie Status' "$(format_status OK)")"
    fi

    # Longest running processes
    if [[ "$VERBOSE" == true ]] && command_exists ps; then
        report_add ""
        report_add "  Longest Running Processes:"
        report_add "  $(printf '%-8s %-12s %-6s %s' 'PID' 'ELAPSED' '%CPU' 'COMMAND')"
        while IFS= read -r line; do
            report_add "  $line"
        done < <(ps -eo pid,etime,%cpu,comm --sort=-etime 2>/dev/null | head -6 | tail -5 | awk '{printf "%-8s %-12s %-6s %s\n", $1, $2, $3, $4}' 2>/dev/null || echo "  (unable to list processes)")
    fi
}

# ------------------------------------------------------------------------------
# Security Section
# ------------------------------------------------------------------------------

check_security() {
    section_header "SECURITY OVERVIEW"
    log INFO "Running security checks..."

    # Check if running as root
    local is_root=false
    if [[ "$(id -u 2>/dev/null)" == "0" ]]; then
        is_root=true
        report_add "$(format_kv 'Running as Root' "Yes $(format_status WARNING)")"
        record_warning "Script is running as root user"
    else
        report_add "$(format_kv 'Running as Root' "No $(format_status OK)")"
    fi

    # Check for users with no password
    local no_pass_count=0
    if [[ -r /etc/shadow ]]; then
        no_pass_count="$(awk -F: '($2 == "" || $2 == "!") && $1 != "root" {count++} END {print count+0}' /etc/shadow 2>/dev/null)"
    fi
    if (( no_pass_count > 0 )); then
        report_add "$(format_kv 'Users w/o Password' "$no_pass_count $(format_status WARNING)")"
        record_warning "$no_pass_count user(s) found without password"
    else
        report_add "$(format_kv 'Users w/o Password' "0 $(format_status OK)")"
    fi

    # SSH configuration check
    if [[ -f /etc/ssh/sshd_config ]]; then
        local root_login
        root_login="$(grep -i '^PermitRootLogin' /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' | head -1)"
        if [[ "$root_login" == "yes" ]]; then
            report_add "$(format_kv 'SSH Root Login' "Enabled $(format_status WARNING)")"
            record_warning "SSH root login is enabled"
        elif [[ -n "$root_login" ]]; then
            report_add "$(format_kv 'SSH Root Login' "$root_login $(format_status OK)")"
        fi

        local pass_auth
        pass_auth="$(grep -i '^PasswordAuthentication' /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' | head -1)"
        if [[ "$pass_auth" == "yes" ]]; then
            report_add "$(format_kv 'SSH Password Auth' "Enabled $(format_status INFO)")"
        fi
    else
        report_add "$(format_kv 'SSH Config' "Not found (sshd may not be installed)")"
    fi

    # Check firewall status
    if command_exists ufw; then
        local ufw_status
        ufw_status="$(ufw status 2>/dev/null | head -1 || echo 'unknown')"
        report_add "$(format_kv 'Firewall (ufw)' "$ufw_status")"
    elif command_exists iptables; then
        local iptables_rules
        iptables_rules="$(iptables -L 2>/dev/null | wc -l || echo 0)"
        report_add "$(format_kv 'Firewall (iptables)' "$iptables_rules rules loaded")"
    elif command_exists firewall-cmd; then
        local fw_state
        fw_state="$(firewall-cmd --state 2>/dev/null || echo 'unknown')"
        report_add "$(format_kv 'Firewall (firewalld)' "$fw_state")"
    else
        report_add "$(format_kv 'Firewall' "No firewall utility detected $(format_status INFO)")"
    fi

    # Pending security updates (Debian/Ubuntu)
    if [[ "$VERBOSE" == true ]] && command_exists apt; then
        local security_updates
        security_updates="$(apt list --upgradable 2>/dev/null | grep -c security || echo 0)"
        if (( security_updates > 0 )); then
            report_add "$(format_kv 'Security Updates' "$security_updates available $(format_status WARNING)")"
            record_warning "$security_updates security updates available"
        else
            report_add "$(format_kv 'Security Updates' "Up to date $(format_status OK)")"
        fi
    fi
}

# ------------------------------------------------------------------------------
# Environment Section
# ------------------------------------------------------------------------------

check_environment() {
    section_header "ENVIRONMENT OVERVIEW"
    log INFO "Checking environment..."

    # Key tool versions
    local tools=("bash" "git" "python3" "node" "docker" "curl" "openssl")
    report_add "  Installed Tools:"
    for tool in "${tools[@]}"; do
        if command_exists "$tool"; then
            local version
            case "$tool" in
                bash)     version="$("$tool" --version 2>/dev/null | head -1 | awk '{print $4}' | cut -d'(' -f1)" ;;
                git)      version="$("$tool" --version 2>/dev/null | awk '{print $3}')" ;;
                python3)  version="$("$tool" --version 2>/dev/null | awk '{print $2}')" ;;
                node)     version="$("$tool" --version 2>/dev/null)" ;;
                docker)   version="$("$tool" --version 2>/dev/null | awk '{print $3}' | tr -d ',')" ;;
                curl)     version="$("$tool" --version 2>/dev/null | head -1 | awk '{print $2}')" ;;
                openssl)  version="$("$tool" version 2>/dev/null | awk '{print $2}')" ;;
                *)        version="installed" ;;
            esac
            report_add "  $(format_kv "  $tool" "${version:-unknown}")"
        else
            if [[ "$VERBOSE" == true ]]; then
                report_add "  $(format_kv "  $tool" "not installed")"
            fi
        fi
    done

    # Environment variable summary
    report_add ""
    report_add "  Environment Summary:"
    report_add "  $(format_kv '  PATH entries' "$(echo "$PATH" | tr ':' '\n' | wc -l | tr -d ' ')")"
    report_add "  $(format_kv '  Total env vars' "$(env 2>/dev/null | wc -l | tr -d ' ')")"

    # Check for common environment issues
    if [[ -z "${LANG:-}" ]]; then
        report_add "  $(format_kv '  LANG' "Not set $(format_status INFO)")"
    else
        report_add "  $(format_kv '  LANG' "$LANG")"
    fi

    if [[ -z "${EDITOR:-}" ]]; then
        report_add "  $(format_kv '  EDITOR' "Not set")"
    else
        report_add "  $(format_kv '  EDITOR' "$EDITOR")"
    fi

    # Disk temp directory
    local tmp_dir="${TMPDIR:-/tmp}"
    if [[ -w "$tmp_dir" ]]; then
        report_add "  $(format_kv '  Temp Directory' "$tmp_dir (writable) $(format_status OK)")"
    else
        report_add "  $(format_kv '  Temp Directory' "$tmp_dir (not writable) $(format_status WARNING)")"
        record_warning "Temp directory $tmp_dir is not writable"
    fi
}

# ------------------------------------------------------------------------------
# JSON Output
# ------------------------------------------------------------------------------

generate_json() {
    local exit_code="$1"
    local status="healthy"
    if (( ${#CRITICALS[@]} > 0 )); then
        status="critical"
    elif (( ${#WARNINGS[@]} > 0 )); then
        status="warning"
    fi

    cat <<JSONEOF
{
  "report": {
    "version": "$SCRIPT_VERSION",
    "timestamp": "$TIMESTAMP",
    "hostname": "$HOSTNAME_SHORT",
    "status": "$status",
    "exitCode": $exit_code,
    "warnings": $(json_array "${WARNINGS[@]+"${WARNINGS[@]}"}"),
    "criticals": $(json_array "${CRITICALS[@]+"${CRITICALS[@]}"}")
  }
}
JSONEOF
}

# Helper to build a JSON array from bash array values
json_array() {
    local items=("$@")
    if (( ${#items[@]} == 0 )); then
        echo "[]"
        return
    fi
    local result="["
    local first=true
    for item in "${items[@]}"; do
        if [[ "$first" != true ]]; then
            result+=","
        fi
        # Escape double quotes and backslashes in the value
        item="${item//\\/\\\\}"
        item="${item//\"/\\\"}"
        result+="\"$item\""
        first=false
    done
    result+="]"
    echo "$result"
}

# ------------------------------------------------------------------------------
# Report Summary
# ------------------------------------------------------------------------------

generate_summary() {
    section_header "HEALTH CHECK SUMMARY"

    local total_warnings=${#WARNINGS[@]}
    local total_criticals=${#CRITICALS[@]}

    if (( total_criticals > 0 )); then
        report_add ""
        report_add "  $(format_status CRITICAL) Critical Issues ($total_criticals):"
        for issue in "${CRITICALS[@]}"; do
            report_add "    - $issue"
        done
    fi

    if (( total_warnings > 0 )); then
        report_add ""
        report_add "  $(format_status WARNING) Warnings ($total_warnings):"
        for issue in "${WARNINGS[@]}"; do
            report_add "    - $issue"
        done
    fi

    if (( total_criticals == 0 && total_warnings == 0 )); then
        report_add ""
        report_add "  $(format_status OK) All checks passed - system is healthy!"
    fi

    report_add ""
    report_add "  Checks Run:     ${#SELECTED_SECTIONS[@]} sections"
    report_add "  Warnings:       $total_warnings"
    report_add "  Critical:       $total_criticals"
    report_add "  Report Time:    $TIMESTAMP"
    report_add ""
}

# ------------------------------------------------------------------------------
# Output Rendering
# ------------------------------------------------------------------------------

render_output() {
    local exit_code="$1"

    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        local json_output
        json_output="$(generate_json "$exit_code")"
        if [[ -n "$OUTPUT_FILE" ]]; then
            echo "$json_output" > "${OUTPUT_FILE}.json"
            log INFO "JSON report saved to ${OUTPUT_FILE}.json"
        else
            echo "$json_output"
        fi
        return
    fi

    # Text output
    local header
    header="$(cat <<'BANNER'

  ╔═══════════════════════════════════════════════════════╗
  ║         System Health Check Report v1.0.0            ║
  ╚═══════════════════════════════════════════════════════╝

BANNER
)"

    if [[ -n "$OUTPUT_FILE" ]]; then
        {
            echo "$header"
            for line in "${REPORT_LINES[@]}"; do
                echo "$line"
            done
        } > "${OUTPUT_FILE}.txt"
        log INFO "Report saved to ${OUTPUT_FILE}.txt"
    else
        echo "$header"
        for line in "${REPORT_LINES[@]}"; do
            echo "$line"
        done
    fi
}

# ------------------------------------------------------------------------------
# Argument Parsing
# ------------------------------------------------------------------------------

show_help() {
    cat <<HELPEOF
${SCRIPT_NAME} v${SCRIPT_VERSION} — System Health Check & Report Generator

USAGE:
    ${SCRIPT_NAME} [OPTIONS]

OPTIONS:
    --output FILE     Save report to FILE.txt (or FILE.json with --json)
    --json            Output report in JSON format
    --section NAME    Run only the specified section (can repeat)
                      Available: ${ALL_SECTIONS[*]}
    --verbose         Include additional details in each section
    --no-color        Disable colored output
    --help            Show this help message
    --version         Show version information

EXAMPLES:
    ${SCRIPT_NAME}                          Run all checks
    ${SCRIPT_NAME} --verbose                Run all checks with extra detail
    ${SCRIPT_NAME} --section disk           Check only disk usage
    ${SCRIPT_NAME} --section cpu --section memory
                                            Check CPU and memory
    ${SCRIPT_NAME} --json --output health   Save JSON report to health.json
    ${SCRIPT_NAME} --no-color               Plain text without ANSI colors

EXIT CODES:
    0  All checks passed
    1  One or more warnings detected
    2  One or more critical issues found
    3  Script error (invalid args, missing deps)

HELPEOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --output)
                if [[ -z "${2:-}" ]]; then
                    log ERROR "--output requires a filename argument"
                    exit 3
                fi
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --json)
                OUTPUT_FORMAT="json"
                USE_COLOR=false
                shift
                ;;
            --section)
                if [[ -z "${2:-}" ]]; then
                    log ERROR "--section requires a section name"
                    exit 3
                fi
                local valid=false
                for s in "${ALL_SECTIONS[@]}"; do
                    if [[ "$s" == "$2" ]]; then
                        valid=true
                        break
                    fi
                done
                if [[ "$valid" != true ]]; then
                    log ERROR "Unknown section: $2. Available: ${ALL_SECTIONS[*]}"
                    exit 3
                fi
                SELECTED_SECTIONS+=("$2")
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --no-color)
                USE_COLOR=false
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            --version)
                echo "${SCRIPT_NAME} v${SCRIPT_VERSION}"
                exit 0
                ;;
            *)
                log ERROR "Unknown option: $1. Use --help for usage."
                exit 3
                ;;
        esac
    done

    # Default to all sections if none specified
    if (( ${#SELECTED_SECTIONS[@]} == 0 )); then
        SELECTED_SECTIONS=("${ALL_SECTIONS[@]}")
    fi
}

# ------------------------------------------------------------------------------
# Section Dispatcher
# ------------------------------------------------------------------------------

run_section() {
    local section="$1"
    case "$section" in
        system)      check_system_info ;;
        cpu)         check_cpu ;;
        memory)      check_memory ;;
        disk)        check_disk ;;
        network)     check_network ;;
        process)     check_processes ;;
        security)    check_security ;;
        environment) check_environment ;;
        *)
            log WARN "Skipping unknown section: $section"
            ;;
    esac
}

# ------------------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------------------

main() {
    parse_args "$@"

    log INFO "Starting system health check (v${SCRIPT_VERSION})..."
    log INFO "Hostname: $HOSTNAME_SHORT"
    log INFO "Sections: ${SELECTED_SECTIONS[*]}"

    # Disable color when writing to file
    if [[ -n "$OUTPUT_FILE" ]]; then
        USE_COLOR=false
    fi

    # Run selected sections
    for section in "${SELECTED_SECTIONS[@]}"; do
        log DEBUG "Running section: $section"
        run_section "$section"
    done

    # Generate summary
    generate_summary

    # Determine exit code
    local exit_code=0
    if (( ${#CRITICALS[@]} > 0 )); then
        exit_code=2
    elif (( ${#WARNINGS[@]} > 0 )); then
        exit_code=1
    fi

    # Output the report
    render_output "$exit_code"

    log INFO "Health check complete. Exit code: $exit_code"
    return "$exit_code"
}

# Run main (only if not being sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
