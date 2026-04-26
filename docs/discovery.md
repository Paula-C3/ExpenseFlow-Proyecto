# Discovery — ExpenseFlow (Plataforma de aprobación de gastos)

## 1. Resumen Ejecutivo

La empresa actualmente gestiona solicitudes de gastos y reembolsos de forma manual mediante correos electrónicos, lo que genera problemas de trazabilidad, duplicación de solicitudes y falta de visibilidad sobre el estado de cada gasto.

Los usuarios principales del sistema son empleados, managers y el equipo de finanzas, quienes participan en la creación, revisión y aprobación de gastos.

El principal dolor del negocio es que el área de finanzas no tiene claridad sobre qué gastos están pendientes, quién los aprobó, si cumplen con las políticas y si ya fueron procesados o pagados.

El objetivo del MVP es construir una plataforma centralizada que permita registrar solicitudes de gasto, gestionar su flujo de aprobación, mantener trazabilidad completa, notificar a los usuarios en cada etapa y visualizar el estado de cada solicitud.

---

## 2. Contexto del Negocio

Actualmente, el proceso funciona de manera manual utilizando correo electrónico como principal herramienta:

1. El empleado envía un correo con la solicitud de gasto y su comprobante.
2. Copia al manager en el correo.
3. El manager revisa manualmente y responde.
4. Finanzas revisa posteriormente el gasto.
5. No existe un sistema centralizado para registrar ni hacer seguimiento.

Problemas del proceso actual:

- Las solicitudes se pierden en cadenas de correo.
- Existen gastos duplicados.
- No hay un historial claro de aprobaciones.
- No hay control de estados del proceso.
- No existen validaciones automáticas (montos, comprobantes, reglas).
- No hay trazabilidad de quién tomó cada decisión.

Herramientas actuales:
- Correo electrónico
- Procesos manuales (posiblemente hojas de cálculo)

---

## 3. Usuarios y Roles

### Employee
- Crea solicitudes de gasto.
- Adjunta comprobantes.
- Consulta el estado de sus solicitudes.
- No puede aprobar gastos.

### Manager
- Revisa solicitudes de su equipo.
- Aprueba o rechaza gastos según reglas de monto.
- No puede aprobar su propio gasto.

### Finance Analyst
- Revisa comprobantes.
- Procesa solicitudes aprobadas.
- Puede solicitar cambios si falta información.

### Finance Admin
- Revisa gastos de alto monto.
- Da aprobación final en casos críticos.
- Cierra solicitudes.

### System Admin
- Gestiona usuarios y permisos del sistema.

---

## 4. Requerimientos Funcionales

RF-01: El sistema debe permitir a un empleado crear una solicitud de gasto.

RF-02: El sistema debe permitir registrar información del gasto (monto, categoría, descripción).

RF-03: El sistema debe permitir adjuntar un comprobante (URL, nombre de archivo o referencia).

RF-04: El sistema debe permitir enviar una solicitud para revisión.

RF-05: El sistema debe permitir a un manager aprobar o rechazar solicitudes según el monto.

RF-06: El sistema debe permitir a finanzas revisar solicitudes aprobadas.

RF-07: El sistema debe permitir solicitar cambios si falta información o comprobante.

RF-08: El sistema debe cambiar el estado de la solicitud según el flujo definido.

RF-09: El sistema debe notificar a los usuarios en eventos importantes (envío, aprobación, rechazo, cambios).

RF-10: El sistema debe permitir marcar una solicitud como pagada (sin procesar dinero real).

RF-11: El sistema debe registrar un historial (auditoría) de todas las acciones realizadas.

RF-12: El sistema debe validar que el monto sea mayor a 0.

RF-13: El sistema debe evitar que un usuario apruebe su propio gasto.

RF-14: El sistema debe aplicar reglas de aprobación según el monto:
- <= 50 USD: no requiere aprobación de manager, pero sí revisión de finanzas.
- > 50 USD y <= 500 USD: requiere aprobación de manager.
- > 500 USD: requiere aprobación de manager y finance admin.

