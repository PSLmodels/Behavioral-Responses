RELEASING BEHAVIORAL-RESPONSES CONDA PACKAGES
=============================================

```
--> on branch X-Y-Z, edit RELEASES.md to finalize X.Y.Z info

--> merge master branch into X-Y-Z branch

--> run `make pytest-all`

--> check docs/index.html for any needed edits

--> commit X-Y-Z branch and push to origin

--> merge X-Y-Z branch into master branch on GitHub

--> on local master branch, ./gitsync

--> create release X.Y.Z on GitHub using master branch

--> create packages with `pbrelease Behavioral-Responses behresp X.Y.Z` command

--> email policybrains-modelers list about the new release and packages
```
