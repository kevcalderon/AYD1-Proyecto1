import { z } from "zod";

const validationSchema = z.object({
  nombre: z.string().min(1, { message: "Campo Requerido" }),
  apellido: z.string().min(1, { message: "Campo Requerido" }),
  usuario: z.string().min(1, { message: "Campo Requerido" }),
  contra: z.string().min(1, { message: "Campo Requerido" }),
  correo: z
    .string()
    .min(1, { message: "Campo Requerido" })
    .email({ message: "Formato de correo incorrecto" }),
  telefono: z
    .string()
    .min(8, { message: "El telefono debe contener al menos 8 digitos" }),
  nit: z.string().min(1, { message: "Campo Requerido" }),
  departamento: z.object({
    DEP_ID: z.number().min(1, { message: "algo" }),
    NOMBRE: z.string().min(1, { message: "algo" }),
  }),
  municipio: z.object({
    MUN_ID: z.number().min(1, { message: "algo" }),
    NOMBRE_MUNICIPIO: z.string().min(1, { message: "algo" }),
  }),
  lugar: z.string().min(1, { message: "Campo Requerido" }),
  licencia: z.object({
    id: z.number(),
    name: z.string(),
  }),
  transporte: z.object({
    id: z.number(),
    value: z.string(),
  }),
});

export default validationSchema;
