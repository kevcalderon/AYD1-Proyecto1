import API_URL from "../app/constants";

export const getDepartamentos = async () => {
  try {
    const response = await fetch(`${API_URL}/mostrarDepartamentos`, {
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
