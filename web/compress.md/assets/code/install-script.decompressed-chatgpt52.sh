#!/usr/bin/env bash
# script-original.sh — System Health Check Script
# Safe, read-only diagnostics + text/JSON report
# Version: 1.0.0

set -euo pipefail

# ----------------------------
# Constants / Defaults
# ----------------------------
SCRIPT_VERSION="1.0.0"
ALL_SECTIONS=(system cpu memory disk network process security environment)

DISK_WARN=80
DISK_CRIT=95
MEM_WARN=85
MEM_CRIT=95
UPTIME_WARN_DAYS=90
MAX_ZOMBIE=5

OUTPUT_FILE=""
OUTPUT_FORMAT="text"   # text | json
SELECTED_SECTIONS=()
VERBOSE=false
USE_COLOR=true

WARNINGS=()
CRITICALS=()
REPORT_LINES=()

# ----------------------------
# Colors
# ----------------------------
RED=$'\033[31m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
BLUE=$'\033[34m'
CYAN=$'\033[36m'
BOLD=$'\033[1m'
RESET=$'\033[0m'

# ----------------------------
# Logging / Report helpers
# ----------------------------
ts() { date '+%Y-%m-%d %H:%M:%S'; }

log() {
  local level="${1:-INFO}"; shift || true
  local msg="${*:-}"
  if [[ "$level" == "DEBUG" && "$VERBOSE" != true ]]; then
    return 0
  fi
  printf '[%s] %s: %s\n' "$(ts)" "$level" "$msg" >&2
}

report_add() { REPORT_LINES+=("$1"); }

section_header() {
  local title="$1"
  local width=72
  local pad="===="
  local line
  line=$(printf '%*s' "$width" '' | tr ' ' '=')
  report_add "$line"
  report_add "$(printf '%s %s %s' "$pad" "$title" "$pad")"
  report_add "$line"
}

format_kv() {
  local key="$1" value="$2" width="${3:-30}"
  printf '  %-*s %s' "$width" "$key" "$value"
}

format_status() {
  local status="$1"
  if [[ "$USE_COLOR" != true ]]; then
    printf '%s' "$status"
    return 0
  fi
  case "$status" in
    OK)       printf '%sOK%s' "$GREEN" "$RESET" ;;
    WARNING)  printf '%sWARNING%s' "$YELLOW" "$RESET" ;;
    CRITICAL) printf '%sCRITICAL%s' "$RED" "$RESET" ;;
    *)        printf '%s' "$status" ;;
  esac
}

record_warning() {
  local msg="$1"
  WARNINGS+=("$msg")
  log "WARN" "$msg"
}

record_critical() {
  local msg="$1"
  CRITICALS+=("$msg")
  log "ERROR" "$msg"
}

command_exists() { command -v "$1" >/dev/null 2>&1; }

safe_read() {
  local file="$1" default="${2:-N/A}"
  if [[ -r "$file" ]]; then
    cat "$file"
  else
    printf '%s' "$default"
  fi
}

calc_percent() {
  local used="$1" total="$2"
  if [[ "$total" -eq 0 ]]; then
    echo 0
  else
    echo $(( (used * 100) / total ))
  fi
}

human_bytes() {
  local bytes="${1:-0}"
  if [[ "$bytes" -ge 1073741824 ]]; then
    echo "$((bytes / 1073741824))GB"
  elif [[ "$bytes" -ge 1048576 ]]; then
    echo "$((bytes / 1048576))MB"
  elif [[ "$bytes" -ge 1024 ]]; then
    echo "$((bytes / 1024))KB"
  else
    echo "${bytes}B"
  fi
}

human_duration() {
  local secs="${1:-0}"
  local d=$((secs / 86400)); secs=$((secs % 86400))
  local h=$((secs / 3600));  secs=$((secs % 3600))
  local m=$((secs / 60))
  if [[ "$d" -gt 0 ]]; then
    printf '%dd %dh %dm' "$d" "$h" "$m"
  elif [[ "$h" -gt 0 ]]; then
    printf '%dh %dm' "$h" "$m"
  else
    printf '%dm' "$m"
  fi
}

