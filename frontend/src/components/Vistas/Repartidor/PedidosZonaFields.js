import ButtonAction from "../../button-action/ButtonAction";

export const fields = (callback) => {
  return [
    {
      accessorKey: "CLIENTE",
      header: "Cliente",
      id: "cliente",
    },
    {
      accessorKey: "DEPARTAMENTO",
      header: "Departamento",
      id: "departamento",
    },
    {
      accessorKey: "MUNICIPIO",
      header: "Municipio",
      id: "municipio",
    },
    {
      accessorKey: "ESTADO",
      header: "Estado",
      id: "estado",
    },
    {
      accessorKey: "LUGAR",
      header: "Lugar",
      id: "lugar",
    },
    {
      accessorKey: "METODO_PAGO",
      header: "Metodo de Pago",
      id: "metodo_pago",
    },
    {
      header: "Acciones",
      id: "acciones",
      Cell: ({ row }) => (
        <div>
          <ButtonAction
            variant="contained"
            color="secondary"
            label="Asignar"
            id_orden={row.original.ORD_ID}
            callBack={callback}
          />
        </div>
      ),
    },
  ];
};
