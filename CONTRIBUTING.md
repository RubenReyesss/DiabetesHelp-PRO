# Guía de Contribución

Gracias por interesarte en contribuir a DiabetesHelp PRO. Este documento proporciona directrices para contribuir al proyecto.

## Código de Conducta

Esperamos que todos los contribuyentes sigan nuestro código de conducta implícito:
- Sé respetuoso con otros
- Sé inclusivo y acogedor
- Enfócate en lo mejor para la comunidad
- Ten paciencia y sé comprensivo

## ¿Cómo Contribuir?

### Reportar Bugs

Antes de crear un reporte de bug, verifica la lista de issues existentes ya que el bug podría ya estar reportado.

Cuando reportes un bug, incluye:
- **Título claro y descriptivo**
- **Descripción detallada** del comportamiento anormal
- **Pasos exactos para reproducir** el problema
- **Comportamiento actual**: Lo que ves actualmente
- **Comportamiento esperado**: Lo que deberías ver
- **Screenshots o GIFs** si es aplicable
- **Tu entorno**: Sistema operativo, versión de Python, etc.

### Sugerir Mejoras

Las sugerencias de mejora son siempre bienvenidas. Para crear una sugerencia:
- Usa un **título claro y descriptivo**
- Proporciona una **descripción detallada** de la mejora
- Explica **por qué** esta mejora sería útil
- Lista **ejemplos similares** de otras aplicaciones

### Pull Requests

- Fork el repositorio
- Crea una rama para tu feature (`git checkout -b feature/NuevaFuncion`)
- Realiza tus cambios
- Asegúrate de que el código siga el estilo del proyecto
- Commit tus cambios (`git commit -m 'Agregar nueva función'`)
- Push a la rama (`git push origin feature/NuevaFuncion`)
- Abre un Pull Request con descripción clara

#### Guía de PR

Tu PR debe incluir:
- Descripción clara de cambios
- Referencia a issue relacionado (si existe)
- Tests si aplica
- Documentación actualizada

## Estilo de Código

- Sigue [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usa nombres descriptivos para variables y funciones
- Agrega comentarios para código complejo
- Incluye docstrings en funciones/clases

### Ejemplo de Función

```python
def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
    """
    Calcula el Índice de Masa Corporal.
    
    Args:
        weight_kg: Peso en kilogramos
        height_cm: Altura en centímetros
        
    Returns:
        Diccionario con IMC y categoría
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return {
        "bmi": round(bmi, 2),
        "category": categorize_bmi(bmi)
    }
```

## Documentación Médica

Si contribuyes con nuevos documentos médicos:

1. **Verifica fuentes**: Solo información de:
   - American Diabetes Association (ADA)
   - European Association for the Study of Diabetes (EASD)
   - Publicaciones médicas revisadas por pares
   - Guías clínicas oficiales

2. **Formato**: Usa Markdown con estructura clara
3. **Disclaimers**: Incluye avisos de que es educativo
4. **Referencias**: Cita fuentes cuando sea posible

### Estructura de Documento Médico

```markdown
# Tema Médico

## Introducción
Breve descripción del tema

## Sección 1
Contenido detallado

## Referencias
- Fuente 1
- Fuente 2

---
**Nota**: Esta información es educativa solamente.
```

## Proceso de Desarrollo

1. **Desarrollo local**
   ```bash
   git clone https://github.com/tu-usuario/DiabetesHelp-PRO.git
   cd DiabetesHelp-PRO
   python -m venv venv
   source venv/bin/activate  # o venv\Scripts\activate en Windows
   pip install -r requirements.txt
   ```

2. **Pruebas**
   ```bash
   python -m pytest
   ```

3. **Linting**
   ```bash
   flake8 src/
   ```

## Áreas donde Puedes Ayudar

- 🐛 **Reportar y fijar bugs**
- 📚 **Mejorar documentación**
- 🌐 **Traducciones**
- 📝 **Documentos médicos nuevos**
- ✨ **Nuevas características**
- 🧪 **Tests y QA**
- 🎨 **Mejoras UI/UX**

## Preguntas?

- Abre un issue con la etiqueta `question`
- Lee la [documentación](README.md)
- Consulta [API OpenRouter](https://openrouter.ai/docs)

## Licencia

Al contribuir, aceptas que tus cambios se publiquen bajo la licencia MIT.

---

¡Gracias por contribuir a DiabetesHelp PRO! 🙏
