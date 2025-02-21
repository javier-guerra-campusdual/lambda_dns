variable "aws_region" {
  description = "AWS region donde se desplegará la infraestructura"
  type        = string
  default     = "eu-west-3"
}

variable "environment" {
  description = "Entorno de despliegue (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "dns-updater"
}

variable "hosted_zone_id" {
  description = "ID de la zona hospedada en Route53"
  type        = string
}

variable "domain_suffix" {
  description = "Sufijo del dominio para los registros DNS"
  type        = string
  default     = ".campusdual.mkcampus.com"
}

variable "lambda_zip_path" {
  description = "Ruta al archivo ZIP con el código de la función Lambda"
  type        = string
  default     = "lambda.zip"
}

variable "tags" {
  description = "Tags comunes para todos los recursos"
  type        = map(string)
  default     = {
    Project     = "DNS Updater"
    Environment = "Development"
    ManagedBy   = "Terraform"
  }
}