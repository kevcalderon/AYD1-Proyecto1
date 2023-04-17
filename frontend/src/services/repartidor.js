import API_URL from "../app/constants";

export const postRepartidor = async (payload) => {
  const formData = new FormData();
  formData.append("nombre", payload.nombre);
  formData.append("apellido", payload.apellido);
  formData.append("telefono", payload.telefono);
  formData.append("correo", payload.correo);
  formData.append("usuario", payload.usuario);
  formData.append("contra", payload.contra);
  formData.append("nit", payload.nit);
  formData.append("lugar", payload.lugar);
  formData.append("documento", payload.documento[0]);
  formData.append("licencia", payload.licencia.name);
  formData.append("transporte", payload.transporte.value);
  formData.append("id_muni", payload.municipio.MUN_ID);
  formData.append("id_dep", payload.departamento.DEP_ID);

  const response = await fetch(`${API_URL}/registrarRepartidor`, {
    method: "POST",
    body: formData,
  });

};
