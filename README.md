# autopkg-recipes

These are our autopkg-recipes.

Some of them use parent recipes from the following repos:
- _Privileges.munki_: https://github.com/autopkg/rtrouton-recipes/



## ⚠️ Deprecation notice

Zentral is winding down this repository. Going forward we will **only maintain
the recipes we use ourselves**:

- `DrataAgent`
- `osquery-extension`
- `Privileges`
- `santa`
- `santa-lite`
- `turbo`
- `zentral_enrollpkgs`

**All other recipes are deprecated and no longer maintained.** They now emit a
`DeprecationWarning` when run. They may stop working at any time and will not
receive further updates.

If you rely on one of the deprecated recipes and would like to take over its
maintenance, we'd be glad to help hand it off — please
[open an issue](https://github.com/autopkg/zentral-recipes/issues) to get in
touch.