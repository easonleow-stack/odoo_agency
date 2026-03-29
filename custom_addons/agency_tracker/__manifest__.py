# -*- coding: utf-8 -*-
{
    'name': 'Agency Task Tracker',
    'version': '18.0.1.0.0',
    'category': 'Project',
    'summary': 'Ads On Marketing — Internal Task & Campaign Tracker',
    'description': """
        Full internal task board for Ads On Marketing Sdn Bhd.
        Features:
        - Task management with status, priority, team, and deadlines
        - Kanban board view mirroring the agency dashboard
        - Per-team filtering (Creative, Media, Social, Strategy, Client Services)
        - CRM integration — link tasks to active sales leads/deals
        - Activity timeline and deadline alerts
    """,
    'author': 'Ads On Marketing Sdn Bhd',
    'website': 'https://www.adsonmarketing.com.my',
    'license': 'LGPL-3',

    # Dependencies — Odoo built-in modules this addon needs
    'depends': [
        'base',      # Core Odoo
        'mail',      # Chatter / internal messages on tasks
        'crm',       # Link tasks to CRM leads/opportunities
        'project',   # Base project model (optional — used for reference)
    ],

    # Data files loaded in order
    'data': [
        'security/ir.model.access.csv',
        'views/agency_task_views.xml',
        'views/menu.xml',
    ],

    # Backend assets (CSS + JS injected into Odoo's web client)
    'assets': {
        'web.assets_backend': [
            'agency_tracker/static/src/css/tracker.css',
            'agency_tracker/static/src/js/tracker.js',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
