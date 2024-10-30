import logging

_logger = logging.getLogger(__name__)
_logger.info("01-post-migration-custom_test.py : Begin of script ...")

env = env  # noqa: F821

for i in range(0, 10):
    partner_name = "Post Script 1 - Partner #%d" % (i)
    _logger.info("Create Partner %s" % partner_name)
    env["res.partner"].create({"name": partner_name})

_logger.info("01-post-migration-custom_test.py : End of script.")

env.cr.commit()
