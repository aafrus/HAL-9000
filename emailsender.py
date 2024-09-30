import mailslurp_client
from smtplib import SMTP

def send_email(subject, content):
    # create a mailslurp configuration
    configuration = mailslurp_client.Configuration()
    configuration.api_key['x-api-key'] = "c5e0afb6e43606767bbff84fcf94c42784cdb757ef4b30c4edd359aefb7ad49e"

    with mailslurp_client.ApiClient(configuration) as api_client:
        # create an inbox
        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        options = mailslurp_client.CreateInboxDto()
        options.name = "Monitor Alert Inbox"
        options.inbox_type = "SMTP_INBOX"
        inbox = inbox_controller.create_inbox_with_options(options)
        print("Email address is: " + inbox.email_address)

        access_details = inbox_controller.get_imap_smtp_access(inbox_id=inbox.id)
        print(access_details)

        # send an email using the SMTP client
        with SMTP(
            host=access_details.secure_smtp_server_host,
            port=access_details.secure_smtp_server_port,
        ) as smtp:
            msg = f"Subject: {subject}\r\n\r\n{content}"
            smtp.login(
                user=access_details.secure_smtp_username,
                password=access_details.secure_smtp_password,
            )
            smtp.sendmail(
                from_addr=inbox.email_address,
                to_addrs=[inbox.email_address],  # You can change this to the actual recipient
                msg=msg,
            )
            smtp.quit()
            print("Sent the email")