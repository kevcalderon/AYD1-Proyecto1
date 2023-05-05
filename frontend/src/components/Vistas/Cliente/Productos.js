import { React, useState, useEffect } from 'react'
import NavbarC from '../../Navbars/NavbarC'
import { useParams } from "react-router-dom";
import { Button, Container } from "react-bootstrap";
import Form from 'react-bootstrap/Form';

import CartaProducto from './CartaProducto';
import CartaCombo from './CartaCombo';
import API_URL from "../../../app/constants";

function Productos() {

  const params = useParams();

  const [productos, setProductos] = useState([]);

  const [combos, setCombos] = useState([]);

  const [tipos, setTipos] = useState([]);

  useEffect(() => {
    const getProductos = async () => {
      await fetch(
        `${API_URL}/mostrarProductosEmpresa/${params.id}`,
        {
          method: "GET",
        }
      )
        .then((response) => response.json())
        .then((res) => { 
          setProductos(res);
        })
        .catch((error) => {
          console.log(error);
        });
    }
    getProductos()
  }, [])

  useEffect(() => {
    const getCombos = async () => {
      await fetch(
        `${API_URL}/obtenerCombosEmpresa/${params.id}`,
        {
          method: "GET",
        }
      )
        .then((response) => response.json())
        .then((res) => {  
          if (res.combos != null) { 
            setCombos(res.combos);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
    getCombos()
  }, [])


  useEffect(() => {
    const getTiposProductos = async () => {
      await fetch(`${API_URL}/VerTiposProductos`)
        .then((response) => response.json())
        .then((res) => {
          setTipos(res.tipos);
        });
    };
    getTiposProductos();
  }, []);


  const obtenerProducs = async (id) => {
    await fetch(
      `${API_URL}/mostrarProductosEmpresa/${params.id}/${id}`,
      {
        method: "GET",
      }
    )
      .then((response) => response.json())
      .then((res) => { 
        setProductos(res);
      })
      .catch((error) => {
        console.log(error);
      });

    await fetch(
      `${API_URL}/VerCombosPorProducto/${id}`,
      {
        method: "GET",
      }
    )
      .then((response) => response.json())
      .then((res) => {
        
        if(res.combos.length == 1){
          if(res.combos[0].NOMBRE === undefined){
            setCombos([])
            return
          }
        }else{
          if (res.combos != null) {
            setCombos(res.combos);
          }
        }
        


       })
      .catch((error) => {
        console.log(error);
      });


  };


  return (
    <div style={{ color: "white" }}>
      <NavbarC />

      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ width: "20%", margin: "10px", marginLeft: "auto", marginRight: "auto" }}>
          <label style={{ fontWeight: "bold" }}>Ver por Tipo de Producto:</label>
          <Form.Select aria-label="Default select example" onChange={e => obtenerProducs(e.target.value)}>
            <option> Seleccione una categoría</option>
            {tipos.map((tipo) => {
              return (
                <option key={tipo.T_PRO_ID} value={tipo.T_PRO_ID}>
                  {tipo.NOMBRE}
                </option>
              );
            })}
          </Form.Select> 
        </div>
      </div>


      <Container style={{ display: 'flex', flexWrap: 'wrap' }}>
        {productos.map((item) => (
          <CartaProducto
            id={item.PRO_ID}
            nombre={item.NOMBRE_PRODUCTO}
            tipo={item.NOMBRE_TIPO_PRODUCTO}
            precio={item.PRECIO}
            imagen={item.FOTOGRAFIA}
            descripcion={item.DESCRIPCION}
            stock={item.STOCK}
            tipoProductoID={item.T_PRO_ID}
          />
        ))}

        {combos.map((item) => (
          <CartaCombo
            id={item.COMBO_COM_ID}
            nombre={item.NOMBRE_COMBO}
            descripcion={item.DESCRIPCION_COMBO}
            precio={item.PRECIO_COMBO}
            productos={item.PRODUCTOS}
            imagen={item.FOTOGRAFIA_COMBO}
          />
        ))}


      </Container>
    </div>
  )
}

export default Productos