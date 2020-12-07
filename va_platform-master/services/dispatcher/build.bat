docker build -f Dockerfile -t gva-flows-dispatcher:latest .
REM docker run -p 2100:2100 gva-flows-dispatcher:latest
REM gcloud auth configure-docker
docker tag gva-flows-dispatcher gcr.io/vulnerability-analytics/gva-flows-dispatcher:latest 
docker push gcr.io/vulnerability-analytics/gva-flows-dispatcher:latest 