# Configuración del Proyecto

Este archivo contiene la configuración estándar para el desarrollo local.

## Variables de Entorno

Ver `.env.example` para el template. Necesitas:

```env
# OpenRouter API (requerido)
OPENROUTER_API_KEY=sk-or-tu-clave-aqui

# Modelo (opcional, default: mistralai/mistral-7b-instruct)
DIABETES_MODEL=mistralai/mistral-7b-instruct

# Puerto (opcional, default: 7861)
GRADIO_SERVER_PORT=7861
```

## Desarrollo Local

### 1. Crear entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables
```bash
cp .env.example .env
# Editar .env y agregar API Key
```

### 4. Ejecutar
```bash
python src/app.py
```

## Testing

Para testing futura (preparado en CI/CD):
```bash
pip install pytest pytest-cov
pytest
```

## Estructura de Carpetas

```
src/              # Código fuente
rag_documents/    # Documentos médicos
.github/          # GitHub Actions
docs/             # Documentación adicional (futuro)
tests/            # Tests (futuro)
```

## Debugging

### Activar logs detallados
En `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Problemas comunes

**"Module not found: gradio"**
```bash
pip install --upgrade gradio
```

**"API Key not working"**
- Verificar .env existe
- Verificar key es válida en OpenRouter
- Verificar permisos en GitHub secrets (si usas CI/CD)

**"Port 7861 already in use"**
```bash
# Cambiar en .env
GRADIO_SERVER_PORT=7862
```

**"RAG not loading"**
- Verificar carpeta `rag_documents/` existe
- Verificar archivos .md están presentes
- Ver logs en terminal

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guía completa.

## Licencia

MIT - Ver [LICENSE](LICENSE)
