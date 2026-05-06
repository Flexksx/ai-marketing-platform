#!/bin/bash
set -e

echo "🚀 Starting Voisso deployment..."

if [ ! -f "infra/terraform.tfvars" ]; then
  echo "❌ Error: infra/terraform.tfvars not found!"
  echo "Please create it from infra/terraform.tfvars.example and fill in your values."
  exit 1
fi

cd infra

echo "📦 Initializing Terraform..."
terraform init

echo "🏗️  Planning deployment..."
terraform plan

read -p "Do you want to proceed with deployment? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
  echo "❌ Deployment cancelled"
  exit 0
fi

echo "🚀 Applying Terraform configuration..."
terraform apply -auto-approve

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service URLs:"
terraform output api_service_url
terraform output worker_service_url
echo ""
echo "📝 Next steps:"
echo "1. Test your API: curl \$(terraform output -raw api_service_url)/health"
echo "2. View logs: gcloud logging read 'resource.type=cloud_run_revision'"

