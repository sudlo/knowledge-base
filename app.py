import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import webbrowser
import urllib.parse
import subprocess
import sys
import os

# ── Palette (Vibrant Synthwave / Cyberpunk) ──────────────────────
BG       = "#1A1A2E" # Deep twilight blue
PANEL    = "#16213E" # Darker contrasting blue
CARD     = "#0F3460" # Rich navy card
INPUT    = "#1A1A2E" 
BORDER   = "#E94560" # Vibrant red/pink border
HOVER    = "#E94560" # Neon pink hover
ACCENT   = "#00D2FC" # Neon cyan
ACCENT2  = "#FF2A71" # Neon pink
GREEN    = "#00FFC6" # Neon mint
AMBER    = "#FFDE59" # Neon yellow
RED      = "#FF3366" # Neon crimson
BLUE     = "#00D2FC" # Neon cyan
PURPLE   = "#B5179E" # Deep neon purple
TEXT1    = "#FFFFFF" # Pure white
TEXT2    = "#E0E0E0" # Off-white
TEXT3    = "#A0A0B0" # Slate grey
TAG      = "#430F58" # Deep purple tag

F_TITLE  = ("Segoe UI", 20, "bold")
F_HEAD   = ("Segoe UI", 12, "bold")
F_BODY   = ("Segoe UI", 11)
F_SMALL  = ("Segoe UI", 10)
F_MONO   = ("Consolas", 10)

# ── Web search sources (no LinkedIn) ─────────────────────────────
def web_urls(query):
    q = urllib.parse.quote_plus(query)
    return [
        ("Google",              f"https://www.google.com/search?q={q}"),
        ("Stack Overflow",      f"https://stackoverflow.com/search?q={q}"),
        ("GitHub",              f"https://github.com/search?q={q}&type=repositories"),
        ("Google (SO only)",    f"https://www.google.com/search?q=site:stackoverflow.com+{q}"),
        ("Microsoft Docs",      f"https://learn.microsoft.com/en-us/search/?terms={q}"),
        ("AWS Docs",            f"https://docs.aws.amazon.com/search/doc-search.html#searchQuery={q}"),
        ("Kubernetes Docs",     f"https://kubernetes.io/docs/search/?q={q}"),
        ("Docker Docs",         f"https://docs.docker.com/search/?q={q}"),
        ("Dev.to",              f"https://dev.to/search?q={q}"),
        ("Reddit r/sysadmin",   f"https://www.reddit.com/r/sysadmin/search/?q={q}&restrict_sr=1"),
        ("Reddit r/devops",     f"https://www.reddit.com/r/devops/search/?q={q}&restrict_sr=1"),
    ]

