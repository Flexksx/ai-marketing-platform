FROM eclipse-temurin:25-jdk AS base
WORKDIR /workspace

FROM base AS build
COPY platform-api-client ./platform-api-client
COPY platform-api-service ./platform-api-service
RUN chmod +x ./platform-api-client/gradlew ./platform-api-service/gradlew
RUN cd ./platform-api-client && ./gradlew --no-daemon publishToMavenLocal
RUN cd ./platform-api-service && ./gradlew --no-daemon clean assemble

FROM base AS dev
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
CMD ["sh", "-c", "cd ./platform-api-client && ./gradlew --no-daemon publishToMavenLocal && cd ../platform-api-service && ./gradlew --no-daemon bootRun --continuous"]
