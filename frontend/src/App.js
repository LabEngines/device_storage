import logo from './logo.svg';
import './App.css';
import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import DeviceCard from './components/DeviceCard'
import 'bootstrap/dist/css/bootstrap.min.css';


class App extends Component {
    state = {
        cars: [
            {name: 'Audi'},
            {name: 'Ford'},
            {name: 'Bmw'},
            {name: 'Lamborghini'}
        ],
        pageTitle: 'React component'
    }

    mainContainer = () => {
        return (
            <Container>
                <Row>
                    <DeviceCard/>
                    <DeviceCard/>
                    <DeviceCard/>
                    <DeviceCard/>
                    <DeviceCard/>
                </Row>
            </Container>
        );
    }

    render() {
        console.log("Render")
        const divStyle = {textAlign: 'center'}
        const cars = this.state.cars
        return (
            <div className="d-flex" style={divStyle}>
                {this.mainContainer()}
            </div>

        );
    }
}

export default App;
