"""
DiabetesHelp PRO - Asistente personalizado de diabetes
Desarrollado por Rubén Reyes | Potenciado por IA
"""

import gradio as gr
from typing import List
import sys
import os
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))

# Cargar variables de entorno desde .env en la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# ✅ LANGFUSE INTEGRATION
try:
    from langfuse import observe, get_client, propagate_attributes
    langfuse_client = get_client()
    LANGFUSE_ENABLED = langfuse_client.auth_check()
    if LANGFUSE_ENABLED:
        print("✅ Langfuse conectado correctamente")
    else:
        print("⚠️ Langfuse no autenticado - monitoreo deshabilitado")
except Exception as e:
    print(f"⚠️ Langfuse no disponible: {e}")
    LANGFUSE_ENABLED = False

from diabetes_tools import DiabetesTools

# RAG lazy loading - se carga solo cuando se necesita (para inicio rápido)
rag = None
rag_loaded = False

def get_rag():
    """Carga RAG de forma lazy (solo cuando se necesita)"""
    global rag, rag_loaded
    if not rag_loaded:
        try:
            from rag_system import RAGSystem
            rag = RAGSystem("rag_documents")
            rag_loaded = True
            print("✅ RAG cargado correctamente en background")
        except Exception as e:
            print(f"⚠️ Error cargando RAG: {e}")
            rag_loaded = True
    return rag

# Configuración de OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DIABETES_MODEL = os.getenv("DIABETES_MODEL", "mistralai/mistral-7b-instruct").strip()

# Variables globales
user_data = {}

def check_api_key():
    """Verifica si hay API key configurada con formato correcto (sk-...)"""
    return bool(OPENROUTER_API_KEY) and OPENROUTER_API_KEY.startswith("sk-")

