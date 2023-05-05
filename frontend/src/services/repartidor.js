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
  formData.append("licencia", payload.licencia);
  formData.append("transporte", payload.transporte);
  formData.append("id_muni", payload.id_muni);
  formData.append("id_dep", payload.id_dep);

  const response = await fetch(`${API_URL}/registrarRepartidor`, {
    method: "POST",
    body: formData,
  });

  return response;
};

export const login = async (username, password) => {
  const response = await fetch(
    `${API_URL}/inicioSesionRepartidor/${username}/${password}`,
    {
      method: "GET",
      headers: { "Content-type": "application/json; charset=UTF-8" },
    }
  );

  if (!response.ok) {
    throw new Error("imposible iniciar sesion");
  }

  const data = await response.json();
  return data;
};

export const getPerfilData = async ({ queryKey }) => {
  const response = await fetch(
    `${API_URL}/VerPerfilRepartidor/${queryKey[1].USUARIO}`,
    {
      method: "GET",
      headers: { "Content-type": "application/json; charset=UTF-8" },
    }
  );

  if (!response.ok) {
    throw new Error("Error intentando obtener los datos del perfil");
  }

  const data = await response.json();

  if (!data.exito)
    throw new Error("Error intentando obtener los datos del perfil");

  console.log(data);
  return data;
};

export const updateRepartidor = async (updatedValues, usuario) => {
  console.log(usuario);
  const response = await fetch(
    `${API_URL}/ActualizarPerfilRepartidor/${usuario}`,
    {
      method: "PUT",
      headers: { "Content-type": "application/json; charset=UTF-8" },
      body: JSON.stringify(updatedValues),
    }
  );

  if (!response) {
    throw new Error("Error intentando actualizar el perfil");
  }

  const data = await response.json();

  if (!data.exito) {
    throw new Error("Error intentando actualizar el perfil");
  }

  return data;
};
