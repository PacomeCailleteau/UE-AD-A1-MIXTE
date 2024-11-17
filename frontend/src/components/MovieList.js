import React, { useState } from "react";
import {useMutation, useQuery} from "@apollo/client";
import { GET_MOVIES } from "../graphql/queries";
import { Link } from "react-router-dom";
import {DELETE_MOVIE} from "../graphql/mutations";

const MovieList = () => {
    const { data, loading, error, refetch } = useQuery(GET_MOVIES);

    const [deleteMovie, { loading: deleting }] = useMutation(DELETE_MOVIE, {
        onCompleted: () => {
            refetch();
        },
    });

    const [currentPage, setCurrentPage] = useState(1);
    const [moviesPerPage, setMoviesPerPage] = useState(5);

    if (loading) return <p>Chargement...</p>;
    if (error) return <p>Erreur : {error.message}</p>;

    const indexOfLastMovie = currentPage * moviesPerPage;
    const indexOfFirstMovie = indexOfLastMovie - moviesPerPage;
    const currentMovies = data.movies.slice(indexOfFirstMovie, indexOfLastMovie);

    const totalPages = Math.ceil(data.movies.length / moviesPerPage);

    const handleDelete = async (id) => {
        const confirmed = window.confirm("Êtes-vous sûr de vouloir supprimer ce film ?");
        if (confirmed) {
            try {
                await deleteMovie({ variables: { id } });
                alert("Le film a été supprimé avec succès !");
            } catch (err) {
                alert("Une erreur s'est produite lors de la suppression du film.");
            }
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) setCurrentPage(currentPage - 1);
    };

    const handleNextPage = () => {
        if (currentPage < totalPages) setCurrentPage(currentPage + 1);
    };

    const handleMoviesPerPageChange = (e) => {
        const value = parseInt(e.target.value, 10);
        if (value > 0) {
            setMoviesPerPage(value);
            setCurrentPage(1);
        }
    };

    const handlePageChange = (e) => {
        const value = parseInt(e.target.value, 10);
        if (value > 0 && value <= totalPages) {
            setCurrentPage(value);
        }
    };

    return (
        <div>
            <ul className="list-group">
                {currentMovies.map((movie) => (
                    <li key={movie.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h5>{movie.title}</h5>
                            <p>Id: {movie.id}</p>
                            <p>Réalisé par : {movie.director}</p>
                            <p>Note : {movie.rating}</p>
                        </div>
                        <div className="d-flex flex-column align-items-end">
                            <Link to={`/update-movie/${movie.id}`} className="btn btn-primary mb-2">Modifier</Link>
                            <button
                                className="btn btn-danger"
                                onClick={() => handleDelete(movie.id)}
                                disabled={deleting}
                            >
                                {deleting ? "Suppression..." : "Supprimer"}
                            </button>
                        </div>
                    </li>
                ))}
            </ul>

            <div className="mt-3">
                <div className="d-flex justify-content-between align-items-center mb-3">
                    <button
                        className="btn btn-secondary"
                        onClick={handlePreviousPage}
                        disabled={currentPage === 1}
                    >
                        Précédent
                    </button>
                    <span>
                        Page {currentPage} sur {totalPages}
                    </span>
                    <button
                        className="btn btn-secondary"
                        onClick={handleNextPage}
                        disabled={currentPage === totalPages}
                    >
                        Suivant
                    </button>
                </div>

                <div className="d-flex justify-content-between align-items-center mb-3">
                    <label>
                        Films par page :
                        <input
                            type="number"
                            value={moviesPerPage}
                            onChange={handleMoviesPerPageChange}
                            className="form-control d-inline-block mx-2"
                            style={{ width: "80px" }}
                        />
                    </label>

                    <label>
                        Aller à la page :
                        <input
                            type="number"
                            value={currentPage}
                            onChange={handlePageChange}
                            className="form-control d-inline-block mx-2"
                            style={{ width: "80px" }}
                        />
                    </label>
                </div>
            </div>
        </div>
    );
};

export default MovieList;
