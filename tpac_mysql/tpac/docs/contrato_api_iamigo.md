# Contrato da API — IAmigo (tpac_mysql/tpac)

## Convenciones generales

| Tema | Regla |
|---|---|
| URL base (desarrollo) | `http://127.0.0.1:8000` |
| Documentación interactiva | `http://127.0.0.1:8000/docs` |
| Formato | JSON (`Content-Type: application/json`) |
| Autenticación | No hay. El front elige un perfil activo y usa su `id` en las rutas. |
| Éxito con contenido | `{"dados": ...}` |
| Éxito sin contenido | `204 No Content`, sin body |
| Error de negocio | `{"detail": "mensagem"}` |
| Error de validación de FastAPI | `422` con `{"detail": [ ... ]}` (lista). Ocurre si falta un campo obligatorio o un tipo es inválido, por ejemplo una fecha mal formada. |
| Fechas | Envío y respuesta en ISO: `prazo` como `AAAA-MM-DD`, `criado_em` como `AAAA-MM-DDTHH:MM:SS` |
| CORS | Orígenes permitidos por defecto: `http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, `http://127.0.0.1:5173`. Configurable con `CORS_ORIGINS` en `.env`. |

### Códigos de estado usados

| Código | Significado en esta API |
|---|---|
| `200` | Operación correcta con datos |
| `201` | Recurso creado |
| `204` | Recurso eliminado |
| `404` | Usuario, tarea o paso inexistente, **o que pertenece a otro usuario/tarea** |
| `422` | Regla de negocio incumplida o body inválido |
| `503` | El servicio de IA (Gemini) no está disponible |

### Objetos

**Usuario**
```json
{ "id": 6, "nome": "Matheus", "estilo_instrucao": "direto", "criado_em": "2026-09-22T21:50:02" }
```
- `estilo_instrucao`: `"direto"` o `"detalhado"`

**Tarefa**
```json
{
  "id": 4, "usuario_id": 6, "tipo": "tarefas_diarias", "titulo": "Arrumar a Casa",
  "descricao": null, "prioridade": "media", "prazo": null, "concluida": false,
  "criado_em": "2026-09-24T19:11:17"
}
```
- `tipo`: `"tarefas_diarias"` o `"tarefas_educacionais"`
- `prioridade`: `"baixa"`, `"media"` o `"alta"`

**Passo**
```json
{ "id": 9, "tarefa_id": 4, "texto": "Coletar lixo e itens soltos", "concluido": false, "ordem": 1 }
```

---

## usuarios
El front necesita listar los perfiles existentes, crear uno nuevo, editarlo o eliminarlo, y seleccionar el perfil activo con el que trabajará.

### GET /usuarios — Listar usuários
- **Estado:** FRONT-READY
- **Éxito:** `200` → `{"dados": [Usuario, ...]}`, ordenados por `nome`
- **Errores:** ninguno de negocio
- **Evidencia:** auditado con spot-check en `/docs` y SELECT en MySQL; coincidencia total entre API y banco. Cubierto por `tests/test_usuario_controller.py`.

### GET /usuarios/{usuario_id} — Buscar um usuário específico
- **Estado:** FRONT-READY
- **Éxito:** `200` → `{"dados": Usuario}`
- **Errores:** `404` "Usuário não encontrado."
- **Evidencia:** ruta nueva con `UsuarioService.buscar_usuario`, que reutiliza `buscar_por_id` del repository. Probado con `id=1` (200) y `id=9999` (404), confirmado con SELECT.

### POST /usuarios — Criar usuário
- **Estado:** FRONT-READY
- **Body:**
```json
{ "nome": "Ana", "estilo_instrucao": "direto" }
```
  `estilo_instrucao` es opcional (por defecto `"direto"`).
- **Éxito:** `201` → `{"dados": Usuario}` (incluye el `id` creado)
- **Errores (`422`):**
  - "O nome não pode ficar vazio."
  - "O nome precisa ter pelo menos 3 caracteres."
  - "O estilo deve ser 'direto' ou 'detalhado'."
  - "Já existe um perfil com esse nome."
