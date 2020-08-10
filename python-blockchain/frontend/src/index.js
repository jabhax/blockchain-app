import React from 'react';
import ReactDOM from 'react-dom';
import {Router, Switch, Route} from 'react-router-dom';
import history from './history';
import './index.css';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';


ReactDOM.render(
    <Router history={history}>
        <Switch>
            <Route path='/' component={App} exact/>
            <Route path='/blockchain' component={Blockchain} exact/>
            <Route path='/conduct-transaction' component={ConductTransaction} exact/>
            <Route path='/transaction-pool' component={TransactionPool} exact/>
        </Switch>
    </Router>,
    document.getElementById('root'));