def call_llm(prompt: str, max_tokens: int = 1000, temperature: float = 0.7, use_rag: bool = False, trace_name: str = "llm_call") -> str:
    """Llama al LLM de OpenRouter con contexto RAG opcional y tracing con Langfuse"""
    
    if not check_api_key():
        return "⚠️ ERROR: OpenRouter API Key no configurada o inválida. Ve a README.md"
    
    try:
        # Agregar contexto RAG si está disponible y solicitado
        rag_context = ""
        rag_documents_used = []
        
        if use_rag:
            try:
                rag_instance = get_rag()
                if rag_instance:
                    rag_context = rag_instance.get_context(prompt, top_k=2)
                    if rag_context:
                        # 📊 LOG RAG en Langfuse
                        if LANGFUSE_ENABLED:
                            try:
                                langfuse_client.trace(
                                    name="rag_retrieval",
                                    input={"query": prompt, "top_k": 2},
                                    output={"context_length": len(rag_context), "chunks": rag_context[:200]}
                                )
                            except:
                                pass
                        prompt = rag_context + "\n\n" + prompt
            except:
                pass  # Si RAG falla, continuar sin él
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:7860",
                "X-Title": "DiabetesHelp PRO"
            },
            json={
                "model": DIABETES_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": """Eres DiabetesHelp, un asistente experto en diabetes, nutrición e insulina.
Basas tus respuestas en información médica profesional y científica.
Responde SIEMPRE en ESPAÑOL de forma clara, concisa y profesional.
Incluye emojis relevantes y formatea bien la respuesta.
SIEMPRE advierte al usuario de consultar con su médico para decisiones médicas.
Sé específico y personalizado en tus respuestas."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 0.95
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result.get("choices", [{}])[0].get("message", {}).get("content", "Error en respuesta")
            
            # 📊 LOG LLM en Langfuse
            if LANGFUSE_ENABLED:
                try:
                    langfuse_client.trace(
                        name=trace_name,
                        input={
                            "prompt": prompt[:300],
                            "model": DIABETES_MODEL,
                            "temperature": temperature,
                            "rag_used": use_rag
                        },
                        output={"response": llm_response[:300]},
                        metadata={"tokens": max_tokens}
                    )
                except:
                    pass
            
            return llm_response
        else:
            error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            return f"❌ Error API ({response.status_code}): {str(error_detail)[:300]}"
    
    except requests.exceptions.Timeout:
        return "❌ La solicitud tardó demasiado. Intenta de nuevo."
    except Exception as e:
        return f"❌ Error: {str(e)[:200]}"


def tab_user_profile(name: str, weight: float, height: float, age: int, sex: str, diabetes_type: str, activity_level: str):
    """Guarda el perfil y genera presentación personalizada con LLM"""
    
    global user_data
    
    if not name or weight <= 0 or height <= 0 or age <= 0:
        return "❌ Por favor completa todos los campos correctamente"
    
    if not check_api_key():
        return "⚠️ API Key no configurada. Edita .env con tu OPENROUTER_API_KEY"
    
    try:
        sex_clean = sex.split(" - ")[0] if " - " in sex else sex
        
        user_data = {
            "nombre": name,
            "peso_kg": weight,
            "altura_cm": height,
            "edad": age,
            "sexo": sex_clean,
            "diabetes_type": diabetes_type,
            "activity_level": activity_level
        }
        
        # 📊 Calcular datos con TOOLS y loguear en Langfuse
        bmi_info = DiabetesTools.calculate_bmi(weight, height)
        cal_info = DiabetesTools.estimate_daily_caloric_needs(weight, height, age, sex_clean, activity_level)
        carb_rec = DiabetesTools.carbohydrate_intake_recommendation(diabetes_type, weight, activity_level)
        
        # LOG TOOLS en Langfuse
        if LANGFUSE_ENABLED:
            try:
                langfuse_client.trace(
                    name="diabetes_tools_calculation",
                    input={
                        "weight_kg": weight,
                        "height_cm": height,
                        "age": age,
                        "sex": sex_clean,
                        "diabetes_type": diabetes_type,
                        "activity_level": activity_level
                    },
                    output={
                        "bmi": bmi_info['bmi'],
                        "bmi_category": bmi_info['category'],
                        "bmr": cal_info['bmr'],
                        "tdee": cal_info['tdee'],
                        "daily_carbs": carb_rec['daily_total']
                    },
                    metadata={"tools_used": ["calculate_bmi", "estimate_daily_caloric_needs", "carbohydrate_intake_recommendation"]}
                )
            except:
                pass
        
        # Usar LLM para generar presentación personalizada
        prompt = f"""
Genera un análisis de perfil profesional y visualmente bonito para un paciente con diabetes.

DATOS DEL USUARIO:
- Nombre: {name}
- Edad: {age} años
- Sexo: {sex_clean}
- Peso: {weight} kg
- Altura: {height} cm
- IMC: {bmi_info['bmi']} ({bmi_info['category']})
- Tipo de Diabetes: {diabetes_type}
- Nivel de Actividad: {activity_level}
- BMR: {cal_info['bmr']} kcal
- TDEE: {cal_info['tdee']} kcal
- Carbohidratos recomendados: {carb_rec['daily_total']}g

Formatea la respuesta así:

**═══ PERFIL DE SALUD ═══**
1. Saludo personalizado amable al usuario
2. Muestra los datos clave formateados profesionalmente

**═══ ANÁLISIS ═══**
3. Análisis detallado de su IMC
4. Evaluación de su nivel de actividad
5. Estado actual con diabetes

**═══ RECOMENDACIONES ═══**
6. Calorías diarias sugeridas
7. Ingesta de carbohidratos
8. 3 consejos específicos y accionables

**═══ PRÓXIMOS PASOS ═══**
9. Qué hacer en la app
10. Tips iniciales de uso

Usa emojis, líneas decorativas y formatea bonito para que se vea profesional y atractivo."""
        
        return call_llm(prompt, max_tokens=1500)
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


def tab_generate_menu(favorite_ingredients: str, restrictions: str, num_days: int):
    """Genera menú personalizado 100% por LLM"""
    
    if not user_data:
        return "❌ Por favor completa tu perfil primero"
    
    if not favorite_ingredients:
        return "❌ Ingresa al menos un ingrediente favorito"
    
    if not check_api_key():
        return "⚠️ API Key no configurada"
    
    try:
        favorite_list = [i.strip() for i in favorite_ingredients.split(",")]
        restrictions_list = [i.strip() for i in restrictions.split(",")] if restrictions else []
        
        # Calcular datos
        carb_rec = DiabetesTools.carbohydrate_intake_recommendation(
            user_data["diabetes_type"],
            user_data["peso_kg"],
            user_data.get("activity_level", "moderado")
        )
        
        prompt = f"""Crea un menú de comidas para hoy para {user_data['nombre']}, paciente con diabetes {user_data['diabetes_type']}.

RESTRICCIONES NUTRICIONALES:
- Máximo {carb_rec['daily_total']}g de carbohidratos por día
- Ingredientes permitidos: {", ".join(favorite_list)}
- Alimentos a evitar: {", ".join(restrictions_list) if restrictions_list else "ninguno"}

Por favor genera un menú con:
1. Desayuno
2. Almuerzo  
3. Cena
4. 1-2 Meriendas

Para cada comida especifica:
- Platos
- Ingredientes
- Gramos de carbohidratos
- Porción de 15g equivalentes

Usa emojis, sé creativo, NUNCA repitas el mismo menú dos veces. Cada menú debe ser diferente."""
        
        return call_llm(prompt, max_tokens=1200, use_rag=True)
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


def tab_health_advice():
    """Genera plan de salud profesional y diario personalizado 100% por LLM"""
    
    if not user_data:
        return "❌ Por favor completa tu perfil primero"
    
    if not check_api_key():
        return "⚠️ API Key no configurada"
    
    try:
        from datetime import datetime
        
        bmi_info = DiabetesTools.calculate_bmi(user_data["peso_kg"], user_data["altura_cm"])
        cal_info = DiabetesTools.estimate_daily_caloric_needs(
            user_data["peso_kg"],
            user_data["altura_cm"],
            user_data["edad"],
            user_data["sexo"],
            user_data["activity_level"]
        )
        carb_rec = DiabetesTools.carbohydrate_intake_recommendation(
            user_data["diabetes_type"],
            user_data["peso_kg"],
            user_data["activity_level"]
        )
        
        # Obtener contexto RAG adicional
        rag_instance = get_rag()
        rag_context = ""
        if rag_instance:
            try:
                rag_context = rag_instance.get_context("plan de salud nutrición ejercicio monitoreo glucosa", top_k=3)
            except:
                pass
        
        dia_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][datetime.now().weekday()]
        
        prompt = f"""GENERA UN PLAN DE SALUD PROFESIONAL PARA HOY ({dia_semana})

DATOS DEL PACIENTE:
- Nombre: {user_data['nombre']}
- Edad: {user_data['edad']} años, Sexo: {user_data['sexo']}
- Tipo de Diabetes: {user_data['diabetes_type']}
- IMC: {bmi_info['bmi']} ({bmi_info['category']})
- Calorías diarias recomendadas: {cal_info['tdee']} kcal
- Carbohidratos recomendados: {carb_rec['daily_total']}g
- Distribución: Desayuno {carb_rec['breakfast']}g | Almuerzo {carb_rec['lunch']}g | Cena {carb_rec['dinner']}g | Snacks {carb_rec['snacks']}g
- Nivel de actividad: {user_data['activity_level']}

{f'INFORMACIÓN MÉDICA RELEVANTE:{chr(10)}{rag_context[:2000]}' if rag_context else ''}

GENERA UN PLAN DE SALUD PROFESIONAL ESTRUCTURADO PARA {dia_semana.upper()}:

1. **HORARIO RECOMENDADO DE COMIDAS** (con distribución de carbohidratos)
   - Desayuno (07:00): Alimentos específicos con {carb_rec['breakfast']}g carbohidratos
   - Snack mañana (10:00): Opción saludable
   - Almuerzo (13:00): Opción balanceada con {carb_rec['lunch']}g carbohidratos
   - Snack tarde (16:00): Alternativa recomendada
   - Cena (20:00): Cena ligera con {carb_rec['dinner']}g carbohidratos

2. **PLAN DE EJERCICIO PARA {dia_semana.upper()}**
   - Tipo de ejercicio recomendado
   - Duración y intensidad
   - Horario ideal
   - Consideraciones especiales

3. **MONITOREO DE GLUCOSA**
   - Horarios para medir glucosa
   - Valores objetivo
   - Acciones si hay desviaciones

4. **HIDRATACIÓN Y BIENESTAR**
   - Litros de agua recomendados
   - Bebidas permitidas
   - Horas de sueño recomendadas

5. **CONSEJOS IMPORTANTES PARA {dia_semana.upper()}**
   - 3-5 recomendaciones específicas
   - Advertencias si es necesario

Sé profesional, específico y adaptado para {dia_semana}. Usa emojis relevantes.
⚠️ SIEMPRE advierte que debe consultar con su médico o endocrinólogo."""
        
        return call_llm(prompt, max_tokens=1200, use_rag=True)
    
    except Exception as e:
        return f"❌ Error: {str(e)}"


