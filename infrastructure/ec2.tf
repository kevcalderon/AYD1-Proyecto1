resource "aws_security_group" "proyecto_ayd1-sg" {
  vpc_id = aws_vpc.proyecto_ayd1.id
  name   = "proyecto_ayd1-sg"
  egress = [
    {
      # Regla de egreso para la comunicacion con cualquier puerto
      cidr_blocks      = ["0.0.0.0/0", ]
      description      = ""
      from_port        = 0
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "-1"
      security_groups  = []
      self             = false
      to_port          = 0
    }
  ]
  ingress = [
    # Regla de ingreso para la comunicacion por ssh
    {
      cidr_blocks      = ["0.0.0.0/0", ]
      description      = ""
      from_port        = 22
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "tcp"
      security_groups  = []
      self             = false
      to_port          = 22
    },
    # Regla de ingreso para la base de datos en el puerto 3306
    {
      cidr_blocks      = ["0.0.0.0/0", ]
      description      = ""
      from_port        = 3306
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "tcp"
      security_groups  = []
      self             = false
      to_port          = 3306
    },
    # Regla de ingreso para el frontend en el puerto 80
    {
      cidr_blocks      = ["0.0.0.0/0"]
      description      = "Allow incoming traffic to frontend"
      from_port        = 80
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "tcp"
      security_groups  = []
      self             = false
      to_port          = 80
    },
    # Regla de ingreso para el backend en el puerto 5000
    {
      cidr_blocks      = ["0.0.0.0/0"]
      description      = "Allow incoming traffic to backend"
      from_port        = 5000
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "tcp"
      security_groups  = []
      self             = false
      to_port          = 5000
    }
  ]
}

resource "aws_key_pair" "proyecto_ayd1-key" {
  key_name   = "proyecto_ayd1"
  public_key = file("${var.PATH_PUBLIC_KEYPAIR}")
}

resource "aws_instance" "ec2_bastion" {
  ami                    = "ami-090fa75af13c156b4"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.proyecto_ayd1-key.key_name
  vpc_security_group_ids = [aws_security_group.proyecto_ayd1-sg.id]
  subnet_id              = aws_subnet.PublicS1.id
  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo yum install -y git",
      "sudo amazon-linux-extras install -y docker",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
      "sudo systemctl enable docker.service",
      "sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose",
      "git clone https://github.com/kevcalderon/AYD1-Proyecto1.git"
    ]
  }
  connection {
    host        = self.public_ip
    user        = var.user_ssh
    private_key = file("${var.PATH_KEYPAIR}")
  }
}



