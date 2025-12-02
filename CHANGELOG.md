# Changelog

Todos los cambios notables en DiabetesHelp PRO se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2025-12-02

### Agregado
- ✅ Aplicación principal con Gradio
- ✅ Sistema RAG con 7 documentos médicos profesionales (6,300+ palabras)
- ✅ Integración con OpenRouter + Mistral-7B
- ✅ 5 pestañas funcionales:
  - Mi Perfil: Análisis personalizado de usuario
  - Generar Menú: Menús únicos y personalizados
  - Plan de Salud: Plan diario adaptado a día de la semana
  - Asistente Chat: Chat continuo con contexto completo
  - Info: Estadísticas del sistema
- ✅ DiabetesTools con 5 funciones médicas:
  - calculate_bmi(): Cálculo de índice de masa corporal
  - estimate_daily_caloric_needs(): Estimación de calorías (Mifflin-St Jeor)
  - carbohydrate_intake_recommendation(): Recomendaciones de carbohidratos
  - estimate_insulin_dosage(): Estimación de insulina
  - get_health_tips(): Tips personalizados
- ✅ RAGSystem con búsqueda semántica y lazy loading
- ✅ Sistema de chat con historial y contexto de perfil completo
- ✅ Documentación profesional (README.md, LICENSE, CONTRIBUTING.md)
- ✅ Scripts de instalación (install.bat, run.bat)
- ✅ Variables de entorno con .env.example
- ✅ .gitignore completo
- ✅ GitHub Actions CI/CD

### Documentos Médicos Incluidos
1. 01_diabetes_tipo_1.md - Fisiopatología y manejo de Tipo 1
2. 02_diabetes_tipo_2.md - Epidemiología y manejo de Tipo 2
3. 03_nutricion_carbohidratos.md - Conteo y distribución de carbohidratos
4. 04_monitoreo_glucosa.md - HbA1c, CGM, protocolos de emergencia
5. 05_complicaciones_diabetes.md - Complicaciones micro y macrovasculares
6. 06_medicamentos_diabetes.md - Insulinas y medicamentos orales
7. 07_prevencion_diabetes.md - Factores de riesgo y prevención

### Tecnologías
- Gradio 4.x - Frontend
- Python 3.8+ - Backend
- Mistral-7B (OpenRouter) - LLM
- RAG System personalizado
- python-dotenv - Gestión de configuración

### Características Principales
- 100% respuestas generadas por IA
- Sistema RAG para respuestas basadas en evidencia
- Perfil personalizado completo (peso, altura, IMC, diabetes, actividad)
- Plan de salud adaptativo (cambia según día de la semana)
- Chat con contexto completo del usuario
- Generación de menús personalizados
- Cálculos médicos profesionales
- Disclaimer médico y educativo

## Roadmap Futuro

### Versión 1.1
- [ ] Base de datos persistente (SQLite)
- [ ] Autenticación básica de usuarios
- [ ] Exportar planes a PDF
- [ ] Historial de planes generados

### Versión 1.2
- [ ] Múltiples idiomas (Inglés, Portugués)
- [ ] Integración con API de glucómetros
- [ ] Análisis de tendencias de glucosa
- [ ] Recordatorios automáticos

### Versión 2.0
- [ ] API REST para terceros
- [ ] Aplicación mobile (React Native)
- [ ] Modo offline con Ollama
- [ ] Base de conocimientos expandida (50+ documentos)

---

## Notas de Desarrollo

### Decisiones Arquitectónicas

1. **RAG System Personalizado**
   - Decidimos no usar LangChain por simplicidad y control
   - Búsqueda semántica basada en palabras clave (no embeddings costosos)
   - Lazy loading para inicio rápido

2. **Mistral-7B en OpenRouter**
   - Bajo costo (~$0.0001 por mensaje)
   - Buena calidad para español
   - Alternativas disponibles sin cambiar código

3. **Gradio vs FastAPI/React**
   - Gradio permite UI rápida sin frontend
   - Perfecto para prototipado
   - Fácil de mantener por una sola persona

4. **Sin Base de Datos en v1.0**
   - Simplifica despliegue
   - Se pueden agregar en v1.1
   - Permite uso educativo sin GDPR complejo

### Aprendizajes

1. **RAG es crucial para reducir alucinaciones**
   - Sin RAG: Respuestas genéricas
   - Con RAG: Respuestas específicas y documentadas

2. **Contexto completo del usuario es esencial**
   - El chat necesita saber peso, IMC, diabetes tipo, actividad
   - Sin esto: Recomendaciones genéricas

3. **Adaptación diaria mejora experiencia**
   - Plan de salud diferente por día de la semana
   - Más realista y útil

---

Última actualización: 2 de Diciembre, 2025
