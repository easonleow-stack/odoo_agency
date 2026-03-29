# -*- coding: utf-8 -*-
{
    'name': 'Agency Website',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Ads On Marketing — Public-facing agency website',
    'description': """
        Full public website for Ads On Marketing Sdn Bhd.
        Features:
        - Modern homepage with live campaign stats from agency.task
        - Services page showcasing all agency capabilities
        - Portfolio page with campaign progress (from agency.task model)
        - Contact form that auto-creates CRM leads
        - Public dashboard with real-time task analytics
        - About page with team information
        - Custom header and footer replacing Odoo defaults
    """,
    'author': 'Ads On Marketing Sdn Bhd',
    'website': 'https://www.adsonmarketing.com.my',
    'license': 'LGPL-3',

    'depends': [
        'website',          # Odoo Website framework
        'agency_tracker',   # Our backend task tracker models
        'crm',              # CRM lead creation from contact form
    ],

    'data': [
        'views/layout.xml',
        'views/homepage.xml',
        'views/services.xml',
        'views/portfolio.xml',
        'views/about.xml',
        'views/contact.xml',
        'views/dashboard.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'agency_website/static/src/css/website.css',
            'agency_website/static/src/js/website.js',
        ],
    },

    'installable': True,
    'application': False,
    'auto_install': False,
}
