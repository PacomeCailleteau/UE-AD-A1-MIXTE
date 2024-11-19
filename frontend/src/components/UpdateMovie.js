import React, { useState, useEffect } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { GET_MOVIE_BY_ID } from "../graphql/queries";
import { UPDATE_MOVIE } from "../graphql/mutations";
import { useParams } from "react-router-dom";
import { Form, Button, Alert } from "react-bootstrap";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const UpdateMovie = () => {
    const { id } = useParams();

    const { data, loading, error } = useQuery(GET_MOVIE_BY_ID, {
        variables: { id },
    });

    const [updateMovie, { loading: updating, error: updateError }] = useMutation(UPDATE_MOVIE);
    const [rating, setRating] = useState("");

    useEffect(() => {
        if (data && data.movie_by_id) {
            setRating(data.movie_by_id.rating);
        }
    }, [data]);

    if (loading) return <p>Chargement des données...</p>;

    if (error) return <p>Erreur : {error.message}</p>;

    const movie = data?.movie_by_id;
    if (!movie) return <p>Film introuvable.</p>;

    const isValidRating = () => {
        const numRating = parseFloat(rating);
        return !isNaN(numRating) && numRating >= 0 && numRating <= 10;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!isValidRating()) return;

        try {
            await updateMovie({
                variables: {
                    id,
                    rating: parseFloat(rating),
                },
            });
            toast.success("Le film a été modifié avec succès !");
        } catch (err) {
            toast.error("Une erreur s'est produite lors de la modification du film.");
        }
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

            <ToastContainer />
        </div>
    );
};

export default UpdateMovie;
