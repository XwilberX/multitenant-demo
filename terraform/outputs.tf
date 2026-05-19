output "cluster_id" {
  value = digitalocean_kubernetes_cluster.demo.id
}

output "cluster_endpoint" {
  value = digitalocean_kubernetes_cluster.demo.endpoint
}

output "kubeconfig_path" {
  value = local_sensitive_file.kubeconfig.filename
}

output "wildcard_fqdn" {
  value = "*.${var.subdomain_prefix}.${var.domain}"
}

output "next_steps" {
  value = <<-EOT

    ✓ Cluster DOKS provisionado.

    1) Configurar kubectl:
       export KUBECONFIG=$(realpath ${local_sensitive_file.kubeconfig.filename})
       kubectl get nodes

    2) Instalar ingress-nginx (manifests en cluster-ops/platform/).

    3) Esperar la EXTERNAL-IP del LB:
       kubectl -n ingress-nginx get svc ingress-nginx-controller -w

    4) Crear el wildcard DNS apuntando al LB:
       terraform apply -var="lb_ip=<EXTERNAL_IP>"

    Para destruir todo: terraform destroy
  EOT
}
