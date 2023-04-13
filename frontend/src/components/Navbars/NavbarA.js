import { React } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const NavbarA = () => {

  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>

          <Nav.Link style={{ color: 'white', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon">
            <img src="https://cdn-icons-png.flaticon.com/512/1453/1453025.png" alt="Logo" width="50" height="50" />
            <span >ADMINISTRADOR</span>
          </Nav.Link>

          <Nav className="me-auto  mx-auto">
            <Nav.Link href="/Repartidor" style={{ color: 'white' }}>Repartidores</Nav.Link>
            <Nav.Link href="/Empresa" style={{ color: 'white' }}>Empresa</Nav.Link>
            <Nav.Link href="/Cliente" style={{ color: 'white' }}>Cliente</Nav.Link>
            <Nav.Link href="/Reportes" style={{ color: 'white' }}>Reportes</Nav.Link>
            <Nav.Link href="/" style={{ color: 'white' }}>Cerrar Sesión</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavbarA
