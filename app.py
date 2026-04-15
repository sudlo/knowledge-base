import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
import webbrowser
import urllib.parse
import urllib.request
import sys
import os
import json

# -- Palette (VS Code / Tailwind Pro Dark Theme) ------------------
BG       = "#0f172a" 
PANEL    = "#1e293b" 
CARD     = "#1e293b" 
INPUT    = "#020617" 
BORDER   = "#334155" 
HOVER    = "#334155" 
ACCENT   = "#3b82f6" 
ACCENT2  = "#8b5cf6" 
GREEN    = "#10b981" 
AMBER    = "#f59e0b" 
RED      = "#ef4444" 
BLUE     = "#3b82f6" 
PURPLE   = "#8b5cf6" 
TEXT1    = "#f8fafc" 
TEXT2    = "#cbd5e1" 
TEXT3    = "#94a3b8" 
TAG      = "#334155" 

F_TITLE  = ("Segoe UI", 20, "bold")
F_HEAD   = ("Segoe UI", 12, "bold")
F_BODY   = ("Segoe UI", 11)
F_SMALL  = ("Segoe UI", 10)
F_MONO   = ("Consolas", 10)

# -- Web search sources -----------------------------
def web_urls(query):
    q = urllib.parse.quote_plus(query)
    return [
        ("Google",              f"https://www.google.com/search?q={q}"),
        ("Stack Overflow",      f"https://stackoverflow.com/search?q={q}"),
        ("GitHub",              f"https://github.com/search?q={q}&type=repositories"),
        ("Microsoft Docs",      f"https://learn.microsoft.com/en-us/search/?terms={q}"),
        ("AWS Docs",            f"https://docs.aws.amazon.com/search/doc-search.html#searchQuery={q}"),
        ("Kubernetes Docs",     f"https://kubernetes.io/docs/search/?q={q}"),
        ("Docker Docs",         f"https://docs.docker.com/search/?q={q}"),
    ]