RF-15: El sistema debe permitir que una solicitud sin comprobante pase a estado de cambios solicitados en lugar de ser rechazada automáticamente.

RF-16: El sistema debe advertir sobre posibles gastos duplicados basándose en monto, fecha y categoría.

RF-17: El sistema debe cerrar automáticamente una solicitud cuando es rechazada.

---

## 5. Requerimientos No Funcionales

### Seguridad
- El sistema debe requerir autenticación de usuarios.
- Debe existir control de acceso basado en roles.
- Un usuario no puede aprobar su propio gasto.

### Trazabilidad
- Todas las acciones deben registrarse (usuario, fecha, acción).
- Debe existir un historial completo de cada solicitud.

### Usabilidad
- La interfaz debe ser simple e intuitiva.
- El usuario debe poder ver fácilmente el estado de sus solicitudes.

### Mantenibilidad
- El sistema debe estar estructurado en capas (domain, application, infrastructure).
- Debe ser fácil de extender con nuevas reglas de negocio.

### Observabilidad
- El sistema debe registrar eventos importantes del flujo.
- Debe permitir monitorear errores o fallos.

### Ambientes
- Debe existir separación entre ambientes de desarrollo (dev) y producción (prod).
- El despliegue debe realizarse mediante procesos automatizados (CI/CD).

---

## 6. Reglas de negocio

| ID    | Regla |
|-------|-------|
| RN-01 | Gastos **≤ 50 USD** no requieren aprobación del Manager; pasan directamente a revisión de Finance Analyst. |
| RN-02 | Gastos **> 50 USD y ≤ 500 USD** requieren aprobación del Manager antes de pasar a Finance Review. |
| RN-03 | Gastos **> 500 USD** requieren aprobación del Manager **y** del Finance Admin. |
| RN-04 | Todo gasto debe incluir un comprobante (URL, nombre de archivo o referencia). Si falta, la solicitud pasa a `CHANGES_REQUESTED`; no se rechaza automáticamente. |
| RN-05 | Un empleado **no puede aprobar su propio gasto** (conflicto de interés). |
| RN-06 | Una solicitud **rechazada queda cerrada**; no puede reabrirse ni transicionar a otro estado. |
| RN-07 | El monto de un gasto debe ser **mayor a 0**. |
| RN-08 | Los campos **categoría** y **descripción** son obligatorios al crear una solicitud. |
| RN-09 | Una solicitud aprobada por todos los niveles requeridos pasa automáticamente a `READY_FOR_PAYMENT`. |
| RN-10 | El sistema debe **advertir** (sin bloquear) si ya existe un gasto similar por monto, fecha y categoría. |
| RN-11 | El MVP **no procesa dinero real**. Finance Analyst puede marcar una solicitud como `PAID` manualmente. |

---

## 7. Estados del flujo principal

La entidad principal es **ExpenseRequest** (solicitud de gasto).

```
DRAFT → SUBMITTED → [MANAGER_REVIEW] → FINANCE_REVIEW → READY_FOR_PAYMENT → PAID
                           ↓                  ↓
                    CHANGES_REQUESTED  CHANGES_REQUESTED
                           ↓                  ↓
                        REJECTED           REJECTED
                                         CANCELLED (por el empleado)
```

> **Nota:** El paso por `MANAGER_REVIEW` depende del monto (RN-01, RN-02, RN-03).

| Estado | Descripción | Quién puede actuar |
|--------|-------------|-------------------|
| `DRAFT` | Solicitud creada pero no enviada. Solo visible para el Employee. | Employee |
| `SUBMITTED` | Solicitud enviada al flujo de aprobación. | Sistema |
| `MANAGER_REVIEW` | Esperando aprobación del Manager (solo si monto > 50 USD). | Manager |
| `FINANCE_REVIEW` | En revisión por Finance Analyst. | Finance Analyst |
| `CHANGES_REQUESTED` | Se detectó un problema (falta comprobante u otro). El Employee debe corregir y reenviar. | Employee |
| `READY_FOR_PAYMENT` | Todos los niveles aprobaron. Pendiente de pago. | Finance Analyst / Finance Admin |
| `PAID` | Marcado manualmente como pagado. Estado final. | Finance Analyst |
| `REJECTED` | Rechazada. Estado final, no reabre. | — |
| `CANCELLED` | Cancelada por el Employee antes de ser procesada. Estado final. | Employee |

