# -*- coding: utf-8 -*

if [ "${SKIP}x" == "1x" ]; then
	echo "skip gitleask"
else
	if [ -f ".gitleaks.toml" ]; then
	  gitleaks protect --staged -v
	else
	  gitleaks protect --staged -v -c .git/hooks/gitleaks.toml
	fi
fi
