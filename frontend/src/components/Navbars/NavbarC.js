import { React } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const NavbarC = () => {

  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container> 

          <Nav.Link style={{ color: 'white', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon"> 
            <img src="https://cdn-icons-png.flaticon.com/512/1453/1453025.png" alt="Logo" width="50" height="50" />
            <span >CLIENTE</span>
          </Nav.Link>

          <Nav className="me-auto  mx-auto">
            <Nav.Link href="/Empresas">Empresas</Nav.Link>
            <Nav.Link href="/MisPedidos">Mis Pedidos</Nav.Link>
            <Nav.Link href="/Carrito">Mi Carrito</Nav.Link> 
            <Nav.Link href="/">Cerrar Sesión</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavbarC 