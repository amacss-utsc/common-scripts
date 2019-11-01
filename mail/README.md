# Domain.com Mail Automator
This script will make domain.com mailboxes and mail forwarding match w/e you have in the `mailboxes.json` file

# Setup
Fill in the template `*.bkp` files by removing the `.bkp` and then replacing the placeholder information

# Usage
The script has a `dry-run` mode

```sh
$ python main.py mailboxes.json -d
```

If you're satisfied with what it's going on then run it for real
```sh
$ python main.py mailboxes.json
```
