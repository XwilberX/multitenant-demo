# multitenant-demo

Demo técnico de arquitectura multi-tenant **bridge model** (pool en cómputo + silo selectivo en datos). Una sola imagen Docker sirve a N tenants con configs distintos. Onboarding de tenant = un PR.

Este repo acompaña la propuesta `PLAN-MULTITENANT-COMERCIALIZACION.md` y valida el modelo en infraestructura real antes de aplicarlo a productos productivos.

---

## Las 3 capas de customización que demuestra el demo

| Capa | Mecanismo | Ejemplo en este repo |
|------|-----------|----------------------|
| **1. Configuración** | YAML por tenant montado en `/etc/tenant/config.yml` | Logo, color primario, nombre del tenant |
| **2. Strategy / Adapter** | Interfaz común con N implementaciones | `PaymentProcessor` con `StripeProcessor` y `MercadoPagoProcessor` |
| **3. Feature flags** | Booleanos en el config del tenant | `enable_advanced_dashboard: true/false` |

## Tenants del demo

| Tenant | URL local | Color | Payment | Dashboard avanzado |
|--------|-----------|-------|---------|--------------------|
| `alpha` | http://localhost:13001 | Azul | Stripe | ✓ |
| `beta`  | http://localhost:13002 | Rojo  | MercadoPago | ✗ |

Ambos corren la **misma imagen** de backend y la **misma imagen** de frontend. Las diferencias provienen exclusivamente del YAML montado.

---

## Día 1 — Levantar el demo localmente

Requisitos: Docker + Docker Compose.

```bash
docker compose up --build -d
```

Abrir en el navegador:

- http://localhost:13001 → branding azul, Stripe, dashboard visible.
- http://localhost:13002 → branding rojo, MercadoPago, sin dashboard.

Probar el adapter pattern con un checkout:

```bash
curl -s -X POST http://localhost:18001/api/checkout \
  -H 'Content-Type: application/json' \
  -d '{"product_id": 2}' | jq

curl -s -X POST http://localhost:18002/api/checkout \
  -H 'Content-Type: application/json' \
  -d '{"product_id": 2}' | jq
```

El primero devuelve `"provider": "Stripe"`, el segundo `"provider": "MercadoPago"`. Mismo binario.

Verificar que es **la misma imagen** para ambos tenants:

```bash
docker inspect demo-backend-alpha demo-backend-beta \
  --format '{{.Image}}'
```

Ambos SHAs son idénticos.

---

## Agregar un tenant nuevo (modelo "onboarding = PR")

1. Crear `tenants/<slug>.yml` con la estructura de `alpha.yml`.
2. Agregar los servicios `backend-<slug>` y `frontend-<slug>` al `docker-compose.yml`.
3. `docker compose up -d <nuevo-servicio>`.

En el modelo K8s (días 2-5) este paso se reduce a: agregar `tenants/<slug>.yaml` al repo y ArgoCD sincroniza automáticamente vía ApplicationSet. **No se toca el cluster.**

---

## Roadmap

- **Día 1 — ✓ App local.** docker compose con alpha y beta. *(este día)*
- **Día 2 — Cluster + plataforma.** Provisionar DOKS con Terraform, instalar ArgoCD, nginx-ingress, cert-manager + Let's Encrypt. DNS wildcard `*.demo.dotinfra.tech`.
- **Día 3 — CI/CD + ApplicationSet.** GitHub Actions build & push a GHCR. Estructura `cluster-ops/` con Kustomize base + ApplicationSet apuntando a `tenants/*.yaml`. Deploy de alpha.
- **Día 4 — Segundo tenant + aislamiento.** Deploy de beta. NetworkPolicy default-deny entre namespaces. Verificación cross-tenant fallida (esperado).
- **Día 5 — Pulir + onboarding en vivo.** PR de `tenants/charlie.yaml` en vivo, ArgoCD sync, tenant arriba en <5 min. Video de respaldo.

---

## Estructura del repo

```
multitenant-demo/
├── app/
│   ├── backend/         # FastAPI — misma imagen para todos los tenants
│   │   ├── main.py
│   │   ├── config.py    # Capa 1
│   │   ├── payment.py   # Capa 2 (strategy)
│   │   └── Dockerfile
│   └── frontend/        # React + Vite + nginx
│       ├── src/
│       ├── nginx.conf.template
│       └── Dockerfile
├── tenants/             # 1 YAML por tenant — esto es lo que cambia el PR
│   ├── alpha.yml
│   └── beta.yml
├── cluster-ops/         # ArgoCD + manifests K8s (días 2-5)
├── terraform/           # DOKS + Cloudflare DNS (día 2)
├── .github/workflows/   # CI/CD (día 3)
└── docker-compose.yml   # demo local del día 1
```