### Transiciones válidas

| Desde | Hacia | Condición |
|-------|-------|-----------|
| `DRAFT` | `SUBMITTED` | Employee envía la solicitud |
| `SUBMITTED` | `MANAGER_REVIEW` | Monto > 50 USD |
| `SUBMITTED` | `FINANCE_REVIEW` | Monto ≤ 50 USD |
| `MANAGER_REVIEW` | `FINANCE_REVIEW` | Manager aprueba |
| `MANAGER_REVIEW` | `CHANGES_REQUESTED` | Falta comprobante u otro problema |
| `MANAGER_REVIEW` | `REJECTED` | Manager rechaza |
| `FINANCE_REVIEW` | `READY_FOR_PAYMENT` | Finance aprueba (+ Finance Admin si monto > 500 USD) |
| `FINANCE_REVIEW` | `CHANGES_REQUESTED` | Finance solicita corrección |
| `FINANCE_REVIEW` | `REJECTED` | Finance rechaza |
| `CHANGES_REQUESTED` | `SUBMITTED` | Employee corrige y reenvía |
| `READY_FOR_PAYMENT` | `PAID` | Finance Analyst marca como pagado |
| `DRAFT` / `SUBMITTED` | `CANCELLED` | Employee cancela |

### Transiciones inválidas

- `PAID`, `REJECTED`, `CANCELLED` → cualquier otro estado (son estados finales).
- Employee no puede mover una solicitud desde `MANAGER_REVIEW` o `FINANCE_REVIEW`.
- No se puede saltar `MANAGER_REVIEW` si el monto lo requiere.

---

## 8. Eventos del sistema

| Evento | Cuándo ocurre | Quién lo dispara | Datos relevantes | Notificación | Auditoría |
|--------|--------------|-----------------|-----------------|:-----------:|:--------:|
| `EXPENSE_CREATED` | Employee crea la solicitud en DRAFT | Employee | expense_id, amount, category, employee_id | No | Sí |
| `EXPENSE_SUBMITTED` | Employee envía la solicitud | Employee | expense_id, amount, category, submitted_at | Sí | Sí |
| `MANAGER_APPROVAL_REQUIRED` | Solicitud entra a MANAGER_REVIEW | Sistema | expense_id, manager_id, amount | Sí | Sí |
| `FINANCE_REVIEW_REQUIRED` | Solicitud entra a FINANCE_REVIEW | Sistema | expense_id, analyst_id, amount | Sí | Sí |
| `EXPENSE_APPROVED` | Manager o Finance aprueba | Manager / Finance Analyst / Finance Admin | expense_id, approved_by, approved_at, level | Sí | Sí |
| `EXPENSE_REJECTED` | Manager o Finance rechaza | Manager / Finance Analyst | expense_id, rejected_by, reason, rejected_at | Sí | Sí |
| `CHANGES_REQUESTED` | Se piden correcciones al Employee | Manager / Finance Analyst | expense_id, requested_by, comment, requested_at | Sí | Sí |
| `EXPENSE_READY_FOR_PAYMENT` | Todos los niveles aprobaron | Sistema | expense_id, total_amount, approved_at | Sí | Sí |
| `EXPENSE_PAID` | Finance marca como pagado | Finance Analyst | expense_id, paid_by, paid_at | Sí | Sí |
| `EXPENSE_CANCELLED` | Employee cancela | Employee | expense_id, cancelled_by, cancelled_at | No | Sí |

---

## 9. Notificaciones

| Evento disparador | Destinatario | Canal | Prioridad |
|-------------------|-------------|-------|-----------|
| `MANAGER_APPROVAL_REQUIRED` | Manager del equipo | In-app | Alta |
| `FINANCE_REVIEW_REQUIRED` | Finance Analyst | In-app | Alta |
| `EXPENSE_APPROVED` | Employee solicitante | In-app | Media |
| `EXPENSE_REJECTED` | Employee solicitante | In-app | Alta |
| `CHANGES_REQUESTED` | Employee solicitante | In-app | Alta |
| `EXPENSE_READY_FOR_PAYMENT` | Finance Analyst, Finance Admin | In-app | Alta |
| `EXPENSE_PAID` | Employee solicitante | In-app | Media |

