import logging

_logger = logging.getLogger(__name__)
_logger.info("Executing post-migration.py script ...")

env = env  # noqa: F821

# Write custom script here

taxes = env["account.tax"].search([])
for tax in taxes:
    tax.write({"country_id": env.ref("base.es").id})

taxes_g = env["account.tax.group"].search([])
for tax_g in taxes_g:
    tax_g.write({"country_id": env.ref("base.es").id})

try:
    companies = env["res.company"].search([])
except Exception as e:
    _logger.error(f"search res.company: {e}")

_logger.info(f"Check companies : {len(companies)}")

chart_template_id = (
    env["account.chart.template"].search([("name", "=", "PGCE PYMEs 2008")])[0].id
)
fields = env["ir.model.fields"].search(
    [
        ("model", "=", "account.account.template"),
        ("name", "in", ["code", "user_type_id"]),
    ]
)

for company in companies:
    try:
        wizard = (
            env["wizard.update.charts.accounts"]
            .with_context(default_company_id=company.id)
            .create({"chart_template_id": chart_template_id})
        )
        for f in fields:
            wizard.account_field_ids = [(3, f.id)]
        wizard.action_find_records()  # code = False  user_type_id = False
        wizard.action_update_records()
        _logger.info(
            f"Update chart templates for companie : {company.id} - {company.name}"
        )
    except Exception as e:
        _logger.error(
            f"Error update chart templates {company.id} - {company.name}: {e}"
        )

# Confirma los cambios
env.cr.commit()
_logger.info("Update chart templates of all companies")

env.cr.commit()
