# 📊 Langfuse Setup - Monitoreo de DiabetesHelp PRO

**Langfuse** es una plataforma open-source de observabilidad para agentes IA que permite monitorear todas las operaciones de tu app en tiempo real.

## 🚀 Paso 1: Crear Cuenta en Langfuse

1. Ve a **https://cloud.langfuse.com/**
2. Regístrate (gratis)
3. Crea un nuevo proyecto

## 🔑 Paso 2: Obtener Credenciales

1. En tu proyecto de Langfuse, ve a **Settings** → **API Keys**
2. Copia:
   - **Public Key** (comienza con `pk-lf-`)
   - **Secret Key** (comienza con `sk-lf-`)

## ⚙️ Paso 3: Configurar en `.env`

Abre tu archivo `.env` y agrega:

```env
# Langfuse
LANGFUSE_PUBLIC_KEY=pk-lf-tu-clave-aqui
LANGFUSE_SECRET_KEY=sk-lf-tu-clave-aqui
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

## ▶️ Paso 4: Ejecutar la App

```bash
python src/app.py
```

## 📈 Paso 5: Ver Trazas en Langfuse

1. Usa la app normalmente (completa perfil, genera menú, pregunta en chat)
2. Vuelve al dashboard de Langfuse
3. Verás todas las operaciones en **Traces**

## 🔍 ¿Qué se Monitorea?

### 1. **diabetes_tools_calculation**
Cuando completas tu perfil:
- ✅ BMI (Índice de Masa Corporal)
- ✅ BMR (Metabolismo Basal)
- ✅ TDEE (Gasto Calórico Diario)
- ✅ Carbohidratos Recomendados

```json
{
  "name": "diabetes_tools_calculation",
  "input": {
    "weight_kg": 75,
    "height_cm": 180,
    "age": 35,
    "diabetes_type": "Tipo 2"
  },
  "output": {
    "bmi": 23.1,
    "bmr": 1800,
    "tdee": 2160,
    "daily_carbs": 225
  }
}
```

### 2. **rag_retrieval**
Cuando el chat busca en documentos médicos:
- ✅ Query del usuario
- ✅ 2 chunks relevantes recuperados
- ✅ Longitud de contexto

```json
{
  "name": "rag_retrieval",
  "input": {
    "query": "¿Cuántos carbohidratos debo comer?",
    "top_k": 2
  },
  "output": {
    "context_length": 450,
    "chunks": "Los carbohidratos representan..."
  }
}
```

### 3. **llm_call**
Cuando el LLM genera una respuesta:
- ✅ Modelo usado (Mistral-7B)
- ✅ Prompt enviado (primeros 300 caracteres)
- ✅ Respuesta generada
- ✅ Tokens utilizados

```json
{
  "name": "llm_call",
  "input": {
    "prompt": "Eres DiabetesHelp...",
    "model": "mistralai/mistral-7b-instruct",
    "rag_used": true
  },
  "output": {
    "response": "Hola, basado en tu perfil..."
  },
  "metadata": {
    "tokens": 1500
  }
}
```

## 📊 Análisis en Langfuse Dashboard

Desde el dashboard puedes:

- **Ver trazas completas** de cada interacción
- **Analizar latencia** de LLM, RAG y tools
- **Calcular costos** de API calls
- **Buscar por usuario** o tipo de operación
- **Crear alertas** si hay errores
- **Exportar datos** para análisis

## 🎯 Casos de Uso

### 1. **Debugging**
Si una respuesta está mal, ve la traza y observa:
- Qué datos entró
- Qué documentos se recuperaron del RAG
- Qué salida generó el LLM

### 2. **Optimización**
- ¿Qué queries son lentas? → Optimiza el RAG
- ¿Qué prompts generan errores? → Mejora la instrucción
- ¿Cuál es el costo real? → Ajusta modelos

### 3. **Portfolio**
- Captura screenshots de trazas interesantes
- Demuestra que sabes debuggear sistemas de IA
- Muestra en entrevistas cómo monitorizas aplicaciones

## 🆘 Troubleshooting

### "Langfuse no autenticado"
```
⚠️ Langfuse no autenticado - monitoreo deshabilitado
```
**Solución:**
1. Verifica que tu `.env` tenga `LANGFUSE_PUBLIC_KEY` y `LANGFUSE_SECRET_KEY` correctas
2. Reinicia la app: `python src/app.py`

### Las trazas no aparecen
1. ¿Langfuse está activado? Mira el mensaje en consola
2. ¿Usaste la app después de reiniciar? (toma 5-10 segundos en aparecer)
3. Revisa el filtro de fechas en Langfuse

## 📚 Recursos

- **Langfuse Docs**: https://langfuse.com/docs
- **GitHub**: https://github.com/langfuse/langfuse
- **Self-hosting**: https://langfuse.com/self-hosting (si no quieres cloud)

---

**Tip Pro:** Langfuse es excelente para tu portfolio. Captura screenshots del dashboard y muéstralos en entrevistas como evidencia de que sabes monitorear sistemas de IA en producción. 🎓
