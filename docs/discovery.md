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