json_escape() {
  # Minimal JSON string escape (quotes, backslashes, newlines, tabs, carriage returns)
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

json_array() {
  local -a items=("$@")
  local out="["
  local i
  for i in "${!items[@]}"; do
    local esc
    esc="$(json_escape "${items[$i]}")"
    out+="\"$esc\""
    if [[ "$i" -lt $((${#items[@]} - 1)) ]]; then
      out+=","
    fi
  done
  out+="]"
  printf '%s' "$out"
}

# ----------------------------
# Platform helpers
# ----------------------------
is_macos() { [[ "$(uname -s)" == "Darwin" ]]; }
is_linux() { [[ "$(uname -s)" == "Linux" ]]; }

get_hostname() { hostname 2>/dev/null || uname -n 2>/dev/null || echo "unknown"; }

get_timezone() {
  if command_exists timedatectl; then
    timedatectl 2>/dev/null | awk -F': *' '/Time zone/ {print $2}' | awk '{print $1}' || true
  elif [[ -r /etc/timezone ]]; then
    cat /etc/timezone
  else
    date +%Z
  fi
}

get_uptime_seconds() {
  if is_linux && [[ -r /proc/uptime ]]; then
    awk '{print int($1)}' /proc/uptime
  elif is_macos; then
    # sysctl kern.boottime gives boot time; compute delta
    local bt now
    bt="$(sysctl -n kern.boottime 2>/dev/null | awk -F'[ ,]' '{for(i=1;i<=NF;i++) if($i~/sec/) {print $(i+1); exit}}' || true)"
    now="$(date +%s)"
    if [[ -n "${bt:-}" ]]; then
      echo $((now - bt))
    else
      echo 0
    fi
  else
    # Fallback: parse uptime output (best-effort)
    local up
    up="$(uptime 2>/dev/null || true)"
    # If we can't parse reliably, return 0
    echo 0
  fi
}

get_os_release() {
  if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    echo "${PRETTY_NAME:-unknown}"
  elif is_macos && command_exists sw_vers; then
    sw_vers 2>/dev/null | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g' | sed 's/[[:space:]]$//'
  else
    echo "unknown"
  fi
}

get_kernel() { uname -r 2>/dev/null || echo "unknown"; }
get_arch() { uname -m 2>/dev/null || echo "unknown"; }

cpu_cores() {
  if command_exists nproc; then
    nproc
  elif is_macos; then
    sysctl -n hw.ncpu 2>/dev/null || echo 1
  else
    echo 1
  fi
}

cpu_threads() {
  if is_linux && [[ -r /proc/cpuinfo ]]; then
    grep -c '^processor' /proc/cpuinfo 2>/dev/null || echo 0
  elif is_macos; then
    sysctl -n hw.logicalcpu 2>/dev/null || echo 0
  else
    echo 0
  fi
}

cpu_model() {
  if is_linux && [[ -r /proc/cpuinfo ]]; then
    awk -F': ' '/model name/ {print $2; exit}' /proc/cpuinfo 2>/dev/null || echo "unknown"
  elif is_macos; then
    sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "unknown"
  else
    echo "unknown"
  fi
}

get_loadavg() {
  if is_linux && [[ -r /proc/loadavg ]]; then
    awk '{print $1, $2, $3}' /proc/loadavg
  elif is_macos; then
    sysctl -n vm.loadavg 2>/dev/null | tr -d '{}' | awk '{$1=$1; print}' || echo "0.00 0.00 0.00"
  else
    echo "0.00 0.00 0.00"
  fi
}

# ----------------------------
# Checks
# ----------------------------
check_system_info() {
  section_header "SYSTEM"
  local host os kern arch user shell tz up_s up_dur
  host="$(get_hostname)"
  os="$(get_os_release)"
  kern="$(get_kernel)"
  arch="$(get_arch)"
  user="${USER:-$(id -un 2>/dev/null || echo unknown)}"
  shell="${SHELL:-unknown}"
  tz="$(get_timezone)"
  up_s="$(get_uptime_seconds)"
  up_dur="$(human_duration "$up_s")"

  report_add "$(format_kv "Hostname:" "$host")"
  report_add "$(format_kv "OS:" "$os")"
  report_add "$(format_kv "Kernel:" "$kern")"
  report_add "$(format_kv "Arch:" "$arch")"
  report_add "$(format_kv "User:" "$user")"
  report_add "$(format_kv "Shell:" "$shell")"
  report_add "$(format_kv "Timezone:" "$tz")"
  report_add "$(format_kv "Uptime:" "$up_dur")"

  local warn_secs=$((UPTIME_WARN_DAYS * 86400))
  if [[ "$up_s" -gt "$warn_secs" ]]; then
    record_warning "Uptime exceeds ${UPTIME_WARN_DAYS} days (${up_dur}). Consider reboot planning."
  fi

  if [[ "$VERBOSE" == true ]]; then
    report_add "$(format_kv "Script version:" "$SCRIPT_VERSION")"
    report_add "$(format_kv "Script path:" "${BASH_SOURCE[0]}")"
    report_add "$(format_kv "PID/PPID:" "$$/$(ps -o ppid= -p $$ 2>/dev/null | awk '{$1=$1;print}' || echo "?")")"
  fi
}

check_cpu() {
  section_header "CPU"
  local model cores threads load1 load5 load15
  model="$(cpu_model)"
  cores="$(cpu_cores)"
  threads="$(cpu_threads)"
  read -r load1 load5 load15 <<<"$(get_loadavg)"

  report_add "$(format_kv "Model:" "$model")"
  report_add "$(format_kv "Cores:" "$cores")"
  report_add "$(format_kv "Threads:" "$threads")"
  report_add "$(format_kv "Load avg (1/5/15):" "$load1 $load5 $load15")"

  # Thresholds: LOAD_WARN=cores*2 ; LOAD_CRIT=cores*4 (use 1-min load)
  local warn=$((cores * 2))
  local crit=$((cores * 4))
  local load1_int
  load1_int="$(printf '%.0f' "$load1" 2>/dev/null || echo 0)"

  if [[ "$load1_int" -ge "$crit" ]]; then
    record_critical "High CPU load (1m=$load1) >= crit(${crit})."
  elif [[ "$load1_int" -ge "$warn" ]]; then
    record_warning "Elevated CPU load (1m=$load1) >= warn(${warn})."
  fi

  if [[ "$VERBOSE" == true ]]; then
    report_add ""
    report_add "  Top 5 CPU consumers:"
    if command_exists ps; then
      # best-effort: different ps flags across platforms
      if ps aux 2>/dev/null | head -n 1 | grep -q '%CPU'; then
        ps aux --sort=-%cpu 2>/dev/null | awk 'NR==1{print "    "$0} NR>1 && NR<=6{print "    "$0}' || true
      else
        ps -Ao pid,ppid,%cpu,comm 2>/dev/null | head -n 6 | awk '{print "    "$0}' || true
      fi
    else
      report_add "    N/A (ps not available)"
    fi
  fi
}

check_memory() {
  section_header "MEMORY"
  local mem_total_kb=0 mem_avail_kb=0 mem_used_kb=0 mem_percent=0
  local swap_total_kb=0 swap_free_kb=0 swap_used_kb=0

  if is_linux && [[ -r /proc/meminfo ]]; then
    mem_total_kb="$(awk '/MemTotal:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
    mem_avail_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
    mem_used_kb=$((mem_total_kb - mem_avail_kb))
    mem_percent="$(calc_percent "$mem_used_kb" "$mem_total_kb")"

    swap_total_kb="$(awk '/SwapTotal:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
    local swap_free_kb_tmp
    swap_free_kb_tmp="$(awk '/SwapFree:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
    swap_free_kb="$swap_free_kb_tmp"
    swap_used_kb=$((swap_total_kb - swap_free_kb))
  elif is_macos && command_exists vm_stat && command_exists sysctl; then
    # macOS: vm_stat pages + hw.memsize bytes
    local pagesize
    pagesize="$(vm_stat 2>/dev/null | awk '/page size of/ {print $8}' || echo 4096)"
    local memsize_bytes
    memsize_bytes="$(sysctl -n hw.memsize 2>/dev/null || echo 0)"
    mem_total_kb=$((memsize_bytes / 1024))

    local free_pages inactive_pages speculative_pages
    free_pages="$(vm_stat 2>/dev/null | awk '/Pages free/ {gsub("\\.","",$3); print $3}' || echo 0)"
    inactive_pages="$(vm_stat 2>/dev/null | awk '/Pages inactive/ {gsub("\\.","",$3); print $3}' || echo 0)"
    speculative_pages="$(vm_stat 2>/dev/null | awk '/Pages speculative/ {gsub("\\.","",$3); print $3}' || echo 0)"
    local avail_pages=$((free_pages + inactive_pages + speculative_pages))
    mem_avail_kb=$(( (avail_pages * pagesize) / 1024 ))
    mem_used_kb=$((mem_total_kb - mem_avail_kb))
    mem_percent="$(calc_percent "$mem_used_kb" "$mem_total_kb")"

    # swap (best-effort)
    if command_exists sysctl; then
      # vm.swapusage: total = X  used = Y  free = Z
      local swap_line
      swap_line="$(sysctl -n vm.swapusage 2>/dev/null || true)"
      # parse like: "total = 1024.00M  used = 512.00M  free = 512.00M"
      # keep as N/A if not parseable
      report_add "$(format_kv "Swap:" "${swap_line:-N/A}")"
    fi
  else
    report_add "$(format_kv "Memory:" "N/A (unsupported platform)")"
    return 0
  fi

  report_add "$(format_kv "Mem total:" "${mem_total_kb} KB")"
  report_add "$(format_kv "Mem used:" "${mem_used_kb} KB")"
  report_add "$(format_kv "Mem avail:" "${mem_avail_kb} KB")"
  report_add "$(format_kv "Mem used %:" "${mem_percent}%")"

  if [[ "$mem_percent" -ge "$MEM_CRIT" ]]; then
    record_critical "High memory usage (${mem_percent}%) >= crit(${MEM_CRIT}%)."
  elif [[ "$mem_percent" -ge "$MEM_WARN" ]]; then
    record_warning "Elevated memory usage (${mem_percent}%) >= warn(${MEM_WARN}%)."
  fi

  if [[ "$VERBOSE" == true ]]; then
    report_add ""
    report_add "  Top 5 memory consumers:"
    if command_exists ps; then
      if ps aux 2>/dev/null | head -n 1 | grep -q '%MEM'; then
        ps aux --sort=-%mem 2>/dev/null | awk 'NR==1{print "    "$0} NR>1 && NR<=6{print "    "$0}' || true
      else
        ps -Ao pid,ppid,%mem,comm 2>/dev/null | head -n 6 | awk '{print "    "$0}' || true
      fi
    else
      report_add "    N/A (ps not available)"
    fi
  fi
}

check_disk() {
  section_header "DISK"
  if ! command_exists df; then
    report_add "  N/A (df not available)"
    return 0
  fi

  report_add "  Filesystems:"
  # POSIX-ish df parsing. Use -P for stable columns where available.
  local df_cmd=("df" "-P" "-h")
  if ! df -P -h >/dev/null 2>&1; then
    df_cmd=("df" "-h")
  fi

  # header
  report_add "    $(printf '%-26s %-8s %-8s %-8s %-6s %s' "Filesystem" "Size" "Used" "Avail" "Use%" "Mounted on")"

  local line
  while IFS= read -r line; do
    # skip header
    if [[ "$line" =~ ^Filesystem ]]; then
      continue
    fi
    # tokenize safely
    # shellcheck disable=SC2206
    local parts=($line)
    local fs="${parts[0]}"
    local size="${parts[1]:-}"
    local used="${parts[2]:-}"
    local avail="${parts[3]:-}"
    local usep="${parts[4]:-}"
    local mnt="${parts[5]:-}"

    # skip ephemeral/virtual fs
    case "$fs" in
      tmpfs|devtmpfs|none|overlay|shm) continue ;;
    esac

    # percent without %
    local pct="${usep%\%}"
    local fs_disp="$fs"
    if [[ "${#fs_disp}" -gt 24 ]]; then
      fs_disp="...${fs_disp: -21}"
    fi

    local status="OK"
    if [[ "$pct" -ge "$DISK_CRIT" ]]; then
      status="CRITICAL"
      record_critical "Disk usage critical on ${mnt} (${pct}%)."
    elif [[ "$pct" -ge "$DISK_WARN" ]]; then
      status="WARNING"
      record_warning "Disk usage high on ${mnt} (${pct}%)."
    fi

    report_add "    $(printf '%-26s %-8s %-8s %-8s %-6s %s' "$fs_disp" "$size" "$used" "$avail" "$usep" "$mnt")  [$(format_status "$status")]"
  done < <("${df_cmd[@]}" 2>/dev/null || true)

  if [[ "$VERBOSE" == true ]]; then
    report_add ""
    report_add "  Inodes (df -i):"
    if df -i >/dev/null 2>&1; then
      df -i 2>/dev/null | awk '{print "    "$0}' || true
    else
      report_add "    N/A"
    fi
  fi
}

check_network() {
  section_header "NETWORK"
  local found=0

  if command_exists ip; then
    report_add "  Interfaces (ip):"
    ip -o link show 2>/dev/null | awk '{print "    "$2}' | sed 's/://g' || true
    found=1
  elif command_exists ifconfig; then
    report_add "  Interfaces (ifconfig):"
    ifconfig -a 2>/dev/null | awk '/flags=/{print "    "$1}' | sed 's/://g' || true
    found=1
  else
    report_add "  Interfaces: N/A (no ip/ifconfig)"
  fi

  if [[ "$found" -eq 0 ]]; then
    record_warning "No network interface tool available (ip/ifconfig missing)."
  fi

  # DNS localhost resolution test
  local dns_ok=false
  if command_exists getent; then
    if getent hosts localhost >/dev/null 2>&1; then dns_ok=true; fi
  elif command_exists host; then
    if host localhost >/dev/null 2>&1; then dns_ok=true; fi
  fi
  report_add "$(format_kv "DNS localhost resolve:" "$( [[ "$dns_ok" == true ]] && echo "OK" || echo "N/A/FAIL" )")"
  if [[ "$dns_ok" != true ]]; then
    record_warning "DNS localhost resolution test failed or tool missing (getent/host)."
  fi

  if [[ "$VERBOSE" == true ]]; then
    report_add ""
    report_add "  Listening ports (top 10):"
    if command_exists ss; then
      ss -tlnp 2>/dev/null | head -n 11 | awk '{print "    "$0}' || true
    elif command_exists netstat; then
      netstat -an 2>/dev/null | grep -E 'LISTEN' | head -n 10 | awk '{print "    "$0}' || true
    else
      report_add "    N/A (no ss/netstat)"
    fi
  fi
}

check_processes() {
  section_header "PROCESSES"
  if ! command_exists ps; then
    report_add "  N/A (ps not available)"
    return 0
  fi

  # total, running, sleeping, zombie
  local total=0 zombies=0
  total="$(ps aux 2>/dev/null | awk 'NR>1{c++} END{print c+0}' || echo 0)"
  zombies="$(ps aux 2>/dev/null | awk 'NR>1 && $8 ~ /^Z/ {c++} END{print c+0}' || echo 0)"

  report_add "$(format_kv "Total processes:" "$total")"
  report_add "$(format_kv "Zombie processes:" "$zombies")"

  if [[ "$zombies" -gt "$MAX_ZOMBIE" ]]; then
    record_critical "Too many zombie processes (${zombies}) > MAX_ZOMBIE(${MAX_ZOMBIE})."
  elif [[ "$zombies" -gt 0 ]]; then
    record_warning "Zombie processes detected (${zombies})."
  fi

  if [[ "$VERBOSE" == true ]]; then
    report_add ""
    report_add "  Longest running processes (best-effort):"
    # Linux: ps -eo pid,etime,%cpu,comm ; macOS supports etime too
    ps -eo pid,etime,%cpu,comm 2>/dev/null | head -n 15 | awk '{print "    "$0}' || true
  fi
}

check_security() {
  section_header "SECURITY"

  local uid
  uid="$(id -u 2>/dev/null || echo 99999)"
  if [[ "$uid" -eq 0 ]]; then
    record_warning "Script is running as root (uid=0). Consider running as non-root for routine checks."
  fi
  report_add "$(format_kv "Running as root:" "$( [[ "$uid" -eq 0 ]] && echo "YES" || echo "NO" )")"

  # /etc/shadow users w/o password (Linux only, best-effort)
  if is_linux && [[ -r /etc/shadow ]]; then
    local nopw
    nopw="$(awk -F: '($2=="" || $2=="!" || $2=="!!") {print $1}' /etc/shadow 2>/dev/null | head -n 20 || true)"
    if [[ -n "$nopw" ]]; then
      record_warning "Some accounts may have empty/locked password fields in /etc/shadow (sample): $(echo "$nopw" | tr '\n' ' ')"
    fi
  fi

  # sshd_config checks
  if [[ -r /etc/ssh/sshd_config ]]; then
    local prl pa
    prl="$(grep -E '^\s*PermitRootLogin\b' /etc/ssh/sshd_config 2>/dev/null | tail -n 1 | awk '{print $2}' || echo "unset")"
    pa="$(grep -E '^\s*PasswordAuthentication\b' /etc/ssh/sshd_config 2>/dev/null | tail -n 1 | awk '{print $2}' || echo "unset")"
    report_add "$(format_kv "sshd PermitRootLogin:" "$prl")"
    report_add "$(format_kv "sshd PasswordAuthentication:" "$pa")"
  else
    report_add "$(format_kv "sshd_config:" "N/A")"
  fi

  # firewall status (best-effort)
  local fw="N/A"
  if command_exists ufw; then
    fw="$(ufw status 2>/dev/null | head -n 1 || echo "unknown")"
  elif command_exists firewall-cmd; then
    fw="$(firewall-cmd --state 2>/dev/null || echo "unknown")"
  elif command_exists iptables; then
    fw="iptables present"
  fi
  report_add "$(format_kv "Firewall:" "$fw")"

  if [[ "$VERBOSE" == true ]]; then
    # apt security updates count (best-effort)
    if command_exists apt-get; then
      # Avoid side effects: no update; just report if unattended-upgrades/logs exist
      report_add "$(format_kv "APT security updates:" "N/A (requires apt update; skipped)")"
    fi
  fi
}

check_environment() {
  section_header "ENVIRONMENT"

  local tools=(bash git python3 node docker curl openssl)
  report_add "  Tool versions:"
  local t
  for t in "${tools[@]}"; do
    if command_exists "$t"; then
      local ver
      case "$t" in
        bash) ver="$("$t" --version 2>/dev/null | head -n 1 || echo "unknown")" ;;
        git) ver="$("$t" --version 2>/dev/null | head -n 1 || echo "unknown")" ;;
        python3) ver="$("$t" --version 2>/dev/null || echo "unknown")" ;;
        node) ver="$("$t" --version 2>/dev/null || echo "unknown")" ;;
        docker) ver="$("$t" --version 2>/dev/null || echo "unknown")" ;;
        curl) ver="$("$t" --version 2>/dev/null | head -n 1 || echo "unknown")" ;;
        openssl) ver="$("$t" version 2>/dev/null || echo "unknown")" ;;
        *) ver="unknown" ;;
      esac
      report_add "    $(format_kv "$t:" "$ver" 18)"
    else
      report_add "    $(format_kv "$t:" "missing" 18)"
    fi
  done

  # env stats
  local path_count env_count lang editor
  path_count="$(echo "${PATH:-}" | awk -F: '{print NF}' || echo 0)"
  env_count="$(env 2>/dev/null | wc -l | awk '{$1=$1;print}' || echo 0)"
  lang="${LANG:-unset}"
  editor="${EDITOR:-unset}"

  report_add ""
  report_add "$(format_kv "PATH entries:" "$path_count")"
  report_add "$(format_kv "Env vars:" "$env_count")"
  report_add "$(format_kv "LANG:" "$lang")"
  report_add "$(format_kv "EDITOR:" "$editor")"

  # TMPDIR writable
  local tmp="${TMPDIR:-/tmp}"
  local tmp_ok=true
  if [[ ! -d "$tmp" ]] || [[ ! -w "$tmp" ]]; then
    tmp_ok=false
  fi
  report_add "$(format_kv "TMPDIR writable:" "$( [[ "$tmp_ok" == true ]] && echo "OK" || echo "WARNING" )")"
  if [[ "$tmp_ok" != true ]]; then
    record_warning "TMPDIR is not writable or missing: $tmp"
  fi
}

