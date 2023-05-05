import { React, useState, useEffect } from 'react'
import { Button, Card, Container } from "react-bootstrap"; 
import API_URL from "../../../app/constants";

function CartaProducto(props) {
    const [imagen, setImagen] = useState("https://cdn-icons-png.flaticon.com/512/1453/1453025.png");
    const [agregado, setAgregado] = useState(false);

    useEffect(() => {
        const existeLocal = () => {
            var carrito = JSON.parse(localStorage.getItem("carrito"));
            if(carrito == null){
                carrito = [];
            }

            for (var i = 0; i < carrito.length; i++) {
                if (carrito[i].idproducto === props.id) {
                    setAgregado(true);
                }
            }
        };
        existeLocal();
    }, []);

    const agregar = () => {
        var cliente = JSON.parse(localStorage.getItem("cliente"));

        var idCliente = cliente.CLI_ID;
        var idProducto = props.id;
        /*
            id={item.PRO_ID}
            nombre={item.NOMBRE_PRODUCTO}
            tipo={item.NOMBRE_TIPO_PRODUCTO}
            precio={item.PRECIO}
            imagen={item.FOTOGRAFIA}
            descripcion={item.DESCRIPCION}
            stock={item.STOCK}
            tipoProductoID={item.T_PRO_ID} 
        */
        var json = { 
            idproducto: props.id,
            nombre: props.nombre,
            tipo: props.tipo,
            precio: props.precio,
            imagen: props.imagen,
            descripcion: props.descripcion,
            stock: props.stock,
            tipoProductoID: props.tipoProductoID,
            cantidad: 1,
            observacion: "",
        }
 
        setAgregado(true);
        var datos = localStorage.getItem('carrito')
        if (datos === null || datos === undefined) { 
            console.log(datos)
            localStorage.setItem('carrito', JSON.stringify([json]))
        }else{
            datos=JSON.parse(datos)
            datos.push(json)
            console.log(datos)
            localStorage.setItem('carrito', JSON.stringify(datos))
        } 
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
                <Card.Text style={{ color: "black" }}>Tipo: {props.tipo}</Card.Text>
                <Card.Text style={{ color: "black" }}>Descripción: {props.descripcion}</Card.Text>
                <Card.Text style={{ color: "black" }}>Precio: {props.precio}</Card.Text>
                <Container>
                    {agregado ? (
                        <Button variant="danger" disabled>
                            AGREGADO
                        </Button>
                    ) : (
                        <Button variant="success" onClick={agregar}>
                            AGREGAR AL CARRITO
                        </Button>
                    )}
                </Container>
            </Card.Body>
        </Card>
    );
}

export default CartaProducto;