# ── All knowledge data ────────────────────────────────────────────
KB = {
    "OS": {
        "Windows Server": {
            "color": BLUE,
            "topics": {
                "AD DS & Domain Services": {
                    "level": "Intermediate", "color": BLUE,
                    "desc": "Active Directory Domain Services is the foundation of Windows identity management. Covers forests, trees, domains, OUs, trusts, and replication.",
                    "concepts": [
                        "Forest / Tree / Domain hierarchy and trust types (forest, external, shortcut, realm)",
                        "Five FSMO roles: Schema Master, Domain Naming, RID Master, PDC Emulator, Infra Master",
                        "LDAP port 389/636 — Kerberos auth flow: AS-REQ → TGT → TGS → service ticket",
                        "AD Replication: KCC builds topology, DFS-R syncs SYSVOL/NETLOGON",
                        "OU design for GPO delegation — keep flat, delegate by role not geography",
                    ],
                    "troubleshooting": [
                        "dcdiag /test:all — comprehensive DC health check",
                        "repadmin /showrepl — replication status per partner",
                        "repadmin /replsummary — quick pass/fail replication overview",
                        "netlogon.log at C:\\Windows\\debug\\netlogon.log — auth failures",
                        "Event 4769 Kerberos failures — check clock skew (must be <5 min)",
                        "dcdiag /test:DNS /fix — repair missing SRV records",
                    ],
                    "tools": ["ADUC", "AD Sites & Services", "ADSI Edit", "repadmin", "dcdiag", "PowerShell AD module"],
                },
                "DNS & DHCP": {
                    "level": "Beginner", "color": BLUE,
                    "desc": "Name resolution and IP address management underpin every network service. Misconfigurations here cascade across all systems.",
                    "concepts": [
                        "Zone types: Primary (AD-integrated), Secondary, Stub, Forward Lookup, Reverse Lookup",
                        "Record types: A, AAAA, CNAME, MX, PTR, SRV, NS, TXT, SOA",
                        "DHCP scopes, exclusions, reservations — options 003 (gateway) 006 (DNS) 015 (domain)",
                        "DHCP failover: Hot Standby (active/passive) vs Load Balance (50/50)",
                        "DNS Scavenging & Aging — prevent stale record accumulation",
                    ],
                    "troubleshooting": [
                        "nslookup hostname — basic forward lookup test",
                        "Resolve-DnsName hostname -Type A — PowerShell DNS query",
                        "ipconfig /flushdns — clear local resolver cache",
                        "ipconfig /registerdns — force re-register client DNS records",
                        "DHCP Event 1012/1016 — scope exhausted, check address utilisation",
                        "Rogue DHCP: enable DHCP Guard on managed switches",
                    ],
                    "tools": ["DNS Manager", "DHCP Console", "nslookup", "Resolve-DnsName", "ipconfig", "Wireshark"],
                },
                "PowerShell Administration": {
                    "level": "Intermediate", "color": BLUE,
                    "desc": "PowerShell is the primary management and automation layer for Windows Server. Objects flow through the pipeline, not text.",
                    "concepts": [
                        "PSRemoting via WinRM (HTTP:5985 / HTTPS:5986) — enable with Enable-PSRemoting",
                        "Pipeline: Get-Process | Where-Object CPU -gt 50 | Sort-Object CPU -Desc",
                        "Modules: ActiveDirectory, Az, AWSPowerShell.NetCore, Microsoft.Graph",
                        "Desired State Configuration (DSC) — declarative node configuration",
                        "Error handling: Try / Catch / Finally — $ErrorActionPreference = 'Stop'",
                        "Credential management: Get-Credential, SecretManagement module, CredSSP",
                    ],
                    "troubleshooting": [
                        "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser — unblock scripts",
                        "Test-WSMan -ComputerName srv01 — verify WinRM connectivity",
                        "Install-Module ModuleName -Force -AllowClobber — fix module conflicts",
                        "Enter-PSSession srv01 -Credential (Get-Credential) — interactive remoting",
                        "Measure-Command { script-block } — profile script performance",
                        "bash -x equivalent: Set-PSDebug -Trace 2 — trace every line",
                    ],
                    "tools": ["PowerShell 7", "Windows Terminal", "VS Code + PS extension", "PSReadLine", "Pester", "SecretManagement"],
                },
                "Event Viewer & Logs": {
                    "level": "Intermediate", "color": BLUE,
                    "desc": "Windows event logs are the complete audit trail. Know the critical Event IDs for security incidents, crashes, and failures.",
                    "concepts": [
                        "Log channels: System, Application, Security, Setup, Forwarded Events",
                        "Event ID 4624 — successful logon (check LogonType: 2=interactive, 3=network, 10=remote)",
                        "Event ID 4625 — failed logon (SubStatus 0xC000006A = wrong password, 0xC0000234 = locked)",
                        "Event ID 7045 — new service installed (common malware persistence indicator)",
                        "Event ID 4688 — process creation (requires audit policy — use Sysmon instead)",
                        "Windows Event Forwarding (WEF/WEC) — centralise logs to collector",
                    ],
                    "troubleshooting": [
                        "Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625} — PowerShell log query",
                        "wevtutil qe Security /q:*[System[EventID=4625]] /f:text — CLI query",
                        "auditpol /get /category:* — check what is actually being audited",
                        "wevtutil set-log Security /ms:1073741824 — set 1GB log size",
                        "Event 7034 service crash → cross-reference Application log for root cause",
                        "Disk errors: Event 7/11 in System log → check storage hardware",
                    ],
                    "tools": ["Event Viewer", "Get-WinEvent", "Sysmon", "wevtutil", "Splunk UF", "Windows Security Compliance Toolkit"],
                },
                "Hyper-V & Virtualisation": {
                    "level": "Advanced", "color": BLUE,
                    "desc": "Hyper-V is a Type-1 hypervisor built into Windows Server. Master VM architecture, live migration, and storage configuration.",
                    "concepts": [
                        "Architecture: parent partition runs management OS, child partitions are VMs",
                        "Virtual switch types: External (physical NIC), Internal (host+VMs), Private (VMs only)",
                        "Gen 1 (BIOS/MBR/IDE) vs Gen 2 (UEFI/GPT/SCSI/SecureBoot) — use Gen 2 for new VMs",
                        "Live Migration requires: shared storage or SMB 3.0, same CPU family, Kerberos delegation",
                        "Hyper-V Replica: async replication to secondary host — 30s minimum interval",
                        "Checkpoints: Standard (saved state) vs Production (VSS-based, application consistent)",
                    ],
                    "troubleshooting": [
                        "VM fails to start: check Hyper-V event log + VM XML config for corruption",
                        "Live migration fails: verify SMB 3.0 multichannel and constrained delegation",
                        "Poor disk IO: use PerfMon Hyper-V Virtual Storage Device counters",
                        "Network performance: ensure Integration Services are current in guest",
                        "Snapshot chain bloat: merge all checkpoints before expanding VHDX",
                        "Quick export then delete to reclaim space from large checkpoint trees",
                    ],
                    "tools": ["Hyper-V Manager", "Failover Cluster Manager", "SCVMM", "PowerShell Hyper-V module", "PerfMon"],
                },
                "Performance Analysis": {
                    "level": "Advanced", "color": BLUE,
                    "desc": "Identify CPU, memory, disk, and network bottlenecks before they become outages. Know which counters matter.",
                    "concepts": [
                        "CPU: %Processor Time >85% sustained = bottleneck; Processor Queue Length >2×cores = saturation",
                        "Memory: Available MBytes <100MB = critical; Pages/sec >20 = memory pressure",
                        "Disk: Avg Disk Queue Length >2 per spindle; %Disk Time >90% = saturated",
                        "Network: Bytes Total/sec vs adapter speed; Output Queue Length >2 = congestion",
                        "Handle leaks: Process\\Handle Count growing without release",
                    ],
                    "troubleshooting": [
                        "Get-Process | Sort-Object CPU -Desc | Select -First 10 — top CPU consumers",
                        "Get-Process | Sort-Object WorkingSet64 -Desc | Select -First 10 — memory hogs",
                        "Resource Monitor → Disk tab → Highest Active Time — find IO bottleneck",
                        "netstat -e — interface-level TX/RX error counters",
                        "xperf + WPA — deep ETW kernel profiling for CPU/disk/network",
                        "Process Explorer (Sysinternals) — real-time handle and DLL inspection",
                    ],
                    "tools": ["Task Manager", "Resource Monitor", "PerfMon", "Process Explorer", "WPA", "xperf"],
                },
                "Group Policy (GPO)": {
                    "level": "Intermediate", "color": BLUE,
                    "desc": "Group Policy is the primary mechanism for enforcing configuration across Windows domain-joined machines at scale.",
                    "concepts": [
                        "GPO processing order: Local → Site → Domain → OU (LSDOU) — last write wins",
                        "Computer vs User policy — Computer applies at boot, User at logon",
                        "WMI filters: target GPOs to specific OS versions or hardware",
                        "Loopback processing: Merge or Replace mode for RDS/VDI environments",
                        "Preference vs Policy: Preferences are configurable by users, Policies enforce",
                    ],
                    "troubleshooting": [
                        "gpresult /h report.html — full GPO RSoP for user+computer",
                        "gpupdate /force — force immediate policy refresh",
                        "gpresult /scope computer /v — verbose computer policy application",
                        "Event 1085/1125 in System log — GPO processing errors",
                        "Group Policy Modeling wizard — simulate GPO impact before apply",
                    ],
                    "tools": ["GPMC", "gpresult", "gpupdate", "RSOP.msc", "Group Policy Modeling"],
                },
                "IIS & Web Server": {
                    "level": "Intermediate", "color": BLUE,
                    "desc": "Internet Information Services hosts ASP.NET, PHP, and static sites. Master application pools, bindings, and SSL configuration.",
                    "concepts": [
                        "Application Pool: isolation boundary — each pool is a separate w3wp.exe process",
                        "Integrated vs Classic pipeline mode — always use Integrated for ASP.NET 4+",
                        "Site bindings: IP, Port, Host Header — SNI for multiple SSL certs on port 443",
                        "Failed Request Tracing (FREB) — captures detailed request trace for 4xx/5xx",
                        "Output caching, kernel caching, and static content compression",
                    ],
                    "troubleshooting": [
                        "HTTP 500.19 — web.config parse error (check XML syntax)",
                        "HTTP 503 Service Unavailable — app pool stopped or rapid fail protection triggered",
                        "appcmd list apppool /processModel.userName:* — find pools running as domain accounts",
                        "Failed Request Tracing: enable in IIS Manager → site → Failed Req Tracing Rules",
                        "netsh http show urlacl — check URL ACL reservations",
                        "icacls C:\\inetpub\\wwwroot — verify IIS_IUSRS has read access",
                    ],
                    "tools": ["IIS Manager", "appcmd", "Failed Request Tracing", "Process Monitor", "Fiddler"],
                },
                "Storage & RAID": {
                    "level": "Intermediate", "color": BLUE,
                    "desc": "Windows Server storage: from basic disks to Storage Spaces Direct (S2D) for hyperconverged infrastructure.",
                    "concepts": [
                        "RAID 0 (stripe), RAID 1 (mirror), RAID 5 (parity), RAID 10 (stripe+mirror)",
                        "Storage Spaces: virtual disks on pooled physical disks — Simple, Mirror, Parity",
                        "Storage Spaces Direct (S2D): software-defined storage using local NVMe/SSD/HDD",
                        "ReFS vs NTFS: ReFS for large volumes and S2D, NTFS for general purpose",
                        "iSCSI initiator: connect to SAN LUNs over IP network",
                        "Volume Shadow Copy Service (VSS): application-consistent snapshots",
                    ],
                    "troubleshooting": [
                        "Get-PhysicalDisk | Where HealthStatus -ne Healthy — find failed disks",
                        "Get-StoragePool | Get-VirtualDisk — check virtual disk health",
                        "chkdsk C: /f /r — check and repair filesystem errors (requires reboot for C:)",
                        "diskpart → list volume / list disk — enumerate storage",
                        "Event ID 7/11 in System log → hardware storage error",
                        "S2D: Get-StorageSubSystem — overall S2D cluster health",
                    ],
                    "tools": ["Disk Management", "diskpart", "Storage Spaces", "Get-PhysicalDisk", "chkdsk"],
                },
            }
        },
        "Linux": {
            "color": AMBER,
            "topics": {
                "Process & Service Management": {
                    "level": "Intermediate", "color": AMBER,
                    "desc": "Linux process lifecycle, systemd service management, and cgroup resource control — the foundation of server stability.",
                    "concepts": [
                        "Process states: R(running) S(sleeping) D(uninterruptible-IO) Z(zombie) T(stopped)",
                        "Signals: SIGTERM(15) graceful stop, SIGKILL(9) force kill, SIGHUP(1) reload config",
                        "systemd unit types: .service .socket .timer .target .mount .path",
                        "cgroups v2: unified hierarchy — CPU weight, memory.max, io.max per unit",
                        "PID namespace: containers use separate PID space — PID 1 is init inside container",
                    ],
                    "troubleshooting": [
                        "ps aux --sort=-%cpu | head -15 — top CPU consumers",
                        "systemctl status nginx.service — state + last 10 journal lines",
                        "journalctl -u nginx -f --since '10 min ago' — follow service logs",
                        "D-state (uninterruptible): ps aux | grep ' D ' — usually NFS/disk hang",
                        "Zombie: kill parent process (kill -9 $(ps -o ppid= -p <zombie_pid>))",
                        "systemd-analyze blame — services slowing down boot",
                    ],
                    "tools": ["htop", "systemctl", "journalctl", "strace -p <pid>", "lsof -p <pid>", "systemd-analyze"],
                },
                "Networking Commands": {
                    "level": "Intermediate", "color": AMBER,
                    "desc": "Linux networking stack diagnostics using modern iproute2 tools. ifconfig and netstat are deprecated — use ip and ss.",
                    "concepts": [
                        "ip addr show — interface addresses (replaces ifconfig)",
                        "ip route show — routing table (replaces route -n)",
                        "ss -tulnp — listening ports with process names (replaces netstat, 10× faster)",
                        "iptables / nftables — kernel netfilter packet filtering chains",
                        "Network namespaces: foundation of containers, VPNs, and network isolation",
                        "tc (traffic control): queueing disciplines for bandwidth shaping",
                    ],
                    "troubleshooting": [
                        "ip -s link show eth0 — TX/RX packets, errors, and drops",
                        "ss -s — socket summary (total established, time-wait, etc.)",
                        "tcpdump -i eth0 'port 80' -w /tmp/cap.pcap — capture to file",
                        "traceroute -T -p 443 host — TCP traceroute bypasses ICMP blocks",
                        "mtr --report host — combined ping+traceroute with packet loss",
                        "conntrack -L | grep host — active connection tracking entries",
                    ],
                    "tools": ["ip / iproute2", "ss", "tcpdump", "nmap", "iperf3", "mtr", "nftables"],
                },
                "Shell Scripting & Bash": {
                    "level": "Intermediate", "color": AMBER,
                    "desc": "Bash is the automation glue of Linux sysadmin. Write safe, portable scripts with proper error handling from the start.",
                    "concepts": [
                        "set -euo pipefail — exit on error, unset variable, pipe failure",
                        "Parameter expansion: ${var:-default} ${var:?error_msg} ${var%suffix}",
                        "Arrays: declare -a arr; mapfile -t arr < file; for i in \"${arr[@]}\"",
                        "Process substitution: diff <(cmd1) <(cmd2) — compare command output",
                        "Trap: trap 'rm -f $tmpfile' EXIT — always clean up temp files",
                        "Here-doc: cat <<EOF ... EOF — multi-line strings without escaping",
                    ],
                    "troubleshooting": [
                        "bash -x script.sh — xtrace: print each command before executing",
                        "shellcheck script.sh — static analysis, catches common bugs",
                        "IFS=$'\\n\\t' — prevent word splitting on spaces in filenames",
                        "Always quote variables: \"$var\" not $var — prevents glob expansion",
                        "Cron PATH is /usr/bin:/bin — use absolute paths in cron scripts",
                        "set -x at top, set +x to turn off — surgical tracing",
                    ],
                    "tools": ["shellcheck", "bash -x", "awk", "sed", "jq", "shfmt", "bats (testing)"],
                },
                "Kernel Tuning & sysctl": {
                    "level": "Advanced", "color": AMBER,
                    "desc": "Linux kernel parameters govern TCP stack behaviour, memory management, and file descriptor limits. Critical for high-traffic servers.",
                    "concepts": [
                        "sysctl -a — list all parameters; /proc/sys/ is the virtual filesystem backing them",
                        "vm.swappiness=10 — prefer RAM over swap (0=never swap, 60=default, 100=aggressive)",
                        "net.core.somaxconn=65535 — max listen() backlog for high-connection services",
                        "fs.file-max and ulimit -n — system-wide and per-process file descriptor limits",
                        "net.ipv4.tcp_tw_reuse=1 — safely reuse TIME_WAIT sockets",
                        "net.ipv4.ip_local_port_range=1024 65535 — available ephemeral port range",
                    ],
                    "troubleshooting": [
                        "Too many open files: check /proc/<pid>/limits and fs.file-max",
                        "TCP port exhaustion: ss -s | grep TIME-WAIT; set tcp_tw_reuse=1",
                        "OOM kills: dmesg | grep -i 'oom\\|killed' — find victim processes",
                        "sysctl -w net.core.somaxconn=65535 — apply immediately (not persistent)",
                        "echo 'net.core.somaxconn=65535' >> /etc/sysctl.d/99-custom.conf — persist",
                        "sysctl -p /etc/sysctl.d/99-custom.conf — reload from file",
                    ],
                    "tools": ["sysctl", "tuned (RHEL)", "numactl", "perf stat", "/proc/sys", "ss"],
                },
                "Log Analysis": {
                    "level": "Intermediate", "color": AMBER,
                    "desc": "Linux logs: systemd journal for modern systems, traditional syslog for legacy. Master filtering for fast incident diagnosis.",
                    "concepts": [
                        "/var/log structure: auth.log, syslog, kern.log, dmesg, secure (RHEL/CentOS)",
                        "journalctl priorities: 0=emerg 1=alert 2=crit 3=err 4=warn 5=notice 6=info 7=debug",
                        "Persistent journal: mkdir /var/log/journal; systemctl restart systemd-journald",
                        "rsyslog: facility.severity → file/remote — /etc/rsyslog.conf",
                        "auditd: immutable audit trail for sudo, file access, exec — required for PCI/SOC2",
                        "logrotate: /etc/logrotate.d/ — daily/weekly rotation with compress and postrotate",
                    ],
                    "troubleshooting": [
                        "journalctl -b -1 — all logs from previous boot (crash diagnosis)",
                        "journalctl -p err..crit --since today — errors and worse since midnight",
                        "dmesg -T | grep -iE 'error|fail|oom|panic' — kernel error filter",
                        "lastb — all failed login attempts with source IP",
                        "ausearch -k exec -ts today — auditd exec events today",
                        "logrotate -d /etc/logrotate.conf — dry-run to test rotation config",
                    ],
                    "tools": ["journalctl", "rsyslog", "auditd / ausearch", "Filebeat", "Loki + Grafana", "logwatch"],
                },
                "Performance (top/vmstat/iostat)": {
                    "level": "Advanced", "color": AMBER,
                    "desc": "USE Method: Utilization, Saturation, Errors — apply to CPU, memory, disk, and network for systematic performance analysis.",
                    "concepts": [
                        "Load average: 1/5/15 min moving average of runnable+uninterruptible threads",
                        "vmstat 1: r(runqueue) b(blocked) si/so(swap in/out) wa(iowait) id(idle)",
                        "iostat -x 1: %util(saturation) await(latency ms) r/s w/s rkB/s wkB/s",
                        "free -m: available = free + reclaimable cache — not just 'free'",
                        "perf top / flamegraphs: CPU profiling with kernel+userspace stack traces",
                        "eBPF / bpftrace: zero-overhead kernel tracing for production systems",
                    ],
                    "troubleshooting": [
                        "Load > nCPU: vmstat 1 → check 'r' column (runqueue length)",
                        "High iowait: iostat -x 1 → find disk with high await or %util",
                        "Swap activity: vmstat si/so > 0 → memory pressure, check what OOMs",
                        "Network retransmit: ss --tcp --info | grep retrans",
                        "Memory leak: watch -n5 'ps aux --sort=-rss | head' — growing RSS",
                        "perf record -g -p PID sleep 30; perf script | flamegraph.pl > out.svg",
                    ],
                    "tools": ["htop", "vmstat", "iostat", "sar", "perf", "bpftrace", "BCC tools"],
                },
                "User & Permission Management": {
                    "level": "Beginner", "color": AMBER,
                    "desc": "Linux user model: UIDs, GIDs, file permissions, sudo, and PAM for authentication policy.",
                    "concepts": [
                        "File permissions: rwx for owner/group/other — octal 755=rwxr-xr-x 644=rw-r--r--",
                        "Special bits: SUID(4000) SGID(2000) Sticky(1000) — chmod 4755, chmod 1777",
                        "ACLs: getfacl / setfacl — per-user/group permissions beyond basic rwx",
                        "sudo: /etc/sudoers via visudo — NOPASSWD, command restrictions, runas",
                        "PAM: /etc/pam.d/ — pluggable auth modules for password policy, MFA, limits",
                        "umask: default permission mask — umask 022 → new files get 644",
                    ],
                    "troubleshooting": [
                        "Permission denied: ls -la to check owner/group/perms, id to check current user",
                        "find / -perm -4000 2>/dev/null — find all SUID binaries (security audit)",
                        "sudo -l -U username — what can this user run via sudo",
                        "getent passwd username — check user exists and shell",
                        "faillock --user username — show failed login attempts and lockout state",
                        "chattr +i /etc/passwd — make file immutable (prevent accidental edit)",
                    ],
                    "tools": ["chmod", "chown", "getfacl/setfacl", "visudo", "PAM", "faillock"],
                },
                "Package Management": {
                    "level": "Beginner", "color": AMBER,
                    "desc": "apt (Debian/Ubuntu) and dnf/yum (RHEL/CentOS/Fedora) — installing, upgrading, and pinning packages safely.",
                    "concepts": [
                        "apt: /etc/apt/sources.list + sources.list.d/ — repository management",
                        "dpkg: low-level Debian package tool — apt uses dpkg underneath",
                        "dnf / yum: RPM-based — /etc/yum.repos.d/ for repository configuration",
                        "Package pinning: apt-mark hold pkg — prevent package from being upgraded",
                        "PPA: Personal Package Archive (Ubuntu) — third-party repositories",
                        "rpm -qa — list all installed RPM packages with version",
                    ],
                    "troubleshooting": [
                        "apt update && apt list --upgradable — see what can be updated",
                        "dpkg -l | grep -i nginx — check if package is installed and version",
                        "apt-get install -f — fix broken dependency chains",
                        "dpkg --configure -a — finish interrupted package configuration",
                        "dnf history undo last — roll back the last dnf transaction",
                        "rpm -qf /usr/bin/curl — which package owns a specific file",
                    ],
                    "tools": ["apt", "dpkg", "dnf", "yum", "rpm", "snap", "flatpak"],
                },
            }
        }
    },
    "Cloud": {
        "AWS": {
            "color": AMBER,
            "Compute":    ["EC2", "Lambda", "ECS", "EKS", "Fargate", "Batch", "Elastic Beanstalk", "Lightsail", "Outposts"],
            "Storage":    ["S3", "EBS", "EFS", "FSx", "S3 Glacier", "Storage Gateway", "AWS Backup", "Snow Family"],
            "Networking": ["VPC", "Route 53", "CloudFront", "ALB/NLB/ELB", "Direct Connect", "Transit Gateway", "PrivateLink", "Global Accelerator"],
            "Database":   ["RDS", "Aurora", "DynamoDB", "ElastiCache", "Redshift", "DocumentDB", "Neptune", "Keyspaces", "Timestream"],
            "DevOps":     ["CodePipeline", "CodeBuild", "CodeDeploy", "CodeCommit", "CloudFormation", "CDK", "Systems Manager", "ECR"],
            "Security":   ["IAM", "KMS", "Secrets Manager", "GuardDuty", "Security Hub", "WAF & Shield", "Macie", "Inspector"],
            "Monitoring": ["CloudWatch", "X-Ray", "CloudTrail", "AWS Config", "Trusted Advisor", "Cost Explorer", "AWS Health"],
        },
        "Azure": {
            "color": BLUE,
            "Compute":    ["Virtual Machines", "Azure Functions", "AKS", "Container Apps", "App Service", "Azure Batch", "Service Fabric", "Spring Apps"],
            "Storage":    ["Blob Storage", "Azure Disk", "Azure Files", "NetApp Files", "Data Lake Gen2", "Archive Storage", "Azure Backup", "Import/Export"],
            "Networking": ["Virtual Network", "Azure DNS", "Azure CDN", "Load Balancer", "Application Gateway", "ExpressRoute", "Azure Firewall", "DDoS Protection"],
            "Database":   ["Azure SQL", "Cosmos DB", "Cache for Redis", "PostgreSQL Flexible", "MySQL Flexible", "Synapse Analytics", "Managed Instance", "MariaDB"],
            "DevOps":     ["Azure Pipelines", "GitHub Actions", "Azure Repos", "Artifacts", "Bicep / ARM", "Container Registry", "DevTest Labs", "Load Testing"],
            "Security":   ["Entra ID", "Key Vault", "Defender for Cloud", "Sentinel", "Azure Policy", "PIM", "Bastion", "Confidential Computing"],
            "Monitoring": ["Azure Monitor", "App Insights", "Log Analytics", "Azure Advisor", "Cost Management", "Service Health", "Network Watcher"],
        },
        "Google Cloud": {
            "color": GREEN,
            "Compute":    ["Compute Engine", "Cloud Run", "GKE", "Cloud Functions", "App Engine", "Cloud Batch", "Bare Metal", "Vertex AI"],
            "Storage":    ["Cloud Storage", "Persistent Disk", "Filestore", "Archive Storage", "Transfer Service", "FUSE CSI driver", "Backup and DR"],
            "Networking": ["VPC", "Cloud DNS", "Cloud CDN", "Cloud Load Balancing", "Cloud Interconnect", "VPC Service Controls", "Cloud Armor", "Network Intelligence"],
            "Database":   ["Cloud SQL", "Firestore", "Bigtable", "Spanner", "BigQuery", "Memorystore", "AlloyDB", "Datastream"],
            "DevOps":     ["Cloud Build", "Cloud Deploy", "Artifact Registry", "Source Repositories", "Config Connector", "Deployment Manager", "Skaffold"],
            "Security":   ["IAM", "Cloud KMS", "Secret Manager", "Security Command Center", "Binary Authorization", "Assured Workloads", "Chronicle SIEM"],
            "Monitoring": ["Cloud Monitoring", "Cloud Trace", "Cloud Logging", "Cloud Profiler", "Error Reporting", "Cost Management", "Operations Suite"],
        },
    },
    "DevOps": {
        "CI/CD": {
            "GitHub Actions": {
                "color": GREEN, "type": "CI/CD",
                "desc": "Event-driven automation workflows. YAML-based, triggers on push/PR/schedule/manual. OIDC for keyless cloud authentication.",
                "deep_dive": [
                    "Workflow anatomy: on (triggers) → jobs → steps → uses/run",
                    "Reusable workflows: workflow_call trigger for DRY pipelines",
                    "OIDC: keyless auth to AWS/Azure/GCP — no stored secrets needed",
                    "Matrix builds: test across multiple OS, Node, Python versions in parallel",
                    "Actions Runner Controller (ARC): self-hosted runners on Kubernetes",
                    "Caching: actions/cache for npm/pip/maven — speeds up builds 3-5×",
                    "Environments: production gates with required reviewers + wait timer",
                    "Composite actions: reusable steps without a full workflow",
                ],
                "troubleshooting": [
                    "Act (local runner): act push — test workflows locally before pushing",
                    "OIDC 403: check audience claim matches cloud provider config",
                    "Cache miss: verify cache key includes lockfile hash",
                    "Runner out of disk: add step to free disk space before large builds",
                    "Concurrency groups: prevent duplicate runs on same branch",
                ],
            },
            "Azure Pipelines": {
                "color": BLUE, "type": "CI/CD",
                "desc": "Multi-stage YAML pipelines for any language, any platform. Microsoft-hosted or self-hosted agents. Deep Azure integration.",
                "deep_dive": [
                    "Multi-stage YAML: stages → jobs → steps hierarchy with dependencies",
                    "Environments: production approval gates, deployment history, rollback",
                    "Service connections: federated identity (OIDC) for Azure/AWS/GCP",
                    "Pipeline templates: extends templates for corporate governance",
                    "Variable groups: shared variables + Azure Key Vault integration",
                    "Deployment strategies: canary, blue-green, rolling in environments",
                    "Self-hosted agent pools on AKS (KEDA-based autoscaling agents)",
                    "Matrix strategy: parallel jobs across OS/framework combinations",
                ],
                "troubleshooting": [
                    "Agent offline: check agent capability vs job demand requirements",
                    "Service connection 401: regenerate service principal secret or use OIDC",
                    "Pipeline stuck: check concurrent job limits on free tier (1 parallel job)",
                    "Artifact not found: ensure publishPipelineArtifact before download step",
                    "Template not found: verify path is relative to repository root",
                ],
            },
            "Jenkins": {
                "color": RED, "type": "CI/CD",
                "desc": "Open-source CI/CD server with 1800+ plugins. Declarative and Scripted Pipelines via Jenkinsfile. Self-hosted, full control.",
                "deep_dive": [
                    "Declarative Pipeline: pipeline → agent → stages → stage → steps",
                    "Shared Libraries: vars/ and src/ directories for reusable code",
                    "Kubernetes plugin: ephemeral pod agents — agent { kubernetes { yaml ... } }",
                    "Blue Ocean: modern pipeline visualisation UI",
                    "Credentials: Username/Password, SSH, Secret Text, Certificate stores",
                    "Docker pipeline plugin: agent { docker { image 'node:18' } }",
                    "Multibranch Pipeline: auto-discover branches and PRs via Jenkinsfile",
                    "Pipeline triggers: SCM polling, GitHub webhooks, upstream jobs",
                ],
                "troubleshooting": [
                    "OutOfMemoryError: increase JAVA_OPTS -Xmx in jenkins.service",
                    "Workspace not found: check agent has disk space and permissions",
                    "Plugin conflict: Safe Restart, then disable conflicting plugin",
                    "Groovy sandbox rejection: approve script in Manage Jenkins → In-process Script Approval",
                    "Build stuck: check executor count vs queued jobs ratio",
                ],
            },
        },
        "IaC": {
            "Terraform": {
                "color": PURPLE, "type": "IaC",
                "desc": "Industry-standard declarative IaC. Provider ecosystem covers every cloud. Remote state enables team collaboration.",
                "deep_dive": [
                    "HCL: resource, data, variable, output, locals, module blocks",
                    "Remote state: S3+DynamoDB lock (AWS), Azure Blob (Azure), GCS (GCP)",
                    "Workspace vs directory-per-environment — prefer directories for isolation",
                    "Module structure: root module calls child modules, publish to registry",
                    "State commands: import, taint, untaint, state mv, state rm, state pull",
                    "Terragrunt: DRY Terraform — keep_terraform_version, generate blocks",
                    "Atlantis: GitOps Terraform — PR comments trigger plan/apply",
                    "Sentinel / OPA: policy-as-code to block non-compliant infrastructure",
                ],
                "troubleshooting": [
                    "State lock: terraform force-unlock <lock-id> if stale lock exists",
                    "Provider version conflict: pin with required_providers block",
                    "Plan shows delete+create: use lifecycle { create_before_destroy = true }",
                    "State drift: terraform refresh then decide whether to import or taint",
                    "Sensitive output: mark output as sensitive = true to hide from logs",
                ],
            },
            "Ansible": {
                "color": RED, "type": "IaC",
                "desc": "Agentless configuration management over SSH. Idempotent YAML playbooks. Push-based. Scales from 1 to 10,000 nodes.",
                "deep_dive": [
                    "Inventory: static INI/YAML, dynamic plugins (aws_ec2, azure_rm, gcp_compute)",
                    "Playbook: plays → tasks → handlers — notify triggers handler on change only",
                    "Roles: files/ templates/ vars/ defaults/ tasks/ handlers/ meta/ structure",
                    "Ansible Vault: ansible-vault encrypt_string for inline secrets",
                    "Jinja2: when conditions, loops (with_items/loop), filters (|default, |quote)",
                    "Collections: install from Galaxy: ansible-galaxy collection install namespace.name",
                    "Molecule + Docker: TDD for roles — molecule init, molecule test",
                    "AWX / Automation Controller: enterprise scheduling, RBAC, credential vaulting",
                ],
                "troubleshooting": [
                    "ansible -m ping all — connectivity check before running playbooks",
                    "ansible-playbook play.yml -vvv — maximum verbosity for debugging",
                    "SSH key not accepted: check ansible_user and ansible_ssh_private_key_file",
                    "Task not idempotent: check module return changed and add when condition",
                    "Vault password prompt in CI: use --vault-password-file or ANSIBLE_VAULT_PASSWORD_FILE",
                ],
            },
            "Bicep / ARM": {
                "color": BLUE, "type": "IaC",
                "desc": "Azure-native IaC. Bicep compiles to ARM JSON. Type-safe, modular, IDE-friendly. Preferred over raw ARM templates.",
                "deep_dive": [
                    "Resource declaration: resource sym 'type@version' = { name: ... properties: ... }",
                    "Modules: module sym './child.bicep' = { params: ... } for reuse",
                    "Parameters, variables, functions (@description, @minLength decorators)",
                    "What-if: az deployment group what-if — preview changes before apply",
                    "Deployment stacks: manage lifecycle of resource groups as a unit",
                    "Template specs: versioned templates shared across subscriptions",
                    "Loops: [for item in array: { ... item ... }] — create resource arrays",
                    "Bicep Registry: private module registry in Azure Container Registry",
                ],
                "troubleshooting": [
                    "bicep build main.bicep — compile to ARM, shows syntax errors",
                    "az deployment group validate — validate against Azure without deploying",
                    "Circular dependency: bicep linter flags dependsOn cycles",
                    "API version mismatch: check az provider show --namespace Microsoft.Compute",
                    "Complete mode accidental delete: always use Incremental mode unless intentional",
                ],
            },
        },
        "Containers": {
            "Docker": {
                "color": BLUE, "type": "Container",
                "desc": "OCI-compliant container runtime and image packaging standard. Foundation for all cloud-native development and deployment.",
                "deep_dive": [
                    "Multi-stage builds: FROM node:18 AS build ... FROM nginx:alpine COPY --from=build",
                    "Layer caching: COPY package*.json first, RUN npm install, then COPY . .",
                    "Networking: bridge (default), host (bypass NAT), overlay (Swarm/multi-host)",
                    "Docker Compose v3: services, volumes, networks, depends_on, healthcheck",
                    "Security: USER nonroot, --read-only filesystem, distroless base images",
                    "BuildKit: --mount=type=cache for package manager caches in builds",
                    "Image scanning: trivy image myapp:latest — CVE scanning before push",
                    "Registry: ECR, ACR, GCR, Harbor (self-hosted with RBAC + scanning)",
                ],
                "troubleshooting": [
                    "docker inspect container — full config, mounts, network, env vars",
                    "docker logs container --tail 100 -f — follow last 100 lines",
                    "docker exec -it container sh — shell into running container",
                    "docker system prune -a — clean all unused images/containers/volumes",
                    "Container OOM: docker stats — CPU/memory usage; check --memory limit",
                    "Network unreachable: docker network inspect bridge — check subnet overlap",
                ],
            },
            "Kubernetes": {
                "color": BLUE, "type": "Container",
                "desc": "Container orchestration: declarative desired state, self-healing, auto-scaling, rolling deployments across clusters.",
                "deep_dive": [
                    "Core objects: Pod, Deployment, StatefulSet, DaemonSet, Job, CronJob",
                    "Services: ClusterIP, NodePort, LoadBalancer, ExternalName, Headless",
                    "Ingress + IngressClass — nginx, traefik, AWS ALB controller",
                    "Storage: PV/PVC/StorageClass, CSI drivers (EBS, Azure Disk, GCE PD)",
                    "RBAC: ClusterRole, Role, Binding, ServiceAccount — least privilege always",
                    "HPA (CPU/memory) + KEDA (event-driven: queue depth, Prometheus metric)",
                    "GitOps: ArgoCD or Flux — cluster state from Git, auto-sync + drift detection",
                    "Probes: liveness (restart if unhealthy), readiness (remove from Service), startup",
                ],
                "troubleshooting": [
                    "kubectl describe pod <pod> — events section shows scheduling/pull failures",
                    "kubectl logs <pod> --previous — logs from crashed previous container",
                    "kubectl exec -it <pod> -- sh — shell into running container",
                    "kubectl get events --sort-by=.lastTimestamp -n <ns> — recent cluster events",
                    "CrashLoopBackOff: check logs + liveness probe configuration",
                    "Pending pod: kubectl describe → Insufficient CPU/memory or no matching node",
                    "ImagePullBackOff: check imagePullSecrets and registry credentials",
                ],
            },
            "Helm": {
                "color": BLUE, "type": "Container",
                "desc": "Kubernetes package manager. Charts bundle manifests into versioned, configurable packages. Releases track deployment history.",
                "deep_dive": [
                    "Chart structure: Chart.yaml, values.yaml, templates/, charts/ (dependencies)",
                    "Template functions: include, toYaml, indent, nindent, required, default",
                    "Values override: helm install -f prod-values.yaml --set key=value",
                    "Hooks: pre-install, post-install, pre-upgrade — database migrations",
                    "Helm 3: no Tiller, releases stored as Secrets in namespace",
                    "OCI registries: helm push mychart oci://registry/repo — store in ECR/ACR/GCR",
                    "Helmfile: declarative releases across environments with diff and sync",
                    "helm diff upgrade: preview changes before applying to cluster",
                ],
                "troubleshooting": [
                    "helm list -A — all releases across all namespaces",
                    "helm history release-name — full upgrade/rollback history",
                    "helm rollback release-name 2 — roll back to revision 2",
                    "helm template . | kubectl apply --dry-run=client -f - — validate manifests",
                    "Stuck in pending-upgrade: helm rollback then re-apply",
                ],
            },
        },
        "Monitoring": {
            "Prometheus & Grafana": {
                "color": AMBER, "type": "Monitoring",
                "desc": "De-facto standard metrics stack for cloud-native. Pull-based metrics with PromQL query language and rich alerting.",
                "deep_dive": [
                    "Data model: metric_name{label=value,...} @ timestamp = float64 value",
                    "PromQL: rate(http_requests_total[5m]) — per-second rate over 5min window",
                    "Alertmanager: routes, receivers (PagerDuty/Slack/email), inhibit_rules, silences",
                    "kube-prometheus-stack: Prometheus Operator + ServiceMonitor/PodMonitor CRDs",
                    "Grafana: variables, data links, annotations, alert rules with contact points",
                    "Remote write: Thanos/Cortex/Mimir for long-term metric storage + HA",
                    "Recording rules: pre-compute expensive aggregations for dashboard performance",
                    "Exporters: node_exporter, blackbox_exporter, postgres_exporter, custom /metrics",
                ],
                "troubleshooting": [
                    "Target down: check /targets in Prometheus UI — scrape error details",
                    "Cardinality explosion: topk(10, count by (__name__)({}) ) — find high-cardinality metrics",
                    "AlertManager not firing: check route match and receiver config in /status",
                    "Grafana no data: verify datasource URL and time range includes data",
                    "PromQL range too short: rate() window must be >2× scrape interval",
                ],
            },
            "ELK / EFK Stack": {
                "color": AMBER, "type": "Monitoring",
                "desc": "Log aggregation and full-text search. Elasticsearch storage, Logstash/Fluentd ingestion, Kibana visualisation.",
                "deep_dive": [
                    "Elasticsearch: indices, shards, replicas — shard count affects parallelism",
                    "ILM (Index Lifecycle Management): hot → warm → cold → frozen → delete",
                    "Logstash pipeline: input (beats/kafka) → filter (grok/mutate/date) → output",
                    "Fluent Bit DaemonSet: lightweight log collector for Kubernetes nodes",
                    "Kibana: Discover, Lens, Canvas, Alerting, APM, Fleet management",
                    "Beats: Filebeat (logs), Metricbeat (metrics), Packetbeat (network), Auditbeat",
                    "OpenSearch: AWS fork of Elasticsearch — compatible API, different licensing",
                    "Security: TLS between nodes, X-Pack auth, field-level security, audit logging",
                ],
                "troubleshooting": [
                    "Cluster red: GET /_cluster/health?pretty — find unassigned shards",
                    "Heap pressure: JVM heap >75% → increase Xmx or reduce shard count",
                    "Logstash pipeline stuck: check Dead Letter Queue for failed events",
                    "Filebeat not shipping: filebeat -e -d '*' — debug output to console",
                    "Index mapping conflict: field type mismatch between indices — use data streams",
                ],
            },
        },
    },
    "Networking": {
        "OSI & TCP/IP Model": {
            "color": BLUE,
            "desc": "The layered model for understanding network communication. OSI helps isolate problems; TCP/IP is what actually runs.",
            "concepts": [
                "L1 Physical: cables, fibre, NICs, signal encoding, hubs (broadcast domain)",
                "L2 Data Link: MAC addresses, ARP, Ethernet frames, VLANs (802.1Q), STP",
                "L3 Network: IPv4/IPv6, routing, ICMP, TTL decrement, fragmentation (MTU)",
                "L4 Transport: TCP (reliable, ordered, congestion control) vs UDP (fast, best-effort)",
                "L5-7 Application: TLS record layer (L5/6), HTTP/DNS/SMTP (L7)",
                "Encapsulation: each layer adds a header; decapsulation strips in reverse at receiver",
            ],
            "troubleshooting": [
                "ping host — L3 ICMP reachability (use -I eth0 to specify source interface)",
                "traceroute / tracert -d — L3 path with per-hop RTT",
                "arp -a / ip neigh — L2 ARP cache (check for duplicate MACs)",
                "tcpdump -i eth0 -nn 'host 10.0.0.1' — L2-L7 packet capture",
                "openssl s_client -connect host:443 — TLS handshake inspection",
            ],
        },
        "Subnetting & CIDR": {
            "color": BLUE,
            "desc": "IP address planning is foundational to cloud and on-premises network design. Mistakes here force painful refactoring.",
            "concepts": [
                "CIDR notation: /24=256IPs /25=128 /22=1024 /16=65536 /8=16M",
                "Usable hosts = 2^(32-prefix) - 2 (network + broadcast reserved)",
                "Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (RFC1918)",
                "Supernetting: summarise multiple routes into one prefix (reduces routing table)",
                "VLSM: allocate different prefix lengths to different subnets to minimise waste",
                "IPv6: /64 per subnet standard, /48 per site, link-local fe80::/10 auto-configured",
            ],
            "troubleshooting": [
                "ipcalc 10.0.1.0/24 — visual subnet breakdown with all addresses",
                "ip route get 8.8.8.8 — which interface and gateway will be used for this dest",
                "VPC CIDR overlap: most common cause of peering failures — plan non-overlapping ranges",
                "Broadcast storms: /31 and /30 correct for point-to-point links",
                "MTU black hole: pmtud failure — test with ping -M do -s 1472 host",
            ],
        },
        "DNS Deep Dive": {
            "color": BLUE,
            "desc": "DNS is the internet's directory. Every service dependency goes through DNS. Understand it fully to debug latency and failures.",
            "concepts": [
                "DNS hierarchy: root (.) → TLD (.com) → authoritative → recursive resolver → client",
                "Record types: A(IPv4), AAAA(IPv6), CNAME(alias), MX(mail), TXT(SPF/DKIM), SRV, PTR, CAA",
                "TTL: controls caching duration — low TTL enables fast failover but increases query load",
                "DNSSEC: cryptographic chain of trust from root → TLD → zone using DS and RRSIG records",
                "Split-horizon: same name resolves differently for internal vs external clients",
                "DNS over HTTPS (DoH) / DNS over TLS (DoT): encrypted resolution (port 443/853)",
            ],
            "troubleshooting": [
                "dig +trace example.com — full resolution from root servers step by step",
                "dig @8.8.8.8 example.com A — query specific resolver directly",
                "dig +short TXT example.com — check SPF/DKIM TXT records",
                "nslookup -type=SRV _kerberos._tcp.domain.com — SRV record lookup",
                "dig +norecurse @authoritative-ns example.com — check authoritative answer only",
                "DNS propagation delay: TTL expiry + upstream resolver cache flush time",
            ],
        },
        "HTTP/HTTPS & TLS": {
            "color": BLUE,
            "desc": "HTTP is the protocol of the web and APIs. TLS provides confidentiality and authentication. Master both for debugging.",
            "concepts": [
                "HTTP/1.1 vs HTTP/2 (multiplexing, HPACK header compression, server push)",
                "HTTP/3: QUIC transport (UDP-based), eliminates head-of-line blocking",
                "Status codes: 1xx info, 2xx success, 3xx redirect, 4xx client error, 5xx server error",
                "TLS 1.3 handshake: ClientHello → ServerHello+Certificate+Finished → client Finished (1-RTT)",
                "Certificate chain: root CA → intermediate CA → leaf (check SAN for hostname)",
                "mTLS: client presents certificate to server — used in service mesh and zero-trust",
            ],
            "troubleshooting": [
                "curl -v https://example.com — verbose TLS handshake + HTTP request/response",
                "openssl s_client -connect host:443 -servername sni.name — cert + chain inspection",
                "curl -w '%{time_connect} %{time_ttfb} %{time_total}\\n' -o /dev/null -s URL",
                "HTTP 502: upstream returned bad response or closed connection",
                "HTTP 504: upstream took too long — check upstream timeout settings",
                "TLS handshake fail: check cipher suite overlap, cert expiry, SNI mismatch",
            ],
        },
        "VPC Design & Peering": {
            "color": BLUE,
            "desc": "Virtual Private Cloud is the foundation of cloud networking. Good design at the start prevents painful re-architecture later.",
            "concepts": [
                "3-tier subnet model: public (internet-facing), private (app), isolated (data/DB)",
                "NAT Gateway / NAT Instance: outbound internet for private subnets (no inbound)",
                "VPC Peering: non-transitive, no overlapping CIDR required, cross-account and cross-region",
                "Transit Gateway: hub-and-spoke for 100s of VPCs — replaces full-mesh peering",
                "VPC Endpoints: Interface (PrivateLink) and Gateway (S3/DynamoDB) — no internet needed",
                "Security Groups (stateful, per-ENI) vs NACLs (stateless, per-subnet, evaluated in order)",
            ],
            "troubleshooting": [
                "VPC Flow Logs: enable on VPC/subnet/ENI — ACCEPT/REJECT records for all traffic",
                "Route table: check target — local, igw-, nat-, pcx-, tgw-, vpce-, vgw-",
                "Security group: stateful — return traffic auto-allowed; NACLs require explicit allow both ways",
                "DNS resolution in VPC: both enableDnsHostnames AND enableDnsSupport must be true",
                "MTU across peering: jumbo frames (9001B) only within VPC — use standard 1500 across peers",
            ],
        },
        "Load Balancing": {
            "color": BLUE,
            "desc": "Distribute traffic across backends for availability and scale. Algorithm and health check design are critical to correctness.",
            "concepts": [
                "Algorithms: Round Robin, Least Connections, Weighted Round Robin, IP Hash, Random",
                "L4 (TCP/UDP): sees IP/port only — no content inspection, very fast, TLS passthrough",
                "L7 (HTTP/HTTPS): can route on URL path, host header, cookies — content-aware",
                "Health checks: HTTP 200 response, TCP connect, custom script — tune interval and threshold",
                "Sticky sessions: cookie-based (insert) or source-IP hash — trade scalability for statefulness",
                "SSL/TLS termination at LB vs TLS passthrough vs re-encryption (end-to-end TLS)",
            ],
            "troubleshooting": [
                "502 Bad Gateway: backend returning invalid HTTP or connection refused",
                "504 Gateway Timeout: backend too slow — increase LB timeout or fix backend",
                "Uneven load: Least Connections better than Round Robin for long-lived connections",
                "Health check false negatives: check interval, threshold, and timeout settings",
                "Draining connections: set deregistration delay to allow in-flight requests to finish",
            ],
        },
        "Firewall & ACLs": {
            "color": BLUE,
            "desc": "Network access control: stateful firewalls (connection tracking) vs stateless ACLs (packet filter). Both have their place.",
            "concepts": [
                "Stateful (iptables/nftables/AWS SG): tracks connection state — return traffic auto-allowed",
                "Stateless (AWS NACL/ACL): evaluates every packet independently — must allow return traffic",
                "iptables chains: PREROUTING → FORWARD → POSTROUTING (routing), INPUT/OUTPUT (local)",
                "nftables: modern replacement for iptables — better performance, atomic rule updates",
                "AWS Security Groups: allow-only rules, per-ENI, stateful — no deny rules",
                "Network ACLs: ordered rule evaluation, lowest number wins, explicit deny possible",
            ],
            "troubleshooting": [
                "iptables -L -n -v — list rules with packet/byte counters",
                "iptables -I INPUT 1 -j LOG --log-prefix 'DROP: ' — log dropped packets",
                "nft list ruleset — nftables equivalent of iptables -L",
                "conntrack -L | grep host — check if connection is tracked",
                "AWS: VPC Flow Logs REJECT records — confirm firewall is the cause",
                "Windows: netsh advfirewall show allprofiles — check firewall state",
            ],
        },
        "BGP & Routing": {
            "color": BLUE,
            "desc": "Border Gateway Protocol is the routing protocol of the internet. Used in cloud Direct Connect, SD-WAN, and large on-premises networks.",
            "concepts": [
                "BGP: path-vector protocol — exchanges prefixes with AS_PATH, MED, LOCAL_PREF attributes",
                "iBGP (within AS) vs eBGP (between AS) — iBGP requires full mesh or route reflectors",
                "BGP attributes: LOCAL_PREF (prefer exit), AS_PATH (prefer shorter), MED (prefer entry)",
                "Route redistribution: inject static/OSPF/EIGRP routes into BGP — be careful with aggregation",
                "BGP communities: tag routes for policy — well-known (NO_EXPORT) and custom",
                "AWS Direct Connect: private VIF uses BGP over dedicated circuit to VPC",
            ],
            "troubleshooting": [
                "show bgp summary — neighbour state: Idle/Active=problem, Established=good",
                "show bgp neighbors x.x.x.x — detailed BGP session state and counters",
                "BGP stuck in Active: TCP reachability issue on port 179 — check firewall",
                "Route not received: check inbound route-map and prefix-list filters",
                "Asymmetric routing: different paths in/out — tune LOCAL_PREF and MED",
            ],
        },
        "Service Mesh (Istio)": {
            "color": PURPLE,
            "desc": "Service mesh adds observability, mTLS security, and traffic management to microservices without changing application code.",
            "concepts": [
                "Sidecar proxy: Envoy injected alongside every pod — intercepts all in/out traffic",
                "Control plane (Istiod): config distribution, certificate authority, telemetry aggregation",
                "mTLS STRICT mode: all pod-to-pod traffic encrypted and mutually authenticated",
                "VirtualService: routing rules — canary split, header-based routing, fault injection",
                "DestinationRule: load balancing policy, circuit breaker, TLS settings per subset",
                "Telemetry: automatic L7 metrics (RED: Rate, Errors, Duration), traces to Jaeger",
            ],
            "troubleshooting": [
                "istioctl analyze — scan cluster for config issues and best-practice violations",
                "istioctl proxy-status — sync state of all Envoy sidecars with control plane",
                "503 UH (no healthy upstream): check DestinationRule subset label selectors",
                "mTLS PERMISSIVE first, then STRICT — migrate gradually to avoid breaking traffic",
                "istioctl proxy-config routes <pod> — inspect Envoy route table in pod",
            ],
        },
    },
    "Database": {
        "PostgreSQL": {
            "color": BLUE,
            "desc": "Most advanced open-source RDBMS. MVCC concurrency, ACID transactions, extensions ecosystem, powerful query planner.",
            "concepts": [
                "MVCC: each transaction sees a snapshot — readers never block writers",
                "VACUUM: reclaims dead tuples from MVCC — autovacuum runs automatically",
                "WAL (Write-Ahead Log): durability, crash recovery, streaming replication, PITR",
                "Query planner: EXPLAIN ANALYZE shows actual rows, loops, time — seq vs index scan",
                "Extensions: pg_stat_statements, pgvector, TimescaleDB, PostGIS, pg_partman",
                "Partitioning: range/list/hash — enables partition pruning and parallel query",
            ],
            "troubleshooting": [
                "SELECT pid,query,state,wait_event FROM pg_stat_activity WHERE state='active'",
                "SELECT * FROM pg_locks l JOIN pg_stat_activity a ON l.pid=a.pid WHERE granted=false",
                "SELECT n_dead_tup,n_live_tup,last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC",
                "SELECT query,calls,total_exec_time/calls AS avg_ms FROM pg_stat_statements ORDER BY avg_ms DESC LIMIT 10",
                "max_connections exhausted: deploy PgBouncer in transaction pooling mode",
                "Replication slot bloat: SELECT * FROM pg_replication_slots WHERE active=false",
            ],
        },
        "MySQL & MariaDB": {
            "color": AMBER,
            "desc": "World's most popular open-source RDBMS. InnoDB storage engine provides ACID compliance, row-level locking, and MVCC.",
            "concepts": [
                "InnoDB: clustered primary key index, buffer pool (target 80% RAM), undo log for MVCC",
                "Binary log (binlog): row/statement/mixed format — replication and PITR",
                "GTID-based replication: globally unique transaction IDs — simplifies failover",
                "Semi-sync replication: at least 1 replica ACK before commit — compromise between sync/async",
                "Query cache: deprecated in 8.0 — use ProxySQL query caching instead",
                "JSON column type: native JSON with generated columns for indexing JSON paths",
            ],
            "troubleshooting": [
                "SHOW PROCESSLIST — active queries, state, time, lock info",
                "SHOW ENGINE INNODB STATUS\\G — latest deadlock, buffer pool stats, transaction list",
                "EXPLAIN ANALYZE SELECT ... — MySQL 8.0+ actual execution plan with timings",
                "SHOW REPLICA STATUS\\G — Seconds_Behind_Source for replication lag",
                "SET GLOBAL slow_query_log=ON; SET GLOBAL long_query_time=1 — enable slow log",
                "pt-query-digest /var/log/mysql/slow.log — analyse slow query log",
            ],
        },
        "Redis": {
            "color": RED,
            "desc": "In-memory data structure store. Sub-millisecond latency. Caching, sessions, pub/sub, rate limiting, leaderboards.",
            "concepts": [
                "Data types: String, Hash, List, Set, Sorted Set, Stream, HyperLogLog, Bitmap",
                "Persistence: RDB snapshot (point-in-time, compact) vs AOF (every write, durable)",
                "Replication: master-replica, Redis Sentinel (auto-failover), Redis Cluster (sharding)",
                "Eviction: volatile-lru, allkeys-lru, allkeys-lfu, noeviction — set per use case",
                "Redis Streams: persistent pub/sub with consumer groups — durable unlike Pub/Sub",
                "Lua scripts: EVAL script 0 arg1 — atomic multi-command without transactions",
            ],
            "troubleshooting": [
                "redis-cli INFO memory — used_memory, mem_fragmentation_ratio (>1.5 = fragmented)",
                "redis-cli SLOWLOG GET 25 — last 25 slow commands (>10ms by default)",
                "redis-cli MONITOR — live command trace (WARNING: impacts performance)",
                "redis-cli DEBUG SLEEP 0 — test connectivity without side effects",
                "TTL mykey → -1=no expiry, -2=key missing — check expiry on cached keys",
                "MEMORY USAGE mykey — bytes used by specific key including overhead",
            ],
        },
        "MongoDB": {
            "color": GREEN,
            "desc": "Document-oriented NoSQL database. Flexible BSON schema, rich aggregation pipeline, horizontal scaling via sharding.",
            "concepts": [
                "Document model: embed for locality, reference for large/shared data — design for queries",
                "Indexes: single, compound, multikey (arrays), text, geospatial, partial, wildcard",
                "Aggregation pipeline: $match → $group → $project → $lookup → $unwind → $sort",
                "Replica set: primary + secondaries, automatic election on primary failure",
                "Sharding: shard key determines data distribution — avoid monotonic keys (hot shard)",
                "Transactions (4.0+): multi-document ACID with snapshot isolation across replica set",
            ],
            "troubleshooting": [
                "db.currentOp({active:true}) — currently running operations with lock info",
                "db.collection.explain('executionStats').find({field:'val'}) — query plan",
                "COLLSCAN in explain → missing index → db.collection.createIndex({field:1})",
                "db.setProfilingLevel(1, {slowms:50}) — enable slow query profiling at 50ms",
                "rs.status() — replica set state, lag, last heartbeat per member",
                "db.serverStatus().opcounters — query/insert/update/delete rates",
            ],
        },
        "Query Optimisation": {
            "color": PURPLE,
            "desc": "Indexes are the single most impactful performance lever. Know when they help, when they hurt, and how the planner chooses.",
            "concepts": [
                "B-Tree index: balanced tree, O(log n) lookup, efficient range scans and ORDER BY",
                "Composite index: column order critical — leftmost prefix rule, equality then range",
                "Index selectivity: high cardinality → small result set → index worth using",
                "Covering index: all query columns in index → index-only scan, zero heap fetches",
                "Partial index: WHERE clause reduces index size — only index frequently queried subset",
                "Function on indexed column: LOWER(col)='x' bypasses index on col — use functional index",
            ],
            "troubleshooting": [
                "EXPLAIN ANALYZE: look for Seq Scan on large table → add index",
                "Index not used: type mismatch (int vs varchar), implicit cast bypasses index",
                "N+1 query: ORM generating 1 query + N queries — use eager loading / JOIN FETCH",
                "ANALYZE table_name — update planner statistics after bulk load",
                "pg_stat_user_indexes: idx_scan=0 → unused index consuming write overhead",
                "auto_explain: log_min_duration=1000 — auto-log slow query plans",
            ],
        },
        "Replication & HA": {
            "color": GREEN,
            "desc": "Database HA strategy is driven by RPO (data loss tolerance) and RTO (downtime tolerance). No single right answer.",
            "concepts": [
                "RPO (Recovery Point Objective): max acceptable data loss — drives sync vs async",
                "RTO (Recovery Time Objective): max acceptable downtime — drives auto vs manual failover",
                "Synchronous replication: 0 data loss, write latency penalty, primary waits for ACK",
                "Asynchronous: low latency, possible data loss on primary crash before replica catches up",
                "Patroni + etcd: PostgreSQL HA with distributed consensus leader election",
                "ProxySQL / PgBouncer: connection pooling + read/write splitting for replicas",
            ],
            "troubleshooting": [
                "Replication lag: monitor pg_stat_replication.replay_lag or Seconds_Behind_Source",
                "Split-brain: two primaries — use STONITH fencing to prevent dual writes",
                "Inactive replication slot holding WAL: drop slot or connect replica quickly",
                "Replica re-sync after long gap: pg_basebackup fresh copy faster than WAL replay",
                "Failover test: simulate primary loss in staging, measure actual RTO vs target",
            ],
        },
        "Backup & Recovery": {
            "color": GREEN,
            "desc": "Backups only have value if recovery works. Test restores regularly. Understand RPO implications of each backup type.",
            "concepts": [
                "Full backup: complete copy — simple restore, large, slow for big databases",
                "Incremental: changes since last backup — fast backup, complex restore (chain)",
                "Differential: changes since last FULL — moderate size, simpler restore than incremental",
                "PITR (Point-in-Time Recovery): replay WAL/binlog to exact point — requires continuous archiving",
                "pg_dump: logical backup (portable), pg_basebackup: physical (faster restore)",
                "3-2-1 rule: 3 copies, 2 different media types, 1 offsite",
            ],
            "troubleshooting": [
                "Restore test: restore to separate instance monthly — validate data integrity",
                "pg_restore version mismatch: use pg_restore from same major version as source",
                "PITR gap: check WAL archive for missing segments before attempting recovery",
                "mysqldump too slow: use Percona XtraBackup (physical, hot backup)",
                "Backup window too long: pg_basebackup --checkpoint=fast --progress",
            ],
        },
        "Performance Tuning": {
            "color": PURPLE,
            "desc": "Database performance is usually the application bottleneck. Systematic tuning from connection pool through query to storage.",
            "concepts": [
                "Buffer/cache hit ratio: >99% target — increase shared_buffers / innodb_buffer_pool_size",
                "Connection pooling: PgBouncer (transaction mode) or ProxySQL — avoid connection storms",
                "work_mem (PostgreSQL): per-sort/hash operation — increase for complex queries",
                "Checkpoint tuning: max_wal_size, checkpoint_completion_target=0.9 — smooth IO",
                "Read replicas: offload reporting and analytics queries from primary",
                "Partitioning + partition pruning: query only relevant partitions on large tables",
            ],
            "troubleshooting": [
                "pg_stat_statements: ORDER BY total_exec_time DESC — top queries by total time",
                "auto_explain.log_min_duration: auto-capture slow query plans in log",
                "temp_files growing: increase work_mem for sort/hash — check log_temp_files",
                "Checkpoint too frequent: increase max_wal_size, checkpoint_completion_target",
                "Connection spike: check max_connections and pgbouncer pool_size settings",
            ],
        },
    },
}