# -- FULL KNOWLEDGE BASE DATA --------------------------------------------
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
                        "LDAP port 389/636 - Kerberos auth flow: AS-REQ -> TGT -> TGS -> service ticket",
                        "AD Replication: KCC builds topology, DFS-R syncs SYSVOL/NETLOGON",
                    ],
                    "troubleshooting": [
                        "dcdiag /test:all - comprehensive DC health check",
                        "repadmin /showrepl - replication status per partner",
                        "Event 4769 Kerberos failures - check clock skew (must be <5 min)",
                    ],
                    "tools": ["ADUC", "AD Sites & Services", "ADSI Edit", "repadmin", "dcdiag"],
                },
                "DNS & DHCP": {
                    "level": "Beginner", "color": BLUE,
                    "desc": "Name resolution and IP address management underpin every network service. Misconfigurations here cascade across all systems.",
                    "concepts": [
                        "Zone types: Primary (AD-integrated), Secondary, Stub, Forward/Reverse Lookup",
                        "Record types: A, AAAA, CNAME, MX, PTR, SRV, NS, TXT, SOA",
                        "DHCP failover: Hot Standby (active/passive) vs Load Balance (50/50)",
                    ],
                    "troubleshooting": [
                        "nslookup hostname - basic forward lookup test",
                        "ipconfig /flushdns - clear local resolver cache",
                        "ipconfig /registerdns - force re-register client DNS records",
                    ],
                    "tools": ["DNS Manager", "DHCP Console", "nslookup", "Resolve-DnsName"],
                },
                "Performance Analysis": {
                    "level": "Advanced", "color": BLUE,
                    "desc": "Identify CPU, memory, disk, and network bottlenecks before they become outages. Know which counters matter.",
                    "concepts": [
                        "CPU: %Processor Time >85% sustained = bottleneck; Processor Queue Length >2x cores",
                        "Memory: Available MBytes <100MB = critical; Pages/sec >20 = memory pressure",
                        "Disk: Avg Disk Queue Length >2 per spindle; %Disk Time >90% = saturated",
                    ],
                    "troubleshooting": [
                        "Get-Process | Sort-Object CPU -Desc | Select -First 10 - top CPU consumers",
                        "Resource Monitor -> Disk tab -> Highest Active Time - find IO bottleneck",
                    ],
                    "tools": ["Task Manager", "Resource Monitor", "PerfMon", "Process Explorer"],
                }
            }
        },
        "Linux": {
            "color": AMBER,
            "topics": {
                "Process & Service Management": {
                    "level": "Intermediate", "color": AMBER,
                    "desc": "Linux process lifecycle, systemd service management, and cgroup resource control.",
                    "concepts": [
                        "Process states: R(running) S(sleeping) D(uninterruptible-IO) Z(zombie)",
                        "Signals: SIGTERM(15) graceful stop, SIGKILL(9) force kill",
                        "systemd unit types: .service .socket .timer .target .mount .path",
                        "cgroups v2: unified hierarchy - CPU weight, memory.max, io.max per unit",
                    ],
                    "troubleshooting": [
                        "ps aux --sort=-%cpu | head -15 - top CPU consumers",
                        "systemctl status nginx.service - state + last 10 journal lines",
                        "Zombie: kill parent process (kill -9 $(ps -o ppid= -p <zombie_pid>))",
                    ],
                    "tools": ["htop", "systemctl", "journalctl", "strace", "lsof"],
                },
                "Networking Commands": {
                    "level": "Intermediate", "color": AMBER,
                    "desc": "Linux networking stack diagnostics using modern iproute2 tools. ifconfig and netstat are deprecated.",
                    "concepts": [
                        "ip addr show - interface addresses (replaces ifconfig)",
                        "ss -tulnp - listening ports with process names (replaces netstat)",
                        "iptables / nftables - kernel netfilter packet filtering chains",
                    ],
                    "troubleshooting": [
                        "ip -s link show eth0 - TX/RX packets, errors, and drops",
                        "tcpdump -i eth0 'port 80' -w /tmp/cap.pcap - capture to file",
                    ],
                    "tools": ["ip / iproute2", "ss", "tcpdump", "nmap", "mtr"],
                },
                "Kernel Tuning & eBPF": {
                    "level": "Advanced", "color": AMBER,
                    "desc": "Linux kernel parameters and dynamic tracing for high-performance servers.",
                    "concepts": [
                        "sysctl -a - list all parameters; /proc/sys/ is the virtual filesystem",
                        "vm.swappiness=10 - prefer RAM over swap (0=never swap, 60=default)",
                        "net.core.somaxconn=65535 - max listen() backlog",
                        "eBPF: run sandboxed programs in kernel space without changing kernel source",
                    ],
                    "troubleshooting": [
                        "TCP port exhaustion: ss -s | grep TIME-WAIT; set tcp_tw_reuse=1",
                        "OOM kills: dmesg | grep -i 'oom\\|killed' - find victim processes",
                    ],
                    "tools": ["sysctl", "bpftrace", "BCC tools", "dmesg"],
                }
            }
        },
        "Virtualization": {
            "color": PURPLE,
            "topics": {
                "VMware vSphere & ESXi": {
                    "level": "Advanced", "color": PURPLE,
                    "desc": "Industry standard bare-metal hypervisor and cluster management.",
                    "concepts": [
                        "ESXi: Type-1 hypervisor. vCenter: Centralized management plane.",
                        "vMotion: Live migration of running VMs (requires shared storage, same CPU family)",
                        "DRS (Distributed Resource Scheduler): Auto-balances CPU/RAM across cluster",
                        "HA (High Availability): Auto-restarts VMs on healthy hosts if a host fails",
                        "Datastores: VMFS, NFS, vSAN. VMDKs are the virtual disk files.",
                    ],
                    "troubleshooting": [
                        "VM Snapshot consolidation fails: Check datastore free space (needs working room)",
                        "vMotion fails at 14%: Usually a vMotion network/vmkernel ping issue between hosts",
                        "PSOD (Purple Screen of Death): Hardware failure, bad driver, or firmware bug",
                    ],
                    "tools": ["vCenter", "esxcli", "PowerCLI", "vRealize Operations"],
                }
            }
        }
    },
    "Architecture": {
        "HA & Disaster Recovery": {
            "color": PURPLE,
            "desc": "Designing systems to withstand regional outages, hardware failures, and data corruption.",
            "concepts": [
                "RPO (Recovery Point Objective): Maximum acceptable data loss (measured in time).",
                "RTO (Recovery Time Objective): Maximum acceptable downtime.",
                "Active-Active: Both regions serve traffic. Hard to sync data (split-brain risk).",
                "Active-Passive (Pilot Light): Minimal footprint in DR region, scale up on failover.",
                "Availability Zones: Physically separate data centers within a region for HA.",
            ],
            "troubleshooting": [
                "Split-brain: Prevent with STONITH (Shoot The Other Node In The Head) or quorum/witness.",
                "Failover testing: Run GameDays/Chaos Engineering to prove RTO/RPO limits are met.",
            ],
        },
        "Microservices & Event-Driven": {
            "color": PURPLE,
            "desc": "Decoupling monolithic architectures to enable independent scaling and deployment.",
            "concepts": [
                "API Gateway: Central entry point (Rate limiting, auth, routing).",
                "Event-Driven: Services communicate via events (Kafka, SQS/SNS) rather than direct REST.",
                "Saga Pattern: Managing distributed transactions across microservices without 2PC.",
                "CQRS: Command Query Responsibility Segregation (separate read DB from write DB).",
                "Strangler Fig: Gradually migrate a monolith by replacing features with microservices.",
            ],
            "troubleshooting": [
                "Cascading failures: Implement Circuit Breakers (prevent calling failing downstream services).",
                "Traceability: Use Distributed Tracing (OpenTelemetry) to track requests across boundaries.",
            ],
        },
        "Well-Architected Framework": {
            "color": PURPLE,
            "desc": "The 5 (or 6) pillars of cloud architecture championed by AWS, Azure, and GCP.",
            "concepts": [
                "Operational Excellence: IaC, CI/CD, Observability, Runbooks.",
                "Security: IAM, Data encryption (at rest/transit), Least Privilege.",
                "Reliability: HA, DR, Auto-scaling, Multi-AZ design.",
                "Performance Efficiency: Right-sizing, caching, serverless, edge delivery.",
                "Cost Optimization: Spot instances, Reserved Instances, Lifecycle policies.",
            ],
            "troubleshooting": [
                "Review cycle: Conduct architecture reviews BEFORE deploying to production.",
            ],
        },
        "Caching Strategies": {
            "color": PURPLE,
            "desc": "Offloading databases and reducing latency by storing frequent data in memory or at the edge.",
            "concepts": [
                "Cache-Aside (Lazy Loading): App checks cache -> if miss, queries DB -> updates cache.",
                "Write-Through: App writes to cache AND DB simultaneously (adds write latency).",
                "TTL (Time to Live): Expiring stale data to prevent serving outdated content.",
                "CDN Caching: Storing static assets (images, JS) at edge PoPs globally.",
            ],
            "troubleshooting": [
                "Cache Stampede (Thundering Herd): Thousands of requests miss cache simultaneously, crushing DB. Fix with jitter or lock.",
                "Eviction policies: LRU (Least Recently Used) is standard for Redis/Memcached.",
            ],
        },
    },
    "Security": {
        "Identity & Access Management (IAM)": {
            "color": RED,
            "desc": "The new perimeter. Managing digital identities, authentication, and authorization.",
            "concepts": [
                "OAuth 2.0: Delegation protocol (gives app A access to app B on your behalf).",
                "OIDC (OpenID Connect): Authentication layer on top of OAuth 2.0 (Identity token).",
                "SAML 2.0: XML-based enterprise SSO standard between Identity Provider (IdP) and Service Provider (SP).",
                "RBAC vs ABAC: Role-Based (You are an admin) vs Attribute-Based (You are an admin AND it is 9 AM).",
                "Zero Trust: Never trust, always verify. No implicit trust for being on the internal network.",
            ],
            "troubleshooting": [
                "SAML failures: Check clock skew between IdP and SP, verify certificate signing.",
                "JWT (JSON Web Token) inspection: Decode at jwt.io to check 'exp' (expiry) and 'sub' (subject) claims.",
            ],
        },
        "Cryptography & PKI": {
            "color": RED,
            "desc": "Protecting data in transit, at rest, and in use.",
            "concepts": [
                "Symmetric (AES-256): Same key encrypts and decrypts (Fast, for bulk data).",
                "Asymmetric (RSA/ECC): Public key encrypts, Private key decrypts (Slow, used for key exchange/TLS).",
                "Hashing (SHA-256): One-way mathematical function. Used for passwords (with salt) and file integrity.",
                "PKI (Public Key Infrastructure): Certificate Authorities (CA), Intermediate CAs, CSRs.",
                "mTLS (Mutual TLS): Both client and server present certificates (Standard in Service Meshes).",
            ],
            "troubleshooting": [
                "TLS Handshake fail: Cipher suite mismatch, expired cert, or missing intermediate cert.",
                "openssl s_client -connect host:443 -showcerts - verify the full certificate chain.",
            ],
        },
        "AppSec & Network Security": {
            "color": RED,
            "desc": "Securing the application layer and network perimeters against exploitation.",
            "concepts": [
                "OWASP Top 10: Injection (SQLi), Broken Auth, XSS, SSRF, Misconfiguration.",
                "SAST vs DAST: Static Analysis (scanning code) vs Dynamic Analysis (attacking running app).",
                "WAF (Web Application Firewall): L7 inspection blocking SQLi/XSS based on regex/rules.",
                "Microsegmentation: East-West firewalling inside the network to prevent lateral movement.",
            ],
            "troubleshooting": [
                "False positives on WAF: Check matched rule ID and create highly specific exclusion.",
                "SQL Injection test: Input a single quote (') into fields to check for unhandled SQL errors.",
            ],
        },
        "SIEM & CSPM": {
            "color": RED,
            "desc": "Monitoring, logging, and enforcing compliance across infrastructure.",
            "concepts": [
                "SIEM (Security Information & Event Management): Aggregates logs (Splunk, Sentinel) to detect threats.",
                "SOAR: Automating the response to SIEM alerts (e.g., auto-blocking IP).",
                "CSPM (Cloud Security Posture Management): Scans cloud environments for misconfigurations (e.g., public S3 buckets).",
                "MITRE ATT&CK: Framework detailing adversary tactics and techniques.",
            ],
            "troubleshooting": [
                "Log ingestion delay: Check forwarding agents (Filebeat, UF) and parsing queues.",
                "Alert fatigue: Tune SIEM correlation rules to require multiple IoCs (Indicators of Compromise) before firing.",
            ],
        },
    },
    "Cloud": {
        "AWS": {
            "color": AMBER,
            "Compute":    ["EC2", "Lambda", "ECS", "EKS", "Fargate", "Batch", "Elastic Beanstalk", "Lightsail", "Outposts", "AppRunner", "Serverless App Repo", "VMware Cloud on AWS", "Wavelength", "Local Zones", "Snowball Edge Compute"],
            "Storage":    ["S3", "EBS", "EFS", "FSx (Windows, Lustre, NetApp, OpenZFS)", "S3 Glacier", "Storage Gateway", "AWS Backup", "Snow Family", "Elastic Disaster Recovery", "DataSync", "Transfer Family"],
            "Networking": ["VPC", "Route 53", "CloudFront", "ALB/NLB/GLB", "Direct Connect", "Transit Gateway", "PrivateLink", "Global Accelerator", "API Gateway", "App Mesh", "Cloud Map", "Client VPN", "Site-to-Site VPN", "VPC Lattice"],
            "Database":   ["RDS", "Aurora", "DynamoDB", "ElastiCache", "Redshift", "DocumentDB", "Neptune", "Keyspaces", "Timestream", "MemoryDB for Redis", "QLDB"],
            "DevOps":     ["CodePipeline", "CodeBuild", "CodeDeploy", "CodeCommit", "CloudFormation", "CDK", "Systems Manager", "ECR", "CodeCatalyst", "CodeStar", "Fault Injection Simulator", "Proton"],
            "Security":   ["IAM", "KMS", "Secrets Manager", "GuardDuty", "Security Hub", "WAF", "Shield", "Macie", "Inspector", "Cognito", "Certificate Manager", "Directory Service", "Network Firewall", "Detective", "Artifact"],
            "Monitoring": ["CloudWatch", "X-Ray", "CloudTrail", "AWS Config", "Trusted Advisor", "Cost Explorer", "AWS Health", "Control Tower", "Compute Optimizer", "Managed Grafana", "Managed Prometheus", "Security Lake"],
            "AI / ML":    ["SageMaker", "Bedrock", "Rekognition", "Polly", "Comprehend", "Translate", "Lex", "Kendra", "Forecast", "Personalize", "Textract", "Transcribe", "DeepRacer"],
            "Analytics":  ["Athena", "EMR", "Kinesis", "Glue", "QuickSight", "Data Pipeline", "Lake Formation", "MSK", "OpenSearch Service"]
        },
        "Azure": {
            "color": BLUE,
            "Compute":    ["Virtual Machines", "Azure Functions", "AKS (Kubernetes)", "Container Apps", "App Service", "Azure Batch", "Service Fabric", "Spring Apps", "VM Scale Sets", "Azure Dedicated Host", "Azure Spot VMs", "CycleCloud", "AVD"],
            "Storage":    ["Blob Storage", "Azure Disk", "Azure Files", "NetApp Files", "Data Lake Storage Gen2", "Archive Storage", "Azure Backup", "Import/Export", "Data Box", "StorSimple", "Azure Site Recovery"],
            "Networking": ["Virtual Network (VNet)", "Azure DNS", "Azure CDN", "Load Balancer", "Application Gateway", "ExpressRoute", "Azure Firewall", "DDoS Protection", "Traffic Manager", "Virtual WAN", "VPN Gateway", "Bastion", "Private Link", "Front Door", "Network Watcher"],
            "Database":   ["Azure SQL Database", "Cosmos DB", "Cache for Redis", "PostgreSQL Flexible Server", "MySQL Flexible Server", "Synapse Analytics", "SQL Managed Instance", "MariaDB", "Data Factory"],
            "DevOps":     ["Azure Pipelines", "GitHub Actions", "Azure Repos", "Azure Artifacts", "Bicep / ARM Templates", "Container Registry (ACR)", "DevTest Labs", "Load Testing", "Azure Boards", "Dev Box", "Automation"],
            "Security":   ["Entra ID (Active Directory)", "Key Vault", "Defender for Cloud", "Microsoft Sentinel", "Azure Policy", "Privileged Identity Management (PIM)", "Confidential Computing", "Information Protection", "DDoS Protection"],
            "Monitoring": ["Azure Monitor", "Application Insights", "Log Analytics", "Azure Advisor", "Cost Management", "Service Health", "Resource Graph", "Log Analytics Workspace"],
            "AI / ML":    ["Azure OpenAI Service", "Machine Learning Studio", "Cognitive Search", "Computer Vision", "Speech Services", "Language Understanding (LUIS)", "Bot Service", "Form Recognizer", "Metrics Advisor"],
            "Analytics":  ["Synapse Analytics", "HDInsight", "Databricks", "Stream Analytics", "Data Explorer", "Data Share", "Time Series Insights", "Event Hubs"]
        },
        "Google Cloud": {
            "color": GREEN,
            "Compute":    ["Compute Engine", "Cloud Run", "GKE (Kubernetes Engine)", "Cloud Functions", "App Engine", "Cloud Batch", "Bare Metal", "VMware Engine", "Preemptible VMs", "Spot VMs", "Sole-tenant Nodes"],
            "Storage":    ["Cloud Storage", "Persistent Disk", "Filestore", "Archive Storage", "Storage Transfer Service", "Backup and DR", "Local SSD", "Cloud Storage for Firebase"],
            "Networking": ["Virtual Private Cloud (VPC)", "Cloud DNS", "Cloud CDN", "Cloud Load Balancing", "Cloud Interconnect", "VPC Service Controls", "Cloud Armor", "Network Intelligence Center", "Cloud NAT", "Cloud VPN", "Service Directory", "Traffic Director"],
            "Database":   ["Cloud SQL", "Firestore", "Bigtable", "Spanner", "BigQuery", "Memorystore", "AlloyDB", "Datastream", "Firebase Realtime Database"],
            "DevOps":     ["Cloud Build", "Cloud Deploy", "Artifact Registry", "Cloud Source Repositories", "Config Connector", "Deployment Manager", "Skaffold", "Cloud Workstations", "Tekton"],
            "Security":   ["IAM", "Cloud KMS", "Secret Manager", "Security Command Center", "Binary Authorization", "Assured Workloads", "Chronicle SIEM", "VPC Service Controls", "Identity-Aware Proxy (IAP)", "BeyondCorp Enterprise"],
            "Monitoring": ["Cloud Monitoring", "Cloud Trace", "Cloud Logging", "Cloud Profiler", "Error Reporting", "Cost Management", "Operations Suite", "Active Assist"],
            "AI / ML":    ["Vertex AI", "Gemini API", "AutoML", "Vision AI", "Speech-to-Text", "Text-to-Speech", "Translation AI", "Natural Language AI", "Dialogflow", "Recommendations AI", "Document AI", "Video AI"],
            "Analytics":  ["BigQuery", "Dataflow", "Dataproc", "Pub/Sub", "Looker", "Dataprep", "Dataplex", "Analytics Hub", "Cloud Data Fusion"]
        },
    },
    "DevOps": {
        "CI/CD": {
            "GitHub Actions": {
                "color": GREEN, "type": "CI/CD",
                "desc": "Event-driven automation workflows. YAML-based, triggers on push/PR/schedule/manual. OIDC for keyless cloud authentication.",
                "deep_dive": [
                    "Workflow anatomy: on (triggers) -> jobs -> steps -> uses/run",
                    "Reusable workflows: workflow_call trigger for DRY pipelines",
                    "OIDC: keyless auth to AWS/Azure/GCP - no stored secrets needed",
                    "Matrix builds: test across multiple OS, Node, Python versions in parallel",
                ],
                "troubleshooting": [
                    "Act (local runner): act push - test workflows locally before pushing",
                    "OIDC 403: check audience claim matches cloud provider config",
                    "Cache miss: verify cache key includes lockfile hash",
                ],
            },
            "Jenkins": {
                "color": RED, "type": "CI/CD",
                "desc": "Open-source CI/CD server with 1800+ plugins. Declarative and Scripted Pipelines via Jenkinsfile. Self-hosted, full control.",
                "deep_dive": [
                    "Declarative Pipeline: pipeline -> agent -> stages -> stage -> steps",
                    "Shared Libraries: vars/ and src/ directories for reusable code",
                    "Kubernetes plugin: ephemeral pod agents - agent { kubernetes { yaml ... } }",
                    "Multibranch Pipeline: auto-discover branches and PRs via Jenkinsfile",
                ],
                "troubleshooting": [
                    "OutOfMemoryError: increase JAVA_OPTS -Xmx in jenkins.service",
                    "Workspace not found: check agent has disk space and permissions",
                    "Plugin conflict: Safe Restart, then disable conflicting plugin",
                ],
            },
            "Azure Pipelines": {
                "color": BLUE, "type": "CI/CD",
                "desc": "Multi-stage YAML pipelines for any language, any platform. Microsoft-hosted or self-hosted agents. Deep Azure integration.",
                "deep_dive": [
                    "Multi-stage YAML: stages -> jobs -> steps hierarchy with dependencies",
                    "Environments: production approval gates, deployment history, rollback",
                    "Service connections: federated identity (OIDC) for Azure/AWS/GCP",
                ],
                "troubleshooting": [
                    "Agent offline: check agent capability vs job demand requirements",
                    "Service connection 401: regenerate service principal secret or use OIDC",
                ],
            }
        },
        "IaC": {
            "Terraform": {
                "color": PURPLE, "type": "IaC",
                "desc": "Industry-standard declarative IaC. Provider ecosystem covers every cloud. Remote state enables team collaboration.",
                "deep_dive": [
                    "HCL: resource, data, variable, output, locals, module blocks",
                    "Remote state: S3+DynamoDB lock (AWS), Azure Blob (Azure), GCS (GCP)",
                    "Workspace vs directory-per-environment - prefer directories for isolation",
                    "State commands: import, taint, untaint, state mv, state rm, state pull",
                ],
                "troubleshooting": [
                    "State lock: terraform force-unlock <lock-id> if stale lock exists",
                    "Provider version conflict: pin with required_providers block",
                    "State drift: terraform refresh then decide whether to import or taint",
                ],
            },
            "Ansible": {
                "color": RED, "type": "IaC",
                "desc": "Agentless configuration management over SSH. Idempotent YAML playbooks. Push-based. Scales from 1 to 10,000 nodes.",
                "deep_dive": [
                    "Inventory: static INI/YAML, dynamic plugins (aws_ec2, azure_rm, gcp_compute)",
                    "Playbook: plays -> tasks -> handlers - notify triggers handler on change only",
                    "Roles: files/ templates/ vars/ defaults/ tasks/ handlers/ meta/ structure",
                ],
                "troubleshooting": [
                    "ansible -m ping all - connectivity check before running playbooks",
                    "ansible-playbook play.yml -vvv - maximum verbosity for debugging",
                    "Task not idempotent: check module return changed and add when condition",
                ],
            }
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
                ],
                "troubleshooting": [
                    "docker inspect container - full config, mounts, network, env vars",
                    "docker logs container --tail 100 -f - follow last 100 lines",
                    "Container OOM: docker stats - CPU/memory usage; check --memory limit",
                ],
            },
            "Kubernetes": {
                "color": BLUE, "type": "Container",
                "desc": "Container orchestration: declarative desired state, self-healing, auto-scaling, rolling deployments across clusters.",
                "deep_dive": [
                    "Core objects: Pod, Deployment, StatefulSet, DaemonSet, Job, CronJob",
                    "Services: ClusterIP, NodePort, LoadBalancer, ExternalName, Headless",
                    "Ingress + IngressClass - nginx, traefik, AWS ALB controller",
                    "Storage: PV/PVC/StorageClass, CSI drivers (EBS, Azure Disk, GCE PD)",
                ],
                "troubleshooting": [
                    "kubectl describe pod <pod> - events section shows scheduling/pull failures",
                    "CrashLoopBackOff: check logs + liveness probe configuration",
                    "Pending pod: kubectl describe -> Insufficient CPU/memory or no matching node",
                ],
            },
            "Helm": {
                "color": BLUE, "type": "Container",
                "desc": "Kubernetes package manager. Charts bundle manifests into versioned, configurable packages. Releases track deployment history.",
                "deep_dive": [
                    "Chart structure: Chart.yaml, values.yaml, templates/, charts/ (dependencies)",
                    "Template functions: include, toYaml, indent, nindent, required, default",
                    "Hooks: pre-install, post-install, pre-upgrade - database migrations",
                ],
                "troubleshooting": [
                    "helm list -A - all releases across all namespaces",
                    "helm history release-name - full upgrade/rollback history",
                    "helm rollback release-name 2 - roll back to revision 2",
                ],
            }
        },
        "Monitoring & Observability": {
            "Prometheus & Grafana": {
                "color": AMBER, "type": "Monitoring",
                "desc": "De-facto standard metrics stack for cloud-native. Pull-based metrics with PromQL query language and rich alerting.",
                "deep_dive": [
                    "Data model: metric_name{label=value,...} @ timestamp = float64 value",
                    "PromQL: rate(http_requests_total[5m]) - per-second rate over 5min window",
                    "Alertmanager: routes, receivers (PagerDuty/Slack/email), inhibit_rules, silences",
                    "kube-prometheus-stack: Prometheus Operator + ServiceMonitor/PodMonitor CRDs",
                ],
                "troubleshooting": [
                    "Target down: check /targets in Prometheus UI - scrape error details",
                    "Cardinality explosion: topk(10, count by (__name__)({}) ) - find high-cardinality metrics",
                    "Grafana no data: verify datasource URL and time range includes data",
                ],
            },
            "ELK / EFK Stack": {
                "color": AMBER, "type": "Monitoring",
                "desc": "Log aggregation and full-text search. Elasticsearch storage, Logstash/Fluentd ingestion, Kibana visualisation.",
                "deep_dive": [
                    "Elasticsearch: indices, shards, replicas - shard count affects parallelism",
                    "ILM (Index Lifecycle Management): hot -> warm -> cold -> frozen -> delete",
                    "Logstash pipeline: input (beats/kafka) -> filter (grok/mutate/date) -> output",
                ],
                "troubleshooting": [
                    "Cluster red: GET /_cluster/health?pretty - find unassigned shards",
                    "Heap pressure: JVM heap >75% -> increase Xmx or reduce shard count",
                    "Logstash pipeline stuck: check Dead Letter Queue for failed events",
                ],
            },
            "OpenTelemetry": {
                "color": AMBER, "type": "Observability",
                "desc": "Vendor-neutral open standard for metrics, logs, and traces (MELT). Unifies observability instrumentation.",
                "deep_dive": [
                    "OTel Collector: Receives, processes, and exports telemetry data.",
                    "Tracing: Context propagation via traceparent headers. Spans represent operations.",
                    "Auto-instrumentation: Bytecode manipulation (Java) or wrappers (Python) for zero-code tracing.",
                ],
                "troubleshooting": [
                    "Missing traces: Ensure context propagation headers are passed through reverse proxies/LBs.",
                    "Collector OOM: Tune batch processor and memory limiter settings in collector.yaml.",
                ],
            }
        }
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
            ],
            "troubleshooting": [
                "ping host - L3 ICMP reachability (use -I eth0 to specify source interface)",
                "traceroute / tracert -d - L3 path with per-hop RTT",
                "arp -a / ip neigh - L2 ARP cache (check for duplicate MACs)",
            ],
        },
        "Subnetting & CIDR": {
            "color": BLUE,
            "desc": "IP address planning is foundational to cloud and on-premises network design. Mistakes here force painful refactoring.",
            "concepts": [
                "CIDR notation: /24=256IPs /25=128 /22=1024 /16=65536 /8=16M",
                "Usable hosts = 2^(32-prefix) - 2 (network + broadcast reserved)",
                "Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 (RFC1918)",
            ],
            "troubleshooting": [
                "ipcalc 10.0.1.0/24 - visual subnet breakdown with all addresses",
                "VPC CIDR overlap: most common cause of peering failures - plan non-overlapping ranges",
                "MTU black hole: pmtud failure - test with ping -M do -s 1472 host",
            ],
        },
        "DNS Deep Dive": {
            "color": BLUE,
            "desc": "DNS is the internet's directory. Every service dependency goes through DNS. Understand it fully to debug latency and failures.",
            "concepts": [
                "DNS hierarchy: root (.) -> TLD (.com) -> authoritative -> recursive resolver -> client",
                "Record types: A(IPv4), AAAA(IPv6), CNAME(alias), MX(mail), TXT(SPF/DKIM), SRV",
                "TTL: controls caching duration - low TTL enables fast failover but increases query load",
            ],
            "troubleshooting": [
                "dig +trace example.com - full resolution from root servers step by step",
                "dig @8.8.8.8 example.com A - query specific resolver directly",
                "nslookup -type=SRV _kerberos._tcp.domain.com - SRV record lookup",
            ],
        },
        "VPC Design & Peering": {
            "color": BLUE,
            "desc": "Virtual Private Cloud is the foundation of cloud networking. Good design at the start prevents painful re-architecture later.",
            "concepts": [
                "3-tier subnet model: public (internet-facing), private (app), isolated (data/DB)",
                "NAT Gateway / NAT Instance: outbound internet for private subnets (no inbound)",
                "VPC Peering: non-transitive, no overlapping CIDR required",
                "Transit Gateway: hub-and-spoke for 100s of VPCs - replaces full-mesh peering",
            ],
            "troubleshooting": [
                "VPC Flow Logs: enable on VPC/subnet/ENI - ACCEPT/REJECT records for all traffic",
                "Route table: check target - local, igw-, nat-, pcx-, tgw-, vpce-, vgw-",
                "Security group: stateful - return traffic auto-allowed; NACLs require explicit allow both ways",
            ],
        },
        "Load Balancing": {
            "color": BLUE,
            "desc": "Distribute traffic across backends for availability and scale. Algorithm and health check design are critical to correctness.",
            "concepts": [
                "Algorithms: Round Robin, Least Connections, Weighted Round Robin, IP Hash",
                "L4 (TCP/UDP): sees IP/port only - no content inspection, very fast, TLS passthrough",
                "L7 (HTTP/HTTPS): can route on URL path, host header, cookies - content-aware",
                "Health checks: HTTP 200 response, TCP connect, custom script - tune interval and threshold",
            ],
            "troubleshooting": [
                "502 Bad Gateway: backend returning invalid HTTP or connection refused",
                "504 Gateway Timeout: backend too slow - increase LB timeout or fix backend",
                "Health check false negatives: check interval, threshold, and timeout settings",
            ],
        },
        "Firewall & ACLs": {
            "color": BLUE,
            "desc": "Network access control: stateful firewalls (connection tracking) vs stateless ACLs (packet filter). Both have their place.",
            "concepts": [
                "Stateful (iptables/nftables/AWS SG): tracks connection state - return traffic auto-allowed",
                "Stateless (AWS NACL/ACL): evaluates every packet independently - must allow return traffic",
                "iptables chains: PREROUTING -> FORWARD -> POSTROUTING (routing), INPUT/OUTPUT (local)",
            ],
            "troubleshooting": [
                "iptables -L -n -v - list rules with packet/byte counters",
                "conntrack -L | grep host - check if connection is tracked",
                "AWS: VPC Flow Logs REJECT records - confirm firewall is the cause",
            ],
        },
        "BGP & Routing": {
            "color": BLUE,
            "desc": "Border Gateway Protocol is the routing protocol of the internet. Used in cloud Direct Connect, SD-WAN, and large on-premises networks.",
            "concepts": [
                "BGP: path-vector protocol - exchanges prefixes with AS_PATH, MED, LOCAL_PREF attributes",
                "iBGP (within AS) vs eBGP (between AS) - iBGP requires full mesh or route reflectors",
                "BGP attributes: LOCAL_PREF (prefer exit), AS_PATH (prefer shorter), MED (prefer entry)",
            ],
            "troubleshooting": [
                "show bgp summary - neighbour state: Idle/Active=problem, Established=good",
                "show bgp neighbors x.x.x.x - detailed BGP session state and counters",
                "BGP stuck in Active: TCP reachability issue on port 179 - check firewall",
            ],
        },
        "Service Mesh (Istio)": {
            "color": PURPLE,
            "desc": "Service mesh adds observability, mTLS security, and traffic management to microservices without changing application code.",
            "concepts": [
                "Sidecar proxy: Envoy injected alongside every pod - intercepts all in/out traffic",
                "Control plane (Istiod): config distribution, certificate authority, telemetry aggregation",
                "mTLS STRICT mode: all pod-to-pod traffic encrypted and mutually authenticated",
                "VirtualService: routing rules - canary split, header-based routing, fault injection",
            ],
            "troubleshooting": [
                "istioctl analyze - scan cluster for config issues and best-practice violations",
                "istioctl proxy-status - sync state of all Envoy sidecars with control plane",
                "503 UH (no healthy upstream): check DestinationRule subset label selectors",
            ],
        },
    },
    "Database": {
        "PostgreSQL": {
            "color": BLUE,
            "desc": "Most advanced open-source RDBMS. MVCC concurrency, ACID transactions, extensions ecosystem, powerful query planner.",
            "concepts": [
                "MVCC: each transaction sees a snapshot - readers never block writers",
                "VACUUM: reclaims dead tuples from MVCC - autovacuum runs automatically",
                "WAL (Write-Ahead Log): durability, crash recovery, streaming replication, PITR",
                "Query planner: EXPLAIN ANALYZE shows actual rows, loops, time - seq vs index scan",
            ],
            "troubleshooting": [
                "SELECT pid,query,state,wait_event FROM pg_stat_activity WHERE state='active'",
                "SELECT * FROM pg_locks l JOIN pg_stat_activity a ON l.pid=a.pid WHERE granted=false",
                "SELECT n_dead_tup,n_live_tup,last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC",
            ],
        },
        "MySQL & MariaDB": {
            "color": AMBER,
            "desc": "World's most popular open-source RDBMS. InnoDB storage engine provides ACID compliance, row-level locking, and MVCC.",
            "concepts": [
                "InnoDB: clustered primary key index, buffer pool (target 80% RAM), undo log for MVCC",
                "Binary log (binlog): row/statement/mixed format - replication and PITR",
                "GTID-based replication: globally unique transaction IDs - simplifies failover",
            ],
            "troubleshooting": [
                "SHOW PROCESSLIST - active queries, state, time, lock info",
                "SHOW ENGINE INNODB STATUS\\G - latest deadlock, buffer pool stats, transaction list",
                "SHOW REPLICA STATUS\\G - Seconds_Behind_Source for replication lag",
            ],
        },
        "MongoDB": {
            "color": GREEN,
            "desc": "Document-oriented NoSQL database. Flexible BSON schema, rich aggregation pipeline, horizontal scaling via sharding.",
            "concepts": [
                "Document model: embed for locality, reference for large/shared data - design for queries",
                "Indexes: single, compound, multikey (arrays), text, geospatial, partial, wildcard",
                "Aggregation pipeline: $match -> $group -> $project -> $lookup -> $unwind -> $sort",
                "Replica set: primary + secondaries, automatic election on primary failure",
            ],
            "troubleshooting": [
                "db.currentOp({active:true}) - currently running operations with lock info",
                "db.collection.explain('executionStats').find({field:'val'}) - query plan",
                "rs.status() - replica set state, lag, last heartbeat per member",
            ],
        },
        "Redis & Memcached": {
            "color": RED,
            "desc": "In-memory data structure stores. Sub-millisecond latency. Caching, sessions, pub/sub, rate limiting, leaderboards.",
            "concepts": [
                "Data types: String, Hash, List, Set, Sorted Set, Stream, HyperLogLog, Bitmap",
                "Persistence: RDB snapshot (point-in-time, compact) vs AOF (every write, durable)",
                "Replication: master-replica, Redis Sentinel (auto-failover), Redis Cluster (sharding)",
                "Eviction: volatile-lru, allkeys-lru, allkeys-lfu, noeviction - set per use case",
            ],
            "troubleshooting": [
                "redis-cli INFO memory - used_memory, mem_fragmentation_ratio (>1.5 = fragmented)",
                "redis-cli SLOWLOG GET 25 - last 25 slow commands (>10ms by default)",
                "redis-cli MONITOR - live command trace (WARNING: impacts performance)",
            ],
        },
        "Kafka & Message Queues": {
            "color": PURPLE,
            "desc": "Distributed event streaming platform for high-throughput data pipelines and decoupled microservices.",
            "concepts": [
                "Topics & Partitions: Data is written to partitions; partition count dictates max consumer parallelism.",
                "Consumer Groups: Each message is delivered to one consumer per group (load balancing).",
                "Retention: Data is stored for a configured time/size, unlike RabbitMQ where it is deleted on read.",
                "Zookeeper / KRaft: Manages cluster metadata and controller election.",
            ],
            "troubleshooting": [
                "Consumer Lag: Consumer is slower than producer. Monitor offset differences.",
                "Under Replicated Partitions (URP): A broker is down or too slow to replicate data.",
            ],
        },
        "Query Optimisation": {
            "color": PURPLE,
            "desc": "Indexes are the single most impactful performance lever. Know when they help, when they hurt, and how the planner chooses.",
            "concepts": [
                "B-Tree index: balanced tree, O(log n) lookup, efficient range scans and ORDER BY",
                "Composite index: column order critical - leftmost prefix rule, equality then range",
                "Covering index: all query columns in index -> index-only scan, zero heap fetches",
            ],
            "troubleshooting": [
                "EXPLAIN ANALYZE: look for Seq Scan on large table -> add index",
                "Index not used: type mismatch (int vs varchar), implicit cast bypasses index",
                "N+1 query: ORM generating 1 query + N queries - use eager loading / JOIN FETCH",
            ],
        },
        "Replication & HA": {
            "color": GREEN,
            "desc": "Database HA strategy is driven by RPO (data loss tolerance) and RTO (downtime tolerance). No single right answer.",
            "concepts": [
                "RPO (Recovery Point Objective): max acceptable data loss - drives sync vs async",
                "RTO (Recovery Time Objective): max acceptable downtime - drives auto vs manual failover",
                "Synchronous replication: 0 data loss, write latency penalty, primary waits for ACK",
            ],
            "troubleshooting": [
                "Replication lag: monitor pg_stat_replication.replay_lag or Seconds_Behind_Source",
                "Split-brain: two primaries - use STONITH fencing to prevent dual writes",
                "Failover test: simulate primary loss in staging, measure actual RTO vs target",
            ],
        },
        "Backup & Recovery": {
            "color": GREEN,
            "desc": "Backups only have value if recovery works. Test restores regularly. Understand RPO implications of each backup type.",
            "concepts": [
                "Full backup: complete copy - simple restore, large, slow for big databases",
                "Incremental: changes since last backup - fast backup, complex restore (chain)",
                "PITR (Point-in-Time Recovery): replay WAL/binlog to exact point - requires continuous archiving",
            ],
            "troubleshooting": [
                "Restore test: restore to separate instance monthly - validate data integrity",
                "PITR gap: check WAL archive for missing segments before attempting recovery",
                "Backup window too long: pg_basebackup --checkpoint=fast --progress",
            ],
        },
        "Performance Tuning": {
            "color": PURPLE,
            "desc": "Database performance is usually the application bottleneck. Systematic tuning from connection pool through query to storage.",
            "concepts": [
                "Buffer/cache hit ratio: >99% target - increase shared_buffers / innodb_buffer_pool_size",
                "Connection pooling: PgBouncer (transaction mode) or ProxySQL - avoid connection storms",
                "work_mem (PostgreSQL): per-sort/hash operation - increase for complex queries",
            ],
            "troubleshooting": [
                "pg_stat_statements: ORDER BY total_exec_time DESC - top queries by total time",
                "temp_files growing: increase work_mem for sort/hash - check log_temp_files",
                "Connection spike: check max_connections and pgbouncer pool_size settings",
            ],
        }
    },
}

