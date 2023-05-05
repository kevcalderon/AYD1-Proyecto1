output "public_ip" {
  value = try(aws_instance.ec2_bastion.public_ip, "")
}


