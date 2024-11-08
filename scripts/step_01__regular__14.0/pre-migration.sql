update ir_cron set active = False;
update ir_mail_server set smtp_host = 'fake_' || smtp_host where 1=1;
update fetchmail_server set active = False;
update res_partner set email = 'fake_' || email where not email is null;
update res_company set name = '[PRE-PROD] ' || name, email = 'fake_' || email where 1=1;
update res_partner set name = '[PRE-PROD] ' || name, lastname = '[PRE-PROD] ' || lastname, commercial_company_name = '[PRE-PROD] ' || commercial_company_name, display_name = '[PRE-PROD] ' || display_name where id in (select partner_id from res_company where 1=1);