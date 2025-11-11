import { Link } from 'react-router-dom'
import './Home.css'

export default function Home() {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1>Welcome to Product & User Manager</h1>
        <p>Manage your products and users with ease</p>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <div className="feature-icon">📦</div>
          <h2>Products</h2>
          <p>Create, read, update, and delete products with full CRUD operations.</p>
          <Link to="/products" className="feature-link">
            Manage Products →
          </Link>
        </div>

        <div className="feature-card">
          <div className="feature-icon">👥</div>
          <h2>Users</h2>
          <p>Manage user accounts, view details, and perform user operations.</p>
          <Link to="/users" className="feature-link">
            Manage Users →
          </Link>
        </div>
      </div>

      <div className="quick-links">
        <h2>Quick Actions</h2>
        <div className="links-grid">
          <Link to="/products/new" className="quick-link">
            Add New Product
          </Link>
          <Link to="/users/new" className="quick-link">
            Add New User
          </Link>
          <Link to="/products" className="quick-link">
            View All Products
          </Link>
          <Link to="/users" className="quick-link">
            View All Users
          </Link>
        </div>
      </div>
    </div>
  )
}

