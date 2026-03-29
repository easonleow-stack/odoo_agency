# -*- coding: utf-8 -*-
from odoo import models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_set_won(self):
        result = super().action_set_won()
        for lead in self:
            if lead.type != 'opportunity':
                continue
            # Only create a task if one doesn't already exist for this lead
            already_exists = self.env['agency.task'].search(
                [('crm_lead_id', '=', lead.id)], limit=1
            )
            if already_exists:
                continue
            task_name = ' — '.join(filter(None, [
                lead.partner_name or lead.contact_name,
                lead.name,
            ]))
            self.env['agency.task'].create({
                'name': task_name,
                'campaign': lead.name,
                'assignee_id': lead.user_id.id if lead.user_id else self.env.uid,
                'crm_lead_id': lead.id,
                'status': 'todo',
                'priority': 'medium',
            })
        return result
