# --- VPC ---
resource "digitalocean_vpc" "vpc" {
  name     = "${var.cluster_name}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"
}
