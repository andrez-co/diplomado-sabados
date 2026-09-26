# 📘 Scrum + TBD Playbook
> **Adaptación de Scrum a entornos de Despliegue Continuo y Trunk-Based Development (TBD)**  
> *Artefacto vivo y operativo de trabajo en equipo*

---

## 🎯 1. Propósito y Contexto
Este Playbook establece los acuerdos de trabajo, responsabilidades, adaptación de ceremonias y criterios de calidad para que el equipo opere bajo el marco **Scrum** alineado con **Trunk-Based Development (TBD)** y **Despliegue Continuo (CD)**.

* **Objetivo:** Garantizar que la rama `main` esté **siempre verde, estable y potencialmente desplegable (releasable)** en cualquier momento, reduciendo los tiempos de ciclo y eliminando el miedo al despliegue.

---

## 🚦 2. Diagnóstico del Flujo Actual (Mapa de Fricciones)
*Dinámica inicial del taller para identificar cuellos de botella y áreas de mejora.*

```mermaid
flowchart LR
    A[Commit local] --> B[Short-Lived PR]
    B --> C[CI Automatizado]
    C --> D[Peer Review]
    D --> E[Merge a main]
    E --> F[Imagen Docker / Build]
    F --> G[Continuous Deploy / Toggle]
```

### Semáforo de Salud del Flujo
| Estado | Elemento del Flujo | Observaciones / Aprendizajes |
| :--- | :--- | :--- |
| 🟢 **Funciona Bien** | *Ej. Tests unitarios rápidos en local* | *Registrar lo que ya aporta valor y estabilidad* |
| 🟡 **Genera Fricción** | *Ej. Esperas prolongadas en Code Review* | *Puntos a optimizar con PRs más pequeños* |
| 🔴 **Rompe Flujo / Miedo** | *Ej. Merge conflicts masivos por ramas largas* | *Eliminar con integración diaria a `main`* |

> **Preguntas Clave del Equipo:**
> 1. *¿Cuánto tiempo vive normalmente una rama de desarrollo en nuestro repo?* (Meta TBD: `< 24 horas`).
> 2. *¿Qué tan seguido integramos realmente a `main`?* (Meta: al menos 1 vez al día por desarrollador).
> 3. *¿Nuestro Definition of Done (DoD) actual garantiza que `main` es desplegable a producción?*

---

## 🧭 3. Los 5 Principios de Oro (Scrum + TBD)
1. **`main` es Sagrado y Siempre Releasable:** Ningún cambio que rompa pruebas o la compilación permanece en `main`. Si `main` se rompe, arreglarlo es la prioridad #1 de todo el equipo.
2. **Small Batches (Lotes Pequeños):** Dividir el trabajo en rebanadas verticales (*slicing*) tan pequeñas que puedan integrarse en cuestión de horas, no días.
3. **Desacoplar Despliegue de Liberación (*Deploy vs Release*):** Usar **Feature Toggles / Flags** para desplegar código incompleto a producción de forma segura sin exponerlo a los usuarios finales.
4. **Calidad Integrada en el Pipeline (CI como Árbitro):** Las pruebas automatizadas, linters y análisis de seguridad son los guardianes de la calidad antes y después del merge.
5. **Responsabilidad Colectiva:** Todo el equipo es dueño de la estabilidad de producción y de la fluidez del pipeline.

---

## 👥 4. Roles Adaptados a TBD + Continuous Deployment

```
┌────────────────────────────────────────────────────────────────────────┐
│                        RESPONSABILIDADES DE ROL                        │
├─────────────────┬────────────────────────────┬─────────────────────────┤
│  Product Owner  │         Developers         │      Scrum Master       │
│                 │                            │                         │
│ • Prioriza por  │ • Mantienen main verde     │ • Facilita disciplina   │
│   valor y batch │ • Lotes pequeños (<24h)    │   de integración diaria │
│ • Define flags  │ • Ownership del pipeline CI│ • Elimina el miedo a    │
│ • Slicea con el │ • Monitorean producción    │   romper main           │
│   equipo        │ • Fast Code Reviews        │ • Protege tiempo CI/CD  │
└─────────────────┴────────────────────────────┴─────────────────────────┘
```

### Compromisos Individuales (*Post-its del Taller*)
> *"Una cosa concreta que voy a hacer diferente en mi rol a partir de mañana"*

* **Product Owner:**
  * [ ] *Ejemplo:* Dividir historias de usuario en entregas con Feature Toggles definidos en el refinamiento.
  * [ ] *(Espacio para compromiso del PO)*
* **Developers:**
  * [ ] *Ejemplo:* No dejar ninguna rama viva más de 24 horas e integrar con PRs de menos de 200 líneas.
  * [ ] *(Espacio para compromiso del Developer 1)*
  * [ ] *(Espacio para compromiso del Developer 2)*
* **Scrum Master:**
  * [ ] *Ejemplo:* Monitorear en las Dailies si hay ramas estancadas y facilitar la revisión inmediata de PRs.
  * [ ] *(Espacio para compromiso del SM)*

---

## 🔄 5. Artefactos y Ceremonias: Clásico vs. TBD + CD

