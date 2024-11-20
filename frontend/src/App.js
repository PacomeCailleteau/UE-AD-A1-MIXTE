import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddMoviePage from './pages/AddMoviePage';
import UpdateMoviePage from './pages/UpdateMoviePage';
import AdminDashboard from "./pages/AdminDashboard";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<AdminDashboard />} />
                <Route path="/add-movie" element={<AddMoviePage />} />
                <Route path="/update-movie/:id" element={<UpdateMoviePage />} />
            </Routes>
        </Router>
    );
}

export default App;
