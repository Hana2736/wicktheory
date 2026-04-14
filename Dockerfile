FROM python:3.12-slim

RUN pip install --no-cache-dir streamlit

WORKDIR /app

COPY app.py admin.py auth.py cart.py data.py ./
COPY assets ./assets

RUN groupadd -g 1002 inksight && \
    useradd -u 1002 -g 1002 --create-home inksight && \
    chown -R inksight:inksight /app

USER inksight

EXPOSE 6368

CMD ["python3", "-m", "streamlit", "run", "app.py", \
     "--server.port=6368", \
     "--server.baseUrlPath=/wicktheory", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
