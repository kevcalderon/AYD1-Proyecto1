import { Backdrop, Button, CircularProgress, TextField } from "@mui/material";
import React, { useMemo } from "react";
import { useQuery } from "react-query";
import {
  marcarComoEntregado,
  verPedidoAsignado,
} from "../../../services/pedidos";
import NavBar from "../../Navbars/NavbarR";
import ShowError from "../../showError/ShowError";
import fields from "./MiPedidoFields";
import MaterialReactTable from "material-react-table";
import noOrdersFound from "../../../assets/no-order.svg";

function MiPedido() {
  const id_repartidor = localStorage.getItem("repartidor");
  const rawPedido = useQuery(
    ["verPedidoAsignado", JSON.parse(id_repartidor)],
    verPedidoAsignado,
    { staleTime: 30000 }
  );

  const columns = useMemo(() => fields(), []);
  const data = useMemo(() => {
    return rawPedido.data;
  }, [rawPedido.data]);

  if (rawPedido.isLoading) {
    return (
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={rawPedido.isLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }

  if (rawPedido.isError) {
    return (
      <ShowError
        title="Error"
        description="Estamos teniendo problemas al cargar esta pagina."
        message="Intenta recargar la pagina. Si el problema presiste comunicate con IT"
      />
    );
  }

  const handleMarkAsComplete = async () => {
    try {
      marcarComoEntregado(rawPedido.data.pedidos.ORD_ID, JSON.parse(id_repartidor));

      rawPedido.refetch();
    } catch (error) {
      console.log(error);
    }
  };

  if (rawPedido.data && !rawPedido.data.exito) {
    return (
      <div>
        <NavBar />
        <div className="mx-auto  w-4/5 mt-20 rounded p-4">
          <img className="w-96 mx-auto my-auto" src={noOrdersFound} />
          <div className="justify-center grid">
            <h2 className="text-white mx-auto text-5xl">No hay pedidos en entrega</h2>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <NavBar />
      <div>
        <div className="mx-auto bg-white w-4/5 mt-20 rounded shadow-sm p-4">
          <h2>INFORMACION DEL PEDIDO</h2>
          <div className="w-1/3 mx-auto grid grid-rows-4 gap-4">
            <TextField
              variant="standard"
              value={rawPedido.data.pedidos.CLIENTE}
              size="small"
              className="w-100"
            />
            <TextField
              variant="standard"
              value={`${rawPedido.data.pedidos.DEPARTAMENTO},${rawPedido.data.MUNICIPIO},${rawPedido.data.LUGAR}`}
              size="small"
              className="w-100"
            />
            <TextField
              variant="standard"
              value={rawPedido.data.pedidos.ESTADO}
              size="small"
              className="w-100"
            />
            <TextField
              variant="standard"
              value={rawPedido.data.pedidos.METODO_PAGO}
              size="small"
              className="w-100"
            />
          </div>
          <h2>PRODUCTOS EN LA ORDEN</h2>
          <div className="">
            <MaterialReactTable
              columns={columns}
              data={data.pedidos.PRODUCTOS}
              enableColumnActions={false}
              enableColumnFilters={false}
              enablePagination={true}
              enableSorting={false}
              enableBottomToolbar={true}
              enableTopToolbar={true}
              muiTableBodyRowProps={{ hover: true }}
            />
          </div>
          <div className="mt-10 grid grid-cols-3">
            <div className="col-span-3 mx-auto">
              <Button variant="contained" onClick={handleMarkAsComplete}>
                Marcar Como Entregado
              </Button>
            </div>
          </div>
        </div>
        <div></div>
      </div>
    </>
  );
}

export default MiPedido;
