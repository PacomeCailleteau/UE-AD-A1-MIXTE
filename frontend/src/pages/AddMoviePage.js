import React from 'react';
import AddMovie from "../components/AddMovie";

function UpdateMoviePage() {
    return (
        <div className="container mt-5 mb-5 px-3 py-4">
            <div className="d-flex justify-content-between align-items-center">
                <h1>Ajouter un film</h1>
                <a href="/" className="btn btn-secondary">Revenir à l'accueil</a>
            </div>
            <AddMovie />
        </div>
    );
}

export default UpdateMoviePage;
