import logging

_logger = logging.getLogger(__name__)
_logger.info("02-post-migration-custom_test.py : Begin of script ...")

env = env  # noqa: F821

env["res.partner"].create({"name": "Post Script 2 - Partner #1"})

_logger.info("02-post-migration-custom_test.py : End of script.")

env.cr.commit()
