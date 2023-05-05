import { useQuery } from "react-query";
import { getDepartamentos } from "../../../services/departamentos";
import { Backdrop, CircularProgress } from "@mui/material";
import ShowError from "../../showError/ShowError";
import repartidorImage from "../../../assets/repartidor.png";
import RegistroFrom from "./RegistroForm";
import NavbarU from "../../Navbars/NavbarU";
import { postRepartidor } from "../../../services/repartidor";

const Registro = () => {
  const departamentos = useQuery("get-departamentos", getDepartamentos, {
    staleTime: 20000,
  });

  if (departamentos.isLoading) {
    return (
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={departamentos.isLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }

  if (!departamentos.isSuccess) {
    return (
      <ShowError
        title="Error"
        description="Estamos teniendo problemas al cargar esta pagina."
        message="Intenta recargar la pagina. Si el problema presiste comunicate con IT"
      />
    );
  }

  const onSubmitForm = async (values) => {
    const result = await postRepartidor(values);

    if (!result.ok) {
      console.log("error");
    }
  };

  return (
    <>
      <NavbarU />
      <div className="grid lg:grid-cols-4 sm:grid-cols-1 my-auto bg-gradient-to-r from-bg[#4ab3f4] to-bg[#4186e0] min-h-screen 	">
        <div className="my-auto mx-auto w-auto">
          <img
            className="w-96 transform -scale-x-100 hover:transform hover:translate-x-10"
            src={repartidorImage}
          />
        </div>
        <div className="my-auto col-span-3 mx-auto w-4/5 ">
          <RegistroFrom
            departamentos={departamentos.data}
            onSubmitForm={onSubmitForm}
          />
        </div>
      </div>
    </>
  );
};

export default Registro;
