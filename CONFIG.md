# Configuración

## Variables de Entorno

Copia `.env.example` a `.env`:

```env
OPENROUTER_API_KEY=sk-or-tu-clave-aqui
DIABETES_MODEL=mistralai/mistral-7b-instruct
```

## Instalación Local

```bash
# Entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar
cp .env.example .env

# Ejecutar
python src/app.py
```

## Troubleshooting

**Puerto ocupado:**
```bash
GRADIO_SERVER_PORT=7862 python src/app.py
```

**RAG no carga:**
- Verificar carpeta `rag_documents/` existe
- Verificar archivos .md están presentes

**API Error:**
- Verificar API Key en .env
- Verificar credenciales en OpenRouter
