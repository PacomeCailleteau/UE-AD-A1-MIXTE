import React from 'react';
import { Link } from 'react-router-dom';
import MovieList from '../components/MovieList';

function AdminDashboard() {
    return (
        <div className="container mt-5 mb-5 px-3 py-4">
            <h1 className="mb-4">Dashboard Administrateur</h1>

            <section>
                <div className="d-flex justify-content-between align-items-center mb-4">
                    <h2>Films disponibles</h2>
                    <Link to="/add-movie">
                        <button className="btn btn-primary">Ajouter un film</button>
                    </Link>
                </div>
                <MovieList />
            </section>
        </div>
    );
}

export default AdminDashboard;