- **Evidencia:** auditado probando las 4 validaciones en `/docs` y SELECT. Respuesta unificada al formato `{"dados": ...}` con `id`. Reglas cubiertas por `tests/test_usuario_service.py`.

### PUT /usuarios/{usuario_id} — Atualizar perfil
- **Estado:** FRONT-READY
- **Body:** (ambos campos obligatorios)
```json
{ "nome": "Matheus Silva", "estilo_instrucao": "detalhado" }
```
- **Éxito:** `200` → `{"dados": Usuario}`
- **Errores:**
  - `404` "Usuário não encontrado."
  - `422` con las mismas reglas de `POST /usuarios`. Mantener el propio nombre está permitido; usar el nombre de **otro** usuario devuelve "Já existe um perfil com esse nome."
- **Evidencia:** probado con éxito (200), usuario inexistente (404) y nombre vacío (422), confirmado con SELECT. Regla del propio nombre cubierta por `tests/test_usuario_service.py`.

### DELETE /usuarios/{usuario_id} — Excluir usuário
- **Estado:** FRONT-READY
- **Éxito:** `204`, sin body
- **Errores:** `404` "Usuário não encontrado."
- **⚠️ Importante:** por `ON DELETE CASCADE`, eliminar un usuario elimina también **todas sus tareas y pasos**. El front debería pedir confirmación antes de llamar a esta ruta.
- **Evidencia:** probado con un usuario descartable (204) e inexistente (404); SELECT confirmó que el usuario ya no existe.

---

## tarefas
Es el recurso central del producto: el front necesita listar las tareas de un usuario, crearlas y marcarlas o desmarcarlas como concluidas.

### GET /usuarios/{usuario_id}/tarefas — Listar tarefas do usuário
- **Estado:** FRONT-READY
- **Éxito:** `200` → `{"dados": [Tarefa, ...]}`, ordenadas por `id`. Lista vacía si el usuario no tiene tareas.
- **Errores:** `404` "Usuário não encontrado."
- **Evidencia:** ruta nueva con `TarefaController` → `TarefaService` → `TarefaRepository` (SQLAlchemy). Probado con usuario existente (200) e inexistente (404), confirmado con SELECT.

### POST /usuarios/{usuario_id}/tarefas — Criar tarefa
- **Estado:** FRONT-READY
- **Body:**
```json
{
  "tipo": "tarefas_diarias",
  "titulo": "Estudar SQL",
  "descricao": null,
  "prioridade": "media",
  "prazo": "2026-10-15"
}
```
  Obligatorios: `tipo`, `titulo`. Opcionales: `descricao` (null), `prioridade` (`"media"`), `prazo` (null, formato `AAAA-MM-DD`).
- **Éxito:** `201` → `{"dados": Tarefa}`
- **Errores:**
  - `404` "Usuário não encontrado."
  - `422` "O título não pode ficar vazio."
  - `422` "O tipo deve ser 'tarefas_diarias' ou 'tarefas_educacionais'."
  - `422` "A prioridade deve ser 'baixa', 'media' ou 'alta'."
  - `422` (lista de FastAPI) si `prazo` no tiene formato `AAAA-MM-DD`
- **Evidencia:** INSERT puntual vía SQLAlchemy, sin el `salvar_dados()` destructivo. Probado con éxito (201), usuario inexistente (404) y título vacío (422), confirmado con SELECT.

### PATCH /usuarios/{usuario_id}/tarefas/{tarefa_id} — Alternar status concluída
- **Estado:** FRONT-READY
- **Body:** ninguno. Cada llamada invierte `concluida` (`false` → `true` → `false`).
- **Éxito:** `200` → `{"dados": Tarefa}`
- **Errores:** `404` "Usuário não encontrado." o "Tarefa não encontrada." (también si la tarea pertenece a otro usuario)
- **Evidencia:** identifica la tarea por `id` de banco, no por índice de lista. Probado con éxito (200), tarea inexistente (404) y tarea de otro usuario (404), confirmado con SELECT.

