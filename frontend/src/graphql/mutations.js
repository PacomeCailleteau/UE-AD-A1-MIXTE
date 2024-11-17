import { gql } from '@apollo/client';

export const CREATE_MOVIE = gql`
    mutation CreateMovie($id: String!, $title: String!, $director: String!, $rating: Float!) {
        create_movie(_id: $id, _title: $title, _director: $director, _rating: $rating) {
            id
            title
            director
            rating
        }
    }
`;

export const UPDATE_MOVIE = gql`
    mutation UpdateMovie($id: String!, $rating: Float!) {
        update_movie_rate(_id: $id, _rate: $rating) {
            id
            rating
        }
    }
`;

export const DELETE_MOVIE = gql`
    mutation DeleteMovie($id: String!) {
        delete_movie(_id: $id)
    }
`;
