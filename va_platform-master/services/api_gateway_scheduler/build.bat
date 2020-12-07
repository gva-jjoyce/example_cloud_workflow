docker build -f Dockerfile -t gva-api-gateway-scheduler:latest .
REM docker run -p 2100:2100  gva-api-gateway-scheduler:latest
REM gcloud auth configure-docker
docker tag gva-api-gateway-scheduler gcr.io/vulnerability-analytics/gva-api-gateway-scheduler:latest 
docker push gcr.io/vulnerability-analytics/gva-api-gateway-scheduler:latest 