from . import ma
from marshmallow import fields, validate

class ReportSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    transaction_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    full_name = fields.Str()
    email = fields.Email()
    type = fields.Str(validate=validate.OneOf(["debit", "credit"]))
    amount = fields.Float()
    status = fields.Str()
    balance_after = fields.Float()
    transaction_date = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)


class ReportSummarySchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    full_name = fields.Str()
    email = fields.Email()
    total_transactions = fields.Int()
    total_credit = fields.Float()
    total_debit = fields.Float()
    current_balance = fields.Float()
    last_transaction_date = fields.DateTime()
    updated_at = fields.DateTime()


report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)
report_summary_schema = ReportSummarySchema()