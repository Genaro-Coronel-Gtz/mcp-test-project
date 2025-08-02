# 🎵 Generador de Música Aleatoria con Docker

Este proyecto contiene un generador de música aleatoria desarrollado en Python que se puede ejecutar fácilmente usando Docker.

## 📁 Estructura del Proyecto

```
.
├── main.py              # Script principal del generador
├── Dockerfile           # Imagen Docker
├── docker-compose.yml   # Orquestación con Docker Compose
├── run.sh              # Script helper para comandos Docker
├── .dockerignore       # Archivos a ignorar en Docker
├── output/             # Directorio para archivos WAV generados
└── README.md           # Este archivo
```

## 🚀 Formas de Ejecutar

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir la imagen
docker-compose build

# Ejecutar el generador (modo interactivo)
docker-compose run --rm music-generator

# Modo desarrollo (bash interactivo)
docker-compose run --rm music-dev
```

### Opción 2: Docker directo

```bash
# Construir imagen
docker build -t music-generator .

# Ejecutar con volúmenes para edición
docker run -it --rm \
  -v $(pwd):/app \
  -v $(pwd)/output:/app/output \
  music-generator
```

### Opción 3: Script Helper

```bash
# Hacer ejecutable (solo la primera vez)
chmod +x run.sh

# Ejecutar script interactivo
./run.sh
```

## 🎼 Funcionalidades

- **Melodías aleatorias** en diferentes escalas musicales
- **Progresiones de acordes** automáticas
- **Canciones completas** (melodía + acordes)
- **Múltiples escalas**: Mayor, menor, pentatónica, blues, dórica, mixolidia
- **Exportación a WAV** de alta calidad (44.1kHz)

## 📂 Volúmenes y Persistencia

### Volúmenes configurados:
- `.:/app` - Código fuente (para edición en tiempo real)
- `./output:/app/output` - Directorio de salida para archivos WAV

### Ventajas de usar volúmenes:
✅ Puedes editar `main.py` desde tu editor favorito  
✅ Los cambios se reflejan inmediatamente en el contenedor  
✅ Los archivos WAV generados se guardan en tu sistema host  
✅ No pierdes el trabajo al reiniciar el contenedor  

## 🛠️ Desarrollo

### Para editar el código:
1. Ejecuta el modo desarrollo: `docker-compose run --rm music-dev`
2. Edita `main.py` desde tu editor favorito (VS Code, PyCharm, etc.)
3. Los cambios se ven inmediatamente en el contenedor
4. Ejecuta `python main.py` dentro del contenedor para probar

### Estructura de directorios:
```
/app/                 # Directorio de trabajo en el contenedor
├── main.py          # Tu código Python
├── output/          # Archivos WAV generados
└── ...              # Otros archivos del proyecto
```

## 🎵 Uso del Generador

Una vez dentro del contenedor, el programa te ofrecerá un menú:

```
🎵 GENERADOR DE MÚSICA ALEATORIA 🎵
==================================================
1. Generar melodía simple
2. Generar progresión de acordes  
3. Generar canción completa
4. Generar múltiples canciones
5. Mostrar escalas disponibles
6. Salir
==================================================
```

## 📁 Archivos de Salida

Los archivos WAV se guardan en el directorio `./output/` con nombres descriptivos:
- `melody_major_1722634567.wav`
- `chords_minor_1722634568.wav` 
- `song_pentatonic_1722634569.wav`

## 🐛 Troubleshooting

### Si el contenedor no inicia:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose run --rm music-generator
```

### Si no puedes editar archivos:
Verifica que el directorio tenga permisos de escritura:
```bash
chmod 755 .
chmod 644 main.py
```

### Para limpiar todo:
```bash
docker-compose down -v
docker system prune -f
```

## 🔧 Personalización

### Cambiar versión de Python:
Edita el `Dockerfile` y cambia la primera línea:
```dockerfile
FROM python:3.6-slim  # o la versión que prefieras
```

### Agregar librerías Python:
Agrega un `requirements.txt` y modifica el Dockerfile:
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
```

## 📊 Escalas Musicales Disponibles

- **Major**: Escala mayor clásica
- **Minor**: Escala menor natural  
- **Pentatonic**: Escala pentatónica
- **Blues**: Escala de blues
- **Dorian**: Modo dórico
- **Mixolydian**: Modo mixolidio

## 🎯 Próximas Mejoras

- [ ] Soporte para más instrumentos
- [ ] Exportación a MIDI
- [ ] Interfaz web
- [ ] Más escalas musicales
- [ ] Efectos de audio

---

¡Disfruta creando música aleatoria! 🎵