import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from '@apollo/client';
import movieClient from './apolloClient';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.css';

const rootElement = document.getElementById("root");
ReactDOM.render(
    <ApolloProvider client={movieClient}>
        <App />
    </ApolloProvider>,
    rootElement
);
