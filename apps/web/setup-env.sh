#!/usr/bin/env bash

# Frontend Environment Setup Script
# This script helps you create .env files for local and production configurations

set -e

echo "🚀 Vozai Frontend Environment Setup"
echo "===================================="
echo ""

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is available
if command -v gcloud &> /dev/null; then
    echo -e "${BLUE}📡 Fetching production API URL from Google Cloud...${NC}"
    PROD_API_URL=$(gcloud run services describe vozai-client-api \
        --region=europe-central2 \
        --project=vozai \
        --format='value(status.url)' 2>/dev/null || echo "")
    
    if [ -n "$PROD_API_URL" ]; then
        echo -e "${GREEN}✓ Found production API: $PROD_API_URL${NC}"
    else
        echo -e "${YELLOW}⚠ Could not fetch production API URL${NC}"
        PROD_API_URL="https://vozai-client-api-728533160997.europe-central2.run.app"
    fi
else
    echo -e "${YELLOW}⚠ gcloud not found, using default production URL${NC}"
    PROD_API_URL="https://vozai-client-api-728533160997.europe-central2.run.app"
fi

# Prompt for Supabase credentials
echo ""
echo -e "${BLUE}📝 Supabase Configuration${NC}"
echo "Enter your Supabase project URL (or press Enter to skip):"
read -r SUPABASE_URL

echo "Enter your Supabase anon key (or press Enter to skip):"
read -r SUPABASE_KEY

# Create .env.local
echo ""
echo -e "${BLUE}📝 Creating .env.local (for local backend)...${NC}"
cat > .env.local << EOF
# Local Development - Connect to Local Backend
# Generated on $(date)

# Backend API (local docker-compose)
PUBLIC_BACKEND_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000

# Supabase
PUBLIC_SUPABASE_URL=${SUPABASE_URL:-https://your-project.supabase.co}
PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_KEY:-your-anon-key}
EOF

echo -e "${GREEN}✓ Created .env.local${NC}"

# Create .env.production
echo ""
echo -e "${BLUE}📝 Creating .env.production (for production backend)...${NC}"
cat > .env.production << EOF
# Production Backend - Connect to Cloud Run
# Generated on $(date)

# Backend API (Cloud Run)
PUBLIC_BACKEND_URL=${PROD_API_URL}
BACKEND_URL=${PROD_API_URL}

# Supabase
PUBLIC_SUPABASE_URL=${SUPABASE_URL:-https://your-project.supabase.co}
PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_KEY:-your-anon-key}
EOF

echo -e "${GREEN}✓ Created .env.production${NC}"

# Summary
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Environment files created:"
echo "  • .env.local      → Local backend (http://localhost:8000)"
echo "  • .env.production → Production backend ($PROD_API_URL)"
echo ""
echo "Next steps:"
echo ""
echo -e "${BLUE}1. Install dependencies:${NC}"
echo "   pnpm install"
echo ""
echo -e "${BLUE}2. Start full local stack:${NC}"
echo "   pnpm full-stack:local"
echo ""
echo -e "${BLUE}3. Or start frontend only:${NC}"
echo "   pnpm dev:local    # → Local backend"
echo "   pnpm dev:prod     # → Production backend"
echo ""
echo "See SETUP.md for more details!"

