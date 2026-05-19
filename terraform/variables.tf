variable "do_token" {
  description = "DigitalOcean API token (scope: write)"
  type        = string
  sensitive   = true
}

variable "cloudflare_token" {
  description = "Cloudflare API token con permisos Zone:Read y DNS:Edit"
  type        = string
  sensitive   = true
}

variable "cloudflare_zone_id" {
  description = "Zone ID de la zona en Cloudflare (panel: Overview → API → Zone ID)"
  type        = string
}

variable "domain" {
  description = "Dominio base para el demo"
  type        = string
  default     = "dotinfra.tech"
}

variable "subdomain_prefix" {
  description = "Subdominio bajo el cual viven los tenants (resultado: *.<prefix>.<domain>)"
  type        = string
  default     = "demo"
}

variable "region" {
  description = "Región de Digital Ocean (nyc1, nyc3, sfo3, ams3, fra1, etc.)"
  type        = string
  default     = "nyc1"
}

variable "node_size" {
  description = "Slug del tamaño de cada nodo (https://slugs.do-api.dev/)"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "node_count" {
  description = "Número de nodos worker en el pool"
  type        = number
  default     = 2
}

variable "lb_ip" {
  description = "IP del LoadBalancer creado por ingress-nginx. Vacío en la primera pasada; se llena después de instalar el ingress."
  type        = string
  default     = ""
}
