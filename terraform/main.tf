provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "app_repo" {
  name = "multi-cloud-devops-demo"
}

resource "aws_ecs_cluster" "app_cluster" {
  name = "multi-cloud-devops-demo-cluster"
}

resource "aws_ecs_task_definition" "app_task" {
  family                   = "multi-cloud-devops-demo-task"
  container_definitions    = jsonencode([
    {
      name  = "multi-cloud-devops-demo"
      image = "${aws_ecr_repository.app_repo.repository_url}:latest"
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
    }
  ])
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
}

resource "aws_ecs_service" "app_service" {
  name            = "multi-cloud-devops-demo-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    assign_public_ip = true
    subnets          = ["subnet-0af1b156295d99e5a"]
    security_groups  = ["sg-0576d4463a46599c6"]
  }
}