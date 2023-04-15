import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { Button, Form } from "react-bootstrap";
import FormInput from "../../form-input/FormInput";
import validationSchema from "./RegistroSchema";
import { useQuery } from "react-query";
import { getDepartamentos } from "../../../services/departamentos";
import { Backdrop, CircularProgress } from "@mui/material";
import ShowError from "../../showError/ShowError";
import repartidorImage from "../../../assets/repartidor.png";
import AutoCompleteForm from "../../autocomplete/Autocomplete";

const Registro = () => {
  const departamentos = useQuery("get-departamentos", getDepartamentos, {
    staleTime: 20000,
  });

  const methods = useForm({
    resolver: zodResolver(validationSchema),
  });

  const {
    reset,
    control,
    handleSubmit,
    register,
    formState: { isSubmitSuccessful, errors },
  } = methods;

  useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
    // eslint-disable-next-line
  }, [isSubmitSuccessful]);

  if (departamentos.isLoading) {
    <Backdrop
      sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={departamentos.isLoading}
    >
      <CircularProgress color="inherit" />
    </Backdrop>;
  }

  if (!departamentos.isSuccess) {
    <ShowError
      title="Error"
      description="Estamos teniendo problemas al cargar esta pagina."
      message="Intenta recargar la pagina. Si el problema presiste comunicate con IT"
    />;
  }

  const onSubmitForm = async (values) => {
    console.log(values);
  };

  console.log(departamentos.data);
  return (
    <div className="grid grid-cols-2 my-auto bg-gradient-to-r from-bg[#4ab3f4] to-bg[#4186e0] min-h-screen 	">
      <div className="my-auto mx-auto w-auto">
        <img
          className="w-80 transform -scale-x-100 hover:transform hover:translate-x-10"
          src={repartidorImage}
        />
      </div>
      <div className="my-auto">
        <div className="lg:w-4/5 m-auto my-auto bg-white rounded-xl shadow-lg overflow-hidden md:max-w-2xl p-4 gap-4">
          <FormProvider {...methods}>
            <Form onSubmit={handleSubmit(onSubmitForm)}>
              <FormInput
                placeholder="Ingresa tu nombre"
                errors={errors}
                name="nombre"
                controlId="nombre"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Ingresa tu apellido"
                errors={errors}
                name="apellido"
                controlId="apellido"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Ingresa tu nombre de usuario"
                errors={errors}
                name="usuario"
                controlId="usuario"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Ingresa tu contraseña"
                errors={errors}
                name="contraseña"
                controlId="contraseña"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Ingresa tu correo electronico"
                errors={errors}
                name="correo"
                controlId="correo"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Ingresa tu numero de telefono"
                errors={errors}
                name="telefono"
                controlId="telefono"
                type="text"
                register={register}
              />
              <FormInput
                placeholder="Ingresa tu numero de nit"
                errors={errors}
                name="nit"
                controlId="nit"
                type="text"
                register={register}
              />
              <AutoCompleteForm
                control={control}
                options={departamentos.data}
                getOptionLabel={(opt) => `${opt.NOMBRE}`}
                isOptionEqualToValue={(opt, value) =>
                  opt.NOMBRE === value.NOMBRE
                }
                renderOptions={(opt) => opt.NOMBRE}
                getKey={(opt) => opt.DEP_ID}
                errors={errors}
                name="Departamento"
                label="Departamento"
              />
              <FormInput
                placeholder="Lugar"
                errors={errors}
                name="lugar"
                controlId="lugar"
                type="text"
                register={register}
              />

              <Button className="p-2 w-100 " type="submit">
                Submit
              </Button>
            </Form>
          </FormProvider>
        </div>
      </div>
    </div>
  );
};

export default Registro;