# ----------------------------
# Output
# ----------------------------
generate_summary() {
  section_header "SUMMARY"

  local w="${#WARNINGS[@]}" c="${#CRITICALS[@]}"
  if [[ "$c" -gt 0 ]]; then
    report_add "  Critical issues:"
    local i
    for i in "${CRITICALS[@]}"; do
      report_add "    - $i"
    done
  fi

  if [[ "$w" -gt 0 ]]; then
    report_add "  Warnings:"
    local i
    for i in "${WARNINGS[@]}"; do
      report_add "    - $i"
    done
  fi

  if [[ "$w" -eq 0 && "$c" -eq 0 ]]; then
    report_add "  All checks passed - system is healthy!"
  fi

  report_add ""
  report_add "$(format_kv "Sections run:" "${#SELECTED_SECTIONS[@]}")"
  report_add "$(format_kv "Warnings:" "$w")"
  report_add "$(format_kv "Criticals:" "$c")"
  report_add "$(format_kv "Timestamp:" "$(ts)")"
}

generate_json() {
  local exit_code="$1"
  local host status
  host="$(get_hostname)"
  if [[ "${#CRITICALS[@]}" -gt 0 ]]; then
    status="CRITICAL"
  elif [[ "${#WARNINGS[@]}" -gt 0 ]]; then
    status="WARNING"
  else
    status="OK"
  fi

  local warnings_json criticals_json
  warnings_json="$(json_array "${WARNINGS[@]:-}")"
  criticals_json="$(json_array "${CRITICALS[@]:-}")"

  cat <<EOF
{
  "report": {
    "version": "$(json_escape "$SCRIPT_VERSION")",
    "timestamp": "$(json_escape "$(ts)")",
    "hostname": "$(json_escape "$host")",
    "status": "$(json_escape "$status")",
    "exitCode": $exit_code,
    "warnings": $warnings_json,
    "criticals": $criticals_json
  }
}
EOF
}

render_output() {
  local exit_code="$1"

  # If writing to file, disable colors in text output.
  if [[ -n "$OUTPUT_FILE" ]]; then
    USE_COLOR=false
  fi

  if [[ "$OUTPUT_FORMAT" == "json" ]]; then
    if [[ -n "$OUTPUT_FILE" ]]; then
      generate_json "$exit_code" > "${OUTPUT_FILE}.json"
    else
      generate_json "$exit_code"
    fi
    return 0
  fi

  # text output
  local banner
  banner="System Health Check Report (v${SCRIPT_VERSION}) — $(ts)"
  if [[ -n "$OUTPUT_FILE" ]]; then
    {
      echo "$banner"
      echo
      printf '%s\n' "${REPORT_LINES[@]}"
    } > "${OUTPUT_FILE}.txt"
  else
    echo "$banner"
    echo
    printf '%s\n' "${REPORT_LINES[@]}"
  fi
}

show_help() {
  cat <<'EOF'
Usage:
  script-original.sh [options]

Options:
  --output FILE        Write report to FILE.txt (text) or FILE.json (json)
  --json               Output JSON instead of text (disables color)
  --section NAME       Run only a specific section (repeatable)
                       Sections: system cpu memory disk network process security environment
  --verbose            Enable debug logs and extra section details
  --no-color           Disable colored status labels in text output
  --help               Show this help and exit
  --version            Print script version and exit

Exit codes:
  0  all checks passed
  1  warnings detected
  2  critical issues detected
  3  script error (bad args / unknown option)

Examples:
  ./script-original.sh
  ./script-original.sh --verbose
  ./script-original.sh --section cpu --section memory
  ./script-original.sh --json
  ./script-original.sh --output /tmp/healthcheck --json
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --output)
        shift
        OUTPUT_FILE="${1:-}"
        if [[ -z "$OUTPUT_FILE" ]]; then
          log "ERROR" "--output requires a filename"
          exit 3
        fi
        shift
        ;;
      --json)
        OUTPUT_FORMAT="json"
        USE_COLOR=false
        shift
        ;;
      --section)
        shift
        local sec="${1:-}"
        if [[ -z "$sec" ]]; then
          log "ERROR" "--section requires a name"
          exit 3
        fi
        # validate
        local ok=false s
        for s in "${ALL_SECTIONS[@]}"; do
          if [[ "$s" == "$sec" ]]; then ok=true; break; fi
        done
        if [[ "$ok" != true ]]; then
          log "ERROR" "Unknown section: $sec"
          exit 3
        fi
        SELECTED_SECTIONS+=("$sec")
        shift
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
        echo "$SCRIPT_VERSION"
        exit 0
        ;;
      *)
        log "ERROR" "Unknown option: $1"
        exit 3
        ;;
    esac
  done

  if [[ "${#SELECTED_SECTIONS[@]}" -eq 0 ]]; then
    SELECTED_SECTIONS=("${ALL_SECTIONS[@]}")
  fi
}

run_section() {
  local section="$1"
  case "$section" in
    system) check_system_info ;;
    cpu) check_cpu ;;
    memory) check_memory ;;
    disk) check_disk ;;
    network) check_network ;;
    process) check_processes ;;
    security) check_security ;;
    environment) check_environment ;;
    *)
      log "WARN" "Unknown section '$section' — skipping"
      ;;
  esac
}

main() {
  parse_args "$@"
  log "INFO" "Starting system health check (v${SCRIPT_VERSION})"
  local sec
  for sec in "${SELECTED_SECTIONS[@]}"; do
    run_section "$sec"
  done
  generate_summary

  local exit_code=0
  if [[ "${#CRITICALS[@]}" -gt 0 ]]; then
    exit_code=2
  elif [[ "${#WARNINGS[@]}" -gt 0 ]]; then
    exit_code=1
  fi

  render_output "$exit_code"
  log "INFO" "Complete (exit_code=$exit_code)"
  return "$exit_code"
}

main "$@"
