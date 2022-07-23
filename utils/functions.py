# send an email 
from mailersend import emails


def send_email(recipient_email, recipient_name, uid, email_type):
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMjI1ODkyMTNjNzE3ZDdjZmVkZDIzOGJmMDRhOWE1OWEyNGVhMDU3NTkyODgyYTQ3NWU3MGJhZmJiMTQ1MTUwOGU0MTBlZmI5NGEwYmVjODciLCJpYXQiOjE2NTc0MTkzNTQuMDAyMDg0LCJuYmYiOjE2NTc0MTkzNTQuMDAyMDg4LCJleHAiOjQ4MTMwOTI5NTMuOTk4NTQ1LCJzdWIiOiIzMTgzMCIsInNjb3BlcyI6WyJlbWFpbF9mdWxsIiwiZG9tYWluc19mdWxsIiwiYWN0aXZpdHlfZnVsbCIsImFuYWx5dGljc19mdWxsIiwidG9rZW5zX2Z1bGwiLCJ3ZWJob29rc19mdWxsIiwidGVtcGxhdGVzX2Z1bGwiLCJzdXBwcmVzc2lvbnNfZnVsbCIsInNtc19mdWxsIl19.kD47M00709UMLKzjirrCzyFH90PlZ6RKvckfzMPatxLvOGU9rAF_F-GPxXYaBRb2T_h28RESz65veTaWXDS7Rh1HXs6TfPcIPq6Za4ezgYnf0iUEZYlbvPj60VtbFCQOgbJupBLz7_kJ3YWmvH4z_3wynTR6z_n1M3NHRhFsVyt62Qf220DzFFCxvKeZbpjvLvbOZTVc-_7b84MHgK0WTBgPuSO6lLiyoa_b5dxUNlLWz-JhkxxgAr6yHFdBtMhhbw5lMOz_fuQX7845baQtlDRaIG95GnA3jK6pAtgeljUZz1eHU8xME7rh7ZZjc4zZgwZc9yO1oez6acDEF9le4YZ9rhhiqkgQJ2m176PJJYxtVQnpx5UaXKx9DR6fV5tIPENTOp76EXZx5SuTxixkU4RNjRhMmaHX7eZXu2HYub4PLRHLVvzVrbaQPz9TboqlTeHnRNuJRQ0woIta47SMJZtkcnkZ5X-KRD2RVMCcNCeXh3fepHLmfSLUCKmPAdk20n44BEXMvZBsBxBlKJOY1B1Hd6nNLBK0tn93uFnKor_eE3KSIB7XZie2HznT_0K_WXAru2ExIbvxCEPzWnjTm-I6XmvVJai25jYQRyK726LF_MejPtJdkAnK6A4WMBwSW5amAaiUECEbiT-xXtPFn8wNW7oxH0zt47W9ImyG-KI"
    mailer = emails.NewEmail(api_key)

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "Hayak Invitations",
        "email": "info@hayaksa.com",
    }

    recipients = [
        {
            "name": f"{recipient_name}",
            "email": f"{recipient_email}",
        }
    ]


    variables = [
        {
            "email": f"{recipient_email}",
            # "uid": f"{uid}",
            # "recipient_name": f"recipient_name",
            "recipient_name": f"{recipient_name}",
            "substitutions": [
                {
                    "var": "foo",
                    "value": "bar",
                    "recipient_name": f"{recipient_name}",
                },
            ]
        }
    ]

    variables = [
        {
            "email": f"{recipient_email}",
            "substitutions": [
                {
                    "var": "name",
                    "value": f"{recipient_name}"
                }
            ]
        }
    ]


    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)  
    if email_type == "confirm":
        mailer.set_subject("Attendance Confirmation", mail_body)
        mailer.set_template("yzkq340e3r3gd796", mail_body)
    elif email_type == "accept":
        mailer.set_subject("Thanks for Confirmation", mail_body)
        mailer.set_template("z3m5jgro55ogdpyo", mail_body)
    elif email_type == "reject":
        mailer.set_subject("Thanks for Confirmation", mail_body)
        mailer.set_template("7dnvo4d9yrrg5r86", mail_body)

    mailer.set_simple_personalization(variables, mail_body)

    print(mailer.send(mail_body))