# Image-Comparator-Anaylsis
For pulling and analyzing data from the Image-Comparator app.

1. ```cp .env_sample .env``` - fill in your details
2. ```pip install requirements.txt```

## Git review:
Make your own branch
```bash
git branch new_branch
```

Checkout your branch
```bash
git checkout new_branch
```

Make changes and add
```bash
git add some_file
...other files
```

Commit changes for all edited files
```bash
git commit -m "a useful message"
```

Push changes to your new branch
```bash
 git push --set-upstream origin new_branch
```

Merge changes to main branch
```
git checkout main
git pull
git merge new_branch
```

Delete your branch
```
git push origin --delete new_branch
```