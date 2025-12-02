"""
Herramientas (Tools) para el asistente diabético
Incluye: cálculo IMC, carbohidratos, menú, consejos, etc.
"""

import math
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import json


class DiabetesTools:
    """Conjunto de herramientas para gestión de diabetes"""
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
        """
        Calcula el Índice de Masa Corporal
        
        Args:
            weight_kg: Peso en kilogramos
            height_cm: Altura en centímetros
            
        Returns:
            Diccionario con IMC y clasificación
        """
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Bajo peso"
            recommendation = "Consulta con médico para mejorar nutrición"
        elif bmi < 25:
            category = "Peso normal"
            recommendation = "Mantén estos hábitos saludables"
        elif bmi < 30:
            category = "Sobrepeso"
            recommendation = "Considera aumentar ejercicio y revisar dieta"
        elif bmi < 35:
            category = "Obesidad clase 1"
            recommendation = "Consulta con nutricionista para plan de pérdida de peso"
        elif bmi < 40:
            category = "Obesidad clase 2"
            recommendation = "Busca apoyo profesional urgentemente"
        else:
            category = "Obesidad clase 3"
            recommendation = "Contacta a profesionales de salud de inmediato"
        
        return {
            "bmi": round(bmi, 2),
            "category": category,
            "recommendation": recommendation,
            "weight_kg": weight_kg,
            "height_cm": height_cm
        }
    
    @staticmethod
    def estimate_daily_caloric_needs(weight_kg: float, height_cm: float, age: int, sex: str, activity_level: str = "moderado") -> Dict[str, Any]:
        """
        Estima necesidades calóricas diarias usando ecuación de Mifflin-St Jeor
        
        Args:
            weight_kg: Peso en kg
            height_cm: Altura en cm
            age: Edad en años
            sex: 'M' para masculino, 'F' para femenino
            activity_level: 'sedentario', 'ligero', 'moderado', 'muy activo', 'extremadamente activo'
            
        Returns:
            Diccionario con calorías base y con actividad
        """
        height_m = height_cm / 100
        
        # Ecuación Mifflin-St Jeor
        if sex.upper() == 'M':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        
        # Factores de actividad
        activity_factors = {
            "sedentario": 1.2,
            "ligero": 1.375,
            "moderado": 1.55,
            "muy_activo": 1.725,
            "extremadamente_activo": 1.9
        }
        
        factor = activity_factors.get(activity_level.lower(), 1.55)
        tdee = bmr * factor
        
        return {
            "bmr": round(bmr),
            "tdee": round(tdee),
            "activity_level": activity_level,
            "note": "Para diabetes tipo 2, considerar pérdida de peso gradual (500-750 cal deficit)"
        }
    
    @staticmethod
    def carbohydrate_intake_recommendation(diabetes_type: str, weight_kg: float, activity_level: str = "moderado") -> Dict[str, Any]:
        """
        Recomienda ingesta diaria de carbohidratos
        
        Args:
            diabetes_type: 'tipo1', 'tipo2', 'gestacional'
            weight_kg: Peso en kg
            activity_level: Nivel de actividad
            
        Returns:
            Recomendaciones de carbohidratos
        """
        recommendations = {
            "tipo1": {
                "sedentario": 130,  # g/día (mínimo)
                "ligero": 150,
                "moderado": 175,
                "muy_activo": 200,
                "extremadamente_activo": 230
            },
            "tipo2": {
                "sedentario": 130,
                "ligero": 140,
                "moderado": 150,
                "muy_activo": 170,
                "extremadamente_activo": 190
            },
            "gestacional": {
                "sedentario": 120,
                "ligero": 130,
                "moderado": 140,
                "muy_activo": 160,
                "extremadamente_activo": 180
            }
        }
        
        daily_carbs = recommendations.get(diabetes_type.lower(), {}).get(activity_level.lower(), 150)
        
        # Por comida
        meals = {
            "desayuno": round(daily_carbs * 0.2),
            "almuerzo": round(daily_carbs * 0.35),
            "cena": round(daily_carbs * 0.25),
            "snacks": round(daily_carbs * 0.2)
        }
        
        return {
            "daily_total": daily_carbs,
            "distribution": meals,
            "portions_per_meal": {
                "desayuno": round(daily_carbs * 0.2 / 15),
                "almuerzo": round(daily_carbs * 0.35 / 15),
                "cena": round(daily_carbs * 0.25 / 15),
            },
            "diabetes_type": diabetes_type,
            "note": "1 porción de carbohidrato = 15g"
        }
    
    @staticmethod
    def estimate_insulin_dosage(weight_kg: float, diabetes_type: str = "tipo1") -> Dict[str, Any]:
        """
        Estima dosis inicial de insulina (solo referencia, requiere supervisión médica)
        
        Args:
            weight_kg: Peso en kg
            diabetes_type: 'tipo1' o 'tipo2'
            
        Returns:
            Estimación de dosis
        """
        if diabetes_type.lower() == "tipo1":
            # 0.5-1.0 unidades por kg
            total_dose = weight_kg * 0.75  # aproximado
            basal = total_dose * 0.4  # 40% basal
            bolus = total_dose * 0.6  # 60% bolus
            
            return {
                "total_daily_insulin": round(total_dose),
                "basal": round(basal),
                "bolus": round(bolus),
                "carb_ratio": f"1:{round(500/total_dose)}",  # regla 500
                "correction_factor": f"1:{round(1800/total_dose)}",  # regla 1800
                "warning": "SOLO REFERENCIA. Requiere supervisión de endocrinólogo"
            }
        else:
            return {
                "note": "Tipo 2: Generalmente se inicia con metformina. Insulina si es necesario.",
                "warning": "Consulta con tu médico para plan personalizado"
            }
    
    @staticmethod
    def generate_menu_day(
        diabetes_type: str,
        weight_kg: float,
        age: int,
        sex: str,
        favorite_ingredients: List[str],
        restrictions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Genera un menú para el día
        
        Args:
            diabetes_type: 'tipo1', 'tipo2', 'gestacional'
            weight_kg: Peso en kg
            age: Edad
            sex: 'M' o 'F'
            favorite_ingredients: Lista de ingredientes favoritos
            restrictions: Lista de restricciones alimentarias
            
        Returns:
            Menú del día con calorías y carbohidratos
        """
        restrictions = restrictions or []
        
        # Base de alimentos seguros para diabéticos
        breakfast_options = [
            {"name": "Avena integral con frutos rojos", "carbs": 35, "protein": 8, "calories": 200},
            {"name": "2 huevos revueltos con pan integral", "carbs": 30, "protein": 14, "calories": 280},
            {"name": "Yogur griego con frutos secos", "carbs": 25, "protein": 18, "calories": 220},
            {"name": "Batido de proteína con plátano", "carbs": 30, "protein": 25, "calories": 240},
        ]
        
        lunch_options = [
            {"name": "Pechuga de pollo a la plancha con arroz integral", "carbs": 50, "protein": 35, "calories": 450},
            {"name": "Salmón con batata y verduras", "carbs": 45, "protein": 30, "calories": 420},
            {"name": "Lentejas con verduras de temporada", "carbs": 55, "protein": 16, "calories": 380},
            {"name": "Pavo molido con pasta integral", "carbs": 48, "protein": 32, "calories": 440},
        ]
        
        dinner_options = [
            {"name": "Pechuga de pavo con brócoli", "carbs": 20, "protein": 28, "calories": 220},
            {"name": "Bacalao con champiñones", "carbs": 15, "protein": 25, "calories": 200},
            {"name": "Tofu salteado con verduras", "carbs": 18, "protein": 22, "calories": 240},
            {"name": "Caldo de verduras con pollo", "carbs": 22, "protein": 24, "calories": 230},
        ]
        
        snack_options = [
            {"name": "Manzana con almendras", "carbs": 30, "protein": 6, "calories": 180},
            {"name": "Yogur bajo en grasa", "carbs": 15, "protein": 12, "calories": 110},
            {"name": "Queso con galletas integrales", "carbs": 18, "protein": 8, "calories": 160},
            {"name": "Hummus con verduras", "carbs": 20, "protein": 5, "calories": 120},
        ]
        
        # Seleccionar opciones (simplificado para demostración)
        breakfast = breakfast_options[0]
        lunch = lunch_options[0]
        dinner = dinner_options[0]
        snack = snack_options[0]
        
        total_carbs = breakfast["carbs"] + lunch["carbs"] + dinner["carbs"] + snack["carbs"]
        total_protein = breakfast["protein"] + lunch["protein"] + dinner["protein"] + snack["protein"]
        total_calories = breakfast["calories"] + lunch["calories"] + dinner["calories"] + snack["calories"]
        
        # Calcular porción de insulina si es tipo 1
        insulin_info = {}
        if diabetes_type.lower() == "tipo1":
            # Asumiendo ratio 1:15
            insulin_for_carbs = round(total_carbs / 15)
            insulin_info = {
                "estimated_insulin_units": insulin_for_carbs,
                "note": "Consulta tu ratio insulina:carbohidrato específico"
            }
        
        return {
            "breakfast": breakfast["name"],
            "breakfast_carbs": breakfast["carbs"],
            "lunch": lunch["name"],
            "lunch_carbs": lunch["carbs"],
            "dinner": dinner["name"],
            "dinner_carbs": dinner["carbs"],
            "snack": snack["name"],
            "snack_carbs": snack["carbs"],
            "total_carbs": total_carbs,
            "total_protein": total_protein,
            "total_calories": total_calories,
            "insulin": insulin_info
        }
    
    @staticmethod
    def get_health_tips(diabetes_type: str, age: int, bmi: float) -> List[str]:
        """
        Proporciona consejos de salud personalizados
        
        Args:
            diabetes_type: Tipo de diabetes
            age: Edad del usuario
            bmi: Índice de masa corporal
            
        Returns:
            Lista de consejos personalizados
        """
        tips = []
        
        # Consejos por tipo de diabetes
        if diabetes_type.lower() == "tipo1":
            tips.append("✓ Monitorea tu glucosa 4-10 veces al día")
            tips.append("✓ Lleva siempre glucosa rápida para hipoglucemias")
            tips.append("✓ Cuenta carbohidratos para cada comida")
            tips.append("✓ Inyecta insulina según plan médico")
        else:
            tips.append("✓ Aumenta actividad física: 150 min/semana mínimo")
            tips.append("✓ Reduce carbohidratos refinados")
            tips.append("✓ Toma medicamentos según prescripción")
            tips.append("✓ Controla presión arterial regularmente")
        
        # Consejos por edad
        if age > 60:
            tips.append("✓ Exámenes de salud más frecuentes (cada 3 meses)")
            tips.append("✓ Protege tu vista: oftalmólogo anualmente")
            tips.append("✓ Revisa tus pies diariamente")
        
        # Consejos por BMI
        if bmi > 30:
            tips.append("✓ Objetivo: Perder 5-10% del peso actual")
            tips.append("✓ Consulta nutricionista para plan personalizado")
            tips.append("✓ Aumenta consumo de verduras y fibra")
        elif bmi < 18.5:
            tips.append("✓ Aumenta ingesta calórica con alimentos saludables")
            tips.append("✓ Consulta con nutricionista")
        
        # Consejos generales
        tips.append("✓ Duerme 7-9 horas diarias")
        tips.append("✓ Maneja estrés: meditación, yoga")
        tips.append("✓ Evita alcohol y cigarrillos")
        tips.append("✓ Bebe al menos 2 litros de agua diaria")
        tips.append("✓ Revisa glucosa después de ejercicio")
        
        return tips
    
    @staticmethod
    def calculate_carbs_in_meal(ingredients: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Calcula carbohidratos en una comida
        
        Args:
            ingredients: Lista de dict con 'name' y 'grams'
            
        Returns:
            Total de carbohidratos y porción de insulina
        """
        # Base de datos de carbohidratos (g per 100g)
        carb_database = {
            "pan": 49,
            "arroz": 28,
            "pasta": 25,
            "plátano": 27,
            "manzana": 25,
            "papa": 17,
            "batata": 20,
            "leche": 5,
            "yogur": 3.5,
        }
        
        total_carbs = 0
        for ingredient in ingredients:
            name = ingredient.get("name", "").lower()
            grams = ingredient.get("grams", 0)
            
            # Buscar en base de datos
            carb_per_100g = next((carb_database[k] for k in carb_database if k in name), 0)
            total_carbs += (grams * carb_per_100g / 100)
        
        insulin_portions = round(total_carbs / 15)
        
        return {
            "total_carbs": round(total_carbs),
            "carb_portions": insulin_portions,
            "estimated_insulin_units": insulin_portions  # asumiendo ratio 1:15
        }


# Funciones helper para llamar desde LangChain
def tool_calculate_bmi(weight_kg: float, height_cm: float) -> str:
    result = DiabetesTools.calculate_bmi(weight_kg, height_cm)
    return json.dumps(result, ensure_ascii=False, indent=2)

def tool_get_health_tips(diabetes_type: str, age: int, bmi: float) -> str:
    tips = DiabetesTools.get_health_tips(diabetes_type, age, bmi)
    return "\n".join(tips)

def tool_generate_menu(
    diabetes_type: str,
    weight_kg: float,
    age: int,
    sex: str,
    favorite_ingredients: str,
    restrictions: str = ""
) -> str:
    fav_list = [i.strip() for i in favorite_ingredients.split(",")]
    rest_list = [i.strip() for i in restrictions.split(",")] if restrictions else []
    
    result = DiabetesTools.generate_menu_day(
        diabetes_type, weight_kg, age, sex, fav_list, rest_list
    )
    return json.dumps(result, ensure_ascii=False, indent=2)

def tool_estimate_insulin(weight_kg: float, diabetes_type: str = "tipo1") -> str:
    result = DiabetesTools.estimate_insulin_dosage(weight_kg, diabetes_type)
    return json.dumps(result, ensure_ascii=False, indent=2)

def tool_carb_recommendation(diabetes_type: str, weight_kg: float, activity_level: str = "moderado") -> str:
    result = DiabetesTools.carbohydrate_intake_recommendation(diabetes_type, weight_kg, activity_level)
    return json.dumps(result, ensure_ascii=False, indent=2)
