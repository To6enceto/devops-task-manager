variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "DigitalOcean region slug"
  type        = string
  default     = "ams3"
}

variable "cluster_name" {
  description = "DOKS cluster name"
  type        = string
  default     = "task-manager-cluster"
}

variable "k8s_version" {
  description = "Kubernetes version prefix (e.g. '1.31' — latest patch will be used)"
  type        = string
  default     = "1.31"
}

variable "node_size" {
  description = "DigitalOcean Droplet size for nodes"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "min_node_count" {
  description = "Minimum number of nodes for autoscaling"
  type        = number
  default     = 1
}

variable "max_node_count" {
  description = "Maximum number of nodes for autoscaling"
  type        = number
  default     = 3
}
