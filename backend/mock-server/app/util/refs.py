from __future__ import annotations

import re

# Matches local schema refs of the form #/components/schemas/Name
REF_RE = re.compile(r"^#/components/schemas/(?P<name>[^/]+)$")


