import {
  useEffect,
  useState,
} from "react";

import type {
  FormEvent,
} from "react";

import {
  eliminarToken,
  guardarToken,
  iniciarSesion,
  obtenerToken,
  peticion,
} from "./api";

import type {
  Estado,
  Prioridad,
  Proyecto,
  Resumen,
  Tarea,
  Usuario,
} from "./types";

interface RespuestaTareas {
  total: number;
  pagina: number;
  limite: number;
  paginas: number;
  tareas: Tarea[];
}


function App() {
  const [usuario, setUsuario] =
    useState<Usuario | null>(null);

  const [tareas, setTareas] =
    useState<Tarea[]>([]);

  const [proyectos, setProyectos] =
    useState<Proyecto[]>([]);

  const [resumen, setResumen] =
    useState<Resumen | null>(null);

  const [modoRegistro, setModoRegistro] =
    useState(false);

  const [cargando, setCargando] =
    useState(true);

  const [error, setError] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [nombre, setNombre] =
    useState("");

  const [titulo, setTitulo] =
    useState("");

  const [descripcion, setDescripcion] =
    useState("");

  const [prioridad, setPrioridad] =
    useState<Prioridad>("Media");

  const [categoria, setCategoria] =
    useState("General");

  const [fechaLimite, setFechaLimite] =
    useState("");

  const [proyectoId, setProyectoId] =
    useState("");

  const [busqueda, setBusqueda] =
    useState("");

  const [filtroEstado, setFiltroEstado] =
    useState("");

  const [filtroPrioridad, setFiltroPrioridad] =
    useState("");


  useEffect(() => {
    if (obtenerToken()) {
      cargarAplicacion();
    } else {
      setCargando(false);
    }
  }, []);


  async function cargarAplicacion() {
    try {
      setCargando(true);

      const perfil = await peticion<Usuario>(
        "/auth/me"
      );

      setUsuario(perfil);

      await Promise.all([
        cargarTareas(),
        cargarProyectos(),
        cargarResumen(),
      ]);

    } catch {
      eliminarToken();
      setUsuario(null);

    } finally {
      setCargando(false);
    }
  }


  async function cargarTareas() {
    const params =
      new URLSearchParams();

    params.set(
      "pagina",
      "1",
    );

    params.set(
      "limite",
      "100",
    );

    if (busqueda) {
      params.set(
        "buscar",
        busqueda,
      );
    }

    if (filtroEstado) {
      params.set(
        "estado",
        filtroEstado,
      );
    }

    if (filtroPrioridad) {
      params.set(
        "prioridad",
        filtroPrioridad,
      );
    }

    const datos =
      await peticion<RespuestaTareas>(
        `/tareas?${params.toString()}`
      );

    setTareas(
      datos.tareas
    );
  }


  async function cargarProyectos() {
    const datos =
      await peticion<Proyecto[]>(
        "/proyectos"
      );

    setProyectos(datos);
  }


  async function cargarResumen() {
    const datos =
      await peticion<Resumen>(
        "/dashboard/resumen"
      );

    setResumen(datos);
  }


  async function enviarAutenticacion(
    evento: FormEvent,
  ) {
    evento.preventDefault();

    setError("");

    try {
      if (modoRegistro) {
        await peticion(
          "/auth/registro",
          {
            method: "POST",
            body: JSON.stringify({
              nombre,
              email,
              password,
            }),
          },
        );
      }

      const token =
        await iniciarSesion(
          email,
          password,
        );

      guardarToken(token);

      await cargarAplicacion();

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Error inesperado."
      );
    }
  }


  async function crearTarea(
    evento: FormEvent,
  ) {
    evento.preventDefault();

    setError("");

    try {
      await peticion(
        "/tareas",
        {
          method: "POST",
          body: JSON.stringify({
            titulo,
            descripcion,
            prioridad,
            estado: "Pendiente",
            categoria,
            fecha_limite:
              fechaLimite || null,
            proyecto_id:
              proyectoId
                ? Number(proyectoId)
                : null,
          }),
        },
      );

      setTitulo("");
      setDescripcion("");
      setPrioridad("Media");
      setCategoria("General");
      setFechaLimite("");
      setProyectoId("");

      await Promise.all([
        cargarTareas(),
        cargarResumen(),
      ]);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Error creando tarea."
      );
    }
  }


  async function cambiarEstado(
    tarea: Tarea,
  ) {
    let nuevoEstado: Estado;

    if (tarea.estado === "Pendiente") {
      nuevoEstado = "En progreso";

    } else if (
      tarea.estado === "En progreso"
    ) {
      nuevoEstado = "Completada";

    } else {
      nuevoEstado = "Pendiente";
    }

    await peticion(
      `/tareas/${tarea.id}/estado`,
      {
        method: "PATCH",
        body: JSON.stringify({
          estado: nuevoEstado,
        }),
      },
    );

    await Promise.all([
      cargarTareas(),
      cargarResumen(),
    ]);
  }


  async function eliminarTarea(
    id: number,
  ) {
    if (
      !window.confirm(
        "¿Seguro que deseas eliminar esta tarea?"
      )
    ) {
      return;
    }

    await peticion(
      `/tareas/${id}`,
      {
        method: "DELETE",
      },
    );

    await Promise.all([
      cargarTareas(),
      cargarResumen(),
    ]);
  }


  async function crearProyecto() {
    const nombreProyecto =
      window.prompt(
        "Nombre del proyecto:"
      );

    if (!nombreProyecto) {
      return;
    }

    const descripcionProyecto =
      window.prompt(
        "Descripción:"
      ) ?? "";

    await peticion(
      "/proyectos",
      {
        method: "POST",
        body: JSON.stringify({
          nombre: nombreProyecto,
          descripcion:
            descripcionProyecto,
        }),
      },
    );

    await cargarProyectos();
  }


  function cerrarSesion() {
    eliminarToken();
    setUsuario(null);
    setTareas([]);
    setProyectos([]);
    setResumen(null);
  }


  if (cargando) {
    return (
      <div className="pantalla-centro">
        <div className="loader" />
        <p>Cargando aplicación...</p>
      </div>
    );
  }


  if (!usuario) {
    return (
      <div className="auth-layout">
        <div className="auth-presentacion">
          <span className="logo-grande">
            TaskFlow
          </span>

          <h1>
            Organiza tus proyectos.
            <br />
            Cumple tus objetivos.
          </h1>

          <p>
            Plataforma moderna para gestionar
            proyectos, tareas, prioridades y
            fechas límite.
          </p>
        </div>

        <div className="auth-panel">
          <form
            className="auth-card"
            onSubmit={
              enviarAutenticacion
            }
          >
            <h2>
              {modoRegistro
                ? "Crear cuenta"
                : "Bienvenido"}
            </h2>

            <p className="texto-secundario">
              {modoRegistro
                ? "Crea tu cuenta para comenzar."
                : "Inicia sesión para continuar."}
            </p>

            {modoRegistro && (
              <input
                placeholder="Nombre"
                value={nombre}
                onChange={(e) =>
                  setNombre(
                    e.target.value
                  )
                }
                required
              />
            )}

            <input
              type="email"
              placeholder="Correo electrónico"
              value={email}
              onChange={(e) =>
                setEmail(
                  e.target.value
                )
              }
              required
            />

            <input
              type="password"
              placeholder="Contraseña"
              value={password}
              onChange={(e) =>
                setPassword(
                  e.target.value
                )
              }
              minLength={8}
              required
            />

            {error && (
              <div className="error">
                {error}
              </div>
            )}

            <button
              className="boton principal"
              type="submit"
            >
              {modoRegistro
                ? "Crear cuenta"
                : "Iniciar sesión"}
            </button>

            <button
              className="boton texto"
              type="button"
              onClick={() =>
                setModoRegistro(
                  !modoRegistro
                )
              }
            >
              {modoRegistro
                ? "Ya tengo una cuenta"
                : "Crear una cuenta"}
            </button>
          </form>
        </div>
      </div>
    );
  }


  return (
    <div className="app">
      <aside className="sidebar">
        <div>
          <h2 className="logo">
            TaskFlow
          </h2>

          <div className="usuario-sidebar">
            <div className="avatar">
              {usuario.nombre
                .charAt(0)
                .toUpperCase()}
            </div>

            <div>
              <strong>
                {usuario.nombre}
              </strong>

              <small>
                {usuario.email}
              </small>
            </div>
          </div>

          <nav>
            <button className="nav-activo">
              Dashboard
            </button>

            <button>
              Mis tareas
            </button>

            <button>
              Proyectos
            </button>
          </nav>
        </div>

        <button
          className="cerrar"
          onClick={cerrarSesion}
        >
          Cerrar sesión
        </button>
      </aside>

      <main className="contenido">
        <header className="cabecera">
          <div>
            <p className="saludo">
              Hola, {usuario.nombre}
            </p>

            <h1>
              Panel de trabajo
            </h1>
          </div>

          <button
            className="boton secundario"
            onClick={crearProyecto}
          >
            + Proyecto
          </button>
        </header>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        <section className="estadisticas">
          <Stat
            titulo="Total"
            valor={resumen?.total ?? 0}
          />

          <Stat
            titulo="Pendientes"
            valor={
              resumen?.pendientes ?? 0
            }
          />

          <Stat
            titulo="En progreso"
            valor={
              resumen?.en_progreso ?? 0
            }
          />

          <Stat
            titulo="Completadas"
            valor={
              resumen?.completadas ?? 0
            }
          />

          <Stat
            titulo="Vencidas"
            valor={
              resumen?.vencidas ?? 0
            }
          />
        </section>

        <section className="grid-principal">
          <div className="panel">
            <div className="panel-titulo">
              <div>
                <h2>
                  Mis tareas
                </h2>

                <p>
                  Administra tu trabajo.
                </p>
              </div>
            </div>

            <div className="filtros">
              <input
                placeholder="Buscar tareas..."
                value={busqueda}
                onChange={(e) =>
                  setBusqueda(
                    e.target.value
                  )
                }
              />

              <select
                value={filtroEstado}
                onChange={(e) =>
                  setFiltroEstado(
                    e.target.value
                  )
                }
              >
                <option value="">
                  Todos los estados
                </option>

                <option>
                  Pendiente
                </option>

                <option>
                  En progreso
                </option>

                <option>
                  Completada
                </option>
              </select>

              <select
                value={filtroPrioridad}
                onChange={(e) =>
                  setFiltroPrioridad(
                    e.target.value
                  )
                }
              >
                <option value="">
                  Todas las prioridades
                </option>

                <option>Baja</option>
                <option>Media</option>
                <option>Alta</option>
                <option>Urgente</option>
              </select>

              <button
                className="boton secundario"
                onClick={
                  cargarTareas
                }
              >
                Filtrar
              </button>
            </div>

            <div className="lista-tareas">
              {tareas.length === 0 && (
                <div className="sin-datos">
                  No hay tareas todavía.
                </div>
              )}

              {tareas.map((tarea) => (
                <article
                  className="tarea"
                  key={tarea.id}
                >
                  <div className="tarea-info">
                    <div className="badges">
                      <span
                        className={
                          "badge " +
                          tarea.prioridad
                            .toLowerCase()
                        }
                      >
                        {tarea.prioridad}
                      </span>

                      <span className="badge estado">
                        {tarea.estado}
                      </span>
                    </div>

                    <h3>
                      {tarea.titulo}
                    </h3>

                    {tarea.descripcion && (
                      <p>
                        {
                          tarea.descripcion
                        }
                      </p>
                    )}

                    <small>
                      {tarea.categoria}

                      {tarea.fecha_limite &&
                        ` · ${tarea.fecha_limite}`}
                    </small>
                  </div>

                  <div className="acciones">
                    <button
                      onClick={() =>
                        cambiarEstado(
                          tarea
                        )
                      }
                    >
                      Cambiar estado
                    </button>

                    <button
                      className="peligro"
                      onClick={() =>
                        eliminarTarea(
                          tarea.id
                        )
                      }
                    >
                      Eliminar
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div className="panel">
            <h2>
              Nueva tarea
            </h2>

            <p className="texto-secundario">
              Añade una nueva actividad.
            </p>

            <form
              className="form-tarea"
              onSubmit={crearTarea}
            >
              <label>
                Título
                <input
                  value={titulo}
                  onChange={(e) =>
                    setTitulo(
                      e.target.value
                    )
                  }
                  placeholder="Ej. Terminar API"
                  required
                />
              </label>

              <label>
                Descripción
                <textarea
                  value={descripcion}
                  onChange={(e) =>
                    setDescripcion(
                      e.target.value
                    )
                  }
                  placeholder="Descripción..."
                />
              </label>

              <label>
                Prioridad
                <select
                  value={prioridad}
                  onChange={(e) =>
                    setPrioridad(
                      e.target
                        .value as Prioridad
                    )
                  }
                >
                  <option>Baja</option>
                  <option>Media</option>
                  <option>Alta</option>
                  <option>Urgente</option>
                </select>
              </label>

              <label>
                Categoría
                <input
                  value={categoria}
                  onChange={(e) =>
                    setCategoria(
                      e.target.value
                    )
                  }
                />
              </label>

              <label>
                Proyecto
                <select
                  value={proyectoId}
                  onChange={(e) =>
                    setProyectoId(
                      e.target.value
                    )
                  }
                >
                  <option value="">
                    Sin proyecto
                  </option>

                  {proyectos.map(
                    (proyecto) => (
                      <option
                        key={
                          proyecto.id
                        }
                        value={
                          proyecto.id
                        }
                      >
                        {
                          proyecto.nombre
                        }
                      </option>
                    )
                  )}
                </select>
              </label>

              <label>
                Fecha límite
                <input
                  type="date"
                  value={fechaLimite}
                  onChange={(e) =>
                    setFechaLimite(
                      e.target.value
                    )
                  }
                />
              </label>

              <button
                className="boton principal"
                type="submit"
              >
                Crear tarea
              </button>
            </form>
          </div>
        </section>
      </main>
    </div>
  );
}


function Stat({
  titulo,
  valor,
}: {
  titulo: string;
  valor: number;
}) {
  return (
    <div className="stat">
      <span>{titulo}</span>
      <strong>{valor}</strong>
    </div>
  );
}


export default App;