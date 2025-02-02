cd ../../services/auth && npm ci && npm run build
cd ../../services/device && npm ci && npm run build
cd ../../services/experiment && npm ci && npm run build
cd ../../services/federation && npm ci && npm run build
cd ../../services/update && npm ci && npm run build
docker build --build-arg "ENV=DEV" ../../services/auth -t crosslab/auth-service-dev
docker build --build-arg "ENV=DEV" ../../services/device -t crosslab/device-service-dev
docker build --build-arg "ENV=DEV" ../../services/experiment -t crosslab/experiment-service-dev
docker build --build-arg "ENV=DEV" ../../services/federation -t crosslab/federation-service-dev
docker build ../../services/gateway -t crosslab/gateway-service-dev
docker build --build-arg "ENV=DEV" ../../services/update -t crosslab/update-service-dev