provider "helm" {
  kubernetes {
    host                   = digitalocean_kubernetes_cluster.primary.endpoint
    cluster_ca_certificate = base64decode(digitalocean_kubernetes_cluster.primary.kube_config[0].cluster_ca_certificate)
    token                  = digitalocean_kubernetes_cluster.primary.kube_config[0].token
  }
}

provider "kubernetes" {
  host                   = digitalocean_kubernetes_cluster.primary.endpoint
  cluster_ca_certificate = base64decode(digitalocean_kubernetes_cluster.primary.kube_config[0].cluster_ca_certificate)
  token                  = digitalocean_kubernetes_cluster.primary.kube_config[0].token
}

# --- ArgoCD ---
resource "helm_release" "argocd" {
  name             = "argocd"
  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  version          = "7.7.5"
  namespace        = "argocd"
  create_namespace = true

  set {
    name  = "server.service.type"
    value = "LoadBalancer"
  }

  set {
    name  = "notifications.enabled"
    value = "true"
  }

  depends_on = [digitalocean_kubernetes_cluster.primary]
}

# --- Sealed Secrets ---
resource "helm_release" "sealed_secrets" {
  name             = "sealed-secrets"
  repository       = "https://bitnami-labs.github.io/sealed-secrets"
  chart            = "sealed-secrets"
  version          = "2.16.2"
  namespace        = "kube-system"
  create_namespace = false

  depends_on = [digitalocean_kubernetes_cluster.primary]
}

# --- Ingress NGINX ---
resource "helm_release" "ingress_nginx" {
  name             = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  version          = "4.11.3"
  namespace        = "ingress-nginx"
  create_namespace = true

  depends_on = [digitalocean_kubernetes_cluster.primary]
}
