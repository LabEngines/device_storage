import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

import './DeviceCard.css'; // Подключаем CSS файл для стилей страницы

function DeviceCard() {
    function DeviceList() {
        const [devices, setDevices] = useState([]);

        useEffect(() => {
            axios.get('http://127.0.0.1:8000/devices/')
                .then(response => setDevices(response.data))
                .catch(error => console.error('Error:', error));
        }, []);
        return (
            devices.map(device => (

                <Card className={"card"}
                    border={device.user === "" ? "success" : "danger"}
                    style={{ width: '18rem', margin: '0.5rem' }}
                    text={'dark'} key={'Danger'}
                >
                    <Card.Img  variant="top" src="https://www.wolflair.com/wp-content/uploads/2017/02/placeholder.jpg" />
                    <Card.Body className={"card__title"}>
                        <Card.Title>Device name: {device.device_name}</Card.Title>

                    </Card.Body>
                    <ListGroup className="list-group-flush">
                        <ListGroup.Item>Device MAC: {device.device_mac}</ListGroup.Item>
                        <ListGroup.Item>User: {device.user || "N/A"}</ListGroup.Item>

                    </ListGroup>
                </Card>

            )
            ))

            // <div className="device-list">
            //     {devices.map(device => (
            //         <div key={device.id} className="mdc-card device-card">
            //             <div className="mdc-card__primary-action device-card__primary-action">
            //                 <div className="device-card__media"></div>
            //                 <div className="device-card__text">
            //                     <h2 className="mdc-typography--headline6">{device.device_name}</h2>
            //                     <h3 className="mdc-typography--subtitle2">Device MAC: {device.device_mac}</h3>
            //                     <p className="mdc-typography--body2">User: {device.user || 'N/A'}</p>
            //                 </div>
            //             </div>
            //         </div>
            //     ))}
            // </div>
        // );
    // }

}
    return DeviceList()
}

export default DeviceCard;