---

## passos
El front necesita mostrar, generar con IA, marcar y eliminar los pasos de cada tarea, que es una funcionalidad central de accesibilidad del producto.

### GET /usuarios/{usuario_id}/tarefas/{tarefa_id}/passos — Listar passos de uma tarefa
- **Estado:** FRONT-READY
- **Éxito:** `200` → `{"dados": [Passo, ...]}`, ordenados por `ordem`. Lista vacía si no hay pasos.
- **Errores:** `404` "Usuário não encontrado." o "Tarefa não encontrada." (también si la tarea es de otro usuario)
- **Evidencia:** modelo `Passo` y `PassoRepository` nuevos, orquestados por `TarefaService`. Probado con lista vacía (200), tarea inexistente (404) y tarea ajena (404), confirmado con SELECT.

### POST /usuarios/{usuario_id}/tarefas/{tarefa_id}/passos/gerar — Gerar passos com IA
- **Estado:** FRONT-READY
- **Body:** ninguno. Usa el `titulo` de la tarea.
- **Éxito:** `201` → `{"dados": [Passo, ...]}` (normalmente 3 o 4 pasos nuevos, guardados en el banco)
- **Errores:**
  - `404` "Usuário não encontrado." o "Tarefa não encontrada."
  - `503` si la IA no está disponible (por ejemplo, falta `GEMINI_API_KEY`)
- **Nota:** cada llamada **agrega** pasos nuevos; no reemplaza los existentes.
- **Evidencia:** reutiliza `gerar_passos_tarefa()` de `core/ia_service.py` sin modificarlo. Probado con Gemini real (201), sin API key (503) y tarea inexistente (404), confirmado con SELECT.

### PATCH /usuarios/{usuario_id}/tarefas/{tarefa_id}/passos/{passo_id} — Alternar status concluído
- **Estado:** FRONT-READY
- **Body:** ninguno. Cada llamada invierte `concluido`.
- **Éxito:** `200` → `{"dados": Passo}`
- **Errores:** `404` "Usuário não encontrado.", "Tarefa não encontrada." o "Passo não encontrado." (también si el paso pertenece a otra tarea)
- **Evidencia:** identifica el paso por `id` de banco (`passo_id`), no por índice. Probado con éxito (200), paso inexistente (404) y paso de otra tarea (404), confirmado con SELECT.

### DELETE /usuarios/{usuario_id}/tarefas/{tarefa_id}/passos/{passo_id} — Excluir passo
- **Estado:** FRONT-READY
- **Éxito:** `204`, sin body
- **Errores:** `404` "Usuário não encontrado.", "Tarefa não encontrada." o "Passo não encontrado."
- **Nota:** los pasos restantes **no** se renumeran; puede quedar un hueco en `ordem` (por ejemplo 1, 2, 3 sin el 4). El front debe ordenar por `ordem`, no asumir números consecutivos.
- **Evidencia:** probado con éxito (204), paso inexistente (404) y paso de otra tarea (404); SELECT confirmó que solo se eliminó el paso indicado.

---

## assistente_ia
El front necesita que el usuario pueda escribir un mensaje libre y recibir una respuesta o una tarea interpretada automáticamente, que es la propuesta de valor principal de IAmigo.

### POST /usuarios/{usuario_id}/mensagens — Interpretar mensagem do usuário
- **Estado:** FRONT-READY
- **Body:**
```json
{ "texto": "preciso estudar matemática amanhã" }
```
- **Éxito:** `200`
```json
{ "dados": { "intencao": "registrar_tarefa", "titulo": "Estudar matemática amanhã", "categoria": "tarefas_educacionais" } }
```
  Si no detecta una tarea: `{"dados": {"intencao": "pergunta", "titulo": null, "categoria": null}}`
