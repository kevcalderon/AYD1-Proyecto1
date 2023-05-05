import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Backdrop, Button, CircularProgress, MenuItem } from "@mui/material";
import FormInput from "../../form-input/FormInput";
import validationSchema from "./RegistroSchema";
import { getDepartamentoPorMunicipio } from "../../../services/municipios";
import { useQuery } from "react-query";
import ShowError from "../../showError/ShowError";
import { Form } from "react-bootstrap";
import SelectForm from "../../select-form/SelectForm";
import { getDepartamentos } from "../../../services/departamentos";
import { useEffect } from "react";

const licencias = [
  {
    id: 1,
    name: "A",
  },
  {
    id: 2,
    name: "C",
  },
  {
    id: 3,
    name: "B",
  },
];

const transporte = [
  {
    id: 1,
    value: "true",
  },
  {
    id: 2,
    value: "false",
  },
];

const RegistroFrom = ({ onSubmitForm, initialValue = undefined }) => {
  const methods = useForm({
    resolver: zodResolver(validationSchema),
  });

  const {
    reset,
    control,
    handleSubmit,
    register,
    watch,
    setValue,
    formState: { isSubmitSuccessful, errors },
  } = methods;

  const departamento = watch("id_dep", -1);
  const rawDepartamentos = useQuery("get-departamentos", getDepartamentos, {
    staleTime: 30000,
  });
  const rawMunicipios = useQuery(
    ["get-municpios-by-departamento", departamento],
    getDepartamentoPorMunicipio,
    {
      enabled: departamento !== -1,
    }
  );

  useEffect(() => {
    if (initialValue) {
      console.log(initialValue);
      setValue("nombre", initialValue.NOMBRE);
      setValue("apellido", initialValue.APELLIDO);
      setValue("usuario", initialValue.USUARIO);
      setValue("contra", initialValue.CONTRASENA);
      setValue("correo", initialValue.CORREO);
      setValue("telefono", initialValue.TELEFONO);
      setValue("nit", initialValue.NIT);
      setValue("id_dep", initialValue.ID_DEP);
      setValue("id_muni", initialValue.ID_MUNI);
      setValue("lugar", initialValue.LUGAR);
      setValue("licencia", initialValue.LICENCIA);
      setValue("transporte", initialValue.TRANSPORTE);
    }
  }, []);

  if (rawDepartamentos.isLoading) {
    return (
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={rawDepartamentos.isLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }

  if (rawMunicipios.isError || rawDepartamentos.isError) {
    return (
      <ShowError
        title="Error"
        description="Estamos teniendo problemas al cargar esta pagina."
        message="Intenta recargar la pagina. Si el problema presiste comunicate con IT"
      />
    );
  }

  const onSubmit = async (values) => {
    if (isSubmitSuccessful) {
      reset();
    }

    const request = { ...values };
    onSubmitForm(request);
  };

  return (
    <div className="bg-white shadow-md  rounded mx-auto">
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid lg:grid-cols-2 sm:grid-cols-1 gap-4 p-4">
            <div>
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
                name="contra"
                controlId="contraseña"
                type="password"
                required={!initialValue  ? true : false}
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
            </div>
            <div>
              <FormInput
                placeholder="Ingresa tu numero de nit"
                errors={errors}
                name="nit"
                controlId="nit"
                type="text"
                register={register}
              />

              <SelectForm
                control={control}
                required={true}
                errors={errors}
                register={register}
                name="id_dep"
                label="Departamento"
                props={{ sx: { mb: "8px" } }}
                defaultValue={1}
              >
                {rawDepartamentos.data.map((d) => (
                  <MenuItem key={d.DEP_ID} value={d.DEP_ID}>
                    {d.NOMBRE}
                  </MenuItem>
                ))}
              </SelectForm>

              {rawMunicipios.data && (
                <SelectForm
                  control={control}
                  required={true}
                  errors={errors}
                  register={register}
                  name="id_muni"
                  label="municipio"
                  props={{ sx: { mb: "8px" } }}
                >
                  {rawMunicipios.data.map((d) => {
                    return (
                      <MenuItem key={d.MUN_ID} value={d.MUN_ID}>
                        {d.NOMBRE_MUNICIPIO}
                      </MenuItem>
                    );
                  })}
                </SelectForm>
              )}

              <FormInput
                placeholder="Lugar"
                errors={errors}
                name="lugar"
                controlId="lugar"
                type="text"
                register={register}
              />
              <SelectForm
                control={control}
                required={true}
                errors={errors}
                register={register}
                name="licencia"
                label="Tipo de Licencia"
                props={{ sx: { mb: "8px" } }}
              >
                {licencias.map((d) => {
                  return (
                    <MenuItem key={d.name} value={d.name}>
                      {d.name}
                    </MenuItem>
                  );
                })}
              </SelectForm>
              <SelectForm
                control={control}
                required={true}
                errors={errors}
                register={register}
                name="transporte"
                label="Posee Transporte"
                props={{ sx: { mb: "8px" } }}
              >
                {transporte.map((d) => {
                  return (
                    <MenuItem key={d.value} value={d.value}>
                      {d.value}
                    </MenuItem>
                  );
                })}
              </SelectForm>
              <span>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Label>Documento</Form.Label>
                  <Form.Control type="file" {...register("documento")} />
                </Form.Group>
              </span>
            </div>
            <Button
              className="p-2 w-100 mx-auto"
              type="submit"
              variant="contained"
            >
              {initialValue ? 'Actualizar': 'Registrar'}
            </Button>
          </div>
        </form>
      </FormProvider>
    </div>
  );
};

export default RegistroFrom;
