import React, { useState, useEffect } from "react";
import { Button, Card, Container } from "react-bootstrap";
import API_URL from "../../../app/constants";

function CartaEmpresa(props) {
    const [imagen, setImagen] = useState("https://cdn-icons-png.flaticon.com/512/1453/1453025.png");
    var tipoGen = "";
    for (let i = 0; i < props.tipos.length; i++) {
        if (props.tipos[i].T_EMP_ID === props.tipo) {
            tipoGen = props.tipos[i].NOMBRE;
        }
    }

    const ver = () => {
        window.location.href = "/ProductosC/" + props.id;
    };

    useEffect(() => {  
        const obtenerImagen = async (valueImage) => {
            await fetch(`${API_URL}/descargarArchivo/${valueImage}`, {
                method: "GET",
                headers: { "Content-Type": "multipart/form-data; charset=utf-8" },
            }).then((response) => {
                response.blob().then((blob) => {
                    let url = window.URL.createObjectURL(blob);
                    setImagen(url);
                });
            });
        }; 
        obtenerImagen(props.imagen);
    }, []);

    return (
        <Card style={{ width: "20%", margin: "10px" }}>
            <Card.Img variant="top" src={imagen} />
            <Card.Body>
                <Card.Title style={{ color: "black" }}>{props.nombre}</Card.Title>
                <Card.Text style={{ color: "black" }}>Tipo: {tipoGen}</Card.Text>
                <Card.Text style={{ color: "black" }}>Descripcion: {props.descripcion}</Card.Text>
                <Container>
                    <Button variant="success" onClick={ver}>
                        VER PRODUCTOS
                    </Button>
                </Container>
            </Card.Body>
        </Card>
    );
}

export default CartaEmpresa;