import React, { useEffect, useState } from 'react';
import NavbarC from '../../Navbars/NavbarC';
import { Container, Button, Form, Table, Modal } from 'react-bootstrap';
import API_URL from '../../../app/constants';

function MisPedidos() {

  const cliente = JSON.parse(localStorage.getItem('cliente'));

  const [orders, setOrders] = useState([]);

  const [showModal, setShowModal] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [comment, setComment] = useState('');
  const [rating, setRating] = useState('');

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedOrder(null);
    setComment('');
    setRating('');
  }

  const handleOpenModal = (order) => {
    setSelectedOrder(order);
    setShowModal(true);
  }



  const renderStars = (numStars) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <Button
          key={i}
          variant={i <= numStars ? 'warning' : 'outline-warning'}
          onClick={() => setRating(i)}
        >
          ★
        </Button>
      );
    }
    return stars;
  }

  const handleSaveRating = () => {
    if (rating >= 0 && rating <= 5) {
      const updatedOrders = orders.map((order) => {
        if (order.ORD_ID === selectedOrder.ORD_ID) {
          return {
            ...order,
            CALIFICACION: rating,
            COMENTARIO: comment
          };
        } else {
          return order;
        }
      });

      console.log(updatedOrders);

      setOrders(updatedOrders);
      handleCloseModal();

      var json = {
        "id_orden": selectedOrder.ORD_ID,
        "calificacion": rating,
        "comentario": comment
      }

      console.log(JSON.stringify(json));

      fetch(`${API_URL}/ActualizarComentarioCalificacion`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
        })
    }
  }



  useEffect(() => {
    const getOrders = async () => {
      await fetch(
        `${API_URL}/VerOrdenesCliente/${cliente.CLI_ID}`,
        {
          method: "GET",
        }
      )
        .then((response) => response.json())
        .then((data) => {
          console.log(data.ordenes)
          setOrders(data.ordenes);
        })
        .catch((error) => {
          console.log(error);
        });
    };
    getOrders();
  }, []);



  return (
    <div style={{ color: 'black' }}>
      <NavbarC />
      <Container style={{ marginTop: '20px', fontSize: '20px' }}>
        <h2>MIS PEDIDOS</h2>
      </Container>
      <Container style={{ backgroundColor: 'white', padding: '20px', marginTop: '20px' }}>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>ID ORDEN</th>
              <th>FECHA ORDEN</th>
              <th>DIRECCIÓN</th>
              <th>NOMBRE REPARTIDOR</th>
              <th>CALIFICACIÓN</th>
              <th>COMENTARIO</th>
              <th>MÉTODO DE PAGO</th>
              <th>ESTADO</th>
              <th>OPCIONES</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.ORD_ID}>
                <td>{order.ORD_ID}</td>
                <td>{order.FECHA}</td>
                <td>{order.LUGAR}</td>
                <td>{order.NOMBRE_REPARTIDOR}</td>
                <td>{order.CALIFICACION}</td>
                <td>{order.COMENTARIO}</td>
                <td>{order.METODO_PAGO}</td>
                <td>{order.ESTADO}</td>
                <td>
                  {
                    order.CALIFICACION === null || order.CALIFICACION === undefined ? (
                      order.ESTADO !== undefined ? (
                        order.ESTADO.toLowerCase() === "entregado" || order.ESTADO.toLowerCase() === "entregada" ? (
                          <Button variant="success" onClick={() => handleOpenModal(order)}>
                            OPCIONES
                          </Button>
                        ) : null
                      ) : null
                    ) : null
                  }
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Calificar servicio</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Comentario</Form.Label>
              <Form.Control
                type="text"
                placeholder="Ingresa tu comentario"
                value={comment}
                onChange={(event) => setComment(event.target.value)}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Calificación</Form.Label>
              <div>{renderStars(parseInt(rating))}</div>
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Cancelar
          </Button>
          <Button variant="primary" onClick={handleSaveRating}>
            Guardar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default MisPedidos;