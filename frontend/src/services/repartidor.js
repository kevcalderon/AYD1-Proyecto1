import API_URL from "../app/constants";

export const postRepartidor = async (payload) => {
  console.log(payload);
  const response = await fetch(`${API_URL}/registrarRepartidor`, {
    method: "POST",
    body: JSON.stringify({
      nombre: payload.nombre,
      apellido: payload.apellido,
      telefono: payload.apellido,
      correo: payload.correo,
      usuario: payload.usuario,
      contra: payload.contra,
      nit: payload.nit,
      lugar: payload.lugar,
      documento: payload.documento,
      licencia: payload.licencia.name,
      transporte: payload.transporte.value,
      id_muni: payload.municipio.MUN_ID,
      id_dep: payload.departamento.DEP_ID,
    }),
    headers: { "Content-type": "application/json; charset=UTF-8" },
  });

  return response;
};
