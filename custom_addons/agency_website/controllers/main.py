# -*- coding: utf-8 -*-
"""
Ads On Marketing — Website Controllers
Public-facing pages that integrate with agency.task and CRM models.
"""
from odoo import http
from odoo.http import request
from datetime import date


class AgencyWebsite(http.Controller):

    # ── Homepage ──────────────────────────────────────────────────
    @http.route('/', type='http', auth='public', website=True)
    def homepage(self, **kw):
        Task = request.env['agency.task'].sudo()

        # Stats for the counter section
        total_tasks = Task.search_count([])
        done_tasks = Task.search_count([('status', '=', 'done')])
        active_campaigns = len(Task.read_group(
            [('status', '!=', 'done')], ['campaign'], ['campaign']
        ))
        teams_count = len(Task.read_group([], ['team'], ['team']))

        # Featured campaigns (latest active ones with progress)
        featured = Task.search([
            ('status', 'in', ['inprogress', 'review']),
            ('campaign', '!=', False),
        ], order='deadline asc', limit=6)

        values = {
            'total_tasks': total_tasks,
            'done_tasks': done_tasks,
            'active_campaigns': active_campaigns,
            'teams_count': teams_count,
            'featured_tasks': featured,
        }
        return request.render('agency_website.homepage', values)

    # ── Services ──────────────────────────────────────────────────
    @http.route('/services', type='http', auth='public', website=True)
    def services(self, **kw):
        return request.render('agency_website.services_page', {})

    # ── Portfolio / Projects ──────────────────────────────────────
    @http.route('/portfolio', type='http', auth='public', website=True)
    def portfolio(self, team=None, **kw):
        Task = request.env['agency.task'].sudo()
        domain = [('campaign', '!=', False)]
        if team:
            domain.append(('team', '=', team))

        # Group tasks by campaign
        tasks = Task.search(domain, order='deadline desc', limit=30)
        campaigns = {}
        for t in tasks:
            key = t.campaign or 'General'
            if key not in campaigns:
                campaigns[key] = {
                    'name': key,
                    'tasks': [],
                    'teams': set(),
                    'progress': 0,
                    'total': 0,
                    'done': 0,
                }
            campaigns[key]['tasks'].append(t)
            campaigns[key]['teams'].add(t.team)
            campaigns[key]['total'] += 1
            if t.status == 'done':
                campaigns[key]['done'] += 1

        for c in campaigns.values():
            c['progress'] = int((c['done'] / c['total'] * 100) if c['total'] else 0)
            c['teams'] = list(c['teams'])

        team_options = [
            ('creative', 'Creative'),
            ('media', 'Media Buying'),
            ('social', 'Social Media'),
            ('strategy', 'Strategy'),
            ('client', 'Client Services'),
            ('field', 'Field Team'),
        ]

        values = {
            'campaigns': campaigns,
            'team_options': team_options,
            'current_team': team or '',
        }
        return request.render('agency_website.portfolio_page', values)

    # ── About ─────────────────────────────────────────────────────
    @http.route('/about', type='http', auth='public', website=True)
    def about(self, **kw):
        return request.render('agency_website.about_page', {})

    # ── Contact — renders form & creates CRM lead ─────────────────
    @http.route('/contact-us', type='http', auth='public', website=True)
    def contact(self, **kw):
        return request.render('agency_website.contact_page', {
            'success': kw.get('success', False),
        })

    @http.route('/contact-us/submit', type='http', auth='public',
                website=True, methods=['POST'], csrf=True)
    def contact_submit(self, **kw):
        """Create a CRM lead from the contact form."""
        vals = {
            'name': kw.get('subject', 'Website Enquiry'),
            'partner_name': kw.get('name', ''),
            'email_from': kw.get('email', ''),
            'phone': kw.get('phone', ''),
            'description': kw.get('message', ''),
            'type': 'lead',
        }
        request.env['crm.lead'].sudo().create(vals)
        return request.redirect('/contact-us?success=1')

    # ── Dashboard (public stats) ──────────────────────────────────
    @http.route('/dashboard', type='http', auth='public', website=True)
    def dashboard(self, **kw):
        Task = request.env['agency.task'].sudo()

        # Status distribution
        status_data = Task.read_group([], ['status'], ['status'])
        status_map = {s['status']: s['status_count'] for s in status_data}

        # Team distribution
        team_data = Task.read_group([], ['team'], ['team'])

        # Priority distribution
        priority_data = Task.read_group([], ['priority'], ['priority'])

        # Overdue tasks
        overdue_count = Task.search_count([
            ('deadline', '<', date.today().strftime('%Y-%m-%d')),
            ('status', 'not in', ['done']),
        ])

        values = {
            'status_map': status_map,
            'team_data': team_data,
            'priority_data': priority_data,
            'overdue_count': overdue_count,
            'total_tasks': Task.search_count([]),
            'done_tasks': Task.search_count([('status', '=', 'done')]),
        }
        return request.render('agency_website.dashboard_page', values)