def tab_assistant_chat(message: str, chat_history: List = None) -> tuple:
    """Chat con RAG - formato messages dict"""
    
    if chat_history is None:
        chat_history = []
    
    if not message or not message.strip():
        return "", chat_history
    
    # Agregar mensaje del usuario
    chat_history.append({"role": "user", "content": message})
    
    if not user_data:
        chat_history.append({"role": "assistant", "content": "❌ Por favor completa tu perfil primero en la pestaña 'Mi Perfil'"})
        return "", chat_history
    
    if not check_api_key():
        chat_history.append({"role": "assistant", "content": "⚠️ API Key no configurada. Revisa el archivo .env"})
        return "", chat_history
    
    try:
        # Calcular métricas del usuario
        bmi_info = DiabetesTools.calculate_bmi(user_data.get('peso_kg', 0), user_data.get('altura_cm', 0))
        cal_info = DiabetesTools.estimate_daily_caloric_needs(
            user_data.get('peso_kg', 0), 
            user_data.get('altura_cm', 0), 
            user_data.get('edad', 0), 
            user_data.get('sexo', 'No especificado'),
            user_data.get('activity_level', 'moderado')
        )
        carb_rec = DiabetesTools.carbohydrate_intake_recommendation(
            user_data.get('diabetes_type', 'Tipo 1'), 
            user_data.get('peso_kg', 0),
            user_data.get('activity_level', 'moderado')
        )
        
        # Obtener contexto RAG
        rag_context = ""
        rag_instance = get_rag()
        if rag_instance:
            try:
                rag_context = rag_instance.get_context(message, top_k=2)
            except:
                pass
        
        # Construir perfil del usuario con todas las métricas
        user_profile = f"""PERFIL DEL USUARIO:
- Nombre: {user_data['nombre']}
- Edad: {user_data.get('edad', 'N/A')} años
- Sexo: {user_data.get('sexo', 'No especificado')}
- Tipo de Diabetes: {user_data['diabetes_type']}
- Peso: {user_data.get('peso_kg', 'N/A')} kg
- Altura: {user_data.get('altura_cm', 'N/A')} cm
- IMC: {bmi_info['bmi']:.1f} ({bmi_info['category']})
- Nivel de Actividad: {user_data.get('activity_level', 'Sedentario')}
- Calorías diarias recomendadas: {cal_info['tdee']:.0f} kcal
- Carbohidratos recomendados: {carb_rec['daily_total']}g/día ({carb_rec['distribution'].get('desayuno', 0)}g desayuno, {carb_rec['distribution'].get('almuerzo', 0)}g almuerzo, {carb_rec['distribution'].get('cena', 0)}g cena, {carb_rec['distribution'].get('snacks', 0)}g snacks)"""
        
        # System prompt con perfil completo y contexto RAG
        system_msg = f"""Eres DiabetesHelp, un asistente médico experto en diabetes.

{user_profile}

{f'INFORMACIÓN MÉDICA RELEVANTE:{chr(10)}{rag_context[:1500]}' if rag_context else ''}

Responde SIEMPRE en español, sé amable, profesional y conciso.
Basa tus respuestas en el perfil del usuario y la información médica proporcionada.
SIEMPRE advierte que debe consultar con su médico para decisiones importantes."""
        
        # Construir mensajes para la API
        api_messages = [{"role": "system", "content": system_msg}]
        
        # Agregar historial (últimos 6 mensajes)
        for msg in chat_history[-6:]:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Llamar LLM
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:7860",
                "X-Title": "DiabetesHelp PRO"
            },
            json={
                "model": DIABETES_MODEL,
                "messages": api_messages,
                "temperature": 0.7,
                "max_tokens": 600
            },
            timeout=25
        )
        
        if response.status_code == 200:
            bot_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error en respuesta")
        else:
            bot_response = f"❌ Error API ({response.status_code}): Intenta de nuevo"
        
        chat_history.append({"role": "assistant", "content": bot_response})
        return "", chat_history
    
    except requests.exceptions.Timeout:
        chat_history.append({"role": "assistant", "content": "⏱️ La respuesta tardó demasiado. Intenta de nuevo."})
        return "", chat_history
    except Exception as e:
        chat_history.append({"role": "assistant", "content": f"❌ Error: {str(e)[:100]}"})
        return "", chat_history


