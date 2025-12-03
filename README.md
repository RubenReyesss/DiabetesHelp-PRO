# 🏥 DiabetesHelp PRO

> **Asistente inteligente para la gestión personalizada de diabetes con búsqueda aumentada y análisis médico profesional**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/gradio-4.0+-ff6b6b.svg)](https://gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Descripción

**DiabetesHelp PRO** es un asistente médico profesional diseñado para proporcionar información, educación y orientación personalizada sobre la gestión de la diabetes. Integra un sistema RAG con **7 documentos médicos profesionales** (~6,300 palabras) para garantizar respuestas basadas en evidencia médica, utilizando modelos de lenguaje avanzados.

### ✨ Características Principales

| Característica | Descripción | Tecnología |
|---|---|---|
| **Respuestas Dinámicas** | Todas las respuestas son personalizadas según el perfil | Modelos LLM avanzados |
| **RAG (Retrieval-Augmented Generation)** | Búsqueda semántica en base de datos médica profesional | Sistema RAG personalizado |
| **Perfil Personalizado** | Análisis completo: IMC, calorías, carbohidratos, diabetes tipo | DiabetesTools + Cálculos médicos |
| **Plan de Salud Adaptativo** | Plan diario que se ajusta según el día de la semana | Integración de fecha/hora |
| **Generador de Menús** | Menús personalizados basados en preferencias y restricciones | LLM + restricciones médicas |
| **Chat Asistente** | Conversación continua con contexto completo del usuario | Historial de mensajes + RAG |
| **Base Médica Profesional** | Documentos de instituciones como ADA, EASD | 7 archivos markdown curados |

## 📋 Documentos Médicos Incluidos

1. **01_diabetes_tipo_1.md** (680 palabras)
   - Fisiopatología de Diabetes Tipo 1
   - Regímenes de insulina (MDI, CSII)
   - Monitoreo y ajuste de dosis

2. **02_diabetes_tipo_2.md** (1,007 palabras)
   - Epidemiología y factores de riesgo
   - Medicamentos de primera línea
   - Estrategias de manejo

3. **03_nutricion_carbohidratos.md** (1,251 palabras)
   - Conteo de carbohidratos
   - Índice glucémico e índice insulinémico
   - Distribución de macronutrientes

4. **04_monitoreo_glucosa.md** (1,547 palabras)
   - HbA1c, glucosa en sangre, monitoreo continuo (CGM)
   - Hipoglucemia y cetoacidosis diabética (DKA)
   - Protocolos de manejo de emergencias

5. **05_complicaciones_diabetes.md** (908 palabras)
   - Complicaciones microvasculares (nefropatía, retinopatía, neuropatía)
   - Complicaciones macrovasculares (cardiovascular, ACV)
   - Otras complicaciones (infecciones, enfermedad coronaria)

6. **06_medicamentos_diabetes.md** (1,040 palabras)
   - Tipos de insulina y regímenes
   - Medicamentos para Tipo 2 (metformina, GLP-1, SGLT2i, etc.)
   - Tabla comparativa de opciones terapéuticas

7. **07_prevencion_diabetes.md** (853 palabras)
   - Factores de riesgo modificables y no modificables
   - Programa de Prevención de Diabetes (DPP)
   - Screening y detección temprana

## 🏗️ Estructura del Proyecto

```
DiabetesHelp-PRO/
├── src/
│   ├── __init__.py                  # Inicialización del paquete
│   ├── app.py                       # Aplicación principal (Gradio UI)
│   ├── rag_system.py                # Sistema RAG con búsqueda semántica
│   └── diabetes_tools.py            # Herramientas de cálculo médico
├── rag_documents/
│   ├── 01_diabetes_tipo_1.md
│   ├── 02_diabetes_tipo_2.md
│   ├── 03_nutricion_carbohidratos.md
│   ├── 04_monitoreo_glucosa.md
│   ├── 05_complicaciones_diabetes.md
│   ├── 06_medicamentos_diabetes.md
│   └── 07_prevencion_diabetes.md
├── .env.example                     # Template de configuración
├── .gitignore                       # Archivos ignorados por git
├── LICENSE                          # MIT License con disclaimer médico
├── README.md                        # Este archivo
├── requirements.txt                 # Dependencias Python
├── install.bat                      # Script de instalación (Windows)
└── run.bat                          # Script para ejecutar (Windows)
```

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Clave API de [OpenRouter](https://openrouter.ai/) (gratis con $5 de crédito inicial)

### Instalación

1. **Clonar repositorio**
```bash
git clone https://github.com/tuUsuario/DiabetesHelp-PRO.git
cd DiabetesHelp-PRO
```

2. **Crear y activar entorno virtual** (recomendado)
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar API Key**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key de OpenRouter
# OPENROUTER_API_KEY=sk-or-...
```

5. **Ejecutar aplicación**
```bash
python src/app.py
```

La aplicación se abrirá en: **http://127.0.0.1:7861**

## 💻 Stack Tecnológico

### Frontend
- **Gradio 4.x** - Interfaz web interactiva
- **Python 3.8+** - Lenguaje base

### Backend
- **Mistral-7B** - Modelo LLM a través de OpenRouter
- **OpenRouter API** - Proveedor de LLM con múltiples modelos
- **RAG System** - Sistema personalizado de recuperación aumentada
- **python-dotenv** - Gestión de variables de entorno
- **Langfuse** (Opcional) - Observabilidad de LLM, RAG y tools

### Componentes Médicos
- **DiabetesTools** - Cálculos médicos (IMC, calorías, carbohidratos)
- **Ecuación Mifflin-St Jeor** - Estimación de necesidades calóricas
- **Documentos médicos profesionales** - ADA, EASD, literatura médica

## 📊 Monitoreo con Langfuse (Opcional)

**Langfuse** es una plataforma de observabilidad para agentes IA que permite monitorear:

- 🔍 **Llamadas al LLM** - Prompts, respuestas, latencia, tokens
- 📚 **Recuperación RAG** - Documentos utilizados, chunks indexados, relevancia
- 🔧 **Uso de Tools** - Herramientas médicas (IMC, calorías, carbohidratos), inputs/outputs
- 📈 **Costos y Rendimiento** - Análisis de gastos, latencias, éxito/error

### Configurar Langfuse

1. **Crear cuenta en Langfuse** (gratis)
   - Ve a https://cloud.langfuse.com/
   - Regístrate y crea un proyecto

2. **Obtener credenciales**
   - En Settings → API Keys
   - Copia `Public Key` y `Secret Key`

3. **Configurar en `.env`**
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

4. **Ejecutar la app**
```bash
python src/app.py
```

5. **Ver trazas en Langfuse**
   - Cada llamada al LLM, RAG y tools aparecerá en tu dashboard
   - Analiza latencia, costos, errores y patrones de uso

### Ejemplo de Observabilidad

Cuando usas la app, Langfuse captura:

```
📝 Trace: tab_user_profile
├── 🔧 diabetes_tools_calculation
│   ├── Input: weight, height, age, sex, diabetes_type, activity_level
│   └── Output: BMI, BMR, TDEE, daily_carbs
├── 📚 rag_retrieval
│   ├── Query: consulta del usuario
│   ├── Documents: 2 chunks relevantes de base médica
│   └── Context length: ~500 caracteres
└── 🤖 llm_call
    ├── Model: mistralai/mistral-7b-instruct
    ├── Prompt: consulta + contexto RAG
    └── Response: análisis personalizado
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# OpenRouter API (requerido)
OPENROUTER_API_KEY=sk-or-tu-clave-aqui

# Modelo LLM (opcional, default: mistral-7b)
DIABETES_MODEL=mistralai/mistral-7b-instruct

# Puerto Gradio (opcional, default: 7861)
GRADIO_SERVER_PORT=7861
```

### Modelos Alternativos Soportados
- `google/gemma-7b-it` - Rápido, bajo costo
- `anthropic/claude-3-haiku` - Mayor calidad, más costo
- `meta-llama/llama-2-7b-chat` - Código abierto

### Costos de API

- **Mistral-7B**: ~$0.0001 USD por mensaje
- **Uso típico**: 50 mensajes/día = $0.005 USD/día
- **Presupuesto inicial OpenRouter**: $5 USD (gratis)

## 📖 Uso de la Aplicación

### Pestaña 1: Mi Perfil
- Ingresa nombre, edad, sexo
- Selecciona tipo de diabetes (Tipo 1, Tipo 2)
- Proporciona peso (kg) y altura (cm)
- Elige nivel de actividad (Sedentario, Ligero, Moderado, Muy Activo)
- **Resultado**: Análisis completo con IMC, calorías recomendadas, carbohidratos

### Pestaña 2: Generar Menú
- El LLM genera menú diario único y personalizado
- Adapta a preferencias dietéticas (carnívoro, vegetariano, etc.)
- Respeta restricciones médicas basadas en tipo de diabetes
- Incluye desglose de nutrientes y carbohidratos

### Pestaña 3: Plan de Salud
- Plan profesional adaptado al día de la semana actual
- Estructura de 5 secciones:
  1. Horario de comidas con distribución de carbohidratos
  2. Plan de ejercicio específico para el día
  3. Cronograma de monitoreo de glucosa
  4. Recomendaciones de hidratación y sueño
  5. Consejos específicos basados en día de la semana
- Integración RAG para recomendaciones basadas en evidencia

### Pestaña 4: Asistente Chat
- Chat continuo con contexto completo del usuario
- Integración RAG automática para respuestas basadas en documentos médicos
- Recuerda TODOS los datos del perfil (peso, IMC, diabetes tipo, calorías, carbohidratos, actividad)
- Soporta conversaciones largas con historial de 6 mensajes recientes
- Respuestas personalizadas según métricas del usuario

### Pestaña 5: Info
- Estadísticas del sistema RAG
- Documentos cargados (debe mostrar 7)
- Chunks indexados (141)
- Tamaño total de documentos
- Estado de API (configurada o no)
- Información del modelo utilizado

## 🤖 Sistema RAG Explicado

**RAG (Retrieval-Augmented Generation)** combina búsqueda de documentos con generación de IA:

### Flujo de Funcionamiento
1. **Indexación** (inicio): Los 7 documentos médicos se dividen en 141 chunks
2. **Búsqueda** (cada pregunta): Se buscan chunks relevantes por similitud de palabras clave
3. **Aumento** (contexto): Los chunks encontrados se incluyen en el prompt del LLM
4. **Generación** (respuesta): Mistral-7B genera respuesta basada en documentos + perfil del usuario

### Ventajas del Sistema
- ✅ Respuestas más precisas basadas en documentos reales
- ✅ Reducción de "alucinaciones" del modelo (respuestas falsas)
- ✅ Control total sobre fuentes de información
- ✅ Actualizaciones fáciles de documentos
- ✅ Trazabilidad de respuestas

## 🏥 Disclaimer Médico

⚠️ **IMPORTANTE: SOLO CON FINES EDUCATIVOS**

```
Esta herramienta es estrictamente educativa e informativa.

❌ NO reemplaza consulta médica profesional
❌ NO para diagnóstico o tratamiento médico
❌ NO para emergencias médicas
❌ La IA puede cometer errores

✅ SIEMPRE consultar con médico para decisiones médicas
✅ En caso de emergencia: Llamar 911 o ir a hospital inmediatamente
✅ Usar solo como herramienta de apoyo educativo

Los usuarios son responsables de verificar información con 
profesionales de salud certificados.
```

## 📊 Estadísticas del Proyecto

- **Documentos médicos**: 7
- **Palabras indexadas**: ~6,300
- **Chunks RAG**: 141
- **Funciones médicas**: 5 (IMC, calorías, carbohidratos, insulina, estrés)
- **Tabs funcionales**: 5 (Perfil, Menú, Salud, Chat, Info)
- **Idioma**: 100% en Español
- **Líneas de código**: 1,200+
- **Dependencias externas**: 3 (gradio, requests, python-dotenv)

## 🔐 Seguridad

- ✅ API Key en variables de entorno (.env)
- ✅ .env excluido de git (en .gitignore)
- ✅ Sin almacenamiento persistente de datos
- ✅ Sin datos de usuario entre sesiones
- ✅ Conexión HTTPS con OpenRouter
- ✅ Sin datos sensibles en logs
- ✅ Validación de entrada

## 🛠️ Desarrollo

### Estructura de Funciones Principales

**src/app.py**
```
- get_rag()                    # Carga lazy del sistema RAG
- check_api_key()              # Validación de configuración
- call_llm()                   # Llamada a OpenRouter API
- tab_user_profile()           # Pestaña de perfil con análisis
- tab_generate_menu()          # Pestaña generador de menús
- tab_health_advice()          # Pestaña de plan de salud diario
- tab_assistant_chat()         # Pestaña de chat con contexto completo
- create_interface()           # Construcción de UI Gradio
```

**src/rag_system.py**
```
- RAGSystem.load_documents()   # Carga archivos .md
- RAGSystem._chunk_document()  # Divide documentos en chunks
- RAGSystem.search()           # Búsqueda semántica por palabras clave
- RAGSystem.get_context()      # Contexto formateado para LLM
- RAGSystem.get_stats()        # Estadísticas del sistema
```

**src/diabetes_tools.py**
```
- calculate_bmi()                           # IMC e interpretación
- estimate_daily_caloric_needs()            # TDEE con Mifflin-St Jeor
- carbohydrate_intake_recommendation()      # Carbohidratos por comida
- estimate_insulin_dosage()                 # Estimación de insulina
- get_health_tips()                         # Tips personalizados
```

## 🚧 Roadmap Futuro

Características planificadas:
- [ ] Base de datos persistente (SQLite/PostgreSQL)
- [ ] Autenticación de usuarios
- [ ] Exportar planes a PDF
- [ ] Integración con CGM (Continuous Glucose Monitor)
- [ ] Múltiples idiomas (Inglés, Portugués, Francés)
- [ ] API REST para aplicaciones terceras
- [ ] Modo offline con modelo local (Ollama)
- [ ] Análisis de tendencias de glucosa
- [ ] Recordatorios de monitoreo
- [ ] Historial de planes generados

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles completos

Incluye disclaimer médico: Esta herramienta es **educativa solamente** y no reemplaza atención médica profesional.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/NuevaFuncion`)
3. Commit cambios (`git commit -m 'Agregar nueva función'`)
4. Push a la rama (`git push origin feature/NuevaFuncion`)
5. Abre un Pull Request con descripción detallada

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tuUsuario/DiabetesHelp-PRO/issues)
- **Documentación médica**: Ver archivos en `rag_documents/`
- **API OpenRouter**: https://openrouter.ai/docs
- **Gradio**: https://gradio.app/docs

## 👨‍💻 Autor

**Desarrollado por Rubén Reyes con ❤️ para la comunidad de personas con diabetes**

Documentación médica basada en:
- American Diabetes Association (ADA)
- European Association for the Study of Diabetes (EASD)
- Organización Mundial de la Salud (OMS)
- Literatura médica revisada por pares

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0.0  
**Estado**: En desarrollo activo

<p align="center">
  🏥 <b>DiabetesHelp PRO</b> 🏥<br>
  Sistema profesional de gestión de diabetes<br>
  <i>Siempre bajo supervisión médica profesional</i>
</p>