def flatten_kb():
    """Build flat searchable index from all KB data."""
    index = []
    for section, section_data in KB.items():
        if section == "Cloud":
            for provider, pdata in section_data.items():
                for cat, services in pdata.items():
                    if cat == "color":
                        continue
                    for svc in services:
                        index.append({
                            "title": svc,
                            "section": section,
                            "parent": f"{provider} → {cat}",
                            "text": f"{svc} {provider} {cat} cloud service",
                            "type": "cloud_service",
                            "provider": provider,
                            "color": pdata["color"],
                        })
        elif section in ("OS",):
            for os_name, osdata in section_data.items():
                for topic, tdata in osdata["topics"].items():
                    blob = " ".join([
                        topic, os_name, tdata["desc"],
                        " ".join(tdata["concepts"]),
                        " ".join(tdata["troubleshooting"]),
                        " ".join(tdata["tools"]),
                    ]).lower()
                    index.append({
                        "title": topic,
                        "section": section,
                        "parent": os_name,
                        "text": blob,
                        "type": "topic",
                        "data": tdata,
                        "color": osdata["color"],
                    })
        elif section == "DevOps":
            for cat, tools in section_data.items():
                for tool_name, tdata in tools.items():
                    blob = " ".join([
                        tool_name, cat, tdata["desc"],
                        " ".join(tdata["deep_dive"]),
                        " ".join(tdata["troubleshooting"]),
                    ]).lower()
                    index.append({
                        "title": tool_name,
                        "section": section,
                        "parent": cat,
                        "text": blob,
                        "type": "devops_tool",
                        "data": tdata,
                        "color": tdata["color"],
                    })
        elif section in ("Networking", "Database"):
            for topic, tdata in section_data.items():
                blob = " ".join([
                    topic, tdata["desc"],
                    " ".join(tdata["concepts"]),
                    " ".join(tdata["troubleshooting"]),
                ]).lower()
                index.append({
                    "title": topic,
                    "section": section,
                    "parent": section,
                    "text": blob,
                    "type": "topic",
                    "data": tdata,
                    "color": tdata["color"],
                })
    return index


