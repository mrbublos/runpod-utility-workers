export VERSION=1.0.3
docker build -t skrendelauth/file-saver:$VERSION -t skrendelauth/file-saver:latest .
#docker buildx build --platform linux/amd64 -t skrendelauth/file-saver:$VERSION -t skrendelauth/file-saver:latest .
#docker push skrendelauth/file-saver:$VERSION