resource "aws_sqs_queue" "appointments_dlq" {
  name                      = "lab-appointments-dlq"
  message_retention_seconds = 86400
}

resource "aws_sqs_queue" "appointments" {
  name                       = "lab-appointments-queue"
  visibility_timeout_seconds = 60
  receive_wait_time_seconds  = 20

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.appointments_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_iam_role" "ecs_task_role" {
  name = "lab-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_task_sqs_policy" {
  name = "lab-ecs-task-sqs"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ]
      Resource = [
        aws_sqs_queue.appointments.arn,
        aws_sqs_queue.appointments_dlq.arn
      ]
    }]
  })
}

resource "aws_ecs_task_definition" "worker" {
  family                   = "lab-worker-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "worker"
      image     = "${aws_ecr_repository.api_repo.repository_url}:latest"
      essential = true
      command   = ["python", "worker.py"]
      environment = [
        {
          name  = "DATABASE_URL"
          value = "mysql+pymysql://${var.db_username}:${var.db_password}@${aws_db_instance.mysql.endpoint}/${aws_db_instance.mysql.db_name}"
        },
        {
          name  = "SQS_QUEUE_URL"
          value = aws_sqs_queue.appointments.url
        },
        {
          name  = "AWS_REGION"
          value = "eu-north-1"
        },
        {
          name  = "REDIS_URL"
          value = "redis://localhost:6379/0"
        }
      ]
      dependsOn = [{
        containerName = "redis"
        condition     = "START"
      }]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.api_logs.name
          "awslogs-region"        = "eu-north-1"
          "awslogs-stream-prefix" = "worker"
        }
      }
    },
    {
      name      = "redis"
      image     = "redis:7-alpine"
      essential = true
      portMappings = [{
        containerPort = 6379
        hostPort      = 6379
        protocol      = "tcp"
      }]
    }
  ])
}

resource "aws_ecs_service" "worker" {
  name            = "lab-worker-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = 1
  launch_type     = "FARGATE"

network_configuration {
    subnets          = [aws_subnet.public_1.id, aws_subnet.public_2.id]
    security_groups  = [aws_security_group.app_sg.id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}

resource "aws_appautoscaling_target" "worker" {
  max_capacity       = 4
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.worker.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "worker_queue_scaling" {
  name               = "lab-worker-sqs-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.worker.resource_id
  scalable_dimension = aws_appautoscaling_target.worker.scalable_dimension
  service_namespace  = aws_appautoscaling_target.worker.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 10.0
    scale_in_cooldown  = 180
    scale_out_cooldown = 60

    customized_metric_specification {
      metric_name = "ApproximateNumberOfMessagesVisible"
      namespace   = "AWS/SQS"
      statistic   = "Average"

      dimensions {
        name  = "QueueName"
        value = aws_sqs_queue.appointments.name
      }
    }
  }
}