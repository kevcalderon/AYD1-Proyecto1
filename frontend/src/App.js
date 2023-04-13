import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./components/Vistas/Inicio";
import LoginAdmin from "./components/Vistas/Administrador/Login";
import LoginCliente from "./components/Vistas/Cliente/Login";
import LoginEmpresa from "./components/Vistas/Empresa/Login";
import LoginRepartidor from "./components/Vistas/Repartidor/Login"; 
import RegistroCliente from "./components/Vistas/Cliente/Registro";
import RegistroEmpresa from "./components/Vistas/Empresa/Registro";
import RegistroRepartidor from "./components/Vistas/Repartidor/Registro";
import AcercaDe from "./components/Vistas/AcercaDe";

// ADMIN
import Cliente from "./components/Vistas/Administrador/Cliente";
import Empresa from "./components/Vistas/Administrador/Empresa";
import Repartidor from "./components/Vistas/Administrador/Repartidores";
import Reportes from "./components/Vistas/Administrador/Reportes";

// EMPRESA
import CrearCombo from "./components/Vistas/Empresa/CrearCombo";
import CrearProducto from "./components/Vistas/Empresa/CrearProducto";
import ReportesE from "./components/Vistas/Empresa/Reportes";
import Pedidos from "./components/Vistas/Empresa/Pedidos";
import Productos from "./components/Vistas/Empresa/Productos";
import VerCombos from "./components/Vistas/Empresa/VerCombos";

// CLIENTE
import MisPedidos from "./components/Vistas/Cliente/MisPedidos";
import Carrito from "./components/Vistas/Cliente/MiCarrito";
import Empresas from "./components/Vistas/Cliente/Empresas";
import ProductosC from "./components/Vistas/Cliente/Productos";

// REPARTIDOR
import MiPedido from "./components/Vistas/Repartidor/MiPedido";
import PedidosZona from "./components/Vistas/Repartidor/PedidosZona";
import Historial from "./components/Vistas/Repartidor/Historial";
import Perfil from "./components/Vistas/Repartidor/MiPerfil";

function App() {
  return (
    <Router>
      <Routes>
        {/*  INICIO  */}
        <Route path={"/"} element={<Login />} />
        <Route path={"/LoginAdmin"} element={<LoginAdmin />} />
        <Route path={"/LoginCliente"} element={<LoginCliente />} />
        <Route path={"/LoginEmpresa"} element={<LoginEmpresa />} />
        <Route path={"/LoginRepartidor"} element={<LoginRepartidor />} />
        <Route path={"/RegistroCliente"} element={<RegistroCliente />} />
        <Route path={"/RegistroEmpresa"} element={<RegistroEmpresa />} />
        <Route path={"/RegistroRepartidor"} element={<RegistroRepartidor />} />
        <Route path={"/AcercaDe"} element={<AcercaDe />} />

        {/*ADMIN*/}
        <Route path={"/Cliente"} element={<Cliente />} />
        <Route path={"/Empresa"} element={<Empresa />} />
        <Route path={"/Repartidor"} element={<Repartidor />} />
        <Route path={"/Reportes"} element={<Reportes />} />

        {/*EMPRESA*/}
        <Route path={"/CrearCombo"} element={<CrearCombo />} />
        <Route path={"/CrearProducto"} element={<CrearProducto />} />
        <Route path={"/ReportesE"} element={<ReportesE />} />
        <Route path={"/Pedidos"} element={<Pedidos />} />
        <Route path={"/Productos"} element={<Productos />} />
        <Route path={"/VerCombos"} element={<VerCombos />} />

        {/*CLIENTE*/}
        <Route path={"/MisPedidos"} element={<MisPedidos />} />
        <Route path={"/Carrito"} element={<Carrito />} />
        <Route path={"/Empresas"} element={<Empresas />} />
        <Route path={"/ProductosC"} element={<ProductosC />} />
        
        {/*REPARTIDOR*/}
        <Route path={"/MiPedido"} element={<MiPedido />} />
        <Route path={"/PedidosZona"} element={<PedidosZona />} />
        <Route path={"/Historial"} element={<Historial />} />
        <Route path={"/Perfil"} element={<Perfil />} />

      </Routes>
    </Router>
  );
}

export default App;
