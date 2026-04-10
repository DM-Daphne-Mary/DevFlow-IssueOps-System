# Phase 6 — Terraform Outputs

output "app_url" {
  description = "URL to access the Flask application"
  value       = "http://localhost:${var.app_port}"
}

output "db_connection" {
  description = "PostgreSQL connection details"
  value       = "postgresql://${var.db_user}:****@localhost:${var.db_port}/${var.db_name}"
}

output "app_container_id" {
  description = "Flask app container ID"
  value       = docker_container.flask_app.id
}

output "db_container_id" {
  description = "PostgreSQL container ID"
  value       = docker_container.postgres.id
}

output "network_name" {
  description = "Docker network name"
  value       = docker_network.app_network.name
}
