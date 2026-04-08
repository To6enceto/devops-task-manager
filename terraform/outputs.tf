output "cluster_name" {
  description = "DOKS cluster name"
  value       = digitalocean_kubernetes_cluster.primary.name
}

output "cluster_endpoint" {
  description = "DOKS cluster endpoint"
  value       = digitalocean_kubernetes_cluster.primary.endpoint
  sensitive   = true
}

output "kubeconfig_command" {
  description = "Command to configure kubectl"
  value       = "doctl kubernetes cluster kubeconfig save ${digitalocean_kubernetes_cluster.primary.name}"
}

output "vpc_name" {
  description = "VPC name"
  value       = digitalocean_vpc.vpc.name
}
