# 🚀 Guía: Subir a GitHub

## Paso 1: Crear Repositorio en GitHub

1. Ir a [github.com/new](https://github.com/new)
2. **Repository name**: `DiabetesHelp-PRO` (o nombre profesional)
3. **Description**: "AI-powered diabetes assistant with RAG system and Mistral-7B"
4. **Visibility**: Public (para portafolio) o Private (si prefieres)
5. **NO** inicializar con README (ya tienes uno)
6. **NO** agregar .gitignore (ya tienes uno)
7. Clic en "Create repository"

## Paso 2: Agregar Remote a tu Repositorio Local

```bash
cd "c:\Users\Ruben Reyes\Desktop\DiabetesHelp"

# Reemplaza 'tuUsuario' con tu usuario de GitHub
git remote add origin https://github.com/tuUsuario/DiabetesHelp-PRO.git

# Renombrar rama a 'main' (estándar moderno)
git branch -M main

# Verificar remote
git remote -v
```

## Paso 3: Subir a GitHub

```bash
# Subir rama main
git push -u origin main

# Verificar que se subió correctamente
git log --oneline
```

## Paso 4: Verificar en GitHub

1. Ir a https://github.com/tuUsuario/DiabetesHelp-PRO
2. Deberías ver todos tus archivos
3. Verificar que .env NO está (debe estar en .gitignore)
4. El README debe mostrarse en la página principal

## Paso 5: Agregar Topics (Etiquetas)

En la página del repositorio en GitHub:
1. Clic en "Settings"
2. Buscar "Topics"
3. Agregar: `diabetes`, `ai`, `rag`, `mistral`, `openrouter`, `gradio`, `healthcare`

## Paso 6: Crear Releases

```bash
# Crear tag para v1.0.0
git tag -a v1.0.0 -m "DiabetesHelp PRO v1.0.0 - Initial release"

# Subir tags
git push origin v1.0.0
```

Luego en GitHub:
1. Ir a "Releases"
2. Clic en "Create release from tag"
3. Agregar descripción y cambios

## Estructura de Branches (Recomendado)

```
main
  ↑
  └── develop (para desarrollo)
       ↑
       ├── feature/chat-improvements
       ├── feature/new-documents
       └── bugfix/rag-search
```

## Flujo de Trabajo para Futuras Contribuciones

```bash
# Crear rama de feature
git checkout -b feature/nueva-funcion

# Hacer cambios y commits
git add .
git commit -m "Agregar nueva función"

# Subir rama
git push origin feature/nueva-funcion

# En GitHub: Abrir Pull Request
# Después de review: Merge a main
```

## Proteger la Rama Main (Recomendado)

En GitHub Settings → Branches:
1. Add rule
2. Branch name pattern: `main`
3. Require pull request reviews: ✓ (al menos 1)
4. Require status checks to pass: ✓
5. Require branches to be up to date: ✓

## Configurar Actions (CI/CD)

El archivo `.github/workflows/tests.yml` ya está creado.

Para activarlo:
1. Ir a "Actions" en GitHub
2. Debería activarse automáticamente
3. Los tests correrán en cada push

## Credenciales Seguras

**IMPORTANTE**: Nunca subas:
- `.env` (está en .gitignore ✓)
- `*.pem` (claves SSH)
- `credentials.json`
- `secrets.json`

## Personalización del Repositorio

### README Badge
Agregar al README.md:
```markdown
[![GitHub stars](https://img.shields.io/github/stars/tuUsuario/DiabetesHelp-PRO.svg)](https://github.com/tuUsuario/DiabetesHelp-PRO/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/tuUsuario/DiabetesHelp-PRO.svg)](https://github.com/tuUsuario/DiabetesHelp-PRO/issues)
```

### Metadata en GitHub

En `setup.py` (si decides crear uno):
```python
setup(
    name='DiabetesHelp-PRO',
    version='1.0.0',
    author='Tu Nombre',
    author_email='tu-email@example.com',
    description='AI-powered diabetes assistant',
    url='https://github.com/tuUsuario/DiabetesHelp-PRO',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
```

## Nombrar Commits Correctamente

Sigue este patrón:

```
feat: Nueva característica
fix: Corrección de bug
docs: Cambios en documentación
style: Cambios en formato/estilo
refactor: Refactorización sin cambios funcionales
perf: Mejoras de rendimiento
test: Agregación/cambio de tests
ci: Cambios en CI/CD
chore: Cambios en configuración
```

Ejemplos:
```bash
git commit -m "feat: Add chat with full user context"
git commit -m "fix: RAG not loading on startup"
git commit -m "docs: Update README with usage examples"
git commit -m "refactor: Simplify RAGSystem search"
```

## Alternativas de Nombres de Repositorio

Si `DiabetesHelp-PRO` no es lo que quieres:

- `AI-Diabetes-Assistant`
- `MistralDiabetes`
- `DiabetesRAG`
- `HealthAI-Diabetes`
- `DiaHelper-AI`
- `GlucoseAssistant`
- `EndoAI`
- `DiabetesPRO` (más simple)

## Verificar Todo Antes de Subir

```bash
# Ver estado actual
git status

# Ver logs
git log --oneline

# Ver remotes
git remote -v

# Listar archivos que serán commiteados
git ls-files
```

## Después de Subir

1. **Compartir en redes**:
   - LinkedIn
   - Twitter
   - GitHub Discussions

2. **Documentación extra**:
   - Crear Wiki en GitHub
   - Crear Discussions para Q&A

3. **Considerar**:
   - PyPI package
   - Docker image
   - Documentación en ReadTheDocs

---

## Comandos Útiles Resumen

```bash
# Ver remotes
git remote -v

# Cambiar remote
git remote set-url origin https://github.com/newuser/repo.git

# Ver branches
git branch -a

# Ver commits
git log --oneline --graph --all

# Sincronizar con main
git fetch origin
git rebase origin/main

# Deshacer último commit (no subido)
git reset --soft HEAD~1

# Ver cambios
git diff
git diff --staged
```

---

**Listo! Tu repositorio está preparado para GitHub 🚀**

Para preguntas: Consulta [GitHub Docs](https://docs.github.com/)
