# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_count = fields.Integer(
        'Merged Task Count', compute='_compute_get_task_count')

    child_merge_task_id = fields.Many2one(
        'project.task', string="Merge Task one")

    child_merge_task_ids = fields.One2many(
        'project.task', 'child_merge_task_id', string="Merge Task")

    def create_single_task(self):
        message = ''
        first_task_flag = True
        is_project_flag = True
        first_task = ' '
        second_task = ' '
        task_vals = {}
        timesheet_list = []
        task_name = []
        tag_ids = []
        date_deadline = []
        description = []
        planned_hours = []

        for rec in self:
            if first_task_flag:
                first_task = rec
                first_task_flag = False

            if first_task.project_id:
                if rec.project_id and first_task.project_id and rec.project_id.id != first_task.project_id.id:
                    raise ValidationError(_("Project Must be Same !"))
                task_vals.update({'project_id': first_task.project_id.id, })

            elif rec.project_id and is_project_flag:
                second_task = rec
                is_project_flag = False
                task_vals.update({'project_id': second_task.project_id.id, })

            if second_task and not is_project_flag:
                if rec.project_id and second_task.project_id and rec.project_id.id != second_task.project_id.id:
                    raise ValidationError(_("Project Must be Same !"))

            if rec.name:
                task_name.append(rec.name),
                task_vals.update({'name': ", ".join(task_name)})

            if rec.timesheet_ids:
                for time_sheet in rec.timesheet_ids:
                    timesheet_list.append(time_sheet.id)
                    task_vals.update(
                        {'timesheet_ids': [(6, 0, timesheet_list)]})

            if rec.tag_ids.ids:
                tag_ids.extend(rec.tag_ids.ids)
                task_vals.update({'tag_ids': [(6, 0, tag_ids)]})

            if rec.date_deadline:
                date_deadline.append(rec.date_deadline)
                task_vals.update({'date_deadline': max(date_deadline)})

            if rec.description:
                description.append(rec.description)
                task_vals.update({'description': "\n".join(description)})

            if rec.planned_hours:
                planned_hours.append(rec.planned_hours)
                task_vals.update({'planned_hours': max(planned_hours), })

            if len(self.ids) < 2:
                raise ValidationError(
                    _("Please Select at least two Tasks for perform merge operation."))
            else:
                task_vals.update({'child_merge_task_ids': [(6, 0, self.ids)]})

            rec.active = False

        demo = self.env['project.task'].with_context({
            'allow_timesheets': True,
        }).create(task_vals)

        message += " This Task is created from Merging Following tasks : " + \
            '<b>'+", &nbsp;".join(task_name) + '</b>'

        self.env['mail.message'].create({
            'partner_ids': [(6, 0, demo.user_ids.partner_id.ids)],
            'model': 'project.task',
            'res_id': demo.id,
            'author_id': demo.env.user.partner_id.id,
            'body': message or False,
            'message_type': 'comment',
        })

        for archive_task in demo.child_merge_task_ids:
            archive_task.active = False

    def action_merged_tasks(self):

        archive_lines = self.env['project.task'].sudo().search(
            [('active', '=', False), ('child_merge_task_id', '=', self.id)])

        return {
            'name': 'Merged Tasks',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('id', 'in', archive_lines.ids), ('active', '=', False)],
            'target': 'current',
        }

    def _compute_get_task_count(self):
        if self:
            archive_lines = self.env['project.task'].sudo().search(
                [('active', '=', False), ('child_merge_task_id', '=', self.id)])

            self.task_count = len(archive_lines)
