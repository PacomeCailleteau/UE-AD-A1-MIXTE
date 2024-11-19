import React, { useState } from "react";
import { useMutation } from "@apollo/client";
import { CREATE_MOVIE } from "../graphql/mutations";
import { Form, Button, Alert } from "react-bootstrap";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const AddMovie = () => {
    const [id, setId] = useState('');
    const [title, setTitle] = useState('');
    const [director, setDirector] = useState('');
    const [rating, setRating] = useState('');
    const [createMovie, { data, loading, error }] = useMutation(CREATE_MOVIE);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createMovie({
                variables: {
                    id,
                    title,
                    director,
                    rating: parseFloat(rating),
                },
            });
            toast.success("Le film a été créé avec succès !");
        } catch (err) {
            toast.error("Une erreur s'est produite lors de la création du film.");
        }
    };

    return (
        <div>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>ID</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Veuillez saisir l'ID"
                        value={id}
                        onChange={(e) => setId(e.target.value)}
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Title</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Veuillez saisir le titre"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Director</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Veuillez saisir le réalisateur"
                        value={director}
                        onChange={(e) => setDirector(e.target.value)}
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Rating</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="Veuillez saisir une note entre 0 et 10"
                        value={rating}
                        onChange={(e) => setRating(e.target.value)}
                    />
                </Form.Group>

                <Button variant="primary" type="submit" disabled={loading}>
                    {loading ? 'Création en cours...' : 'Ajouter le film'}
                </Button>
            </Form>

            {error && <Alert variant="danger" className="mt-3">{error.message}</Alert>}
            {data && (
                <Alert variant="success" className="mt-3">
                    <strong>Film créé !</strong>
                    <p>ID : {id}</p>
                    <p>Title : {title}</p>
                    <p>Réalisé par : {director}</p>
                    <p>Note : {rating}</p>
                </Alert>
            )}

            <ToastContainer />
        </div>
    );
};

export default AddMovie;
