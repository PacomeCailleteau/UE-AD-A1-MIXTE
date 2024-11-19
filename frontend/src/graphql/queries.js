import {gql} from "@apollo/client";

export const GET_MOVIES = gql`
    query GetMovies {
        movies {
            id
            title
            director
            rating
        }
    }
`;

export const GET_MOVIE_BY_ID = gql`
    query GetMovieById($id: String!) {
        movie_by_id(_id: $id) {
            id
            title
            director
            rating
        }
    }
`;
