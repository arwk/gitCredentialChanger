# gitCredentialChanger

## Why does this project exist?
This is just a small private project developed in lack of a proper solution to manage multiple developers using the same computer/server working in the same git repository.

## How do I use it?
The magic happens in credch.py. It's really just a small python script that reads the config file (`gitCredentials.json`) and interacts with the user.
To test it just rename the demo config file `gitCredentialsDemo.json` to `gitCredentials.json` and run the script.
```sh
python credch.py
```

### 'Installation'
To use the script in your existing repository rather than in this cloned one, some further steps are required:

The easiest way is to create an alias, so that the script can be called from any other directory:
```sh
alias gitCred='python /<Path>/<to>/<this>/<repository>/credch.py'
```

To make this alias 'permanent' add the previous command to your `~/.bashrc`.

### Configuration
Change to your repository where you want to control the git-credentials. Then call `credch.py` (If you followed the previous steps you can enter `gitCred`).
The script should exit with a message that it could not find a configuration file.
To create one, copy the demo file  `gitCredentialsDemo.json` to the toplevel directory of your repository and rename it to `gitCredentials.json`.
Then run `credch.py` again.

## Usage
```sh
credch.py -h
```
