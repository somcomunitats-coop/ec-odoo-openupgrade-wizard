update ir_mail_server set from_filter=(SELECT SUBSTRING(email FROM POSITION('@' IN email) + 1) from res_company where id=company_id) where company_id is not null;
