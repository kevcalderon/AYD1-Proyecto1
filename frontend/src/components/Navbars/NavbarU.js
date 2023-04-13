import { React, useState } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Icon } from '@iconify/react';

import userIcon from '@iconify-icons/fa-solid/user';
import empresaIcon from '@iconify-icons/mdi/company';
import repartidorIcon from '@iconify-icons/ic/twotone-delivery-dining';
import adminIcon from '@iconify-icons/wpf/administrator' 

const NavbarU = () => {
  const [showEmpresaMenu, setShowEmpresaMenu] = useState(false);
  const [showClienteMenu, setShowClienteMenu] = useState(false);
  const [showRepartidorMenu, setShowRepartidorMenu] = useState(false);
  const [showAdministradorMenu, setShowAdministradorMenu] = useState(false);


  const handleEmpresaClick = () => {
    setShowEmpresaMenu(!showEmpresaMenu);
    setShowClienteMenu(false);
    setShowRepartidorMenu(false);
    setShowAdministradorMenu(false);
  }

  const handleClienteClick = () => {
    setShowClienteMenu(!showClienteMenu);
    setShowEmpresaMenu(false);
    setShowRepartidorMenu(false);
    setShowAdministradorMenu(false);
  }

  const handleRepartidorClick = () => {
    setShowRepartidorMenu(!showRepartidorMenu);
    setShowEmpresaMenu(false);
    setShowClienteMenu(false);
    setShowAdministradorMenu(false);
  }

  const handleAdministradorClick = () => {
    setShowAdministradorMenu(!showAdministradorMenu);
    setShowEmpresaMenu(false);
    setShowClienteMenu(false);
    setShowRepartidorMenu(false);
  }



  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="/">
            <img src="https://cdn-icons-png.flaticon.com/512/1453/1453025.png" alt="Logo" width="50" height="50" />
          </Navbar.Brand>

          <Nav className="me-auto  mx-auto">
            <Nav.Link href="/" style={{ color: 'white' }}>Inicio</Nav.Link>

            <NavDropdown title="Autenticación" id="basic-nav-dropdown" style={{ color: 'white' }}>
              <Nav.Link onClick={handleEmpresaClick} style={{ color: 'black', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon">
                <Icon icon={empresaIcon} />
                <span>Empresa</span>
              </Nav.Link> 
              {showEmpresaMenu &&
                <>
                  <NavDropdown.Item href="/LoginEmpresa">Login</NavDropdown.Item>
                  <NavDropdown.Item href="/RegistroEmpresa">Registrarse</NavDropdown.Item>
                </>
              }

              <Nav.Link onClick={handleClienteClick} style={{ color: 'black', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon">
                <Icon icon={userIcon} />
                <span>Cliente</span>  
              </Nav.Link>
              {showClienteMenu &&
                <>
                  <NavDropdown.Item href="/LoginCliente">Login</NavDropdown.Item>
                  <NavDropdown.Item href="/RegistroCliente">Registrarse</NavDropdown.Item>
                </>
              }

              <Nav.Link onClick={handleRepartidorClick} style={{ color: 'black', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon">
                <Icon icon={repartidorIcon} />
                <span>Repartidor</span>
              </Nav.Link>
              {showRepartidorMenu &&
                <>
                  <NavDropdown.Item href="/LoginRepartidor">Login</NavDropdown.Item>
                  <NavDropdown.Item href="/RegistroRepartidor">Registrarse</NavDropdown.Item>
                </>
              }

              <Nav.Link onClick={handleAdministradorClick} style={{ color: 'black', display: 'flex', alignItems: 'center', gap: '0.5rem' }} className="nav-link-icon">
                <Icon icon={adminIcon} />
                <span>Administrador</span>
              </Nav.Link>
              {showAdministradorMenu &&
                <>
                  <NavDropdown.Item href="/LoginAdmin">Login</NavDropdown.Item>
                </>
              }

            </NavDropdown>
            <Nav.Link href="/AcercaDe" style={{ color: 'white' }}>Acerca De</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavbarU
