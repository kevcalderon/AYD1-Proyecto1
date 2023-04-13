import { React } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const NavbarE = () => {

  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container> 

          <Nav.Link style={{ color: 'white', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon"> 
            <img src="https://cdn-icons-png.flaticon.com/512/1453/1453025.png" alt="Logo" width="50" height="50" />
            <span >EMPRESA</span>
          </Nav.Link>

          <Nav className="me-auto  mx-auto">
            <Nav.Link href="/Pedidos">Pedidos</Nav.Link>
            <Nav.Link href="/CrearProducto">Crear Producto</Nav.Link>
            <Nav.Link href="/Productos">Productos</Nav.Link>
            <Nav.Link href="/CrearCombo">Crear Combo</Nav.Link>
            <Nav.Link href="/VerCombos">Ver Combos</Nav.Link>
            <Nav.Link href="/ReportesE">Reportes</Nav.Link>
            <Nav.Link href="/">Cerrar Sesión</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavbarE 