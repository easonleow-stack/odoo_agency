# Business Process — Ads On Marketing Sdn Bhd (Odoo Agency System)

## Overview

The system has two modules working together:

| Module | Type | Purpose |
|---|---|---|
| `agency_tracker` | Internal (Odoo backend) | Task/project management board + CRM menu |
| `agency_website` | Public website | Client-facing pages + live stats from task data |

---

## End-to-End Business Flow

### Stage 1 — Lead Capture (Website)

1. A potential client visits the public website (`/contact-us`)
2. They fill in the **"Send Us a Message"** contact form (name, email, phone, company, service interest, message)
3. On submit, the controller (`/contact-us/submit`) creates a **CRM lead** (`crm.lead`) automatically
4. The client sees a success message; no account needed

**Result:** A new lead appears in **Sales Pipeline** (CRM)

---

### Stage 2 — Lead Qualification (CRM / Sales Pipeline)

1. The sales team sees the new lead in **Agency Board → Sales Pipeline**
2. They review the enquiry details (message, service interest, company)
3. They assign the lead to a salesperson (the "Sales Directory")
4. They work the lead through the standard CRM stages (New → Qualified → Proposition → Won/Lost)
5. Once won, the lead becomes an **opportunity/project** to deliver

**Result:** A qualified client opportunity is ready to be executed

---

### Stage 3 — Task Creation & Assignment (Task Tracker)

1. After winning the deal, the account/project manager goes to **Agency Board → Task Tracker**
2. They create one or more `agency.task` records for the campaign
   - Fill in: Task name, Campaign name, Team (Creative / Media / Social / Strategy / Client Services / Field), Assignee, Reviewer, Priority, Deadline
   - Link the task to the CRM lead/opportunity via the **CRM Lead** field — this pulls in the `client_name` automatically
3. Tasks start at status **To Do**

**Result:** Campaign tasks are created and assigned to the right teams

---

### Stage 4 — Task Execution (Task Tracker — Kanban Board)

The Kanban board shows 5 columns that represent the task lifecycle:

```
[ To Do ] → [ In Progress ] → [ Review ] → [ Done ]
                                              ↑
                              [ Stuck ] ──────┘  (can be unblocked back to In Progress)
```

| Status | What it means |
|---|---|
| **To Do** | Task created, not started yet |
| **In Progress** | Assignee has started working; progress % is updated manually |
| **Review** | Work submitted, waiting for reviewer/client approval |
| **Done** | Approved and completed; progress auto-sets to 100%, `date_closed` is recorded |
| **Stuck** | Blocked — needs attention or escalation |

**Within each task:**
- Assignee updates the **progress bar** (0–100%)
- Any blocker → move to **Stuck** (shows red border, appears on overdue dashboard)
- When work is ready → move to **Review**
- Reviewer approves → click **Mark Done** (or button in header)
- Chatter records all status changes, comments, and activity logs

**Overdue logic:** If today > deadline AND status is not Done → `is_overdue = True` → red border on kanban card, flagged in dashboard

---

### Stage 5 — Visibility (Public Website Dashboard & Portfolio)

The public website reads live data from `agency.task` (no login required):

| Page | What it shows |
|---|---|
| **Homepage** (`/`) | Total tasks, completed tasks, active campaigns count, teams count + 6 featured in-progress/review campaigns |
| **Portfolio** (`/portfolio`) | All campaigns grouped by campaign name, with task count, completion %, team badge — filterable by team |
| **Dashboard** (`/dashboard`) | KPIs: total tasks, completed, overdue count, completion rate %; status breakdown; team distribution; priority breakdown |

This gives clients and management a real-time view of active work without needing an Odoo login.

---

## Summary Flow Diagram

```
[Client visits website]
        │
        ▼
[Fills "Send Us a Message" form]
        │
        ▼
[CRM Lead auto-created in Odoo]  ──────────────────────────────┐
        │                                                        │
        ▼                                                        │
[Sales team reviews in Sales Pipeline]                          │
        │                                                        │
        ▼                                                        │
[Assign salesperson → qualify → Win opportunity]                │
        │                                                        │
        ▼                                                        │
[Project manager creates Agency Tasks]                          │
[Links task to CRM lead → client name auto-fills] ◄────────────┘
        │
        ▼
[Tasks go through Kanban: To Do → In Progress → Review → Done]
        │                          │
        │                   (Stuck if blocked)
        ▼
[Done: date_closed recorded, progress = 100%]
        │
        ▼
[Live stats update on public website (Portfolio, Dashboard, Homepage)]
```

---

## Menu Structure (Odoo Backend)

```
Agency Board
├── Task Tracker        → Kanban/list/form view of agency.task
└── Sales Pipeline      → Standard Odoo CRM (crm.lead)
```

---

## Access Rights

| Role | Task Tracker | CRM |
|---|---|---|
| Regular user (staff) | Create, read, edit tasks — cannot delete | Standard CRM access |
| System/manager | Full CRUD including delete | Full CRM access |

---

## What is Currently NOT in the System

These are gaps in the current version that may need future development:

- No **client portal** — clients cannot log in to see their own project status
- No **invoice/billing** integration — winning a deal does not trigger any billing
- No **approval workflow** — Review stage is visual only, no formal approve/reject action
- No **notifications** — no automatic email/alert when a task goes overdue or moves to Stuck
- No **time tracking** — progress is manual percentage, not hours logged
- No **task templates** — each task is created from scratch per campaign
