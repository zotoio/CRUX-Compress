---
generated: 2026-02-08 14:32
sourceChecksum: 1689381612
beforeTokens: ~9764
afterTokens: ~1665
reducedBy: 83%
confidence: 90%
---

> [!IMPORTANT]
> Generated file - do not edit!

# System Health Check Script

```crux
⟦CRUX:script-original.sh
Ρ{sys health check+report generator; bash; safe read-only diagnostics}

Κ{bash builtins; uname,hostname,date,df,ps,ip/ifconfig,awk,grep,wc,bc}

Φ.const{
  SCRIPT_VERSION=1.0.0;
  SECTIONS=[system,cpu,memory,disk,network,process,security,environment]
}
Φ.thresholds{
  DISK_WARN=80%; DISK_CRIT=95%;
  MEM_WARN=85%; MEM_CRIT=95%;
  LOAD_WARN=cores*2; LOAD_CRIT=cores*4;
  UPTIME_WARN=90d; MAX_ZOMBIE=5
}
Φ.colors{RED,GREEN,YELLOW,BLUE,CYAN,BOLD,RESET→ANSI codes}
Φ.state{WARNINGS=[]; CRITICALS=[]; REPORT_LINES=[]; OUTPUT_FILE="";
  OUTPUT_FORMAT=text; SELECTED_SECTIONS=[]; VERBOSE=⊥; USE_COLOR=⊤}

Λ.log{level,msg→void;
  io{stderr→[$ts] $level: $msg};
  DEBUG→only if VERBOSE=⊤}
Λ.report_add{line→void; REPORT_LINES+=$line}
Λ.section_header{title→void; format=padded centered w/ '=' borders}
Λ.format_kv{key,value,width?=30→str; printf "  %-${width}s %s"}
Λ.status_label{val,warn,crit→OK|WARNING|CRITICAL;
  val≥crit→CRITICAL; val≥warn→WARNING; else→OK}
Λ.format_status{status→str; USE_COLOR?colored:[status]}
Λ.record_warning{msg→void; WARNINGS+=$msg; log WARN $msg}
Λ.record_critical{msg→void; CRITICALS+=$msg; log ERROR $msg}
Λ.command_exists{cmd→bool; command -v $cmd >&/dev/null}
Λ.safe_read{file,default="N/A"→str; -r $file?cat:$default}
Λ.human_bytes{bytes→str; ≥1G→GB; ≥1M→MB; ≥1K→KB; else→B}
Λ.human_duration{secs→str; d/h/m format}
Λ.calc_percent{used,total→int; total=0→0; (used*100)/total}

Λ.check_system_info{→void;
  gather: hostname,os_release,kernel,arch,uptime,user,shell,tz;
  src: /etc/os-release|sw_vers, /proc/uptime|sysctl kern.boottime;
  check: uptime>90d→record_warning;
  VERBOSE→+script version,path,PID,PPID}

Λ.check_cpu{→void;
  gather: cpu_model,cores,threads,load_avg[1,5,15];
  src: /proc/cpuinfo|sysctl machdep.cpu, /proc/loadavg|sysctl vm.loadavg;
  check: load vs cores*[2,4]→status_label→record_warn|crit;
  VERBOSE→+top 5 CPU consumers via ps aux --sort=-%cpu}

Λ.check_memory{→void;
  gather: mem_total,used,free,available,swap_total,used,free;
  src: /proc/meminfo|vm_stat+sysctl;
  check: mem_percent vs 85%/95%→record_warn|crit;
  VERBOSE→+top 5 memory consumers via ps aux --sort=-%mem}

Λ.check_disk{→void;
  iter: df -h→each filesystem;
  skip: tmpfs,devtmpfs,none,overlay,shm;
  check: usage% vs 80%/95%→record_warn|crit;
  truncate: filesystem name>24→"...${name: -21}";
  VERBOSE→+inode usage via df -i}

Λ.check_network{→void;
  gather: interfaces via ip|ifconfig;
  check: interfaces_found=0→record_warning;
  dns: test localhost resolve via getent|host;
  VERBOSE→+listening ports top 10 via ss -tlnp|netstat}

Λ.check_processes{→void;
  count: total,running,sleeping,zombie via ps aux;
  check: zombie>MAX_ZOMBIE→CRITICAL; zombie>0→WARNING;
  VERBOSE→+longest running processes via ps -eo pid,etime,%cpu,comm}

Λ.check_security{→void;
  check: id -u=0→running as root→WARNING;
  check: /etc/shadow users w/o password→WARNING;
  ssh: /etc/ssh/sshd_config→PermitRootLogin,PasswordAuthentication;
  firewall: ufw|iptables|firewall-cmd status;
  VERBOSE→+apt security updates count}

Λ.check_environment{→void;
  tools: [bash,git,python3,node,docker,curl,openssl]→version check;
  env: PATH entries count, total env vars, LANG, EDITOR;
  check: TMPDIR writable→OK|WARNING}

Λ.generate_json{exit_code→stdout;
  output: {report:{version,timestamp,hostname,status,exitCode,
    warnings:json_array,criticals:json_array}}}
Λ.json_array{items[]→str; escape "\,"; format ["item1","item2"]}

Λ.generate_summary{→void;
  criticals>0→list critical issues;
  warnings>0→list warnings;
  both=0→"All checks passed - system is healthy!";
  footer: sections count, warnings, criticals, timestamp}

Λ.render_output{exit_code→void;
  json→generate_json→OUTPUT_FILE.json|stdout;
  text→header banner+REPORT_LINES→OUTPUT_FILE.txt|stdout;
  OUTPUT_FILE set→USE_COLOR=⊥}

Λ.show_help{→stdout; usage,options,examples,exit codes}
Λ.parse_args{argv→void;
  --output FILE→OUTPUT_FILE=$FILE;
  --json→OUTPUT_FORMAT=json,USE_COLOR=⊥;
  --section NAME→validate∈ALL_SECTIONS,SELECTED_SECTIONS+=$NAME;
  --verbose→VERBOSE=⊤;
  --no-color→USE_COLOR=⊥;
  --help→show_help,exit 0;
  --version→echo version,exit 0;
  unknown→log ERROR,exit 3;
  default: SELECTED_SECTIONS=ALL_SECTIONS if empty}

Λ.run_section{section→void;
  dispatch: system→check_system_info; cpu→check_cpu;
    memory→check_memory; disk→check_disk; network→check_network;
    process→check_processes; security→check_security;
    environment→check_environment; unknown→log WARN skip}

Γ.main{argv→int;
  parse_args→log INFO start→
  ∀section∈SELECTED_SECTIONS{run_section}→
  generate_summary→
  exit_code: criticals>0→2; warnings>0→1; else→0;
  render_output→log INFO complete→return exit_code}

P.io{
  log→stderr via >&2;
  report→REPORT_LINES buffer→stdout|file;
  json→stdout|file}

P.exit{
  0=all checks passed;
  1=warnings detected;
  2=critical issues;
  3=script error (bad args,missing deps)}

P.safety{
  set -euo pipefail;
  read-only checks; ¬side effects;
  suppress cmd errors via 2>/dev/null}

Ω.decomp{
  emulate=shellcheck;src=sh;
  focus=[
    io_redir(log fn→stderr via >&2),
    quoting(word_split in arrays+cmd subst),
    subshell_capture($(cmd) patterns),
    arithmetic((( )) vs [ ] contexts),
    array_syntax([@] vs [*] expansion)
  ]
}
⟧
```
