Daily Whiskers
==============

Emails you (or unsuspecting others) silly pictures of cats with made up names.

Names made up by ~~secret~~ algorithm and cats pics from reddit's /r/cats.

# Setup instructions #

## Requirements ##

The emailing is done with [mailgun](http://www.mailgun.com/), so you'll need an account.  Accounts are free though :) 

## Setup ##

Update ```config.json``` with your mailgun info and a list of recipients.

## Run ##

Install the requirements with 

```pip install -r requirements.txt```

Run it, eg. with cron:

``` 0 9  *   *   *     python3 /home/pi/dailywhiskers/cats.py >> /home/pi/dailywhiskers/cats.log 2>&1```

## Testing ##

```python3 -m pytest test```

## Deploy ##

On the server, create a new git repo, add add this as a remote.  Then, to allow pushing to a checked out branch, run
```git config receive.denyCurrentBranch ignore``` from your server.  

Symlink the post-receive hook.

```ln -s <repo_dir>/git-hooks/post-receive <repo_dir>/.git/hooks/post-receive```

This post-receive hook is set up to checkout the ```production``` branch whenever it is pushed to.
