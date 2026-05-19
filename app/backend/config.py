import os
from functools import lru_cache

import yaml
from pydantic import BaseModel


class Branding(BaseModel):
    name: str
    color: str
    logo_text: str


class TenantConfig(BaseModel):
    slug: str
    branding: Branding
    payment_provider: str
    features: dict[str, bool]


@lru_cache(maxsize=1)
def load_tenant_config() -> TenantConfig:
    path = os.environ.get("TENANT_CONFIG_PATH", "/etc/tenant/config.yml")
    with open(path) as f:
        data = yaml.safe_load(f)
    return TenantConfig(**data)
