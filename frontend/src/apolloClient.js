import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';

const movieClient = new ApolloClient({
    link: new HttpLink({
        uri: 'http://localhost:3001/graphql',
    }),
    cache: new InMemoryCache(),
});

export default movieClient;
