Daily Whiskers
==============

Emails you (or unsuspecting others) silly pictures of cats with made up names.

Names made up by secret algorithm and cats pics from reddit's /r/cats.

# Setup instructions #

## Deploy ##

On the server, create a new git repo.  Then, to allow pushing to a checked out branch, run

```
git config receive.denyCurrentBranch ignore
```

Symlink the post-receive hook.

```ln -s <repo_dir>/git-hooks/post-receive <repo_dir>/.git/hooks/post-receive```

This post-receive hook is set up to checkout the ```production``` branch.

## Run ##

Install the requirements with 

```pip install -r requirements.txt```

Run it, eg. with cron:

``` 0 9  *   *   *     python3 /home/pi/dailywhiskers/cats.py >> /home/pi/dailywhiskers/cats.log 2>&1```

## Testing ##

```python3 -m pytest test```
