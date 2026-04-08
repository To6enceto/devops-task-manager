# --- DOKS Cluster ---
data "digitalocean_kubernetes_versions" "available" {
  version_prefix = "${var.k8s_version}."
}

resource "digitalocean_kubernetes_cluster" "primary" {
  name     = var.cluster_name
  region   = var.region
  version  = data.digitalocean_kubernetes_versions.available.latest_version
  vpc_uuid = digitalocean_vpc.vpc.id

  node_pool {
    name       = "${var.cluster_name}-pool"
    size       = var.node_size
    auto_scale = true
    min_nodes  = var.min_node_count
    max_nodes  = var.max_node_count

    labels = {
      environment = "production"
      managed-by  = "terraform"
    }
  }
}
