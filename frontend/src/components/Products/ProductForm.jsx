import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { productApi } from '../../services/api'
import './ProductForm.css'

export default function ProductForm() {
  const navigate = useNavigate()
  const { productId } = useParams()
  const isEditing = !!productId

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    tags: '',
    in_stock: true,
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (isEditing) {
      loadProduct()
    }
  }, [productId])

  const loadProduct = async () => {
    setLoading(true)
    try {
      const product = await productApi.getById(parseInt(productId))
      setFormData({
        name: product.name,
        description: product.description,
        price: product.price,
        category: product.category,
        tags: product.tags.join(', '),
        in_stock: product.in_stock,
      })
    } catch (err) {
      setError(err.message || 'Failed to load product')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const payload = {
        name: formData.name,
        description: formData.description,
        price: parseFloat(formData.price),
        category: formData.category,
        tags: formData.tags
          .split(',')
          .map((tag) => tag.trim())
          .filter((tag) => tag),
        in_stock: formData.in_stock,
      }

      if (isEditing) {
        await productApi.update(parseInt(productId), payload)
      } else {
        await productApi.create(payload)
      }

      navigate('/products')
    } catch (err) {
      setError(err.message || 'Failed to save product')
    } finally {
      setLoading(false)
    }
  }

  if (loading && isEditing) {
    return <div className="loading">Loading product...</div>
  }

  return (
    <div className="product-form-container">
      <h1>{isEditing ? 'Edit Product' : 'Create New Product'}</h1>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="product-form">
        <div className="form-group">
          <label htmlFor="name">Product Name *</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter product name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            placeholder="Enter product description"
            rows="4"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="price">Price (USD) *</label>
            <input
              type="number"
              id="price"
              name="price"
              value={formData.price}
              onChange={handleChange}
              required
              step="0.01"
              min="0"
              placeholder="0.00"
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">Category *</label>
            <input
              type="text"
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
              placeholder="e.g., Electronics"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags (comma-separated)</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="e.g., premium, wireless, audio"
          />
        </div>

        <div className="form-group checkbox">
          <input
            type="checkbox"
            id="in_stock"
            name="in_stock"
            checked={formData.in_stock}
            onChange={handleChange}
          />
          <label htmlFor="in_stock">In Stock</label>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : isEditing ? 'Update Product' : 'Create Product'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/products')}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

