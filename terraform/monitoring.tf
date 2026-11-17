resource "aws_sns_topic" "alerts" {
  name = "lab-api-alerts"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "lytvyn.vladyslav2006@gmail.com"
}

resource "aws_cloudwatch_metric_alarm" "ecs_high_cpu_alarm" {
  alarm_name          = "lab-api-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 60
  statistic           = "Average"
  threshold           = 70
  alarm_description   = "Triggers when ECS CPU utilization exceeds 70% for 2 minutes"
  treat_missing_data  = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.api_service.name
  }
}

resource "aws_cloudwatch_metric_alarm" "alb_5xx_alarm" {
  alarm_name          = "lab-api-5xx-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Triggers on HTTP 5xx errors from ALB"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    LoadBalancer = aws_lb.main.arn_suffix
  }
}

resource "aws_cloudwatch_dashboard" "main_dashboard" {
  dashboard_name = "API-Monitoring"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["ECS/ContainerInsights", "RunningTaskCount", "ServiceName", aws_ecs_service.api_service.name, "ClusterName", aws_ecs_cluster.main.name],
            [".", "DesiredTaskCount", ".", ".", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "eu-north-1"
          period  = 60
          stat    = "Average"
          title   = "ECS Instances (Running vs Desired)"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/ECS", "CPUUtilization", "ServiceName", aws_ecs_service.api_service.name, "ClusterName", aws_ecs_cluster.main.name]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "eu-north-1"
          period  = 60
          stat    = "Average"
          title   = "ECS CPU Utilization (%)"
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 8
        height = 6
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", aws_lb.main.arn_suffix]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "eu-north-1"
          period  = 60
          stat    = "Sum"
          title   = "Requests per Minute"
        }
      },
      {
        type   = "metric"
        x      = 8
        y      = 6
        width  = 8
        height = 6
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", aws_lb.main.arn_suffix]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "eu-north-1"
          period  = 60
          stat    = "p95"
          title   = "Latency p95 (s)"
        }
      },
      {
        type   = "metric"
        x      = 16
        y      = 6
        width  = 8
        height = 6
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "HTTPCode_Target_5XX_Count", "LoadBalancer", aws_lb.main.arn_suffix]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "eu-north-1"
          period  = 60
          stat    = "Sum"
          title   = "HTTP 5xx Errors"
        }
      }
    ]
  })
}