# Terraform Helm release for kube-prometheus-stack
resource "helm_release" "kube_prometheus_stack" {
  name             = "kube-prometheus-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  version          = "65.8.1"
  namespace        = "monitoring"
  create_namespace = true
  timeout          = 600

  values = [file("${path.module}/../monitoring/prometheus/values.yaml")]

  depends_on = [digitalocean_kubernetes_cluster.primary]
}

# Loki
resource "helm_release" "loki" {
  name             = "loki"
  repository       = "https://grafana.github.io/helm-charts"
  chart            = "loki-stack"
  version          = "2.10.2"
  namespace        = "monitoring"
  create_namespace = false
  timeout          = 600

  values = [file("${path.module}/../monitoring/loki/values.yaml")]

  depends_on = [helm_release.kube_prometheus_stack]
}
