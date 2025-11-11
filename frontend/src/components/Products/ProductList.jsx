import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { productApi } from '../../services/api'
import ProductCard from './ProductCard'
import './ProductList.css'

export default function ProductList() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await productApi.getAll()
      setProducts(data)
    } catch (err) {
      setError(err.message || 'Failed to fetch products')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    try {
      await productApi.delete(id)
      setProducts(products.filter((p) => p.id !== id))
    } catch (err) {
      setError(err.message || 'Failed to delete product')
    }
  }

  if (loading) {
    return <div className="loading">Loading products...</div>
  }

  return (
    <div className="product-list-container">
      <div className="product-list-header">
        <h1>Products</h1>
        <Link to="/products/new" className="btn btn-primary">
          Add New Product
        </Link>
      </div>

      {error && <div className="error-message">{error}</div>}

      {products.length === 0 ? (
        <div className="empty-state">
          <p>No products found. Create one to get started!</p>
          <Link to="/products/new" className="btn btn-primary">
            Create First Product
          </Link>
        </div>
      ) : (
        <div className="products-grid">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}