def flatten_kb():
    """Build flat searchable index from all KB data."""
    index = []
    for section, section_data in KB.items():
        if section == "Cloud":
            for provider, pdata in section_data.items():
                for cat, services in pdata.items():
                    if cat == "color": continue
                    for svc in services:
                        index.append({
                            "title": svc, "section": section, "parent": f"{provider} -> {cat}",
                            "text": f"{svc} {provider} {cat} cloud service", "type": "cloud_service",
                            "provider": provider, "cat": cat, "color": pdata["color"],
                        })
        else:
            for category, data in section_data.items():
                if "topics" in data:
                    for topic, tdata in data["topics"].items():
                        blob = " ".join([topic, category, tdata.get("desc","")]).lower()
                        index.append({
                            "title": topic, "section": section, "parent": category,
                            "text": blob, "type": "topic", "data": tdata, "color": data.get("color", TEXT2),
                        })
                elif "desc" in data:
                    blob = " ".join([category, data.get("desc","")]).lower()
                    index.append({
                        "title": category, "section": section, "parent": section,
                        "text": blob, "type": "topic", "data": data, "color": data.get("color", TEXT2),
                    })
                else:
                    for tool_name, tdata in data.items():
                        if type(tdata) is dict and "desc" in tdata:
                            blob = " ".join([tool_name, category, tdata.get("desc","")]).lower()
                            index.append({
                                "title": tool_name, "section": section, "parent": category,
                                "text": blob, "type": "devops_tool", "data": tdata, "color": tdata.get("color", TEXT2),
                            })
    return index

