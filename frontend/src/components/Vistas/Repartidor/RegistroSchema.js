import { z } from "zod";

const validationSchema = z.object({
  nombre: z.string().min(1, { message: "Campo Requerido" }),
  apellido: z.string().min(1, { message: "Campo Requerido" }),
  usuario: z.string().min(1, { message: "Campo Requerido" }),
  contraseña: z.string().min(1, { message: "Campo Requerido" }),
  correo: z
    .string()
    .min(1, { message: "Campo Requerido" })
    .email({ message: "Formato de correo incorrecto" }),
  telefono: z
    .string()
    .min(8, { message: "El telefono debe contener al menos 8 digitos" }),
  nit: z.string().min(1, { message: "Campo Requerido" }),
  Departamento: z.string().min(1, { message: "Campo Requerido" }),
  Municipio: z.string().min(1, { message: "Campo Requerido" }),
  Lugar: z.string().min(1, { message: "Campo Requerido" }),
  Licencia: z.string().min(1, { message: "Campo Requerido" }),
  Transporte: z.string().min(1, { message: "Campo Requerido" }),
});

export default validationSchema;
