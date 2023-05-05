import API_URL from "../app/constants";

export const getMunicipios = async () => {
  try {
    const response = await fetch(`${API_URL}/mostrarMunicipios`, {
      method: "GET",
      headers: { "Content-type": "application/json; charset=UTF-8" },
    });

    const data = await response.json();

    return data;
  } catch (error) {
    console.log(error);
    throw error;
  }
};

export const getDepartamentoPorMunicipio = async ({ queryKey }) => {
  console.log(queryKey[1])
  const response = await fetch(`${API_URL}/mostrarMunicipios/${queryKey[1]}`, {
    method: "GET",
    headers: { "Content-type": "application/json; charset=UTF-8" },
  });

  if (!response.ok) {
    throw new Error("Eror al obtener los municpios");
  }

  const data = await response.json();
  console.log(data)
  return data;
};
