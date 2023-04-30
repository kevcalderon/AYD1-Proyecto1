import { z } from "zod";

const validationSchema = z.object({
  nombre: z.string().min(1, { message: "Campo Requerido" }),
  apellido: z.string().min(1, { message: "Campo Requerido" }),
  usuario: z.string().min(1, { message: "Campo Requerido" }),
  contra: z.string().optional(),
  correo: z
    .string()
    .min(1, { message: "Campo Requerido" })
    .email({ message: "Formato de correo incorrecto" }),
  telefono: z
    .string()
    .min(8, { message: "El telefono debe contener al menos 8 digitos" }),
  nit: z.string().min(1, { message: "Campo Requerido" }),
  id_dep: z.number().min(1, { message: "Campo Requerido" }),
  id_muni: z.number().min(1, { message: "Campo Requerido" }),
  lugar: z.string().min(1, { message: "Campo Requerido" }),
  licencia: z.string().min(1, { message: "Campo Requerido" }),
  transporte: z.string().min(1, { message: "Campo Requerido" }),
  documento: z.any(),
});

export default validationSchema;
