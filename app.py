import tkinter as tk
from tkinter import ttk, scrolledtext
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
                    "Act (local runner): act push — test workflows locally before pushing",
                    "OIDC 403: check audience claim matches cloud provider config",
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
                ],
                "troubleshooting": [
                    "State lock: terraform force-unlock <lock-id> if stale lock exists",
                    "Provider version conflict: pin with required_providers block",
                ],
            },
        },
    },
    "Networking": {
        "VPC Design & Peering": {
            "color": BLUE,
            "desc": "Virtual Private Cloud is the foundation of cloud networking. Good design at the start prevents painful re-architecture later.",
            "concepts": [
                "3-tier subnet model: public (internet-facing), private (app), isolated (data/DB)",
                "NAT Gateway / NAT Instance: outbound internet for private subnets (no inbound)",
                "VPC Peering: non-transitive, no overlapping CIDR required",
            ],
            "troubleshooting": [
                "VPC Flow Logs: enable on VPC/subnet/ENI — ACCEPT/REJECT records for all traffic",
                "Route table: check target — local, igw-, nat-, pcx-, tgw-, vpce-, vgw-",
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
            ],
            "troubleshooting": [
                "SELECT pid,query,state,wait_event FROM pg_stat_activity WHERE state='active'",
                "SELECT * FROM pg_locks l JOIN pg_stat_activity a ON l.pid=a.pid WHERE granted=false",
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
                    blob = " ".join([topic, os_name, tdata["desc"]]).lower()
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
                    blob = " ".join([tool_name, cat, tdata["desc"]]).lower()
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
                blob = " ".join([topic, tdata["desc"]]).lower()
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

    def _build(self):
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
        
        btn_row = tk.Frame(inner, bg=BG, pady=10)
        btn_row.pack(anchor="w")
        tk.Button(btn_row, text="Web search ↗", font=F_SMALL, fg=ACCENT2, bg=TAG, 
                  bd=0, padx=10, pady=6, cursor="hand2", command=lambda: self._open_web(title)).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_row, text="Ask IronHide", font=F_SMALL, fg=TEXT1, bg=ACCENT, 
                  bd=0, padx=10, pady=6, cursor="hand2", command=lambda: [win.destroy(), self._show("agent"), self._prefill(f"Deep dive on {title}")]).pack(side=tk.LEFT)

    def _section_block(self, parent, title, items, color):
        if not items: return
        tk.Label(parent, text=title, font=F_HEAD, fg=color, bg=BG).pack(anchor="w", pady=(10, 2))
        for item in items:
            r = tk.Frame(parent, bg=BG)
            r.pack(fill=tk.X, pady=1)
            tk.Label(r, text="•", font=F_BODY, fg=color, bg=BG, width=2).pack(side=tk.LEFT, anchor="n", pady=2)
            tk.Label(r, text=item, font=F_SMALL, fg=TEXT2, bg=BG, wraplength=780, justify=tk.LEFT, anchor="w").pack(side=tk.LEFT, fill=tk.X)

    def _build_search(self):
        f = self._frame("search")
        self._hdr(f, "Search", "Type anything — topic, error, command, tool name")

        bar = tk.Frame(f, bg=INPUT, padx=10, pady=8)
        bar.pack(fill=tk.X, pady=(0, 12))
        self._sv = tk.StringVar()
        ent = tk.Entry(bar, textvariable=self._sv, font=F_BODY, bg=INPUT, fg=TEXT1, insertbackground=TEXT1, bd=0)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        ent.bind("<Return>", self._do_search)
        tk.Button(bar, text="Search", font=F_SMALL, fg=ACCENT2, bg=INPUT, bd=0, cursor="hand2", command=self._do_search).pack(side=tk.RIGHT)

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
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=item["title"], font=F_BODY, fg=TEXT1, bg=CARD, padx=14, pady=8, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(row, text=item["section"], font=F_SMALL, fg=item.get("color", TEXT2), bg=CARD, padx=10).pack(side=tk.RIGHT)
        row.bind("<Button-1>", lambda e: self._detail_win(item["title"], item["parent"], item["data"]))

    def _build_os(self):
        f = self._frame("os")
        self._hdr(f, "Operating Systems", "Windows Server and Linux")
        for os_name, osdata in KB["OS"].items():
            blk = tk.Frame(f, bg=BG, pady=4)
            blk.pack(fill=tk.X)
            hdr = tk.Frame(blk, bg=osdata["color"], padx=14, pady=8)
            hdr.pack(fill=tk.X)
            tk.Label(hdr, text=os_name, font=F_HEAD, fg="white", bg=osdata["color"]).pack(side=tk.LEFT)
            for topic, tdata in osdata["topics"].items():
                self._row_btn(blk, topic, tdata["level"], color=TEXT2, cmd=lambda t=topic, d=tdata, o=os_name: self._detail_win(t, o, d))

    def _build_cloud(self):
        f = self._frame("cloud")
        self._hdr(f, "Cloud", "AWS, Azure, and Google Cloud")
        self._cloud_btns = {}
        bar = tk.Frame(f, bg=BG)
        bar.pack(anchor="w", pady=(0, 12))
        self._cloud_content = tk.Frame(f, bg=BG)
        self._cloud_content.pack(fill=tk.X)

        for pname in KB["Cloud"]:
            color = KB["Cloud"][pname]["color"]
            b = tk.Button(bar, text=pname, font=F_BODY, fg=TEXT2, bg=CARD, bd=0, padx=16, pady=8, cursor="hand2", command=lambda p=pname: self._load_cloud(p))
            b.pack(side=tk.LEFT, padx=4)
            self._cloud_btns[pname] = (b, color)
        self._load_cloud("AWS")

    def _load_cloud(self, provider):
        for w in self._cloud_content.winfo_children(): w.destroy()
        data = KB["Cloud"][provider]
        for cat, services in data.items():
            if cat == "color": continue
            tk.Label(self._cloud_content, text=cat.upper(), font=("Segoe UI", 10, "bold"), fg=TEXT3, bg=BG).pack(anchor="w", pady=(8, 2))
            grid = tk.Frame(self._cloud_content, bg=BG)
            grid.pack(fill=tk.X)
            for i, svc in enumerate(services):
                r, c = divmod(i, 4)
                card = tk.Frame(grid, bg=CARD, padx=12, pady=10, cursor="hand2")
                card.grid(row=r, column=c, padx=4, pady=3, sticky="ew")
                grid.columnconfigure(c, weight=1)
                tk.Label(card, text=svc, font=F_SMALL, fg=TEXT1, bg=CARD, anchor="w", wraplength=170).pack(anchor="w")

    def _build_devops(self):
        f = self._frame("devops")
        self._hdr(f, "DevOps", "CI/CD, IaC, Containers")
        self._devops_content = tk.Frame(f, bg=BG)
        self._devops_content.pack(fill=tk.X)
        for cat in KB["DevOps"]:
            for tool_name, tdata in KB["DevOps"][cat].items():
                self._row_btn(self._devops_content, tool_name, tdata["type"], cmd=lambda t=tool_name, d=tdata: self._detail_win(t, d["type"], d, True))

    def _build_networking(self):
        f = self._frame("networking")
        self._hdr(f, "Networking", "Protocols, architectures, and troubleshooting")
        for topic, tdata in KB["Networking"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata: self._detail_win(t, "Networking", d))

    def _build_database(self):
        f = self._frame("database")
        self._hdr(f, "Database", "SQL, NoSQL, performance")
        for topic, tdata in KB["Database"].items():
            self._row_btn(f, topic, cmd=lambda t=topic, d=tdata: self._detail_win(t, "Database", d))

    # ─── AI Agent section ────────────────────────────────────────
    def _build_agent(self):
        f = self._frame("agent")
        self._hdr(f, "IronHide", "Your personal assistant for scripts, errors, and architectures")

        chips_lbl = tk.Label(f, text="Quick prompts:", font=F_SMALL, fg=TEXT3, bg=BG)
        chips_lbl.pack(anchor="w", pady=(0, 4))
        chips = tk.Frame(f, bg=BG)
        chips.pack(anchor="w", pady=(0, 10))
        quick = [
            "Write a Terraform script for Azure VM",
            "Linux server OOM killer investigation",
            "Ansible playbook to install Nginx",
        ]
        for q in quick:
            tk.Button(chips, text=q, font=F_SMALL, fg=ACCENT2, bg=TAG, bd=0, padx=8, pady=5, cursor="hand2", command=lambda t=q: self._prefill(t)).pack(side=tk.LEFT, padx=3)

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
        
        self._append("system", "IronHide is online via a free, serverless API. How can I help you today?\n\n")

        input_row = tk.Frame(f, bg=CARD, padx=10, pady=8)
        input_row.pack(fill=tk.X)
        self._agent_input = tk.Text(input_row, font=F_BODY, bg=INPUT, fg=TEXT1, insertbackground=TEXT1, bd=0, height=3, wrap=tk.WORD, padx=8, pady=6)
        self._agent_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._agent_input.bind("<Return>", self._agent_enter)

        side = tk.Frame(input_row, bg=CARD)
        side.pack(side=tk.RIGHT, padx=(8, 0))
        self._send_btn = tk.Button(side, text="Send\n↵ Enter", font=F_SMALL, fg="white", bg=ACCENT, bd=0, padx=14, pady=8, cursor="hand2", command=self._agent_send)
        self._send_btn.pack(fill=tk.X, pady=(0, 4))
        tk.Button(side, text="Clear", font=F_SMALL, fg=TEXT2, bg=PANEL, bd=0, padx=12, pady=6, cursor="hand2", command=self._agent_clear).pack(fill=tk.X)

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
        if not q: return
        self._agent_input.delete("1.0", tk.END)
        self._append("user", q)
        self._send_btn.config(state=tk.DISABLED, text="Thinking...")
        self.agent_history.append({"role": "user", "content": q})
        threading.Thread(target=self._run_agent, daemon=True).start()

    def _run_agent(self):
        import urllib.request
        import json

        try:
            # 1. Format the prompt context
            messages = [{
                "role": "system", 
                "content": "You are IronHide, a Senior DevOps Engineer and coding assistant. Write clean, production-ready scripts. Keep explanations extremely brief. Provide exactly the code requested."
            }]
            
            for msg in self.agent_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # 2. Call a free, keyless AI endpoint using standard built-in Python libraries
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
            
            with urllib.request.urlopen(req, timeout=45) as response:
                # Pollinations returns the raw text directly
                answer = response.read().decode('utf-8').strip()
            
            self.agent_history.append({"role": "assistant", "content": answer})
            self.after(0, lambda: self._append("ai", answer))

        except Exception as ex:
            self.after(0, lambda: self._append("err", f"Connection Error: {ex}\nEnsure you have an active internet connection."))
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