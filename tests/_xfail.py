__all__ = ["xfail_param"]

from typing import Any

import pytest


def xfail_param(*param: Any, reason: str = "") -> pytest.param:
    return pytest.param(*param, marks=pytest.mark.xfail(reason=reason))
