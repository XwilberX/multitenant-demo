resource "cloudflare_record" "demo_wildcard" {
  count = var.lb_ip == "" ? 0 : 1

  zone_id = var.cloudflare_zone_id
  name    = "*.${var.subdomain_prefix}"
  type    = "A"
  content = var.lb_ip
  ttl     = 60
  proxied = false
  comment = "Wildcard del demo multi-tenant apuntando al LB del cluster"
}
