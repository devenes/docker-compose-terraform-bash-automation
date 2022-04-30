####################################
#### Required AWS Configuration ####
####################################

variable "region" {
  default = "us-east-1"
}

variable "profile" {
  default = "default"
}

variable "backend" {
  default     = "terraform-env-bucket"
  description = "The name of the S3 bucket to store Terraform state"
}

variable "tf_key" {
  default     = "tf/terraform.tfstate"
  description = "The key of the S3 bucket to store Terraform state"
}

########################################
# Required AWS Resources Configuration #
########################################

variable "key_name" {
  default = "east1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "instance_name" {
  default = "Docker Web Server"
}

variable "security_group_name" {
  default = "docker-sec-gr"
}
