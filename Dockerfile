# Dockerfile para el Generador de Música Aleatoria
FROM python:3.9-slim

# Información del mantenedor
LABEL maintainer="Generador de Música"
LABEL description="Contenedor para ejecutar el generador de música aleatoria en Python"

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para audio
RUN apt-get update && apt-get install -y \
    alsa-utils \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Crear un usuario no-root para seguridad
RUN useradd -m -u 1000 musicgen && \
    chown -R musicgen:musicgen /app

# Cambiar al usuario no-root
USER musicgen

# Crear directorio para los archivos de música generados
RUN mkdir -p /app/output

# Copiar el script principal (opcional, también se puede montar como volumen)
# COPY main.py /app/

# Comando por defecto
CMD ["python", "main.py"]

# Exponer puerto si fuera necesario (para futuras funcionalidades web)
# EXPOSE 8000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1