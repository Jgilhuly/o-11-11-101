import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import ProductList from './components/Products/ProductList'
import ProductForm from './components/Products/ProductForm'
import UserList from './components/Users/UserList'
import UserForm from './components/Users/UserForm'
import Home from './pages/Home'
import './App.css'

export default function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          
          {/* Product Routes */}
          <Route path="/products" element={<ProductList />} />
          <Route path="/products/new" element={<ProductForm />} />
          <Route path="/products/:productId/edit" element={<ProductForm />} />
          
          {/* User Routes */}
          <Route path="/users" element={<UserList />} />
          <Route path="/users/new" element={<UserForm />} />
          <Route path="/users/:userId/edit" element={<UserForm />} />
          
          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  )
}

