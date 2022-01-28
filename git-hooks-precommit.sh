# -*- coding: utf-8 -*

if [ -f ".gitleaks.toml" ]; then
  gitleaks protect --staged -v
else
  gitleaks protect --staged -v -c .git/hooks/gitleaks.toml
fi