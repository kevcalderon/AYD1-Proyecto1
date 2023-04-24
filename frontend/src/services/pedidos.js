import API_URL from "../app/constants";

export const fetchPedidosPendientes = async ({ queryKey }) => {
  const response = await fetch(
    `${API_URL}/VerPedidosPendientesRepartidor/${queryKey[1].USUARIO}`,
    {
      method: "GET",
      headers: { "Content-type": "application/json; charset=UTF-8" },
    }
  );

  if (!response.ok) {
    throw new Error("Error al obtener los datos del servidor");
  }

  const data = await response.json();

  if (!data.exito) {
    throw new Error("Error al obtener los datos del servidor");
  }

  return data.pedidos;
};

export const asignarPedido = async (id_repartidor, id_orden) => {
  const payload = {
    id_ord: id_orden,
    user_rep: id_repartidor,
  };
  console.log(payload);
  const response = await fetch(`${API_URL}/AsignarPedidoRepartidor`, {
    method: "PUT",
    headers: { "Content-type": "application/json; charset=UTF-8" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Error al intentar asignar el pedido");
  }

  const data = await response.json();

  console.log(data);

  return data;
};
