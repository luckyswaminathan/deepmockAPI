from __future__ import annotations

from pathlib import Path

import schemathesis
from hypothesis import HealthCheck, settings

from app.main import app


SPEC_PATH = Path(__file__).resolve().parents[2] / "openapi.yaml"
schema = schemathesis.from_path(str(SPEC_PATH))


@schema.parametrize()
@settings(max_examples=1, suppress_health_check=[HealthCheck.too_slow], deadline=None)
def test_contract(case):
    response = case.call_asgi(app)
    case.validate_response(response)
