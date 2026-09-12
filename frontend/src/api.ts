const API_URL =
  import.meta.env.VITE_API_URL ??
  "http://127.0.0.1:8000";


export function obtenerToken(): string | null {
  return localStorage.getItem("token");
}


export function guardarToken(
  token: string,
): void {
  localStorage.setItem(
    "token",
    token,
  );
}


export function eliminarToken(): void {
  localStorage.removeItem("token");
}


export async function peticion<T>(
  ruta: string,
  opciones: RequestInit = {},
): Promise<T> {

  const token = obtenerToken();

  const headers = new Headers(
    opciones.headers
  );

  if (
    opciones.body &&
    !(opciones.body instanceof URLSearchParams)
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  if (token) {
    headers.set(
      "Authorization",
      `Bearer ${token}`,
    );
  }

  const respuesta = await fetch(
    `${API_URL}${ruta}`,
    {
      ...opciones,
      headers,
    },
  );

  if (!respuesta.ok) {
    let mensaje = "Ha ocurrido un error.";

    try {
      const datos = await respuesta.json();

      mensaje =
        typeof datos.detail === "string"
          ? datos.detail
          : JSON.stringify(datos.detail);

    } catch {
      mensaje = respuesta.statusText;
    }

    throw new Error(mensaje);
  }

  if (respuesta.status === 204) {
    return undefined as T;
  }

  return respuesta.json();
}


export async function iniciarSesion(
  email: string,
  password: string,
): Promise<string> {

  const cuerpo = new URLSearchParams();

  cuerpo.set(
    "username",
    email,
  );

  cuerpo.set(
    "password",
    password,
  );

  const respuesta = await fetch(
    `${API_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
      body: cuerpo,
    },
  );

  if (!respuesta.ok) {
    const datos = await respuesta.json();

    throw new Error(
      datos.detail ??
      "No se pudo iniciar sesión."
    );
  }

  const datos = await respuesta.json();

  return datos.access_token;
}