docker build -f Dockerfile -t gva-getfakefindings:latest .
REM docker run -p 2100:2100 gva-getfakefindings:latest
REM gcloud auth configure-docker
docker tag gva-getfakefindings gcr.io/vulnerability-analytics/gva-getfakefindings:latest 
docker push gcr.io/vulnerability-analytics/gva-getfakefindings:latest 