SEARCH_INDEX = flatten_kb()

def local_search(query):
    q = query.lower().strip()
    if not q: return []
    terms = q.split()
    scored = []
    for item in SEARCH_INDEX:
        score = 0
        title_lower = item["title"].lower()
        for t in terms:
            if t in title_lower: score += 10
            if t in item["text"]: score += item["text"].count(t)
        if score > 0: scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:20]]


# -- Main App ------------------------------------------------------
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

    def _build(self):
        nav = tk.Frame(self, bg=PANEL, width=220)
        nav.pack(side=tk.LEFT, fill=tk.Y)
        nav.pack_propagate(False)

        tk.Label(nav, text="Knowledge Base", font=("Segoe UI", 14, "bold"),
                 fg=TEXT1, bg=PANEL, pady=18).pack()
        tk.Frame(nav, height=1, bg=BORDER).pack(fill=tk.X, padx=14)

        self._nav_btns = {}
        items = [
            ("🔍 Search", "search"),
            ("💻 OS & Virt", "os"),
            ("☁️ Cloud", "cloud"),
            ("🏛️ Architecture", "architecture"),
            ("🛡️ Security", "security"),
            ("⚙️ DevOps", "devops"),
            ("🌐 Networking", "networking"),
            ("🗄️ Database", "database"),
            ("📋 Log Analyzer", "logs"), 
            ("🤖 IronHide", "agent"),
        ]
        for label, key in items:
            b = tk.Button(nav, text=label, anchor="w", font=F_BODY,
                          fg=TEXT2, bg=PANEL, bd=0, padx=20, pady=12,
                          activeforeground=TEXT1, activebackground=HOVER,
                          cursor="hand2", command=lambda k=key: self._show(k))
            b.pack(fill=tk.X)
            self._nav_btns[key] = b

        self._main = tk.Frame(self, bg=BG)
        self._main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(self._main, bg=BG, highlightthickness=0)
        self._sb = ttk.Scrollbar(self._main, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._sb.set)
        self._sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._inner = tk.Frame(self._canvas, bg=BG)
        self._cw = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")
        self._inner.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>", lambda e: self._canvas.itemconfig(self._cw, width=e.width))
        self._canvas.bind_all("<MouseWheel>", lambda e: self._canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._sections = {}
        self._build_search()
        self._build_os()
        self._build_cloud()
        self._build_architecture()
        self._build_security()
        self._build_devops()
        self._build_networking()
        self._build_database()
        self._build_logs() 
        self._build_agent()

    def _show(self, key):
        for f in self._sections.values():
            f.pack_forget()
        self._sections[key].pack(fill=tk.BOTH, expand=True, padx=26, pady=20)
        for k, b in self._nav_btns.items():
            b.config(fg=ACCENT2 if k == key else TEXT2, bg=HOVER if k == key else PANEL)
        self._canvas.yview_moveto(0)

    def _frame(self, name):
        f = tk.Frame(self._inner, bg=BG)
        self._sections[name] = f
        return f

    def _hdr(self, parent, title, sub=""):
        tk.Label(parent, text=title, font=F_TITLE, fg=TEXT1, bg=BG).pack(anchor="w")
        if sub:
            tk.Label(parent, text=sub, font=F_BODY, fg=TEXT3, bg=BG).pack(anchor="w")
        tk.Frame(parent, height=1, bg=BORDER).pack(fill=tk.X, pady=(10, 16))

    def _row_btn(self, parent, text, sub="", color=TEXT2, cmd=None):
        row = tk.Frame(parent, bg=CARD, cursor="hand2")
        row.pack(fill=tk.X, pady=3)
        tk.Label(row, text=text, font=F_BODY, fg=TEXT1, bg=CARD, padx=16, pady=12, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        if sub:
            tk.Label(row, text=sub, font=F_SMALL, fg=color, bg=CARD, padx=8).pack(side=tk.RIGHT)
        tk.Label(row, text=">", font=("Segoe UI", 13), fg=TEXT3, bg=CARD, padx=10).pack(side=tk.RIGHT)
        if cmd:
            for w in [row] + list(row.winfo_children()):
                w.bind("<Button-1>", lambda e, c=cmd: c())
        return row

    def _open_web(self, query):
        self._show_web_popup(query)

    def _show_web_popup(self, query):
        pop = tk.Toplevel(self)
        pop.title(f"Web search - {query}")
        pop.geometry("700x460")
        pop.configure(bg=BG)
        pop.grab_set()
        tk.Label(pop, text=f'🌍 Web search: "{query}"', font=F_HEAD, fg=TEXT1, bg=BG, pady=14, padx=20).pack(anchor="w")
        grid = tk.Frame(pop, bg=BG, padx=16, pady=10)
        grid.pack(fill=tk.BOTH, expand=True)
        for i, (name, url) in enumerate(web_urls(query)):
            r, c = divmod(i, 3)
            b = tk.Button(grid, text=name, font=F_SMALL, fg=TEXT1, bg=CARD, bd=0, padx=12, pady=10, cursor="hand2", relief=tk.FLAT, command=lambda u=url: webbrowser.open(u), activeforeground=ACCENT2, activebackground=HOVER, wraplength=150, justify=tk.LEFT)
            b.grid(row=r, column=c, padx=5, pady=4, sticky="ew")
            grid.columnconfigure(c, weight=1)
        tk.Button(pop, text="Close", font=F_SMALL, fg=TEXT2, bg=PANEL, bd=0, padx=20, pady=8, cursor="hand2", command=pop.destroy).pack(pady=10)

    def _open_cloud_svc(self, svc, provider, cat):
        if provider == "AWS":
            url = f"https://docs.aws.amazon.com/search/doc-search.html?searchPath=documentation&searchQuery={urllib.parse.quote_plus(svc)}"
        elif provider == "Azure":
            url = f"https://learn.microsoft.com/en-us/search/?terms={urllib.parse.quote_plus('Azure ' + svc)}"
        else:
            url = f"https://cloud.google.com/search?q={urllib.parse.quote_plus(svc)}"
            
        data = {
            "desc": f"{provider} {svc} is a {cat.lower()} service. Since architectures are highly customized, use the '⚡ Ask IronHide' button below to instantly stream a complete architectural deep-dive, Terraform code generation, or specific troubleshooting steps tailored to your environment.",
            "concepts": [
                f"Core architecture and primary use cases for {svc}",
                f"Integration patterns with other {provider} services",
                "Security, IAM policies, and compliance best practices",
                "Pricing model considerations and cost optimization"
            ],
            "troubleshooting": [
                f"Generate custom {svc} error code analysis via IronHide",
                f"Review {provider} monitoring, logging, and performance metrics",
                "Verify networking, VPC routing, and firewall/security group configurations"
            ],
            "url": url
        }
        self._detail_win(svc, f"{provider} > {cat}", data)

    def _detail_win(self, title, parent_label, data, is_devops=False):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("900x720")
        win.configure(bg=BG)

        hdr = tk.Frame(win, bg=CARD, padx=24, pady=16)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text=title, font=F_TITLE, fg=TEXT1, bg=CARD).pack(anchor="w")
        tk.Label(hdr, text=parent_label, font=F_SMALL, fg=TEXT3, bg=CARD).pack(anchor="w")
        tk.Label(hdr, text=data.get("desc", ""), font=F_BODY, fg=TEXT2, bg=CARD, wraplength=840, justify=tk.LEFT).pack(anchor="w", pady=(6, 0))

        cv = tk.Canvas(win, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(win, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        cv.pack(fill=tk.BOTH, expand=True)
        inner = tk.Frame(cv, bg=BG, padx=24, pady=16)
        cw = cv.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>", lambda e: cv.itemconfig(cw, width=e.width))
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))

        key1 = "deep_dive" if is_devops else "concepts"
        lbl1 = "Deep dive topics" if is_devops else "Core concepts"
        self._section_block(inner, lbl1, data.get(key1, []), ACCENT2)
        self._section_block(inner, "Troubleshooting", data.get("troubleshooting", []), GREEN)
        
        btn_row = tk.Frame(inner, bg=BG, pady=14)
        btn_row.pack(anchor="w")
        
        if "url" in data:
            tk.Button(btn_row, text="📘 Official Docs ↗", font=F_SMALL, fg=ACCENT2, bg=TAG, bd=0, padx=12, pady=8, cursor="hand2", command=lambda u=data["url"]: webbrowser.open(u)).pack(side=tk.LEFT, padx=(0, 8))
        else:
            tk.Button(btn_row, text="🌍 Web search ↗", font=F_SMALL, fg=ACCENT2, bg=TAG, bd=0, padx=12, pady=8, cursor="hand2", command=lambda: self._open_web(title)).pack(side=tk.LEFT, padx=(0, 8))
            
        tk.Button(btn_row, text="⚡ Ask IronHide", font=F_SMALL, fg=TEXT1, bg=ACCENT, bd=0, padx=12, pady=8, cursor="hand2", command=lambda: [win.destroy(), self._show("agent"), self._prefill(f"Give me an architectural deep dive and code examples for: {title}")]).pack(side=tk.LEFT)

    def _section_block(self, parent, title, items, color):
        if not items: return
        tk.Label(parent, text=title, font=F_HEAD, fg=color, bg=BG).pack(anchor="w", pady=(12, 4))
        for item in items:
            r = tk.Frame(parent, bg=BG)
            r.pack(fill=tk.X, pady=2)
            tk.Label(r, text="-", font=F_BODY, fg=color, bg=BG, width=2).pack(side=tk.LEFT, anchor="n", pady=2)
            tk.Label(r, text=item, font=F_SMALL, fg=TEXT2, bg=BG, wraplength=800, justify=tk.LEFT, anchor="w").pack(side=tk.LEFT, fill=tk.X)

    # --- Search section ------------------------------------------
    def _build_search(self):
        f = self._frame("search")
        self._hdr(f, "Search", "Type anything - topic, error, command, tool name")

        bar = tk.Frame(f, bg=INPUT, padx=12, pady=10)
        bar.pack(fill=tk.X, pady=(0, 16))
        self._sv = tk.StringVar()
        ent = tk.Entry(bar, textvariable=self._sv, font=F_BODY, bg=INPUT, fg=TEXT1, insertbackground=TEXT1, bd=0)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ent.bind("<Return>", self._do_search)
        tk.Button(bar, text="🔍 Search", font=F_SMALL, fg=ACCENT2, bg=INPUT, bd=0, cursor="hand2", command=self._do_search).pack(side=tk.RIGHT)

        self._search_results = tk.Frame(f, bg=BG)
        self._search_results.pack(fill=tk.BOTH, expand=True)

    def _do_search(self, event=None):
        q = self._sv.get().strip()
        for w in self._search_results.winfo_children(): w.destroy()
        if not q: return
        results = local_search(q)
        if results:
            for item in results:
                self._search_result_row(item, q)
        else:
            tk.Label(self._search_results, text="No matches found.", font=F_SMALL, fg=TEXT3, bg=BG, pady=8).pack(anchor="w")

    def _search_result_row(self, item, query):
        row = tk.Frame(self._search_results, bg=CARD, cursor="hand2")
        row.pack(fill=tk.X, pady=3)
        tk.Label(row, text=item["title"], font=F_BODY, fg=TEXT1, bg=CARD, padx=16, pady=10, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(row, text=item["section"], font=F_SMALL, fg=item.get("color", TEXT2), bg=CARD, padx=12).pack(side=tk.RIGHT)
        
        row.bind("<Button-1>", lambda e, it=item: self._handle_search_click(it))
        for w in row.winfo_children():
            w.bind("<Button-1>", lambda e, it=item: self._handle_search_click(it))

    def _handle_search_click(self, item):
        if item.get("type") == "cloud_service":
            self._open_cloud_svc(item["title"], item["provider"], item.get("cat", ""))
        else:
            self._detail_win(item["title"], item["parent"], item["data"])


    def _build_os(self):
        f = self._frame("os")
        self._hdr(f, "Operating Systems & Virtualization", "Windows Server, Linux, and VMware")
        for os_name, osdata in KB["OS"].items():
            blk = tk.Frame(f, bg=BG, pady=4)
            blk.pack(fill=tk.X)
            hdr = tk.Frame(blk, bg=osdata["color"], padx=14, pady=8)
            hdr.pack(fill=tk.X)
            tk.Label(hdr, text=os_name, font=F_HEAD, fg="white", bg=osdata["color"]).pack(side=tk.LEFT)
            for topic, tdata in osdata["topics"].items():
                self._row_btn(blk, topic, tdata.get("level",""), color=TEXT2, cmd=lambda t=topic, d=tdata, o=os_name: self._detail_win(t, o, d))

    def _build_architecture(self):
        f = self._frame("architecture")
        self._hdr(f, "Architecture Patterns", "System design, HA/DR, and Enterprise frameworks")
        for topic, tdata in KB["Architecture"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata: self._detail_win(t, "Architecture", d))

    def _build_security(self):
        f = self._frame("security")
        self._hdr(f, "Security", "IAM, Cryptography, AppSec, and Compliance")
        for topic, tdata in KB["Security"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata: self._detail_win(t, "Security", d))

    def _build_cloud(self):
        f = self._frame("cloud")
        self._hdr(f, "Cloud", "AWS, Azure, and Google Cloud services")
        self._cloud_btns = {}
        bar = tk.Frame(f, bg=BG)
        bar.pack(anchor="w", pady=(0, 14))
        self._cloud_content = tk.Frame(f, bg=BG)
        self._cloud_content.pack(fill=tk.X)

        for pname in KB["Cloud"]:
            color = KB["Cloud"][pname]["color"]
            b = tk.Button(bar, text=pname, font=F_BODY, fg=TEXT2, bg=CARD, bd=0, padx=18, pady=10, cursor="hand2", command=lambda p=pname: self._load_cloud(p))
            b.pack(side=tk.LEFT, padx=5)
            self._cloud_btns[pname] = (b, color)
        self._load_cloud("AWS")

    def _load_cloud(self, provider):
        for w in self._cloud_content.winfo_children(): w.destroy()
        for p, (b, c) in self._cloud_btns.items():
            b.config(fg="white" if p == provider else TEXT2, bg=c if p == provider else CARD)
        data = KB["Cloud"][provider]
        for cat, services in data.items():
            if cat == "color": continue
            tk.Label(self._cloud_content, text=cat.upper(), font=("Segoe UI", 10, "bold"), fg=TEXT3, bg=BG).pack(anchor="w", pady=(10, 4))
            grid = tk.Frame(self._cloud_content, bg=BG)
            grid.pack(fill=tk.X)
            for i, svc in enumerate(services):
                r, c = divmod(i, 5) 
                card = tk.Frame(grid, bg=CARD, padx=12, pady=10, cursor="hand2")
                card.grid(row=r, column=c, padx=4, pady=4, sticky="ew")
                grid.columnconfigure(c, weight=1)
                tk.Label(card, text=svc, font=F_SMALL, fg=TEXT1, bg=CARD, anchor="w", wraplength=140).pack(anchor="w")
                for w in [card] + list(card.winfo_children()):
                    w.bind("<Button-1>", lambda e, s=svc, p=provider, ct=cat: self._open_cloud_svc(s, p, ct))

    def _build_devops(self):
        f = self._frame("devops")
        self._hdr(f, "DevOps", "CI/CD, IaC, Containers, Monitoring")
        self._devops_content = tk.Frame(f, bg=BG)
        self._devops_content.pack(fill=tk.X)
        for cat in KB["DevOps"]:
            for tool_name, tdata in KB["DevOps"][cat].items():
                self._row_btn(self._devops_content, tool_name, tdata.get("type",""), cmd=lambda t=tool_name, d=tdata: self._detail_win(t, d.get("type",""), d, True))

    def _build_networking(self):
        f = self._frame("networking")
        self._hdr(f, "Networking", "Protocols, architectures, and troubleshooting")
        for topic, tdata in KB["Networking"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata: self._detail_win(t, "Networking", d))

    def _build_database(self):
        f = self._frame("database")
        self._hdr(f, "Database", "SQL, NoSQL, performance, caching, messaging")
        for topic, tdata in KB["Database"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata: self._detail_win(t, "Database", d))

    # --- LOG ANALYZER section ----------------------------------------
    def _build_logs(self):
        f = self._frame("logs")
        self._hdr(f, "Log & Ticket Analyzer", "Upload logs or CSV ticket dumps for root-cause and trend analysis.")

        input_container = tk.Frame(f, bg=CARD, padx=14, pady=14)
        input_container.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(input_container, text="Paste raw logs, JSON, CSV ticket dumps, or error stacks here:", font=F_SMALL, fg=TEXT2, bg=CARD).pack(anchor="w", pady=(0, 6))
        
        self._log_input = scrolledtext.ScrolledText(
            input_container, font=F_MONO, bg=INPUT, fg=TEXT1, bd=0,
            padx=12, pady=12, wrap=tk.WORD, height=8, insertbackground=TEXT1
        )
        self._log_input.pack(fill=tk.X, expand=True)

        btn_row = tk.Frame(input_container, bg=CARD)
        btn_row.pack(fill=tk.X, pady=(12, 0))
        
        tk.Button(btn_row, text="📁 Upload File (.log/.txt/.csv)", font=F_SMALL, fg=TEXT1, bg=PANEL, bd=0, padx=16, pady=10, cursor="hand2", command=self._load_log_file).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_row, text="🗑️ Clear", font=F_SMALL, fg=TEXT3, bg=CARD, bd=0, padx=16, pady=10, cursor="hand2", command=lambda: self._log_input.delete("1.0", tk.END)).pack(side=tk.LEFT)
        
        self._analyze_btn = tk.Button(btn_row, text="🔬 Analyze with IronHide", font=F_BODY, fg="white", bg=ACCENT, bd=0, padx=24, pady=10, cursor="hand2", command=self._run_log_analysis)
        self._analyze_btn.pack(side=tk.RIGHT)

        tk.Label(f, text="*Note: Image/Diagram upload is not supported in the free tier. Please describe diagrams in text.*", font=("Segoe UI", 9, "italic"), fg=TEXT3, bg=BG).pack(anchor="w", pady=(0,6))

        output_container = tk.Frame(f, bg=CARD, padx=14, pady=14)
        output_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(output_container, text="Analysis & Resolution Steps:", font=F_SMALL, fg=TEXT2, bg=CARD).pack(anchor="w", pady=(0, 6))
        
        self._log_output = scrolledtext.ScrolledText(
            output_container, font=F_MONO, bg=PANEL, fg=GREEN, bd=0,
            padx=14, pady=12, wrap=tk.WORD, state=tk.DISABLED, insertbackground=TEXT1
        )
        self._log_output.pack(fill=tk.BOTH, expand=True)
        self._log_output.tag_config("system", spacing1=10, spacing3=10)

    def _load_log_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("Log & Text", "*.log *.txt"), ("CSV Data", "*.csv"), ("All files", "*.*"))
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if len(content) > 15000:
                        content = content[-15000:] + "\n\n[...File truncated to last 15,000 characters to fit context limits...]"
                    self._log_input.delete("1.0", tk.END)
                    self._log_input.insert("1.0", f"--- Loaded from {os.path.basename(filepath)} ---\n{content}")
            except Exception as e:
                self._log_input.delete("1.0", tk.END)
                self._log_input.insert("1.0", f"Error reading file: {str(e)}")

    def _run_log_analysis(self):
        raw_log = self._log_input.get("1.0", tk.END).strip()
        if not raw_log: return
        self._analyze_btn.config(state=tk.DISABLED, text="Analyzing...")
        self._log_output.config(state=tk.NORMAL)
        self._log_output.delete("1.0", tk.END)
        self._log_output.insert(tk.END, "IronHide is scanning the data and correlating issues...\n")
        self._log_output.config(state=tk.DISABLED)
        threading.Thread(target=self._process_log_request, args=(raw_log,), daemon=True).start()

    def _process_log_request(self, log_content):
        try:
            system_prompt = (
                "You are IronHide, an expert Cloud Infrastructure and DevOps Specialist. "
                "Analyze the following log snippet, error trace, or CSV ticket dump. "
                "If this is a ticket dump (CSV/text), identify common trends, frequent failing services, and recommend architectural improvements. "
                "If this is a standard error log, format your response cleanly with these exact headers: "
                "\n1. Root Cause Analysis\n2. Suggested Fix / Commands\n3. Preventive Measures."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please analyze this data/issue:\n\n{log_content}"}
            ]
            url = "https://text.pollinations.ai/"
            data = json.dumps({"messages": messages, "model": "openai"}).encode('utf-8')
            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            
            with urllib.request.urlopen(req, timeout=60) as response:
                answer_raw = response.read().decode('utf-8').strip()
                
            try:
                parsed = json.loads(answer_raw)
                if isinstance(parsed, dict):
                    if "choices" in parsed:
                        answer = parsed["choices"][0]["message"].get("content", "")
                    elif "content" in parsed and parsed["content"]:
                        answer = parsed["content"]
                    else:
                        answer = answer_raw
                else:
                    answer = answer_raw
            except Exception:
                answer = answer_raw
                
            if not answer:
                answer = "Error: Received an empty response from the AI."

            self.after(0, lambda: self._update_log_output(answer))
        except Exception as ex:
            self.after(0, lambda: self._update_log_output(f"Analysis Failed: {ex}\nPlease check your internet connection or try a smaller log snippet."))
        finally:
            self.after(0, lambda: self._analyze_btn.config(state=tk.NORMAL, text="🔬 Analyze with IronHide"))

    def _update_log_output(self, text):
        self._log_output.config(state=tk.NORMAL)
        self._log_output.delete("1.0", tk.END)
        self._log_output.insert(tk.END, text, "system")
        self._log_output.config(state=tk.DISABLED)


    # --- AI Agent section ----------------------------------------
    def _build_agent(self):
        f = self._frame("agent")
        self._hdr(f, "IronHide", "Your personal assistant for scripts, errors, and architecture.")

        chips_lbl = tk.Label(f, text="Quick scripting prompts:", font=F_SMALL, fg=TEXT3, bg=BG)
        chips_lbl.pack(anchor="w", pady=(0, 4))
        chips = tk.Frame(f, bg=BG)
        chips.pack(anchor="w", pady=(0, 10))
        quick = [
            "Python script to monitor CPU usage",
            "Bash script to backup a MySQL DB",
            "PowerShell script to list AD users",
            "Ansible playbook to install Nginx",
        ]
        for q in quick:
            tk.Button(chips, text=q, font=F_SMALL, fg=ACCENT2, bg=TAG, bd=0, padx=10, pady=6, cursor="hand2", command=lambda t=q: self._prefill(t)).pack(side=tk.LEFT, padx=4)

        chat_outer = tk.Frame(f, bg=CARD)
        chat_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self._chat = scrolledtext.ScrolledText(
            chat_outer, font=F_MONO, bg=PANEL, fg=TEXT1, bd=0,
            padx=16, pady=12, wrap=tk.WORD, state=tk.DISABLED, height=22,
            insertbackground=TEXT1, selectbackground=ACCENT, selectforeground="white"
        )
        self._chat.pack(fill=tk.BOTH, expand=True)
        
        self._chat.tag_config("user",    foreground=ACCENT2, font=("Segoe UI", 11, "bold"), spacing1=10, spacing3=5)
        self._chat.tag_config("ai",      foreground=TEXT1,   font=F_MONO, lmargin1=20, lmargin2=20, spacing3=15)
        self._chat.tag_config("system",  foreground=TEXT3,   font=F_SMALL, spacing1=10, spacing3=10)
        self._chat.tag_config("err",     foreground=RED,     font=F_SMALL, spacing3=10)
        
        self._append("system", "IronHide is online. I can write scripts in ANY language (Python, Bash, PowerShell, Go, Terraform, etc). How can I help you today?\n")

        input_row = tk.Frame(f, bg=CARD, padx=12, pady=10)
        input_row.pack(fill=tk.X)
        self._agent_input = tk.Text(input_row, font=F_BODY, bg=INPUT, fg=TEXT1, insertbackground=TEXT1, bd=0, height=3, wrap=tk.WORD, padx=10, pady=8)
        self._agent_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._agent_input.bind("<Return>", self._agent_enter)

        side = tk.Frame(input_row, bg=CARD)
        side.pack(side=tk.RIGHT, padx=(10, 0))
        self._send_btn = tk.Button(side, text="🚀 Send\n↵ Enter", font=F_SMALL, fg="white", bg=ACCENT, bd=0, padx=16, pady=10, cursor="hand2", command=self._agent_send)
        self._send_btn.pack(fill=tk.X, pady=(0, 5))
        tk.Button(side, text="🗑️ Clear", font=F_SMALL, fg=TEXT2, bg=PANEL, bd=0, padx=14, pady=8, cursor="hand2", command=self._agent_clear).pack(fill=tk.X)

    def _append(self, role, text):
        self._chat.config(state=tk.NORMAL)
        if role == "user":
            self._chat.insert(tk.END, "You:\n", "user")
            self._chat.insert(tk.END, text + "\n", "ai")
        elif role == "ai":
            self._chat.insert(tk.END, "IronHide:\n", "user")
            self._chat.insert(tk.END, text + "\n", "ai")
        elif role == "err":
            self._chat.insert(tk.END, f"⚠  {text}\n", "err")
        else:
            self._chat.insert(tk.END, text + "\n", "system")
        self._chat.config(state=tk.DISABLED)
        self._chat.see(tk.END)

    def _agent_clear(self):
        self._chat.config(state=tk.NORMAL)
        self._chat.delete("1.0", tk.END)
        self._chat.config(state=tk.DISABLED)
        self.agent_history = []
        self._append("system", "Chat cleared.\n")

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
        if not q: return
        self._agent_input.delete("1.0", tk.END)
        self._append("user", q)
        self._send_btn.config(state=tk.DISABLED, text="Thinking...")
        self.agent_history.append({"role": "user", "content": q})
        threading.Thread(target=self._run_agent, daemon=True).start()

    def _run_agent(self):
        try:
            system_prompt = (
                "You are IronHide, a Senior Cloud & DevOps AI. "
                "Write clean, production-ready code. "
                "CRITICAL RULES: "
                "1. Strictly format all code using proper indentation and Markdown code blocks. "
                "2. Keep explanations extremely brief. "
                "3. At the very end of your response, ALWAYS include a '🔗 Sources & References' section with actual URLs to official GitHub repositories, Terraform Registries, or official documentation (AWS/Azure/GCP/Microsoft) for the modules/commands used."
            )
            
            messages = [{"role": "system", "content": system_prompt}]
            for msg in self.agent_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            url = "https://text.pollinations.ai/"
            data = json.dumps({
                "messages": messages,
                "model": "openai"
            }).encode('utf-8')
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "KnowledgeBase/1.0"
            }
            
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            
            with urllib.request.urlopen(req, timeout=60) as response:
                answer_raw = response.read().decode('utf-8').strip()
                
            try:
                parsed = json.loads(answer_raw)
                if isinstance(parsed, dict):
                    if "choices" in parsed:
                        answer = parsed["choices"][0]["message"].get("content", "")
                    elif "content" in parsed and parsed["content"]:
                        answer = parsed["content"]
                    else:
                        answer = answer_raw
                else:
                    answer = answer_raw
            except Exception:
                answer = answer_raw
                
            if not answer:
                answer = "Error: Received an empty response from the AI."
            
            self.agent_history.append({"role": "assistant", "content": answer})
            self.after(0, lambda: self._append("ai", answer))

        except Exception as ex:
            self.after(0, lambda: self._append("err", f"Connection Error: {ex}\nEnsure you have an active internet connection."))
        finally:
            self.after(0, lambda: self._send_btn.config(state=tk.NORMAL, text="🚀 Send\n↵ Enter"))

if __name__ == "__main__":
    try:
        app = KnowledgeBase()
        app.mainloop()
    except Exception as e:
        import traceback
        with open("kb_error.log", "w") as f:
            traceback.print_exc(file=f)
        raise