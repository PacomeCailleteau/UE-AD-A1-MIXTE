import React, { useState } from "react";
import { useMutation } from "@apollo/client";
import { CREATE_MOVIE } from "../graphql/mutations";
import { Form, Button, Alert } from "react-bootstrap";

const AddMovie = () => {
    const [id, setId] = useState('');
    const [title, setTitle] = useState('');
    const [director, setDirector] = useState('');
    const [rating, setRating] = useState('');
    const [createMovie, { data, loading, error }] = useMutation(CREATE_MOVIE);

    const isValidId = () => /^[0-9S]+$/.test(id);
    const isValidRating = () => {
        const numRating = parseFloat(rating);
        return !isNaN(numRating) && numRating >= 0 && numRating <= 10;
    };
    const isFormValid = () => id && title && director && isValidId() && isValidRating();

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!isFormValid()) return;
        createMovie({
            variables: {
                id,
                title,
                director,
                rating: parseFloat(rating),
            },
        });
    };

    return (
        <div>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>ID</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="Veuillez saisir l'ID"
                        value={id}
                        onChange={(e) => setId(e.target.value)}
                        isInvalid={id && !isValidId()}
                    />
                    <Form.Control.Feedback type="invalid">
                        L'ID doit contenir uniquement des chiffres ou le caractère "-".
                    </Form.Control.Feedback>
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
                        isInvalid={rating && !isValidRating()}
                    />
                    <Form.Control.Feedback type="invalid">
                        La note doit être un nombre entre 0 et 10.
                    </Form.Control.Feedback>
                </Form.Group>

                <Button variant="primary" type="submit" disabled={!isFormValid() || loading}>
                    {loading ? 'Creating...' : 'Créer le film'}
                </Button>
            </Form>

            {error && <Alert variant="danger" className="mt-3">{error.message}</Alert>}
            {data && (
                <Alert variant="success" className="mt-3">
                    <strong>Movie Created!</strong>
                    <p>ID: {id}</p>
                    <p>Title: {title}</p>
                    <p>Director: {director}</p>
                    <p>Rating: {rating}</p>
                </Alert>
            )}
        </div>
    );
};

export default AddMovie;
