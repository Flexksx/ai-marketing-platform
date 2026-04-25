FROM node:22-alpine AS build
WORKDIR /workspace
COPY . .
RUN if [ ! -f package.json ]; then \
      echo "apps/webapp/package.json not found. Skipping frontend build."; \
    else \
      if [ -f pnpm-lock.yaml ]; then \
        corepack enable && pnpm install --frozen-lockfile && pnpm build; \
      elif [ -f yarn.lock ]; then \
        corepack enable && yarn install --frozen-lockfile && yarn build; \
      elif [ -f package-lock.json ]; then \
        npm ci && npm run build; \
      else \
        npm install && npm run build; \
      fi; \
    fi

FROM node:22-alpine AS dev
WORKDIR /workspace
ENV PNPM_HOME=/root/.local/share/pnpm
ENV STORE_PATH=/root/.local/share/pnpm/store
CMD ["sh", "-c", "if [ ! -f package.json ]; then echo 'apps/webapp/package.json not found. Frontend dev server is idle.'; tail -f /dev/null; fi; if [ -f pnpm-lock.yaml ]; then corepack enable && pnpm config set store-dir /root/.local/share/pnpm/store && pnpm install && pnpm dev --host 0.0.0.0; elif [ -f yarn.lock ]; then corepack enable && yarn install --frozen-lockfile && yarn dev --host 0.0.0.0; elif [ -f package-lock.json ]; then npm ci && npm run dev -- --host 0.0.0.0; else npm install && npm run dev -- --host 0.0.0.0; fi"]
