# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_product_variant_count_all(self):
        for rec in self:
            rec.product_variant_count_all = (
                self.with_context(active_test=False)
                .env["product.product"]
                .search_count([("product_tmpl_id", "=", rec.id)])
            )

    product_variant_count_all = fields.Integer(
        "Inactive variants", compute=_compute_product_variant_count_all
    )

    def _create_variant_ids(self):
        return super(
            ProductTemplate, self.with_context(no_reactivate=True)
        )._create_variant_ids()

    @api.depends("product_variant_ids.active")
    def _compute_product_variant_count(self):
        return super()._compute_product_variant_count()
