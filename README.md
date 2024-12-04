# PT_START_BOTICKВ
В git указать другую ссылка, т.к я ее поменял(в tg_playbook)

И если вы будете запускать, то на 2 машине надо изменить в моем боте.py функцию get_repl_logs, т.к я на ansible писал немного другое
```
def get_repl_logs(update: Update, context):
    connect_to_machine('192.168.0.109')
    stdin, stdout, stderr = client.exec_command('cat /tmp/postgresql.log | tail -20')
    update.message.reply_text(print_info(stdout,stderr))
```