SEARCH_INDEX = flatten_kb()


def local_search(query):
    q = query.lower().strip()
    if not q:
        return []
    terms = q.split()
    scored = []
    for item in SEARCH_INDEX:
        score = 0
        title_lower = item["title"].lower()
        for t in terms:
            if t in title_lower:
                score += 10
            if t in item["text"]:
                score += item["text"].count(t)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:20]]


# ── Main App ──────────────────────────────────────────────────────
class KnowledgeBase(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Knowledge Base")
        self.geometry("1300x820")
        self.minsize(1000, 640)
        self.configure(bg=BG)
        self.agent_history = []
        self._build()
        self._show("search")

    # ─────────────────────────────────────────────────────────────
    def _build(self):
        # Left nav
        nav = tk.Frame(self, bg=PANEL, width=192)
        nav.pack(side=tk.LEFT, fill=tk.Y)
        nav.pack_propagate(False)

        tk.Label(nav, text="Knowledge Base", font=("Segoe UI", 13, "bold"),
                 fg=TEXT1, bg=PANEL, pady=18).pack()
        tk.Frame(nav, height=1, bg=BORDER).pack(fill=tk.X, padx=14)

        self._nav_btns = {}
        items = [
            ("Search", "search"),
            ("OS", "os"),
            ("Cloud", "cloud"),
            ("DevOps", "devops"),
            ("Networking", "networking"),
            ("Database", "database"),
            ("IronHide", "agent"),
        ]
        for label, key in items:
            b = tk.Button(nav, text=label, anchor="w", font=F_BODY,
                          fg=TEXT2, bg=PANEL, bd=0, padx=20, pady=10,
                          activeforeground=TEXT1, activebackground=HOVER,
                          cursor="hand2", command=lambda k=key: self._show(k))
            b.pack(fill=tk.X)
            self._nav_btns[key] = b

        # Main area with scrollable canvas
        self._main = tk.Frame(self, bg=BG)
        self._main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(self._main, bg=BG, highlightthickness=0)
        self._sb = ttk.Scrollbar(self._main, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._sb.set)
        self._sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._inner = tk.Frame(self._canvas, bg=BG)
        self._cw = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")
        self._inner.bind("<Configure>", lambda e: self._canvas.configure(
            scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>", lambda e: self._canvas.itemconfig(self._cw, width=e.width))
        self._canvas.bind_all("<MouseWheel>", lambda e: self._canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))

        # Build all section frames inside inner
        self._sections = {}
        self._build_search()
        self._build_os()
        self._build_cloud()
        self._build_devops()
        self._build_networking()
        self._build_database()
        self._build_agent()

    def _show(self, key):
        for f in self._sections.values():
            f.pack_forget()
        self._sections[key].pack(fill=tk.BOTH, expand=True, padx=22, pady=14)
        for k, b in self._nav_btns.items():
            b.config(fg=ACCENT2 if k == key else TEXT2,
                     bg=HOVER if k == key else PANEL)
        self._canvas.yview_moveto(0)

    # ─── helpers ─────────────────────────────────────────────────
    def _frame(self, name):
        f = tk.Frame(self._inner, bg=BG)
        self._sections[name] = f
        return f

    def _hdr(self, parent, title, sub=""):
        tk.Label(parent, text=title, font=F_TITLE, fg=TEXT1, bg=BG).pack(anchor="w")
        if sub:
            tk.Label(parent, text=sub, font=F_BODY, fg=TEXT3, bg=BG).pack(anchor="w")
        tk.Frame(parent, height=1, bg=BORDER).pack(fill=tk.X, pady=(6, 12))

    def _row_btn(self, parent, text, sub="", color=TEXT2, cmd=None):
        row = tk.Frame(parent, bg=CARD, cursor="hand2")
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=text, font=F_BODY, fg=TEXT1, bg=CARD,
                 padx=14, pady=10, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        if sub:
            tk.Label(row, text=sub, font=F_SMALL, fg=color, bg=CARD, padx=8).pack(side=tk.RIGHT)
        tk.Label(row, text="›", font=("Segoe UI", 13), fg=TEXT3, bg=CARD, padx=10).pack(side=tk.RIGHT)
        if cmd:
            for w in [row] + list(row.winfo_children()):
                w.bind("<Button-1>", lambda e, c=cmd: c())
        return row

    def _open_web(self, query):
        self._show_web_popup(query)

    def _show_web_popup(self, query):
        pop = tk.Toplevel(self)
        pop.title(f"Web search — {query}")
        pop.geometry("700x460")
        pop.configure(bg=BG)
        pop.grab_set()
        tk.Label(pop, text=f'Web search: "{query}"', font=F_HEAD,
                 fg=TEXT1, bg=BG, pady=14, padx=20).pack(anchor="w")
        tk.Label(pop, text="Click a source to open in your browser",
                 font=F_SMALL, fg=TEXT3, bg=BG, padx=20).pack(anchor="w")
        grid = tk.Frame(pop, bg=BG, padx=16, pady=10)
        grid.pack(fill=tk.BOTH, expand=True)
        for i, (name, url) in enumerate(web_urls(query)):
            r, c = divmod(i, 3)
            b = tk.Button(grid, text=name, font=F_SMALL, fg=TEXT1, bg=CARD,
                          bd=0, padx=12, pady=10, cursor="hand2", relief=tk.FLAT,
                          command=lambda u=url: webbrowser.open(u),
                          activeforeground=ACCENT2, activebackground=HOVER,
                          wraplength=150, justify=tk.LEFT)
            b.grid(row=r, column=c, padx=5, pady=4, sticky="ew")
            grid.columnconfigure(c, weight=1)
        tk.Button(pop, text="Close", font=F_SMALL, fg=TEXT2, bg=PANEL,
                  bd=0, padx=20, pady=8, cursor="hand2",
                  command=pop.destroy).pack(pady=10)

    def _detail_win(self, title, parent_label, data, is_devops=False):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("880x680")
        win.configure(bg=BG)

        hdr = tk.Frame(win, bg=CARD, padx=20, pady=14)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text=title, font=F_TITLE, fg=TEXT1, bg=CARD).pack(anchor="w")
        tk.Label(hdr, text=parent_label, font=F_SMALL, fg=TEXT3, bg=CARD).pack(anchor="w")
        if is_devops:
            tk.Label(hdr, text=data.get("desc", ""), font=F_BODY, fg=TEXT2, bg=CARD,
                     wraplength=820, justify=tk.LEFT).pack(anchor="w", pady=(4, 0))
        else:
            tk.Label(hdr, text=data.get("desc", ""), font=F_BODY, fg=TEXT2, bg=CARD,
                     wraplength=820, justify=tk.LEFT).pack(anchor="w", pady=(4, 0))

        cv = tk.Canvas(win, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(win, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        cv.pack(fill=tk.BOTH, expand=True)
        inner = tk.Frame(cv, bg=BG, padx=20, pady=14)
        cw = cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>", lambda e: cv.itemconfig(cw, width=e.width))
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

        key1 = "deep_dive" if is_devops else "concepts"
        lbl1 = "Deep dive topics" if is_devops else "Core concepts"
        self._section_block(inner, lbl1, data.get(key1, []), ACCENT2)
        self._section_block(inner, "Troubleshooting", data.get("troubleshooting", []), GREEN)
        if not is_devops:
            self._section_block(inner, "Key tools", data.get("tools", []), AMBER)

        btn_row = tk.Frame(inner, bg=BG, pady=10)
        btn_row.pack(anchor="w")
        tk.Button(btn_row, text="Web search ↗", font=F_SMALL,
                  fg=ACCENT2, bg=TAG, bd=0, padx=10, pady=6, cursor="hand2",
                  command=lambda: self._open_web(title)).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_row, text="Ask IronHide", font=F_SMALL,
                  fg=TEXT1, bg=ACCENT, bd=0, padx=10, pady=6, cursor="hand2",
                  command=lambda: [win.destroy(), self._show("agent"),
                                   self._prefill(f"Deep dive on {title}")]).pack(side=tk.LEFT)

    def _section_block(self, parent, title, items, color):
        tk.Label(parent, text=title, font=F_HEAD, fg=color, bg=BG).pack(anchor="w", pady=(10, 2))
        for item in items:
            r = tk.Frame(parent, bg=BG)
            r.pack(fill=tk.X, pady=1)
            tk.Label(r, text="•", font=F_BODY, fg=color, bg=BG, width=2).pack(side=tk.LEFT, anchor="n", pady=2)
            tk.Label(r, text=item, font=F_SMALL, fg=TEXT2, bg=BG,
                     wraplength=780, justify=tk.LEFT, anchor="w").pack(side=tk.LEFT, fill=tk.X)

    # ─── Search section ──────────────────────────────────────────
    def _build_search(self):
        f = self._frame("search")
        self._hdr(f, "Search", "Type anything — topic, error, command, tool name")

        bar = tk.Frame(f, bg=INPUT, padx=10, pady=8)
        bar.pack(fill=tk.X, pady=(0, 12))
        tk.Label(bar, text="🔍", font=("Segoe UI", 13), bg=INPUT, fg=TEXT2).pack(side=tk.LEFT)
        self._sv = tk.StringVar()
        ent = tk.Entry(bar, textvariable=self._sv, font=F_BODY, bg=INPUT, fg=TEXT1,
                       insertbackground=TEXT1, bd=0, relief=tk.FLAT)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ent.bind("<KeyRelease>", self._do_search)
        ent.bind("<Return>", self._do_search)
        tk.Button(bar, text="Web search ↗", font=F_SMALL, fg=ACCENT2, bg=INPUT,
                  bd=0, cursor="hand2",
                  command=lambda: self._open_web(self._sv.get())).pack(side=tk.RIGHT)
        ent.focus_set()

        self._search_results = tk.Frame(f, bg=BG)
        self._search_results.pack(fill=tk.BOTH, expand=True)
        self._search_hint()

    def _search_hint(self):
        for w in self._search_results.winfo_children():
            w.destroy()
        hints = [
            "nginx 502 bad gateway", "AD replication error", "Kubernetes CrashLoopBackOff",
            "PostgreSQL slow query", "terraform state lock", "Docker OOM killed",
            "Linux high iowait", "Azure pipeline 403", "Redis maxmemory eviction",
            "DNS SRV record missing",
        ]
        tk.Label(self._search_results, text="Try searching for:", font=F_SMALL,
                 fg=TEXT3, bg=BG, pady=8).pack(anchor="w")
        wrap = tk.Frame(self._search_results, bg=BG)
        wrap.pack(anchor="w")
        for h in hints:
            b = tk.Button(wrap, text=h, font=F_SMALL, fg=ACCENT2, bg=TAG,
                          bd=0, padx=8, pady=5, cursor="hand2",
                          command=lambda t=h: [self._sv.set(t), self._do_search()])
            b.pack(side=tk.LEFT, padx=3, pady=3)

    def _do_search(self, event=None):
        q = self._sv.get().strip()
        for w in self._search_results.winfo_children():
            w.destroy()
        if not q:
            self._search_hint()
            return
        results = local_search(q)
        if results:
            tk.Label(self._search_results,
                     text=f"{len(results)} result{'s' if len(results)!=1 else ''} in knowledge base",
                     font=F_SMALL, fg=TEXT3, bg=BG, pady=4).pack(anchor="w")
            for item in results:
                self._search_result_row(item, q)
        else:
            tk.Label(self._search_results,
                     text="No matches in knowledge base — try web search:",
                     font=F_SMALL, fg=TEXT3, bg=BG, pady=8).pack(anchor="w")

        # Always show web fallback buttons at the bottom
        sep = tk.Frame(self._search_results, height=1, bg=BORDER)
        sep.pack(fill=tk.X, pady=10)
        tk.Label(self._search_results, text="Also search the web:", font=F_SMALL,
                 fg=TEXT3, bg=BG).pack(anchor="w")
        row = tk.Frame(self._search_results, bg=BG)
        row.pack(anchor="w", pady=4)
        for name, url in web_urls(q)[:6]:
            tk.Button(row, text=name, font=F_SMALL, fg=ACCENT2, bg=TAG,
                      bd=0, padx=8, pady=5, cursor="hand2",
                      command=lambda u=url: webbrowser.open(u)).pack(side=tk.LEFT, padx=3, pady=2)

    def _search_result_row(self, item, query):
        row = tk.Frame(self._search_results, bg=CARD, cursor="hand2")
        row.pack(fill=tk.X, pady=2)
        color = item.get("color", TEXT2)

        tk.Label(row, text=item["title"], font=F_BODY, fg=TEXT1, bg=CARD,
                 padx=14, pady=8, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(row, text=item["parent"], font=F_SMALL, fg=TEXT3, bg=CARD,
                 padx=6).pack(side=tk.RIGHT)
        tk.Label(row, text=item["section"], font=F_SMALL, fg=color, bg=CARD,
                 padx=10).pack(side=tk.RIGHT)

        def on_click(it=item):
            if it["type"] == "topic":
                self._detail_win(it["title"], it["parent"], it["data"])
            elif it["type"] == "devops_tool":
                self._detail_win(it["title"], it["parent"], it["data"], is_devops=True)
            elif it["type"] == "cloud_service":
                self._open_web(f'{it["provider"]} {it["title"]} documentation')

        for w in [row] + list(row.winfo_children()):
            w.bind("<Button-1>", lambda e, fn=on_click: fn())

    # ─── OS section ──────────────────────────────────────────────
    def _build_os(self):
        f = self._frame("os")
        self._hdr(f, "Operating Systems", "Windows Server and Linux — deep dives and troubleshooting")
        for os_name, osdata in KB["OS"].items():
            blk = tk.Frame(f, bg=BG, pady=4)
            blk.pack(fill=tk.X)
            hdr = tk.Frame(blk, bg=osdata["color"], padx=14, pady=8)
            hdr.pack(fill=tk.X)
            tk.Label(hdr, text=os_name, font=F_HEAD, fg="white", bg=osdata["color"]).pack(side=tk.LEFT)
            level_colors = {"Beginner": GREEN, "Intermediate": AMBER, "Advanced": RED}
            for topic, tdata in osdata["topics"].items():
                lc = level_colors.get(tdata["level"], TEXT2)
                self._row_btn(blk, topic, tdata["level"], color=lc,
                              cmd=lambda t=topic, d=tdata, o=os_name:
                              self._detail_win(t, o, d))

    # ─── Cloud section ───────────────────────────────────────────
    def _build_cloud(self):
        f = self._frame("cloud")
        self._hdr(f, "Cloud", "AWS, Azure, and Google Cloud service browser")

        self._cloud_btns = {}
        bar = tk.Frame(f, bg=BG)
        bar.pack(anchor="w", pady=(0, 12))
        self._cloud_content = tk.Frame(f, bg=BG)
        self._cloud_content.pack(fill=tk.X)

        for pname in KB["Cloud"]:
            color = KB["Cloud"][pname]["color"]
            b = tk.Button(bar, text=pname, font=F_BODY, fg=TEXT2, bg=CARD,
                          bd=0, padx=16, pady=8, cursor="hand2",
                          command=lambda p=pname: self._load_cloud(p))
            b.pack(side=tk.LEFT, padx=4)
            self._cloud_btns[pname] = (b, color)
        self._load_cloud("AWS")

    def _load_cloud(self, provider):
        for w in self._cloud_content.winfo_children():
            w.destroy()
        for p, (b, c) in self._cloud_btns.items():
            b.config(fg="white" if p == provider else TEXT2,
                     bg=c if p == provider else CARD)
        data = KB["Cloud"][provider]
        for cat, services in data.items():
            if cat == "color":
                continue
            tk.Label(self._cloud_content, text=cat.upper(), font=("Segoe UI", 10, "bold"),
                     fg=TEXT3, bg=BG).pack(anchor="w", pady=(8, 2))
            grid = tk.Frame(self._cloud_content, bg=BG)
            grid.pack(fill=tk.X)
            for i, svc in enumerate(services):
                r, c = divmod(i, 4)
                card = tk.Frame(grid, bg=CARD, padx=12, pady=10, cursor="hand2")
                card.grid(row=r, column=c, padx=4, pady=3, sticky="ew")
                grid.columnconfigure(c, weight=1)
                tk.Label(card, text=svc, font=F_SMALL, fg=TEXT1, bg=CARD,
                         anchor="w", wraplength=170).pack(anchor="w")
                for w in [card] + list(card.winfo_children()):
                    w.bind("<Button-1>", lambda e, s=svc, p=provider:
                           self._open_web(f"{p} {s}"))

    # ─── DevOps section ──────────────────────────────────────────
    def _build_devops(self):
        f = self._frame("devops")
        self._hdr(f, "DevOps", "CI/CD, IaC, Containers, and Monitoring")

        self._devops_cat_btns = {}
        bar = tk.Frame(f, bg=BG)
        bar.pack(anchor="w", pady=(0, 12))
        self._devops_content = tk.Frame(f, bg=BG)
        self._devops_content.pack(fill=tk.X)

        for cat in KB["DevOps"]:
            b = tk.Button(bar, text=cat, font=F_BODY, fg=TEXT2, bg=CARD,
                          bd=0, padx=16, pady=8, cursor="hand2",
                          command=lambda c=cat: self._load_devops(c))
            b.pack(side=tk.LEFT, padx=4)
            self._devops_cat_btns[cat] = b
        self._load_devops("CI/CD")

    def _load_devops(self, cat):
        for w in self._devops_content.winfo_children():
            w.destroy()
        for c, b in self._devops_cat_btns.items():
            b.config(fg=TEXT1 if c == cat else TEXT2,
                     bg=ACCENT if c == cat else CARD)
        for tool_name, tdata in KB["DevOps"][cat].items():
            card = tk.Frame(self._devops_content, bg=CARD, pady=0)
            card.pack(fill=tk.X, pady=4)
            top = tk.Frame(card, bg=CARD, padx=14, pady=10)
            top.pack(fill=tk.X)
            tk.Label(top, text=tool_name, font=F_HEAD, fg=TEXT1, bg=CARD).pack(side=tk.LEFT)
            tk.Label(top, text=tdata["type"], font=F_SMALL, fg=tdata["color"],
                     bg=CARD, padx=8).pack(side=tk.LEFT)
            tk.Label(top, text=tdata["desc"][:80]+"...", font=F_SMALL, fg=TEXT2,
                     bg=CARD, wraplength=480, anchor="w").pack(side=tk.LEFT, padx=10)
            btn_row = tk.Frame(card, bg=CARD, padx=14, pady=6)
            btn_row.pack(fill=tk.X)
            tk.Button(btn_row, text="Deep dive", font=F_SMALL, fg=ACCENT2, bg=TAG,
                      bd=0, padx=10, pady=5, cursor="hand2",
                      command=lambda t=tool_name, d=tdata:
                      self._detail_win(t, d["type"], d, is_devops=True)).pack(side=tk.LEFT, padx=(0, 6))
            tk.Button(btn_row, text="Web search ↗", font=F_SMALL, fg=TEXT2, bg=PANEL,
                      bd=0, padx=10, pady=5, cursor="hand2",
                      command=lambda t=tool_name: self._open_web(t)).pack(side=tk.LEFT, padx=(0, 6))
            tk.Button(btn_row, text="Ask IronHide", font=F_SMALL, fg=TEXT2, bg=PANEL,
                      bd=0, padx=10, pady=5, cursor="hand2",
                      command=lambda t=tool_name: [self._show("agent"),
                                                    self._prefill(f"Complete guide for {t}")]).pack(side=tk.LEFT)

    # ─── Networking section ──────────────────────────────────────
    def _build_networking(self):
        f = self._frame("networking")
        self._hdr(f, "Networking", "Protocols, architectures, and troubleshooting")
        for topic, tdata in KB["Networking"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata:
                          self._detail_win(t, "Networking", d))

    # ─── Database section ────────────────────────────────────────
    def _build_database(self):
        f = self._frame("database")
        self._hdr(f, "Database", "SQL, NoSQL, performance, HA, and backup")
        for topic, tdata in KB["Database"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata:
                          self._detail_win(t, "Database", d))

    # ─── AI Agent section ────────────────────────────────────────
    def _build_agent(self):
        f = self._frame("agent")
        self._hdr(f, "IronHide", "Your personal assistant for errors, concepts, code, and troubleshooting steps")

        chips_lbl = tk.Label(f, text="Quick prompts:", font=F_SMALL, fg=TEXT3, bg=BG)
        chips_lbl.pack(anchor="w", pady=(0, 4))
        chips = tk.Frame(f, bg=BG)
        chips.pack(anchor="w", pady=(0, 10))
        quick = [
            "Troubleshoot: nginx 502 on Kubernetes",
            "PostgreSQL high CPU root cause",
            "Terraform remote state setup Azure",
            "Linux server OOM killer investigation",
            "Docker container keeps restarting",
            "AD replication failure diagnosis",
        ]
        for q in quick:
            tk.Button(chips, text=q, font=F_SMALL, fg=ACCENT2, bg=TAG,
                      bd=0, padx=8, pady=5, cursor="hand2",
                      command=lambda t=q: self._prefill(t)).pack(side=tk.LEFT, padx=3)

        chat_outer = tk.Frame(f, bg=CARD)
        chat_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self._chat = scrolledtext.ScrolledText(
            chat_outer, font=F_MONO, bg=PANEL, fg=TEXT1, bd=0,
            padx=14, pady=10, wrap=tk.WORD, state=tk.DISABLED, height=22,
            insertbackground=TEXT1, selectbackground=ACCENT, selectforeground="white"
        )
        self._chat.pack(fill=tk.BOTH, expand=True)
        self._chat.tag_config("user",    foreground=ACCENT2, font=("Segoe UI", 11, "bold"))
        self._chat.tag_config("ai",      foreground=TEXT1,   font=F_MONO)
        self._chat.tag_config("system",  foreground=TEXT3,   font=F_SMALL)
        self._chat.tag_config("err",     foreground=RED,     font=F_SMALL)
        self._append("system", "IronHide is online and ready. Type a question or pick a quick prompt above.\n\n")

        input_row = tk.Frame(f, bg=CARD, padx=10, pady=8)
        input_row.pack(fill=tk.X)
        self._agent_input = tk.Text(input_row, font=F_BODY, bg=INPUT, fg=TEXT1,
                                    insertbackground=TEXT1, bd=0, height=3, wrap=tk.WORD, padx=8, pady=6)
        self._agent_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._agent_input.bind("<Return>", self._agent_enter)

        side = tk.Frame(input_row, bg=CARD)
        side.pack(side=tk.RIGHT, padx=(8, 0))
        self._send_btn = tk.Button(side, text="Send\n↵ Enter", font=F_SMALL,
                                   fg="white", bg=ACCENT, bd=0, padx=14, pady=8,
                                   cursor="hand2", command=self._agent_send)
        self._send_btn.pack(fill=tk.X, pady=(0, 4))
        tk.Button(side, text="Web search", font=F_SMALL, fg=ACCENT2, bg=TAG,
                  bd=0, padx=12, pady=6, cursor="hand2",
                  command=lambda: self._open_web(self._agent_input.get("1.0", tk.END).strip())).pack(fill=tk.X, pady=(0, 4))
        tk.Button(side, text="Clear", font=F_SMALL, fg=TEXT2, bg=PANEL,
                  bd=0, padx=12, pady=6, cursor="hand2",
                  command=self._agent_clear).pack(fill=tk.X)

    def _append(self, role, text):
        self._chat.config(state=tk.NORMAL)
        if role == "user":
            self._chat.insert(tk.END, "\nYou:  ", "user")
            self._chat.insert(tk.END, text + "\n", "ai")
        elif role == "ai":
            self._chat.insert(tk.END, "\nIronHide:\n", "user")
            self._chat.insert(tk.END, text + "\n\n", "ai")
        elif role == "err":
            self._chat.insert(tk.END, f"\n⚠  {text}\n\n", "err")
        else:
            self._chat.insert(tk.END, text, "system")
        self._chat.config(state=tk.DISABLED)
        self._chat.see(tk.END)

    def _agent_clear(self):
        self._chat.config(state=tk.NORMAL)
        self._chat.delete("1.0", tk.END)
        self._chat.config(state=tk.DISABLED)
        self.agent_history = []
        self._append("system", "Chat cleared.\n\n")

    def _agent_enter(self, event):
        if event.state == 0:
            self._agent_send()
            return "break"

    def _prefill(self, text):
        self._agent_input.delete("1.0", tk.END)
        self._agent_input.insert("1.0", text)
        self._agent_input.focus_set()

    def _agent_send(self):
        q = self._agent_input.get("1.0", tk.END).strip()
        if not q:
            return
        self._agent_input.delete("1.0", tk.END)
        self._append("user", q)
        self._send_btn.config(state=tk.DISABLED, text="Thinking...")
        self.agent_history.append({"role": "user", "content": q})
        threading.Thread(target=self._run_agent, daemon=True).start()

    def _run_agent(self):
        try:
            cmd = ["claude", "--print", "--no-markdown"]
            # Build conversation as a single prompt with history
            history_text = ""
            for msg in self.agent_history[:-1]:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_text += f"{role}: {msg['content']}\n\n"
            last_q = self.agent_history[-1]["content"]

            system = (
                "You are a Senior DevOps/Cloud/Systems Engineer. "
                "Answer concisely with practical commands, real examples, and root-cause analysis. "
                "For errors: diagnostic commands first, then fix. "
                "Use plain text, no markdown formatting."
            )
            full_prompt = f"{system}\n\n{history_text}User: {last_q}\n\nAssistant:"

            result = subprocess.run(
                cmd, input=full_prompt, capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0 and result.stdout.strip():
                answer = result.stdout.strip()
                self.agent_history.append({"role": "assistant", "content": answer})
                self.after(0, lambda: self._append("ai", answer))
            else:
                err = result.stderr.strip() or "claude CLI returned no output."
                self.after(0, lambda: self._append("err",
                    f"claude CLI error: {err}\n"
                    "Make sure Claude Code is installed: https://claude.ai/download"))
        except FileNotFoundError:
            self.after(0, lambda: self._append("err",
                "claude CLI not found.\n"
                "Install Claude Code from https://claude.ai/download\n"
                "The rest of the Knowledge Base works fully offline without it."))
        except subprocess.TimeoutExpired:
            self.after(0, lambda: self._append("err", "Request timed out after 60 seconds."))
        except Exception as ex:
            self.after(0, lambda: self._append("err", f"{type(ex).__name__}: {ex}"))
        finally:
            self.after(0, lambda: self._send_btn.config(state=tk.NORMAL, text="Send\n↵ Enter"))


if __name__ == "__main__":
    try:
        app = KnowledgeBase()
        app.mainloop()
    except Exception as e:
        import traceback
        with open("kb_error.log", "w") as f:
            traceback.print_exc(file=f)
        raise