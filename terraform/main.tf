data "digitalocean_kubernetes_versions" "current" {}

resource "digitalocean_kubernetes_cluster" "demo" {
  name    = "multitenant-demo"
  region  = var.region
  version = data.digitalocean_kubernetes_versions.current.latest_version

  node_pool {
    name       = "worker-pool"
    size       = var.node_size
    node_count = var.node_count
    tags       = ["multitenant-demo"]
  }

  tags = ["multitenant-demo"]
}

resource "local_sensitive_file" "kubeconfig" {
  content         = digitalocean_kubernetes_cluster.demo.kube_config[0].raw_config
  filename        = "${path.module}/../kubeconfig"
  file_permission = "0600"
}
