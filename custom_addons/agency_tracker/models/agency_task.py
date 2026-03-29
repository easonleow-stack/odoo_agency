# -*- coding: utf-8 -*-
"""
Agency Task Model — Ads On Marketing Sdn Bhd
Mirrors the AgencyBoard HTML tracker with full Odoo backend persistence,
chatter (message log), and CRM lead linkage.
"""
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class AgencyTask(models.Model):
    _name = 'agency.task'
    _description = 'Agency Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']   # Adds chatter + activity log
    _order = 'priority desc, deadline asc, id desc'

    # ── Core Fields ────────────────────────────────────────────────
    name = fields.Char(
        string='Task',
        required=True,
        tracking=True,
        help="Short description of the task"
    )

    description = fields.Html(
        string='Details / Notes',
        help="Full task brief, links, attachments context"
    )

    campaign = fields.Char(
        string='Campaign / Project',
        tracking=True,
        help="Campaign name (e.g. Hari Raya 2026, KL Property Expo)"
    )

    # ── Assignment ─────────────────────────────────────────────────
    assignee_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        default=lambda self: self.env.user,
        tracking=True,
    )

    reviewer_id = fields.Many2one(
        'res.users',
        string='Reviewer',
        tracking=True,
    )

    team = fields.Selection([
        ('creative',  'Creative'),
        ('media',     'Media Buying'),
        ('social',    'Social Media'),
        ('strategy',  'Strategy'),
        ('client',    'Client Services'),
        ('field',     'Field Team'),
    ], string='Team', tracking=True, default='creative')

    # ── Status & Priority ──────────────────────────────────────────
    status = fields.Selection([
        ('todo',       'To Do'),
        ('inprogress', 'In Progress'),
        ('review',     'Review'),
        ('done',       'Done'),
        ('stuck',      'Stuck'),
    ], string='Status', default='todo', tracking=True,
        group_expand='_group_by_status')

    priority = fields.Selection([
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='medium', tracking=True)

    # ── Dates ──────────────────────────────────────────────────────
    deadline = fields.Date(string='Due Date', tracking=True)

    date_started = fields.Date(string='Start Date', default=fields.Date.today)

    date_closed = fields.Datetime(string='Closed On', readonly=True)

    # ── Progress ───────────────────────────────────────────────────
    progress = fields.Integer(
        string='Progress (%)',
        default=0,
        help="0–100 progress percentage"
    )

    # ── CRM Integration ────────────────────────────────────────────
    crm_lead_id = fields.Many2one(
        'crm.lead',
        string='Linked Deal / Lead',
        help="Link this task to a CRM opportunity or lead"
    )

    client_name = fields.Char(
        string='Client Name',
        related='crm_lead_id.partner_name',
        store=True, readonly=True
    )

    # ── Computed Fields ────────────────────────────────────────────
    is_overdue = fields.Boolean(
        string='Overdue',
        compute='_compute_is_overdue',
        store=False
    )

    color = fields.Integer(
        string='Kanban Color',
        compute='_compute_color',
        store=False
    )

    # ── Active / Archive ───────────────────────────────────────────
    active = fields.Boolean(default=True)

    # ── Methods ────────────────────────────────────────────────────
    @api.depends('deadline', 'status')
    def _compute_is_overdue(self):
        today = date.today()
        for rec in self:
            rec.is_overdue = (
                bool(rec.deadline) and
                rec.deadline < today and
                rec.status not in ('done',)
            )

    @api.depends('priority', 'status')
    def _compute_color(self):
        color_map = {
            'urgent': 1,    # Red
            'high':   2,    # Orange
            'medium': 4,    # Blue
            'low':    10,   # Green
        }
        for rec in self:
            if rec.status == 'stuck':
                rec.color = 1
            elif rec.status == 'done':
                rec.color = 10
            else:
                rec.color = color_map.get(rec.priority, 4)

    @api.constrains('progress')
    def _check_progress(self):
        for rec in self:
            if not (0 <= rec.progress <= 100):
                raise ValidationError("Progress must be between 0 and 100.")

    @api.onchange('status')
    def _onchange_status_done(self):
        """Auto-set progress to 100 when marked Done."""
        if self.status == 'done':
            self.progress = 100

    @api.model
    def _group_by_status(self, present_ids, domain, **kwargs):
        """Ensures all Kanban columns show even when empty."""
        return [
            ('todo',       'To Do'),
            ('inprogress', 'In Progress'),
            ('review',     'Review'),
            ('done',       'Done'),
            ('stuck',      'Stuck'),
        ]

    def action_mark_done(self):
        self.write({'status': 'done', 'progress': 100,
                    'date_closed': fields.Datetime.now()})

    def action_mark_inprogress(self):
        self.write({'status': 'inprogress'})


class AgencyTaskTag(models.Model):
    """Optional tags for tasks (e.g. 'Urgent Client', 'Billboards', 'KOL')."""
    _name = 'agency.task.tag'
    _description = 'Agency Task Tag'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color Index')
    task_ids = fields.Many2many('agency.task', string='Tasks')
