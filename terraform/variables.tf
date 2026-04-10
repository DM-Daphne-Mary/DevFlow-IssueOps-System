# Phase 6 — Terraform Variables

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "complaintsdb"
}

variable "db_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "PostgreSQL password"
  type        = string
  default     = "admin123"
  sensitive   = true
}

variable "db_port" {
  description = "External port for PostgreSQL"
  type        = number
  default     = 5433
}

variable "app_port" {
  description = "External port for Flask application"
  type        = number
  default     = 5001
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"
}
