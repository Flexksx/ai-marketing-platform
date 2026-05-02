#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

SPEC="${OPENAPI_INPUT:-../../../openapi.json}"

rm -rf src/lib/api/generated

exec pnpm exec openapi-generator-cli generate \
	-i "$SPEC" \
	-g typescript-fetch \
	-o src/lib/api/generated \
	--global-property apiDocs=false,modelDocs=false,skipFormModel=false \
	--additional-properties=modelPropertyNaming=camelCase,paramNaming=camelCase,enumPropertyNaming=camelCase,withSeparateModelsAndApi=true,apiPackage=apis,modelPackage=models,supportsES6=true,typescriptThreePlus=true