def create_interface():
    """Crea la interfaz profesional"""
    
    with gr.Blocks(title="DiabetesHelp PRO") as interface:
        
        gr.Markdown("""
        # 🏥 DiabetesHelp PRO
        ## Tu Asistente Personalizado de Diabetes
        
        **Desarrollado por Rubén Reyes**
        
        - 📋 Perfil personalizado
        - 🍽️ Menús dinámicos
        - 💪 Consejos basados en IA
        - 🤖 Chat inteligente
        
        ⚠️ Sistema educativo. Siempre consulta con tu médico.
        """)
        
        with gr.Tabs():
            
            # TAB 1: Perfil
            with gr.Tab("👤 Mi Perfil"):
                gr.Markdown("## Completa tu información")
                
                with gr.Row():
                    name = gr.Textbox(label="👤 Nombre", placeholder="Juan García")
                    age = gr.Number(label="🎂 Edad", minimum=1, maximum=120, value=30)
                
                with gr.Row():
                    weight = gr.Number(label="⚖️ Peso (kg)", minimum=1, maximum=300, value=75)
                    height = gr.Number(label="📏 Altura (cm)", minimum=50, maximum=250, value=175)
                
                with gr.Row():
                    sex = gr.Radio(label="⚧ Sexo", choices=["M - Masculino", "F - Femenino"], value="M - Masculino")
                    diabetes_type = gr.Dropdown(
                        label="💊 Diabetes",
                        choices=["tipo1", "tipo2", "gestacional"],
                        value="tipo2"
                    )
                
                activity = gr.Dropdown(
                    label="🏃 Actividad Física",
                    choices=["sedentario", "ligero", "moderado", "muy_activo", "extremadamente_activo"],
                    value="moderado"
                )
                
                submit_btn = gr.Button("✅ Procesar Perfil", variant="primary", size="lg")
                output = gr.Textbox(label="Análisis", lines=25, interactive=False)
                
                submit_btn.click(
                    fn=lambda n, w, h, a, s, d, ac: tab_user_profile(n, w, h, a, s, d, ac),
                    inputs=[name, weight, height, age, sex, diabetes_type, activity],
                    outputs=output
                )
            
            # TAB 2: Menú
            with gr.Tab("🍽️ Generar Menú"):
                gr.Markdown("## Menú personalizado")
                
                ingredients = gr.Textbox(
                    label="❤️ Ingredientes favoritos",
                    placeholder="pollo, arroz, tomate",
                    lines=3,
                    info="Separa con comas"
                )
                
                restrictions = gr.Textbox(
                    label="🚫 Restricciones",
                    placeholder="pescado, gluten",
                    lines=2,
                    info="Opcional"
                )
                
                days = gr.Slider(label="Días", minimum=1, maximum=7, value=1, step=1)
                
                gen_btn = gr.Button("🍳 Generar Menú", variant="primary", size="lg")
                menu_out = gr.Textbox(label="Menú", lines=30, interactive=False)
                
                gen_btn.click(
                    fn=tab_generate_menu,
                    inputs=[ingredients, restrictions, days],
                    outputs=menu_out
                )
            
            # TAB 3: Consejos
            with gr.Tab("💪 Plan de Salud"):
                gr.Markdown("## Tu plan personalizado")
                
                health_btn = gr.Button("📊 Generar Plan", variant="primary", size="lg")
                health_out = gr.Textbox(label="Plan", lines=35, interactive=False)
                
                health_btn.click(
                    fn=tab_health_advice,
                    outputs=health_out
                )
            
            # TAB 4: Chat
            with gr.Tab("🤖 Chat"):
                gr.Markdown("### 💬 Pregunta lo que quieras sobre diabetes")
                
                chatbot = gr.Chatbot(height=450)
                
                msg = gr.Textbox(
                    label="Escribe tu mensaje",
                    placeholder="¿Cómo me pongo la insulina?",
                    lines=1
                )
                
                send_btn = gr.Button("📤 Enviar", variant="primary", size="lg")
                
                send_btn.click(
                    fn=tab_assistant_chat,
                    inputs=[msg, chatbot],
                    outputs=[msg, chatbot]
                )
                
                msg.submit(
                    fn=tab_assistant_chat,
                    inputs=[msg, chatbot],
                    outputs=[msg, chatbot]
                )
            
            # TAB 5: Info
            with gr.Tab("ℹ️ Info"):
                # Obtener stats de RAG si está disponible
                rag_stats = ""
                if rag:
                    stats = rag.get_stats()
                    rag_stats = f"""
**📚 Sistema RAG (Retrieval Augmented Generation)**
- Documentos cargados: {stats['documentos_cargados']}
- Chunks indexados: {stats['chunks_totales']}
- Base médica: {', '.join(stats['documentos'])}
"""
                
                gr.Markdown(f"""
## DiabetesHelp PRO

**Desarrollo:** Rubén Reyes  
**Tecnología:** Mistral-7B vía OpenRouter + RAG médico

✨ Respuestas personalizadas y precisas
✨ Base de conocimiento médico actualizada
✨ Seguro y educativo
✨ Basado en estudios y datos profesionales

**🔑 Configuración**
- API: {'✅ OK' if OPENROUTER_API_KEY else '❌ No configurada'}
- Modelo: {DIABETES_MODEL}
- RAG: {'✅ Activado' if rag else '❌ No disponible'}

{rag_stats}

**Para configurar:** Lee README.md

---
**⚠️ Siempre consulta con tu médico**
- Esta app es educativa
- No reemplaza atención profesional
- La IA puede cometer errores
- Para emergencias: 911
                """)
    
    return interface


if __name__ == "__main__":
    print("🚀 Iniciando DiabetesHelp...")
    print("📚 Precargando RAG (puede tardar unos segundos)...")
    get_rag()  # Precargar RAG antes de crear la interfaz
    interface = create_interface()
    print("✅ Interfaz creada, iniciando servidor...")
    interface.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7862,
        show_error=True
    )
