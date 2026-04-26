FROM node:24-alpine AS build
WORKDIR /workspace
RUN corepack enable
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/webapp/spa/package.json ./apps/webapp/spa/
COPY lib/platform-api-client/package.json ./lib/platform-api-client/
RUN pnpm install --frozen-lockfile
COPY apps/webapp/spa ./apps/webapp/spa
COPY lib/platform-api-client ./lib/platform-api-client
RUN pnpm --filter spa build

FROM node:24-alpine AS dev
WORKDIR /workspace
RUN corepack enable
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/webapp/spa/package.json ./apps/webapp/spa/
COPY lib/platform-api-client/package.json ./lib/platform-api-client/
RUN pnpm install --frozen-lockfile
COPY apps/webapp/spa ./apps/webapp/spa
COPY lib/platform-api-client ./lib/platform-api-client
CMD ["pnpm", "--filter", "spa", "run", "dev", "--host", "0.0.0.0"]
