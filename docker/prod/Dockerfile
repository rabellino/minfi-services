FROM python:3.12-alpine

ARG maintainer
LABEL maintainer "${maintainer}"

# Install system dependencies for Alpine
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY ./docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY ./python/services/src/api_services.py /app/app.py

# Run with gunicorn
ENV PORT 8080
ENV WORKERS 2
ENV LOGLEVEL info

EXPOSE $PORT

# Create entry script to run service
RUN echo "#!/bin/sh" > /app/entry.sh && \
    echo "gunicorn --chdir /app -w \${WORKERS}  \\" >> /app/entry.sh && \
    echo "   -b 0.0.0.0:\${PORT} --worker-tmp-dir /dev/shm \\" >> /app/entry.sh && \
    echo "   --enable-stdio-inheritance --access-logfile - --error-logfile - \\"  >> /app/entry.sh && \
    echo "   --access-logformat '%(h)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(T)s %(M)s' \\"  >> /app/entry.sh && \
    echo "    --log-level \${LOGLEVEL} 'app:app' " >> /app/entry.sh && \
    chmod a+x /app/entry.sh

ENTRYPOINT ["/app/entry.sh"]