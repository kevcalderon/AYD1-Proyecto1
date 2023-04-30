import { Backdrop, CircularProgress, Rating } from "@mui/material";
import React from "react";
import { useQuery } from "react-query";
import { getPerfilData, updateRepartidor } from "../../../services/repartidor";
import NavBar from "../../Navbars/NavbarR";
import ShowError from "../../showError/ShowError";
import RegistroFrom from "./RegistroForm";

function MiPerfil() {
  const id_repartidor = localStorage.getItem("repartidor");
  const rawPerfilData = useQuery(
    ["getPerfilData", JSON.parse(id_repartidor)],
    getPerfilData,
    { staleTime: 30000 }
  );

  if (rawPerfilData.isLoading) {
    return (
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={rawPerfilData.isLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }

  if (rawPerfilData.isError) {
    return (
      <ShowError
        title="Error"
        description="Estamos teniendo problemas al cargar esta pagina."
        message="Intenta recargar la pagina. Si el problema presiste comunicate con IT"
      />
    );
  }

  const onSubmit = async (values) => {
    try {
      await updateRepartidor(values, rawPerfilData.data.repartidor.USUARIO);
    } catch (error) {
      console.log(error);
    } finally {
      rawPerfilData.refetch();
    }
  };

  return (
    <div>
      <NavBar />
      <div className="grid grid-cols-3 bg-white w-11/12 mx-auto p-4 mt-10 rounded">
        <div className="grid grid-cols-2 my-auto">
          <Rating
            name="no-value"
            value={rawPerfilData.data.repartidor.CALIFICACION}
            sx={{ fontSize: "4rem" }}
          />
        </div>
        <div className="my-auto col-span-2">
          <div className="ml-auto">
            <h2 className="">
              Comisiones Generadas: Q {rawPerfilData.data.repartidor.COMISION}
              .00
            </h2>
          </div>
        </div>
      </div>

      <div className="w-11/12 mx-auto mt-10">
        <RegistroFrom
          onSubmitForm={onSubmit}
          initialValue={rawPerfilData.data.repartidor}
        />
      </div>
    </div>
  );
}

export default MiPerfil;
