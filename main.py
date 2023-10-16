from text_send import TextSender

# TODO Pull recipes from recipe API (or from ChatGPT)
# TODO Compile recipes into SMS message to send to user
# TODO Connect to Windows Task Manager to automate process every Friday at noon

body = "This is a separate text of the body system."

texter = TextSender()
texter.send_text(body=body)
