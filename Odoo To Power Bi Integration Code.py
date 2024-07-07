import xmlrpc.client
import pandas as pd

odoo_url = "<Replace with yours>"

db_name = "<Replace with yours>" 

username = "<Replace with yours>"

password = "<Replace with yours>"

odoo_model = "account.analytic.line"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))

uid = common.authenticate(db_name, username, password, {})

models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")

all_fields = models.execute_kw(db_name, uid, password, odoo_model, 'fields_get', [], {'attributes': ['string', 'type']})


fields_to_retrieve = list(all_fields.keys())

data_types = {field: field_info['type'] for field, field_info in all_fields.items()}


record_ids = models.execute_kw(db_name, uid, password, odoo_model, 'search', [[]])


records = models.execute_kw(db_name, uid, password, odoo_model, 'read', [record_ids], {'fields': fields_to_retrieve})


df = pd.DataFrame(records)


for field, data_type in data_types.items():
    if data_type == 'integer':
        df[field] = pd.to_numeric(df[field], errors='coerce', downcast='integer')
    elif data_type == 'float':
        df[field] = pd.to_numeric(df[field], errors='coerce', downcast='float')
    elif data_type == 'datetime':
        df[field] = pd.to_datetime(df[field], errors='coerce')

print("\n df==========", df)