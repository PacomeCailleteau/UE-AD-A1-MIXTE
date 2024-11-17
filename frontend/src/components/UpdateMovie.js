import React, { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { GET_MOVIE_BY_ID } from "../graphql/queries";
import { UPDATE_MOVIE } from "../graphql/mutations";
import { useParams } from "react-router-dom";
import { Form, Button, Alert } from "react-bootstrap";

const UpdateMovie = () => {
    const { id } = useParams();

    const { data, loading, error } = useQuery(GET_MOVIE_BY_ID, {
        variables: { id },
    });

    const [updateMovie, { loading: updating, error: updateError }] = useMutation(UPDATE_MOVIE);
    const [rating, setRating] = useState("");

    if (loading) return <p>Chargement des données...</p>;

    if (error) return <p>Erreur : {error.message}</p>;

    const movie = data?.movie_by_id;
    if (!movie) return <p>Film introuvable.</p>;

    if (rating === "" && movie.rating !== undefined) setRating(movie.rating);

    const isValidRating = () => {
        const numRating = parseFloat(rating);
        return !isNaN(numRating) && numRating >= 0 && numRating <= 10;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!isValidRating()) return;

        updateMovie({
            variables: {
                id,
                rating: parseFloat(rating),
            },
        });
    };

    return (
        <div>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Titre</Form.Label>
                    <Form.Control
                        type="text"
                        value={movie.title}
                        disabled
                        className="form-control my-2"
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Réalisateur</Form.Label>
                    <Form.Control
                        type="text"
                        value={movie.director}
                        disabled
                        className="form-control my-2"
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Note</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="Veuillez saisir une note entre 0 et 10"
                        value={rating}
                        onChange={(e) => setRating(e.target.value)}
                        isInvalid={rating && !isValidRating()}
                    />
                    <Form.Control.Feedback type="invalid">
                        Veuillez indiquer une note comprise entre 0 et 10.
                    </Form.Control.Feedback>
                </Form.Group>

                <Button variant="primary" type="submit" disabled={!isValidRating() || updating}>
                    {updating ? "Modification..." : "Modifier le film"}
                </Button>
            </Form>

            {updateError && <Alert variant="danger" className="mt-3">{updateError.message}</Alert>}
        </div>
    );
};

export default UpdateMovie;