| Artefacto / Ceremonia | Versión Clásica | Adaptación TBD + CD | Guía de Acción en el Equipo |
| :--- | :--- | :--- | :--- |
| **Product Backlog** | Lista de historias grandes por funcionalidad completa. | Historias sliceadas + plan de **Feature Toggles** + Criterios de Aceptación verificables en producción. | Escribir historias pensadas en activación progresiva (*Dark launching / Toggles*). |
| **Sprint Backlog** | Compromiso de paquetes cerrados de trabajo al final del sprint. | Flujo de trabajo continuo que se integra a `main` diariamente en micro-incrementos. | Medir rendimiento por *Cycle Time* y estabilidad de ramas en lugar de estimaciones rígidas. |
| **Incremento** | Paquete de software entregable solo al final del Sprint. | **Cada commit en `main` que pasa CI es un Incremento potencial listo para producción.** | El valor se entrega continuamente a lo largo del Sprint. |
| **Sprint Planning** | Planificación enfocada en estimar puntos de historia. | Planificación enfocada en **estrategia de Slicing y arquitectura de flags**. | Definir cómo entrará cada historia a `main` sin romper funcionalidades existentes. |
| **Daily Scrum** | "¿Qué hice ayer? ¿Qué haré hoy? ¿Qué impedimentos tengo?" | **"¿Qué voy a integrar hoy a `main` y qué necesito del equipo para que sea seguro y rápido?"** | Foco total en destrabar PRs y mantener `main` verde. |
| **Sprint Review** | Demo tradicional en ambiente local o staging del trabajo acumulado. | **Demo de lo que ya está (o puede estar) en producción con feedback real y métricas.** | Demostrar activación/desactivación de features en vivo usando Feature Flags. |
| **Sprint Retrospective** | Enfoque exclusivo en dinámicas de equipo y comunicación. | **Mejora del flujo de valor + salud del pipeline + disciplina de TBD + métricas DORA.** | Analizar fallos de CI, tiempo de vida de ramas y tiempos de code review. |

---

## ✅ 6. Definition of Done (DoD) Adaptada

Para que una historia o tarea se considere **Done**, debe cumplir con:

### ⚙️ Criterios Técnicos
- [ ] Código desarrollado en una rama de vida corta (< 24h).
- [ ] Pruebas unitarias e integración añadidas y pasando en local y en CI.
- [ ] Linter y análisis estático aprobados sin warnings críticos.
- [ ] Code Review aprobado por al menos 1 par (enfocado en cambios pequeños).
- [ ] **Merged a `main` exitosamente y pipeline de CI en verde.**
- [ ] Si la funcionalidad está incompleta: protegida detrás de un **Feature Flag**.

### 💼 Criterios de Negocio y Operación
- [ ] Criterios de Aceptación validados con el Product Owner.
- [ ] Feature Flag configurado y testeado en apagado/encendido (*Dark Launching*).
- [ ] Logs y métricas básicas implementadas para observar el comportamiento.
- [ ] Documentación técnica o de API actualizada si aplica.

---

## 🛠️ 7. Dinámica: "Traduce tu Realidad" (Template de Slicing)
*Utilizar esta plantilla para descomponer historias grandes en rebanadas aptas para TBD.*

### 📋 Ficha de Historia Sliceada
```markdown
### Historia: [Nombre de la Historia]

#### 1. Rebanada 1 (Día 1):
* **Alcance:** Creación del endpoint base + modelo de datos (sin UI activa).
* **Estrategia TBD / Flag:** `FLAG_NUEVA_FUNCIONALIDAD = False`
* **Criterio de Verificación:** Test unitario + Test de integración pasando en CI.

#### 2. Rebanada 2 (Día 2):
* **Alcance:** Conexión con lógica de negocio y validaciones.
* **Estrategia TBD / Flag:** Flag activo solo para usuarios internos / staging.
* **Criterio de Verificación:** Pruebas E2E y validación con PO.

#### 3. Rebanada 3 (Día 3 - Release):
* **Alcance:** Interfaz de usuario final expuesta.
* **Estrategia TBD / Flag:** Activación del Flag al 100% de los usuarios.
* **Criterio de Verificación:** Métricas de uso y telemetría estables en producción.
```

---

## 📌 8. Acuerdos Técnicos y Decisiones Pendientes

| Tema | Estado / Decisión | Responsable | Fecha Límite |
| :--- | :--- | :--- | :--- |
| **Branch Protection Rules** | Bloquear push directo a `main`, exigir CI verde y 1 aprobación. | Tech Lead / DevOps | Inmediato |
| **Gestor de Feature Flags** | Evaluar ConfigCat / Unleash / Flags por Variables de Entorno. | Equipo de Desarrollo | Próximo Sprint |
| **Pipeline CI (GitHub Actions)**| Automatizar lint, pytest, build Docker en cada PR. | DevOps / Developers | En progreso |
| **Métricas DORA** | Medir *Deployment Frequency* y *Lead Time for Changes*. | Scrum Master | Sprint + 1 |

---

## 🚀 9. Regla de Emergencia: `main` roto
Si un commit en `main` rompe el pipeline de CI:
1. **Detener nuevos merges:** Nadie integra a `main` hasta que esté resuelto.
2. **Regla de los 10 minutos:** Si el fix no se encuentra en 10 minutos, se hace **`git revert`** del commit causante de inmediato.
3. **Investigar en local:** El desarrollador soluciona el problema en su entorno antes de volver a intentar el PR.
