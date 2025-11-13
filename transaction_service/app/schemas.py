from . import ma
from marshmallow import fields, validate

class TransactionSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(["debit", "credit"]))
    amount = fields.Float(required=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
