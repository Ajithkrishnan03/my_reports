from odoo import models, fields
from odoo import api, tools

class PayAmount(models.Model):
	_name ='pay.amount'
	_auto = False
	_discription ='pay record'

	so_number= fields.Many2one('sale.order', string='Sale Order Number')
	reference = fields.Char(string='Delivery_Order_Number')
	product_id = fields.Many2one('product.product',string='Product_Name')
	product_qty = fields.Float(string='Done_Quantity')
	name = fields.Char(string='Invoice_Number')
	product_uom_qty = fields.Float(string='Demand_Quantity')
	quantity = fields.Float(string='Invoiced_Quantity')

	@api.model
	def init(self):
		tools.drop_view_if_exists(self._cr, 'pay_amount')
		self._cr.execute("""CREATE OR REPLACE VIEW pay_amount AS (
		SELECT
				row_number() over(ORDER BY so.id) as id,
				so.id as so_number,
				sol.product_id,
				sol.product_uom_qty,
				sm.reference,
				sm.product_qty,
				am.name,
				aml.quantity
		FROM
			sale_order as so
		LEFT JOIN
			sale_order_line as sol ON sol.order_id = so.id
		LEFT JOIN
			stock_move as sm ON sm.sale_line_id = sol.id
		LEFT JOIN
			x_account_move_stock_picking_rel as xam ON xam.stock_picking_id = sm.picking_id
	    LEFT JOIN
			account_move as am ON am.id = xam.account_move_id
		LEFT JOIN
			account_move_line as aml ON aml.move_id = am.id AND sol.product_id = aml.product_id
		WHERE
			sm.state='done'
	)""")