> **Canal MVP:** notificaciones in-app únicamente. Email e integraciones externas quedan fuera del alcance del MVP.

---

## 10. Alcance MVP

El MVP cubre el flujo completo de una solicitud de gasto desde su creación hasta el marcado como pagado:

- Autenticación de usuarios con roles (Employee, Manager, Finance Analyst, Finance Admin, System Admin).
- Crear solicitud de gasto con monto, categoría, descripción y comprobante (referencia de texto).
- Envío de solicitud por parte del Employee.
- Aprobación o rechazo por Manager (según monto).
- Revisión, aprobación o rechazo por Finance Analyst.
- Aprobación adicional por Finance Admin para gastos > 500 USD.
- Solicitud de cambios y reenvío corregido por el Employee.
- Marcado manual como `PAID` por Finance Analyst.
- Notificaciones in-app por eventos del flujo.
- Historial y auditoría de acciones sobre cada solicitud.
- Advertencia (no bloqueo) de posible gasto duplicado.
- Listado de solicitudes filtrado por rol del usuario.
- Vista de detalle por solicitud.

---

## 11. Fuera de alcance

Los siguientes elementos **no** se construirán en el MVP:

- Procesamiento de pagos o transferencias bancarias reales.
- Integración con sistemas bancarios o pasarelas de pago.
- OCR o lectura automática de comprobantes (fotos de recibos, facturas escaneadas).
- Carga real de archivos a cloud storage (solo referencia/URL en texto).
- Reportes financieros avanzados o dashboards analíticos.
- Reglas tributarias o cálculos de impuestos.
- Notificaciones por email o SMS.
- Aplicación móvil nativa.

---

## 12. Riesgos, supuestos y preguntas abiertas

### Riesgos

| ID   | Tipo | Descripción | Impacto |
|------|------|-------------|---------|
| R-01 | Alcance | La lógica de aprobación por monto puede crecer si el cliente define más niveles en el futuro. | Medio |
| R-02 | Negocio | Sin validación de comprobante real, un empleado puede enviar referencias falsas. | Bajo (aceptado en MVP) |
| R-03 | Técnico | Si el event bus falla, las notificaciones pueden perderse sin afectar el flujo de negocio. | Medio |
| R-04 | Alcance | El cliente puede pedir detección más estricta de duplicados (bloqueo en lugar de advertencia). | Bajo |
| R-05 | Negocio | Conflicto de interés si un Manager es también el solicitante — el sistema debe validarlo activamente. | Alto |

### Supuestos

- Cada Employee tiene exactamente un Manager asignado.
- El comprobante en el MVP es una referencia de texto (URL o nombre); no se sube archivo real.
- Solo existe un Finance Admin activo que aprueba gastos > 500 USD.
- El MVP no maneja múltiples monedas; todo es en USD.
- Las notificaciones in-app se muestran en el frontend; no se envían emails.
- Un gasto cancelado en `DRAFT` o `SUBMITTED` no genera notificación a terceros.

### Preguntas abiertas

| ID    | Pregunta | Responsable |
|-------|----------|-------------|
| PA-01 | ¿Puede un Manager rechazar un gasto que ya pasó a Finance Review si detecta un error? | Cliente |
| PA-02 | ¿Existe un tiempo límite para aprobar una solicitud antes de escalar automáticamente? | Cliente |
| PA-03 | ¿El Finance Admin puede también actuar como Finance Analyst en el mismo flujo? | Cliente |
| PA-04 | ¿El Employee puede ver el historial de solicitudes de otros empleados (solo lectura)? | Cliente |
| PA-05 | ¿La advertencia de duplicado solo muestra aviso o puede bloquear el envío bajo ciertas condiciones? | Equipo (decisión de diseño) |
