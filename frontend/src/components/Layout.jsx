import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

export default function Layout({ children }) {
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname.startsWith(path)
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            Product & User Manager
          </Link>
          <ul className="navbar-menu">
            <li>
              <Link
                to="/products"
                className={`nav-link ${isActive('/products') ? 'active' : ''}`}
              >
                Products
              </Link>
            </li>
            <li>
              <Link
                to="/users"
                className={`nav-link ${isActive('/users') ? 'active' : ''}`}
              >
                Users
              </Link>
            </li>
          </ul>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

