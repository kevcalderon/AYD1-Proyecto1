import { React } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const NavbarR = () => {

  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>

          <Nav.Link style={{ color: 'white', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon">
            <img src="https://cdn-icons-png.flaticon.com/512/1453/1453025.png" alt="Logo" width="50" height="50" />
            <span >REPARTIDOR</span>
          </Nav.Link>

          <Nav className="me-auto  mx-auto">
            <Nav.Link href="/PedidosZona" style={{ color: 'white' }}>Pedidos en la Zona</Nav.Link>
            <Nav.Link href="/MiPedido" style={{ color: 'white' }}>Mi Pedido</Nav.Link>
            <Nav.Link href="/Perfil" style={{ color: 'white' }}>Mi Perfil</Nav.Link>
            <Nav.Link href="/Historial" style={{ color: 'white' }}>Historial</Nav.Link>
            <Nav.Link href="/" style={{ color: 'white' }}>Cerrar Sesión</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavbarR 