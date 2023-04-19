import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useMemo, useState } from "react";
import { Backdrop, Button, CircularProgress, IconButton } from "@mui/material";
import FormInput from "../../form-input/FormInput";
import validationSchema from "./RegistroSchema";
import AutoCompleteForm from "../../autocomplete/Autocomplete";
import { getDepartamentoPorMunicipio } from "../../../services/municipios";
import { useQuery } from "react-query";
import ShowError from "../../showError/ShowError";
import { Form } from "react-bootstrap";

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

const tieneLicencia = [
  {
    id: 1,
    value: "true",
  },
  {
    id: 2,
    value: "false",
  },
];

const RegistroFrom = ({ departamentos, onSubmitForm }) => {
  const methods = useForm({
    resolver: zodResolver(validationSchema),
  });

  const {
    reset,
    control,
    handleSubmit,
    register,
    watch,
    formState: { isSubmitSuccessful, errors },
  } = methods;

  const departamento = watch("departamento", -1);
  const [documentError, setDocumentError] = useState(false);
  const [documento, setDocumento] = useState();
  const [mustFetchMunicipios, setMustFetchMunicipios] = useState(false);
  const [municipios, setMunicipios] = useState([]);
  const rawMunicipios = useQuery(
    ["get-municpios-by-departamento", departamento],
    getDepartamentoPorMunicipio,
    {
      enabled: mustFetchMunicipios,
    }
  );

  useMemo(() => {
    setMunicipios(rawMunicipios.data);
  }, [rawMunicipios.data]);

  useEffect(() => {
    setMustFetchMunicipios(true);
  }, [departamento]);

  useEffect(() => {
    setMustFetchMunicipios(false);
  }, [municipios]);

  if (rawMunicipios.isError) {
    console.log(rawMunicipios);
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
      setDocumento(undefined);
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
              <AutoCompleteForm
                control={control}
                options={departamentos}
                getOptionLabel={(opt) => `${opt.NOMBRE}`}
                isOptionEqualToValue={(opt, value) =>
                  opt.NOMBRE === value.NOMBRE
                }
                renderOptions={(opt) => opt.NOMBRE}
                getKey={(opt) => opt.DEP_ID}
                errors={errors}
                name="departamento"
                label="Departamento"
                classname="mb-2"
              />
              {rawMunicipios.data && (
                <AutoCompleteForm
                  control={control}
                  options={municipios}
                  getOptionLabel={(opt) => `${opt.NOMBRE_MUNICIPIO}`}
                  isOptionEqualToValue={(opt, value) =>
                    opt.NOMBRE_MUNICIPIO === value.NOMBRE_MUNICIPIO
                  }
                  renderOptions={(opt) => opt.NOMBRE_MUNICIPIO}
                  getKey={(opt) => opt.MUN_ID}
                  errors={errors}
                  name="municipio"
                  label="Municipios"
                  classname="mb-2"
                />
              )}
              <FormInput
                placeholder="Lugar"
                errors={errors}
                name="lugar"
                controlId="lugar"
                type="text"
                register={register}
              />
              <AutoCompleteForm
                control={control}
                options={licencias}
                getOptionLabel={(opt) => `${opt.name}`}
                isOptionEqualToValue={(opt, value) => opt.name === value.name}
                renderOptions={(opt) => opt.name}
                getKey={(opt) => opt.id}
                errors={errors}
                name="licencia"
                label="Licencia"
                classname="mb-2"
              />
              <AutoCompleteForm
                control={control}
                options={tieneLicencia}
                getOptionLabel={(opt) => `${opt.value}`}
                isOptionEqualToValue={(opt, value) => opt.value === value.value}
                renderOptions={(opt) => opt.value}
                getKey={(opt) => opt.id}
                errors={errors}
                name="transporte"
                label="Transporte"
                classname="mb-2"
              />
              <span>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Label>Documento</Form.Label>
                  <Form.Control type="file" {...register("documento")} />
                </Form.Group>
                {documentError && (
                  <small className="text-red-600">
                    El documento es un campo obligatorio
                  </small>
                )}
              </span>
            </div>
            <Button
              className="p-2 w-100 mx-auto"
              type="submit"
              variant="contained"
            >
              Registrar
            </Button>
          </div>
        </form>
      </FormProvider>
    </div>
  );
};

export default RegistroFrom;
