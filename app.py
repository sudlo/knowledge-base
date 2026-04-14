import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
import webbrowser
import urllib.parse
import sys
import os

# ── Palette (Vibrant Synthwave / Cyberpunk) ──────────────────────
BG       = "#1A1A2E" 
PANEL    = "#16213E" 
CARD     = "#0F3460" 
INPUT    = "#1A1A2E" 
BORDER   = "#E94560" 
HOVER    = "#E94560" 
ACCENT   = "#00D2FC" 
ACCENT2  = "#FF2A71" 
GREEN    = "#00FFC6" 
AMBER    = "#FFDE59" 
RED      = "#FF3366" 
BLUE     = "#00D2FC" 
PURPLE   = "#B5179E" 
TEXT1    = "#FFFFFF" 
TEXT2    = "#E0E0E0" 
TEXT3    = "#A0A0B0" 
TAG      = "#430F58" 

F_TITLE  = ("Segoe UI", 20, "bold")
F_HEAD   = ("Segoe UI", 12, "bold")
F_BODY   = ("Segoe UI", 11)
F_SMALL  = ("Segoe UI", 10)
F_MONO   = ("Consolas", 10)

# ── Web search sources ─────────────────────────────
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
                    ],
                    "troubleshooting": [
                        "dcdiag /test:all — comprehensive DC health check",
                        "repadmin /showrepl — replication status per partner",
                        "netlogon.log at C:\\Windows\\debug\\netlogon.log — auth failures",
                    ],
                    "tools": ["ADUC", "AD Sites & Services", "ADSI Edit", "repadmin", "dcdiag"],
                },
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
                    ],
                    "troubleshooting": [
                        "ps aux --sort=-%cpu | head -15 — top CPU consumers",
                        "systemctl status nginx.service — state + last 10 journal lines",
                        "journalctl -u nginx -f --since '10 min ago' — follow service logs",
                    ],
                    "tools": ["htop", "systemctl", "journalctl", "strace", "lsof"],
                },
            }
        }
    },
    "Cloud": {
        "AWS": {
            "color": AMBER,
            "Compute":    ["EC2", "Lambda", "ECS", "EKS", "Fargate", "Elastic Beanstalk"],
            "Storage":    ["S3", "EBS", "EFS", "FSx", "S3 Glacier", "Storage Gateway"],
            "Networking": ["VPC", "Route 53", "CloudFront", "ALB/NLB/ELB", "Transit Gateway"],
        },
        "Azure": {
            "color": BLUE,
            "Compute":    ["Virtual Machines", "Azure Functions", "AKS", "Container Apps"],
            "Storage":    ["Blob Storage", "Azure Disk", "Azure Files", "NetApp Files"],
            "Networking": ["Virtual Network", "Azure DNS", "Azure CDN", "Load Balancer"],
        },
        "Google Cloud": {
            "color": GREEN,
            "Compute":    ["Compute Engine", "Cloud Run", "GKE", "Cloud Functions"],
            "Storage":    ["Cloud Storage", "Persistent Disk", "Filestore", "Archive Storage"],
            "Networking": ["VPC", "Cloud DNS", "Cloud CDN", "Cloud Load Balancing"],
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
                ],
                "troubleshooting": [
                    "Act (local runner): act push —