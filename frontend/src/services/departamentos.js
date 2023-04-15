import API_URL from "../app/constants";

export const getDepartamentos = async () => {
  try {
    const response = await fetch(`${API_URL}/mostrarDepartamentos`, {
      method: "GET",
      headers: { "Content-type": "application/json; charset=UTF-8" },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        return data;
      })
      .catch((error) => {
        throw error;
      });
  } catch (error) {
    console.log(error);
    throw error;
  }
};