- **Errores:** `404` "Usuário não encontrado."
- **Nota:** solo clasifica el texto; **no guarda nada** en el banco. No usa Gemini.
- **Evidencia:** reutiliza `interpretar_mensagem()` de `core/interpretador.py` sin modificarlo. Probado con intención de tarea, con pregunta y con usuario inexistente.

### POST /usuarios/{usuario_id}/perguntas — Responder pergunta geral
- **Estado:** FRONT-READY
- **Body:**
```json
{ "texto": "o que é uma variável em programação?" }
```
- **Éxito:** `200` → `{"dados": ["línea 1", "línea 2", ...]}`. La respuesta se adapta al `estilo_instrucao` del usuario.
- **Errores:**
  - `404` "Usuário não encontrado."
  - `503` si la IA no está disponible
- **Nota:** no guarda la pregunta ni la respuesta.
- **Evidencia:** reutiliza `obter_resposta_ia()` de `core/ia_service.py` sin modificarlo. Probado con dos preguntas reales (200) y usuario inexistente (404).

### POST /usuarios/{usuario_id}/conversa — Cadastro de tarefa por conversa
- **Estado:** FRONT-READY
- **Cómo funciona:** el servidor **no guarda** el estado de la conversación. El front debe reenviar en cada llamada el `estado` y la `tarefa` que recibió en la respuesta anterior (como `tarefa_parcial`).
- **Body:**
```json
{ "mensagem": "preciso lavar o carro", "estado": null, "tarefa_parcial": null }
```
- **Éxito:** `200`
```json
{
  "dados": {
    "respostas": ["📝 Entendi o que você precisa fazer!", "📌 Lavar o carro", "Qual é o prazo?", "..."],
    "estado": "esperando_prazo",
    "tarefa": { "titulo": "Lavar o carro", "categoria": "tarefas_diarias", "prazo": null, "prioridade": "media" }
  }
}
```
- **Flujo:**

| Paso | `estado` enviado | `mensagem` esperada | `estado` devuelto |
|---|---|---|---|
| 1 | `null` | Texto con una tarea ("preciso ...") | `esperando_prazo` |
| 2 | `esperando_prazo` | `DD/MM/AAAA` o `sem prazo` | `esperando_prioridade` |
| 3 | `esperando_prioridade` | `1`/`2`/`3` o `baixa`/`media`/`alta` | `esperando_mensagem` (tarea guardada) |

  - En cualquier paso, `cancelar` reinicia el flujo sin guardar.
  - Si el prazo o la prioridad son inválidos, responde `200` con un mensaje de ayuda y **mantiene el mismo estado**.
  - **⚠️ Cuando la respuesta trae `"estado": "esperando_mensagem"`, la siguiente llamada debe enviar `"estado": null`.** Enviar `"esperando_mensagem"` devuelve `422` "Estado de conversa inválido."
- **Errores:**
  - `404` "Usuário não encontrado."
  - `422` "Estado de conversa inválido."
  - `422` "Não consegui identificar uma tarefa nessa mensagem." (paso 1 sin intención de tarea)
- **Evidencia:** se corrigió la arquitectura de `ConversaTarefa`, que guardaba el estado en memoria del proceso: ahora el estado viaja en el cliente. La tarea final se guarda con `TarefaService.criar_tarefa()`. Probado con el flujo completo de 3 llamadas, usuario inexistente y estado inválido, confirmado con SELECT.

---

## Limitaciones conocidas

1. **Fallas técnicas sin código `500`.** Si falla la base de datos, la mayoría de las rutas devuelven el mensaje "Não foi possível concluir a operação." con `404` o `422` en vez de `500`. El detalle queda registrado en la terminal del servidor. Excepción: `GET /usuarios` sí devuelve `500`.
2. **Eliminación en cascada.** `DELETE /usuarios/{id}` elimina todas las tareas y pasos del usuario.
3. **Sin autenticación.** Cualquier cliente con acceso a la API puede operar sobre cualquier `usuario_id`.
4. **`ordem` de pasos no consecutivo** después de eliminar pasos.
