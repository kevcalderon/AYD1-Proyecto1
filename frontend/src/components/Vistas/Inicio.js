import React from "react";
import NavBar from "../Navbars/NavbarU";
import DeliveryImage from "./inicio.jpg";
import Badge from "react-bootstrap/Badge";

function Inicio() {
  return (
    <div style={{ color: "white" }}>
      <NavBar />
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-around",
          padding: "50px",
        }}
      >
        <div>
          <h1 style={{ fontSize: "3rem", marginBottom: "20px" }}>
            <Badge bg="danger">¡Todo lo que necesites, te lo llevamos! </Badge>
          </h1>
          <p
            style={{
              fontSize: "1.5rem",
              maxWidth: "700px",
              textAlign: "justify",
            }}
          >
            En AlChilazo, no hay límites para tu imaginación. Lo que sea que
            desees, lo llevamos directamente desde tu mente hasta donde estés en
            cuestión de minutos. Pide lo que quieras y deja que nosotros nos
            encarguemos del resto. En AlChilazo, hacemos realidad tus deseos en
            un abrir y cerrar de ojos.
          </p>
          <p
            style={{
              fontSize: "1.5rem",
              maxWidth: "700px",
              textAlign: "justify",
            }}
          >
            ¿Quieres algo? ¡Consíguelo! Pide desde los mejores restaurantes, haz
            tus compras de supermercado, consigue la comida para tu mascota,
            compra bebidas para tus amigos, y mucho más. Con AlChilazo, puedes
            tener todo lo que necesitas entregado directamente en tu puerta en
            solo unos simples pasos. Descubre, pide y recibe a domicilio con
            AlChilazo.
          </p>
        </div>
        <img
          src={DeliveryImage}
          alt="Delivery"
          style={{ width: "500px", height: "500px", objectFit: "contain" }}
        />
      </div>
    </div>
  );
}

export default Inicio;
