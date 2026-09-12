export type Estado =
  | "Pendiente"
  | "En progreso"
  | "Completada";

export type Prioridad =
  | "Baja"
  | "Media"
  | "Alta"
  | "Urgente";


export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  activo: boolean;
  fecha_creacion: string;
}


export interface Proyecto {
  id: number;
  nombre: string;
  descripcion: string;
  usuario_id: number;
  fecha_creacion: string;
}


export interface Tarea {
  id: number;
  titulo: string;
  descripcion: string;
  prioridad: Prioridad;
  estado: Estado;
  categoria: string;
  fecha_limite: string | null;
  proyecto_id: number | null;
  usuario_id: number;
  fecha_creacion: string;
  fecha_actualizacion: string;
}


export interface Resumen {
  total: number;
  pendientes: number;
  en_progreso: number;
  completadas: number;
  vencidas: number;
}