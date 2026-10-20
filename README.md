# AWS Cloud Lab

Контейнеризований REST API застосунок на Flask, розгорнутий у хмарі AWS з використанням Docker, Terraform та CI/CD.

## Public Address:
`lab-alb-329320074.eu-north-1.elb.amazonaws.com`

## Project Structure:

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD пайплайн
├── config/
│   └── app.yml                 # Конфігураційні файли застосунку
├── my_project/
│   └── auth/
│       ├── controller/         # Контролери
│       ├── dao/                # Data Access Objects
│       ├── domain/             # SQLAlchemy моделі таблиць
│       ├── route/              # Flask Blueprints
│       └── service/            # Бізнес-логіка
├── terraform/
│   ├── alb.tf                  # Application Load Balancer та Target Group
│   ├── database.tf             # AWS RDS
│   ├── ecr.tf                  # Elastic Container Registry
│   ├── ecs.tf                  # AWS ECS Fargate кластер, task та сервіс
│   ├── github.tf               # OIDC та IAM Ролі
│   ├── monitoring.tf           # CloudWatch метрики, дашборди та SNS алерти
│   ├── network.tf              # VPC, Subnets, Internet Gateway
│   ├── outputs.tf              # Вихідні змінні
│   ├── provider.tf             # Налаштування AWS
│   ├── security.tf             # Security Groups для ALB, ECS та RDS
│   └── variables.tf            # Вхідні змінні середовища
├── .dockerignore
├── .gitignore
├── app.py                      # Файл ініціалізації та запуску Flask
├── compose.yaml                # Локальний запуск API та БД
├── Dockerfile                  # Інструкції для збірки Docker-образу
├── extensions.py
├── README.md
└── requirements.txt