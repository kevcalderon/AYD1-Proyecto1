import { React, useState, useEffect } from 'react'
import NavbarC from '../../Navbars/NavbarC'
import CartaEmpresa from './CartaEmpresa';
import { Container } from "react-bootstrap";
import Form from 'react-bootstrap/Form';
import API_URL from "../../../app/constants";

function Empresas() {
  const [empresas, setEmpresas] = useState([]);
  const [categorias, setCategorias] = useState([]);

  useEffect(() => {
    const getTiposEmpresa = async () => {
      await fetch(`${API_URL}/mostrarTiposEmpresa`)
        .then((response) => response.json())
        .then((res) => {
          setCategorias(res);
        });
    };

    getTiposEmpresa();
  }, []);



  useEffect(() => {
    const getEmpresas = async () => {
      await fetch(
        `${API_URL}/obtenerListaEmpresas`,
        {
          method: "GET",
        }
      )
        .then((response) => response.json())
        .then((res) => {
          if (res.exito) {
            setEmpresas(res.empresas)
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
    getEmpresas()
  }, [])

  const obtenerEmpresas = async (tipo) => {
    await fetch(
      `${API_URL}/VerEmpresasPorTipo/${tipo}`,
      {
        method: "GET",
      }
    )
      .then((response) => response.json())
      .then((res) => {
        if (!res.exito){
          setEmpresas([])
          return
        }
        setEmpresas(res.empresas)
      })
      .catch((error) => {
        console.log(error);
      });
  }


  return (
    <div style={{ color: "white" }}>
      <NavbarC />

      <div style={{ display: "flex", flexDirection: "row" }}>
        <div style={{ width: "20%", margin: "10px", marginLeft: "auto", marginRight: "auto" }}>
          <label style={{ fontWeight: "bold" }}>Ver por Categoría:</label>
          <Form.Select aria-label="Default select example" onChange={e => obtenerEmpresas(e.target.value)}>
            <option>Seleccione una categoría</option>
            {categorias.map((tipo) => {
              return (
                <option key={tipo.T_EMP_ID} value={tipo.T_EMP_ID}>
                  {tipo.NOMBRE}
                </option>
              );
            })}
          </Form.Select>
        </div>
      </div>


      <Container style={{ display: 'flex', flexWrap: 'wrap' }}>
        {empresas.map((item) => (
          <CartaEmpresa
            id={item.EMP_ID}
            nombre={item.NOMBRE}
            tipos={categorias}
            tipo={item.TIPO_EMPRESA_T_EMP_ID || item.T_EMP_ID}
            descripcion={item.DESCRIPCION}
            imagen={item.DOCUMENTO}
          />
        ))}



      </Container>
    </div>

  )
}

export default Empresas