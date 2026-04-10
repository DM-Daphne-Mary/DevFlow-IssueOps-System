# Phase 6 — Terraform: Infrastructure as Code
# Provisions Docker containers locally to simulate cloud infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Configure the Docker provider
provider "docker" {}

# --- Network ---
resource "docker_network" "app_network" {
  name = "complaint-app-network"
}

# --- PostgreSQL Database ---
resource "docker_image" "postgres" {
  name         = "postgres:15-alpine"
  keep_locally = true
}

resource "docker_volume" "postgres_data" {
  name = "complaint-postgres-data"
}

resource "docker_container" "postgres" {
  name  = "complaint-db-terraform"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_DB=${var.db_name}",
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_password}"
  ]

  ports {
    internal = 5432
    external = var.db_port
  }

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  restart = "unless-stopped"
}

# --- Flask Application ---
resource "docker_image" "flask_app" {
  name         = "complaint-management-system:latest"
  keep_locally = true
}

resource "docker_container" "flask_app" {
  name  = "complaint-app-terraform"
  image = docker_image.flask_app.image_id

  env = [
    "DB_HOST=complaint-db-terraform",
    "DB_NAME=${var.db_name}",
    "DB_USER=${var.db_user}",
    "DB_PASSWORD=${var.db_password}"
  ]

  ports {
    internal = 5000
    external = var.app_port
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  depends_on = [docker_container.postgres]
  restart    = "unless-stopped"
}
