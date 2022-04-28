output "docker-server-ip" {
  value = "http://${aws_instance.docker-server.public_ip}"
}

output "docker-server-dns" {
  value = "http://${aws_instance.docker-server.public_dns}"
}

output "to-do-list-ip" {
  value = "http://${aws_instance.docker-server.public_ip}/todos"
}
