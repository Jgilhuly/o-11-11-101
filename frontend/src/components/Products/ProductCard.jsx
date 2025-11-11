import { Link } from 'react-router-dom'
import './ProductCard.css'

export default function ProductCard({ product, onDelete }) {
  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${product.name}"?`)) {
      onDelete(product.id)
    }
  }

  return (
    <div className="product-card">
      <div className="product-header">
        <h3>{product.name}</h3>
        <span className={`stock-badge ${product.in_stock ? 'in-stock' : 'out-of-stock'}`}>
          {product.in_stock ? 'In Stock' : 'Out of Stock'}
        </span>
      </div>
      <p className="product-description">{product.description}</p>
      <div className="product-meta">
        <div className="price">${product.price.toFixed(2)}</div>
        <div className="category">{product.category}</div>
      </div>
      {product.tags && product.tags.length > 0 && (
        <div className="tags">
          {product.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      )}
      <div className="product-actions">
        <Link to={`/products/${product.id}/edit`} className="btn btn-primary">
          Edit
        </Link>
        <button onClick={handleDelete} className="btn btn-danger">
          Delete
        </button>
      </div>
    </div>
  )
}

