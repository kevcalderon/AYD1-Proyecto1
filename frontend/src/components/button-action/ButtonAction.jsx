import { Button } from "@mui/material";
import { asignarPedido } from "../../services/pedidos";

const ButtonAction = ({ variant, color, label, callBack, id_orden }) => {
  return (
    <Button variant={variant} color={color} onClick={() => callBack(id_orden)}>
      {label}
    </Button>
  );
};

export default ButtonAction;
