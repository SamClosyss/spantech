from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def _get_relay_domains(self):
        """Fetch relay domains from system parameter (comma-separated)."""
        param_val = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("helpdesk.relay_domains", default="")
        )
        return [d.strip().lower() for d in param_val.split(",") if d.strip()]

    def _is_relay_address(self, email):
        """Check if an email belongs to a configured relay domain."""
        relay_domains = self._get_relay_domains()
        return any(domain in email for domain in relay_domains)

    def _loop_guard_clean_relay(self, message, message_dict):
        """
        Detect if the same display name already exists with a real email
        in this ticket, and block relay addresses from creating loops.
        """
        email_from = (message_dict.get("email_from") or "").lower()
        display_name = (message_dict.get("from") or "").split("<")[0].strip().lower()

        # Case: relay address detected
        if self._is_relay_address(email_from):
            # Look for a real partner with the same display name in this ticket
            real_partner = (
                self.env["res.partner"]
                .sudo()
                .search(
                    [
                        ("id", "in", self.message_partner_ids.ids),
                        ("name", "ilike", display_name),
                        ("email", "!=", False),
                    ],
                    limit=1,
                )
            )

            if real_partner and not self._is_relay_address(real_partner.email.lower()):
                # Relay detected → clean it up
                relay_partner = (
                    self.env["res.partner"]
                    .sudo()
                    .search([("email", "=", email_from)], limit=1)
                )
                if relay_partner:
                    # Remove from followers uncomment if you also want to remove from followers
                    # self.message_follower_ids = (
                    #     self.message_follower_ids - relay_partner
                    # )

                    if message:
                        # Remove from notifications
                        message.notified_partner_ids = (
                            message.notified_partner_ids - relay_partner
                        )
                        message.notification_ids.filtered(
                            lambda n: n.res_partner_id == relay_partner
                        ).unlink()

                return True  # stop further processing

        return False


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):
        # Apply only to helpdesk tickets
        if model == "helpdesk.ticket" and thread_id:
            ticket = self.env[model].browse(thread_id)
            if ticket and ticket._loop_guard_clean_relay(None, message_dict):
                return []  # block relay message completely

        return super().message_route(
            message, message_dict, model, thread_id, custom_values
        )
