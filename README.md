# Image-Comparator-Anaylsis
For pulling and analyzing data from the Image-Comparator app.

1. ```cp .env_sample .env``` - fill in your details

##
I set this up with pdm and if interested, here is how I make a venv and work:
```bash
pdm venv create --name image-comparator-analysis
pdm init # choose venv we created and tell it to import requirements.txt
./init_pdm.sh
#pdm install - should work after importing requirement.txt but it is not working now

# remove venv
pdm venv remove image-comparator-analysis

eval $(pdm venv activate image-comparator-analysis)

# Add packages
pdm add pandas
pdm add request
pdm add python-dotenv
pdm add matplotlib
pdm add networkx
pdm add scikit-learn
pdm remove sklearn


# "pycrumbs @ git+https://github.com/CPBridge/pycrumbs@40390ba92e127325f7b2ebef2bc97d521334ccb3",
# "smmap==5.0.0",
# "pandas>=1.5.3",
# "python-dotenv>=1.0.0",
# "requests>=2.28.2",
# "setuptools>=67.6.0",
# "choix>=0.3.5",
```

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