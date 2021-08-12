from odoo import models, fields
from odoo import api, tools

class PayAmount(models.Model):
	_name ='pay.amount'
	_auto = False
	_discription ='pay record'

	invoice_number = fields.Char(string='new_invoice_number')
	invoice_date = fields.Date(string='invoice_date')
	product_name = fields.Many2one('product.product', string='product_name')
	product_category = fields.Many2one('product.category', string='product_category')
	customer_name = fields.Many2one('res.partner', string='customer_name')
	quantity = fields.Float(string='quantity')
	price = fields.Float(string='price')
	untaxed_amount = fields.Integer(string='untaxed_amount')
	total = fields.Integer(string='total')

	@api.model
	def init(self):
		tools.drop_view_if_exists(self._cr, 'pay_amount')
		self._cr.execute("""CREATE OR REPLACE VIEW pay_amount AS (
			SELECT
				row_number() over() as id,
			 	am.name as invoice_number,
				am.date as invoice_date,
				aml.product_id as product_name,
				new.categ_id as product_category,
				aml.quantity,
				am.partner_id as customer_name,
				aml.price_unit as price,
				am.amount_untaxed as untaxed_amount,
				am.amount_total as total

				FROM
				   account_move as am
				LEFT JOIN
				   account_move_line as aml ON 'out invoice' LIKE am.type AND 'posted' LIKE am.state AND
				   aml.product_id is NOT NULL AND am.id = aml.move_id
				LEFT JOIN
				   product_template as pt ON pt.id = aml.move_id
				LEFT JOIN(
                    		SELECT
					pp.id,
					pp.product_tmpl_id,
					pt.categ_id
                    		FROM
				    product_product as pp
				LEFT JOIN
				    product_template as pt ON pt.id = pp.product_tmpl_id)
				    as new ON new.id = aml.product_id

	)""")

